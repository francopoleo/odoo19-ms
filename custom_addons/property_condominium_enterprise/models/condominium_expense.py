from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CondominiumExpense(models.Model):
    _name = "property.condominium.expense"
    _description = "Despesa Comum do Condomínio"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "expense_date desc, id desc"

    name = fields.Char(required=True, tracking=True)
    complex_id = fields.Many2one("property.complex", required=True, tracking=True, ondelete="cascade")
    expense_date = fields.Date(required=True, tracking=True)
    vendor_id = fields.Many2one("res.partner", tracking=True)
    category = fields.Selection(
        [("utilities", "Utilidades"), ("security", "Segurança"), ("cleaning", "Limpeza"), ("maintenance", "Manutenção"), ("improvement", "Benfeitoria"), ("other", "Outros")],
        default="other",
        tracking=True,
    )
    allocation_rule = fields.Selection(
        [("equal", "Igual"), ("fractional", "Fração Ideal"), ("gla", "Por ABL"), ("manual", "Manual")],
        default="fractional",
        tracking=True,
    )
    amount = fields.Monetary(currency_field="currency_id", tracking=True)
    currency_id = fields.Many2one(related="complex_id.currency_id", store=True, readonly=True)
    move_id = fields.Many2one("account.move", string="Lançamento Contábil", ondelete="set null", copy=False)
    allocated_amount = fields.Monetary("Valor Rateado", currency_field="currency_id", compute="_compute_allocated_amount", store=False)
    allocation_line_ids = fields.One2many(
        "property.condominium.expense.allocation",
        "expense_id",
        string="Rateio",
    )
    allocation_total = fields.Monetary("Total Rateado", currency_field="currency_id", compute="_compute_allocated_amount", store=False)
    state = fields.Selection(
        [
            ("draft", "Rascunho"),
            ("to_approve", "Em Aprovação"),
            ("approved", "Aprovada"),
            ("posted", "Lançada"),
            ("cancelled", "Cancelada"),
        ],
        default="draft",
        tracking=True,
    )

    @api.depends("amount")
    def _compute_allocated_amount(self):
        for rec in self:
            rec.allocated_amount = rec.amount or 0.0
            rec.allocation_total = sum(rec.allocation_line_ids.mapped("amount"))

    def action_request_approval(self):
        for rec in self:
            if rec.state != "draft":
                continue
            if not rec.allocation_line_ids:
                rec.action_generate_allocation()
            rec.state = "to_approve"
            rec.message_post(body=_("Despesa enviada para aprovação."))

    def action_approve(self):
        for rec in self:
            if rec.state != "to_approve":
                continue
            rec.state = "approved"
            rec.message_post(body=_("Despesa aprovada."))

    def action_post(self):
        for rec in self:
            if rec.state not in ("approved",):
                raise UserError(_("A despesa precisa ser aprovada antes do lançamento contábil."))
            rec.state = "posted"
            rec.message_post(body=_("Despesa lançada no condomínio."))

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def _get_expense_account(self):
        self.ensure_one()
        params = self.env["ir.config_parameter"].sudo()
        account_id = int(params.get_param("property_condominium.income_account_id", 0) or 0)
        return self.env["account.account"].browse(account_id) if account_id else self.env["account.account"]

    def action_create_account_move(self):
        self.ensure_one()
        if self.state != "approved":
            raise UserError(_("A despesa precisa estar aprovada para gerar a conta a pagar."))
        if self.move_id:
            raise UserError(_("Esta despesa já possui lançamento contábil."))
        if not self.vendor_id:
            raise UserError(_("Informe o fornecedor para gerar a conta a pagar."))
        account = self._get_expense_account()
        if not account:
            raise UserError(_("Configure uma conta contábil para o condomínio em Configurações."))
        move = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.vendor_id.id,
            "invoice_date": self.expense_date,
            "invoice_date_due": self.expense_date,
            "ref": self.name,
            "invoice_line_ids": [
                (0, 0, {
                    "name": self.name,
                    "account_id": account.id,
                    "quantity": 1.0,
                    "price_unit": self.amount,
                }),
            ],
        })
        self.move_id = move.id
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": move.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_view_move(self):
        self.ensure_one()
        if not self.move_id:
            raise UserError(_("Não existe lançamento contábil para esta despesa."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.move_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_generate_allocation(self):
        for rec in self:
            rec.allocation_line_ids.unlink()
            units = rec.complex_id.asset_ids.filtered(lambda u: u.status != "inactive")
            if not units:
                continue
            if rec.allocation_rule == "equal":
                shares = {u.id: 1.0 / len(units) for u in units}
            elif rec.allocation_rule == "gla":
                total = sum(units.mapped("gla")) or 1.0
                shares = {u.id: (u.gla or 0.0) / total for u in units}
            else:
                total = sum(units.mapped("condo_fraction")) or 1.0
                shares = {u.id: (u.condo_fraction or 0.0) / total for u in units}
            for unit in units:
                rec.env["property.condominium.expense.allocation"].create({
                    "expense_id": rec.id,
                    "unit_id": unit.id,
                    "amount": rec.amount * shares[unit.id],
                })
        return True


class CondominiumExpenseAllocation(models.Model):
    _name = "property.condominium.expense.allocation"
    _description = "Rateio de Despesa do Condomínio"

    expense_id = fields.Many2one("property.condominium.expense", required=True, ondelete="cascade")
    unit_id = fields.Many2one("property.asset", required=True, ondelete="cascade")
    currency_id = fields.Many2one(related="expense_id.currency_id", store=True, readonly=True)
    amount = fields.Monetary(currency_field="currency_id", required=True)
