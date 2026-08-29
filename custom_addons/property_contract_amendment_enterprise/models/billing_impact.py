# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PropertyContractBillingImpact(models.Model):
    _name = "property.contract.billing.impact"
    _description = "Parcela Afetada por Aditivo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "amendment_id, period_start, due_date, id"

    amendment_id = fields.Many2one(
        "property.contract.amendment",
        string="Aditivo",
        required=True,
        ondelete="cascade",
        index=True,
    )
    contract_id = fields.Many2one(
        related="amendment_id.contract_id",
        string="Contrato",
        store=True,
        readonly=True,
        index=True,
    )
    billing_plan_id = fields.Many2one(
        "property.contract.billing.plan",
        string="Parcela Original",
        ondelete="set null",
        index=True,
    )
    created_billing_plan_id = fields.Many2one(
        "property.contract.billing.plan",
        string="Parcela Complementar/Crédito Gerado",
        readonly=True,
        copy=False,
    )
    rent_schedule_id = fields.Many2one(
        "property.contract.rent.schedule",
        string="Linha da Tabela de Valores",
        ondelete="set null",
    )
    financial_adjustment_id = fields.Many2one(
        "property.contract.financial.adjustment",
        string="Ajuste Financeiro",
        ondelete="set null",
    )

    name = fields.Char(string="Descrição", compute="_compute_name", store=True)
    impact_source_type = fields.Selection([
        ("rent_schedule", "Tabela de valores"),
        ("financial_adjustment", "Ajuste financeiro"),
        ("manual", "Manual"),
    ], string="Origem do Impacto", default="rent_schedule", required=True)
    impact_type = fields.Selection([
        ("base_rent_change", "Alteração de aluguel-base"),
        ("discount", "Desconto"),
        ("extra_charge", "Acréscimo/cobrança adicional"),
        ("retroactive_debit", "Débito retroativo"),
        ("retroactive_credit", "Crédito retroativo"),
        ("complementary_debit", "Parcela complementar"),
        ("credit", "Crédito"),
        ("adjustment", "Ajuste"),
    ], string="Tipo de Impacto", default="adjustment", required=True)
    application_rule = fields.Selection([
        ("future_recalculation", "Recalcular parcela futura"),
        ("open_update", "Atualizar parcela em aberto"),
        ("complementary_debit", "Gerar parcela complementar"),
        ("credit_note", "Gerar crédito"),
        ("ignored", "Não alterar parcela"),
    ], string="Regra de Aplicação", default="future_recalculation", required=True)
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("simulated", "Simulado"),
        ("applied", "Aplicado"),
        ("reversed", "Revertido"),
        ("ignored", "Ignorado"),
    ], string="Status", default="simulated", tracking=True)

    billing_status = fields.Char(string="Status da Parcela", compute="_compute_billing_status", store=True)
    period_start = fields.Date(string="Início da Competência")
    period_end = fields.Date(string="Fim da Competência")
    due_date = fields.Date(string="Vencimento")
    original_amount = fields.Monetary(string="Valor Original", currency_field="currency_id")
    new_amount = fields.Monetary(string="Novo Valor", currency_field="currency_id")
    delta_amount = fields.Monetary(string="Diferença", currency_field="currency_id")
    original_base_rent_amount = fields.Monetary(string="Aluguel-base Original", currency_field="currency_id")
    new_base_rent_amount = fields.Monetary(string="Novo Aluguel-base", currency_field="currency_id")
    original_discount_amount = fields.Monetary(string="Desconto Original", currency_field="currency_id")
    new_discount_amount = fields.Monetary(string="Novo Desconto", currency_field="currency_id")
    original_extra_charge_amount = fields.Monetary(string="Acréscimo Original", currency_field="currency_id")
    new_extra_charge_amount = fields.Monetary(string="Novo Acréscimo", currency_field="currency_id")
    is_retroactive = fields.Boolean(string="Retroativo")
    applied_at = fields.Datetime(string="Aplicado em", readonly=True, copy=False)
    applied_by = fields.Many2one("res.users", string="Aplicado por", readonly=True, copy=False)
    reversed_at = fields.Datetime(string="Revertido em", readonly=True, copy=False)
    reversed_by = fields.Many2one("res.users", string="Revertido por", readonly=True, copy=False)
    notes = fields.Text(string="Observações")
    company_id = fields.Many2one(related="contract_id.company_id", string="Empresa", store=True, readonly=True)
    currency_id = fields.Many2one(related="contract_id.currency_id", string="Moeda", store=True, readonly=True)

    @api.depends("amendment_id", "billing_plan_id", "period_start", "period_end", "impact_type")
    def _compute_name(self):
        type_labels = dict(self._fields["impact_type"].selection)
        for rec in self:
            period = ""
            if rec.period_start and rec.period_end:
                period = "%s a %s" % (rec.period_start, rec.period_end)
            elif rec.period_start:
                period = str(rec.period_start)
            rec.name = "%s - %s" % (type_labels.get(rec.impact_type, _("Impacto")), period or rec.amendment_id.display_name)

    @api.depends("billing_plan_id.status")
    def _compute_billing_status(self):
        status_labels = dict(self.env["property.contract.billing.plan"]._fields["status"].selection)
        for rec in self:
            rec.billing_status = status_labels.get(rec.billing_plan_id.status, "") if rec.billing_plan_id else ""

    def action_apply(self):
        for impact in self:
            impact._apply_one()

    def action_reverse(self):
        for impact in self:
            impact._reverse_one()

    def _apply_one(self):
        self.ensure_one()
        if self.status == "applied":
            return
        if self.status in ("reversed", "ignored"):
            raise UserError(_("Não é possível aplicar impacto revertido ou ignorado."))
        if not self.billing_plan_id and self.application_rule not in ("complementary_debit", "credit_note"):
            raise UserError(_("Este impacto não possui parcela original para atualização."))

        if self.application_rule == "ignored":
            self.write({"status": "ignored"})
            return

        if self.application_rule in ("future_recalculation", "open_update"):
            self._apply_to_existing_billing_plan()
        elif self.application_rule in ("complementary_debit", "credit_note"):
            self._create_complementary_billing_plan()

        self.write({
            "status": "applied",
            "applied_at": fields.Datetime.now(),
            "applied_by": self.env.user.id,
        })

    def _apply_to_existing_billing_plan(self):
        self.ensure_one()
        plan = self.billing_plan_id
        if not plan:
            return
        vals = {}
        if self.impact_type == "base_rent_change":
            vals["base_rent_amount"] = self.new_base_rent_amount
        elif self.impact_type in ("discount", "retroactive_credit", "credit"):
            vals["discount_amount"] = self.new_discount_amount
        elif self.impact_type in ("extra_charge", "retroactive_debit", "complementary_debit", "adjustment"):
            vals["extra_charge_amount"] = self.new_extra_charge_amount
        else:
            vals["extra_charge_amount"] = (plan.extra_charge_amount or 0.0) + (self.delta_amount or 0.0)
        vals.update({
            "source_amendment_ids": [(4, self.amendment_id.id)],
            "amendment_effective_date": self.amendment_id.effective_date,
            "amendment_applied_date": fields.Datetime.now(),
            "has_amendment_adjustment": True,
        })
        if not plan.original_total_amount:
            vals["original_total_amount"] = self.original_amount
        plan.write(vals)
        self.env["property.contract.billing.line"].create({
            "billing_plan_id": plan.id,
            "amendment_id": self.amendment_id.id,
            "rent_schedule_id": self.rent_schedule_id.id or False,
            "sequence": 90,
            "line_type": self._billing_line_type(),
            "name": self.name or _("Ajuste por aditivo"),
            "amount": self.delta_amount,
            "period_start": self.period_start,
            "period_end": self.period_end,
        })

    def _create_complementary_billing_plan(self):
        self.ensure_one()
        amount = abs(self.delta_amount or 0.0)
        if not amount:
            return
        values = {
            "contract_id": self.contract_id.id,
            "period_start": self.period_start or self.amendment_id.effective_date,
            "period_end": self.period_end or self.amendment_id.effective_date,
            "due_date": fields.Date.context_today(self),
            "status": "draft",
            "base_rent_amount": 0.0,
            "discount_amount": amount if self.delta_amount < 0 else 0.0,
            "extra_charge_amount": amount if self.delta_amount > 0 else 0.0,
            "tax_amount": 0.0,
            "source_amendment_ids": [(4, self.amendment_id.id)],
            "original_total_amount": 0.0,
            "amendment_effective_date": self.amendment_id.effective_date,
            "amendment_applied_date": fields.Datetime.now(),
            "has_amendment_adjustment": True,
        }
        created = self.env["property.contract.billing.plan"].create(values)
        self.env["property.contract.billing.line"].create({
            "billing_plan_id": created.id,
            "amendment_id": self.amendment_id.id,
            "rent_schedule_id": self.rent_schedule_id.id or False,
            "sequence": 10,
            "line_type": self._billing_line_type(),
            "name": self.name or _("Parcela complementar por aditivo"),
            "amount": self.delta_amount,
            "period_start": self.period_start,
            "period_end": self.period_end,
        })
        self.created_billing_plan_id = created.id

    def _reverse_one(self):
        self.ensure_one()
        if self.status != "applied":
            raise UserError(_("Somente impactos aplicados podem ser revertidos."))
        if self.created_billing_plan_id:
            self.created_billing_plan_id.write({"status": "cancelled"})
        elif self.billing_plan_id:
            plan = self.billing_plan_id
            vals = {
                "source_amendment_ids": [(3, self.amendment_id.id)],
                "amendment_applied_date": False,
                "amendment_effective_date": False,
            }
            if self.impact_type == "base_rent_change":
                vals["base_rent_amount"] = self.original_base_rent_amount
            elif self.impact_type in ("discount", "retroactive_credit", "credit"):
                vals["discount_amount"] = self.original_discount_amount
            else:
                vals["extra_charge_amount"] = self.original_extra_charge_amount
            plan.write(vals)
        self.write({
            "status": "reversed",
            "reversed_at": fields.Datetime.now(),
            "reversed_by": self.env.user.id,
        })

    def _billing_line_type(self):
        self.ensure_one()
        if self.impact_type in ("discount", "retroactive_credit", "credit") or (self.delta_amount or 0.0) < 0:
            return "credit"
        if self.impact_type == "base_rent_change":
            return "adjustment"
        return "adjustment"
