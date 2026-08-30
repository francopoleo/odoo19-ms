import base64
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CondominiumCharge(models.Model):
    _name = "property.condominium.charge"
    _description = "Cobrança de Condomínio"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "due_date desc, id desc"

    name = fields.Char(required=True, tracking=True)
    complex_id = fields.Many2one("property.complex", required=True, tracking=True, ondelete="cascade")
    unit_id = fields.Many2one("property.asset", tracking=True, ondelete="set null")
    partner_id = fields.Many2one("res.partner", tracking=True)
    due_date = fields.Date(required=True, tracking=True)
    period = fields.Char(tracking=True, help="Período de referência, por exemplo 2026-06.")
    currency_id = fields.Many2one(related="complex_id.currency_id", store=True, readonly=True)
    amount_base = fields.Monetary(currency_field="currency_id", tracking=True)
    amount_fine = fields.Monetary(currency_field="currency_id", tracking=True)
    amount_interest = fields.Monetary(currency_field="currency_id", tracking=True)
    amount_total = fields.Monetary(currency_field="currency_id", compute="_compute_amount_total", store=True)
    days_overdue = fields.Integer(compute="_compute_overdue", store=False)
    is_overdue = fields.Boolean(compute="_compute_overdue", store=False)
    state = fields.Selection(
        [("draft", "Rascunho"), ("open", "Aberta"), ("paid", "Paga"), ("overdue", "Vencida"), ("cancelled", "Cancelada")],
        default="draft",
        tracking=True,
    )
    invoice_id = fields.Many2one("account.move", tracking=True, ondelete="set null")
    remittance_state = fields.Selection(
        [("pending", "Pendente"), ("sent", "Enviada"), ("returned", "Retornada")],
        default="pending",
        tracking=True,
    )
    remittance_reference = fields.Char("Referência de Remessa", copy=False)
    barcode = fields.Char("Linha Digitável / Código de Barras", copy=False)
    cnab_file_name = fields.Char("Arquivo CNAB", copy=False)

    @api.depends("amount_base", "amount_fine", "amount_interest")
    def _compute_amount_total(self):
        for rec in self:
            rec.amount_total = (rec.amount_base or 0.0) + (rec.amount_fine or 0.0) + (rec.amount_interest or 0.0)

    @api.depends("due_date", "state")
    def _compute_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.state in ("paid", "cancelled") or not rec.due_date:
                rec.days_overdue = 0
                rec.is_overdue = False
                continue
            delta = today - rec.due_date
            rec.days_overdue = max(delta.days, 0)
            rec.is_overdue = delta.days > 0

    def action_open(self):
        self.write({"state": "open"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_mark_paid(self):
        self.write({"state": "paid"})

    def action_recalculate_charges(self):
        for rec in self:
            if rec.state not in ("open", "overdue", "draft"):
                continue
            if not rec.due_date:
                continue
            today = fields.Date.context_today(self)
            if today <= rec.due_date:
                rec.amount_fine = 0.0
                rec.amount_interest = 0.0
                rec.state = "open"
                continue
            days = (today - rec.due_date).days
            fine_rate = 0.02
            daily_interest_rate = 0.00033
            rec.amount_fine = rec.amount_base * fine_rate
            rec.amount_interest = rec.amount_base * daily_interest_rate * days
            rec.state = "overdue"

    def _get_income_account(self):
        self.ensure_one()
        params = self.env["ir.config_parameter"].sudo()
        account_id = int(params.get_param("property_condominium.income_account_id", 0) or 0)
        if not account_id:
            account_id = int(params.get_param("property_core.rent_income_account_id", 0) or 0)
        return self.env["account.account"].browse(account_id) if account_id else self.env["account.account"]

    def action_register_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            raise UserError(_("Esta cobrança já possui uma fatura."))
        income_account = self._get_income_account()
        if not income_account:
            raise UserError(_("Configure a conta de receita do condomínio em Configurações."))
        move = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner_id.id if self.partner_id else False,
            "invoice_date": fields.Date.context_today(self),
            "invoice_date_due": self.due_date,
            "ref": self.name,
            "invoice_line_ids": [
                (0, 0, {
                    "name": self.name,
                    "quantity": 1.0,
                    "price_unit": self.amount_base,
                    "account_id": income_account.id,
                }),
                (0, 0, {
                    "name": _("Multa"),
                    "quantity": 1.0,
                    "price_unit": self.amount_fine,
                    "account_id": income_account.id,
                }),
                (0, 0, {
                    "name": _("Juros"),
                    "quantity": 1.0,
                    "price_unit": self.amount_interest,
                    "account_id": income_account.id,
                }),
            ],
        })
        self.invoice_id = move.id
        self.state = "open"
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": move.id,
            "view_mode": "form",
            "target": "current",
        }

    @api.model
    def _compute_unit_share(self, complex_rec, unit):
        rule = complex_rec.common_area_rateio_key or "fractional"
        if rule == "equal":
            units = complex_rec.asset_ids.filtered(lambda u: u.status != "inactive")
            return 1.0 / len(units) if units else 0.0
        if rule == "gla":
            total = sum(complex_rec.asset_ids.mapped("gla")) or 0.0
            return (unit.gla or 0.0) / total if total else 0.0
        return unit.condo_fraction or 0.0

    @api.model
    def action_generate_monthly_charges(self):
        complexes = self.env["property.complex"].search([("condo_active", "=", True)])
        Charge = self.env["property.condominium.charge"]
        today = fields.Date.context_today(self)
        created = 0
        for complex_rec in complexes:
            due_date = today.replace(day=min(complex_rec.condo_rent_day or 10, 28))
            units = complex_rec.asset_ids.filtered(lambda u: u.status != "inactive")
            total_share = sum(self._compute_unit_share(complex_rec, u) for u in units) or 1.0
            for unit in units:
                partner = unit.condo_billing_partner_id or unit.owner_id or unit.active_contract_id.partner_id
                base_amount = unit.condo_fee_override or complex_rec.condo_fee_amount or 0.0
                share = self._compute_unit_share(complex_rec, unit)
                amount = base_amount if complex_rec.charge_model == "manual" else (complex_rec.common_area_budget or complex_rec.condo_fee_amount or 0.0) * (share / total_share)
                exists = Charge.search_count([
                    ("complex_id", "=", complex_rec.id),
                    ("unit_id", "=", unit.id),
                    ("period", "=", today.strftime("%Y-%m")),
                    ("state", "!=", "cancelled"),
                ])
                if exists:
                    continue
                Charge.create({
                    "name": f"Condomínio {complex_rec.name} - {unit.display_name_full or unit.name}",
                    "complex_id": complex_rec.id,
                    "unit_id": unit.id,
                    "partner_id": partner.id if partner else False,
                    "due_date": due_date,
                    "period": today.strftime("%Y-%m"),
                    "amount_base": amount,
                    "state": "open",
                })
                created += 1
        return created

    @api.model
    def action_process_overdues(self):
        overdue = self.search([("state", "in", ("open", "draft"))])
        overdue.action_recalculate_charges()
        return True

    def action_view_invoice(self):
        self.ensure_one()
        if not self.invoice_id:
            raise UserError(_("Não existe fatura para esta cobrança."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.invoice_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_mark_sent(self):
        self.write({"remittance_state": "sent"})

    def action_generate_remittance_file(self):
        self.ensure_one()
        filename, payload = self.env["property.condominium.cnab.service"].generate_remittance(self)
        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": base64.b64encode(payload),
            "res_model": self._name,
            "res_id": self.id,
            "mimetype": "text/plain",
        })
        self.write({
            "remittance_state": "sent",
            "remittance_reference": attachment.name,
            "cnab_file_name": attachment.name,
        })
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }
