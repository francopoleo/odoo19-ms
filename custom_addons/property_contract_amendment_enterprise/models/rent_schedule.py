# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PropertyContractRentSchedule(models.Model):
    _name = "property.contract.rent.schedule"
    _description = "Tabela de Valores do Contrato"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "contract_id, start_date, sequence, id"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade", index=True)
    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo", ondelete="set null")
    name = fields.Char(string="Nome", required=True)
    sequence = fields.Integer(string="Sequência", default=10)
    charge_type = fields.Selection([
        ("base_rent", "Aluguel-base"),
        ("discount", "Desconto"),
        ("extra_charge", "Acréscimo"),
        ("rent_free_period", "Período sem aluguel"),
        ("grace_period", "Carência"),
        ("step_rent", "Aluguel escalonado"),
        ("percentage_rent", "Aluguel percentual"),
        ("minimum_rent", "Aluguel mínimo"),
        ("turnover_rent", "Aluguel sobre faturamento"),
        ("iptu", "IPTU"),
        ("condominium", "Condomínio"),
        ("cam", "Despesas comuns/despesas comuns"),
        ("insurance", "Seguro"),
        ("utilities", "Utilidades"),
        ("marketing_fund", "Fundo de marketing"),
        ("service_charge", "Taxa de serviço"),
        ("penalty", "Multa"),
        ("interest", "Juros"),
        ("monetary_correction", "Correção monetária"),
        ("adjustment", "Ajuste"),
        ("credit", "Crédito"),
        ("other", "Outro"),
    ], string="Tipo de Cobrança", required=True, default="base_rent")
    financial_reason_id = fields.Many2one("property.contract.financial.reason", string="Motivo Financeiro")
    amount_type = fields.Selection([
        ("fixed", "Fixo"),
        ("percentage", "Percentual"),
        ("variable", "Variável"),
        ("formula", "Fórmula"),
    ], string="Tipo de Valor", required=True, default="fixed")
    amount = fields.Monetary(string="Valor", currency_field="currency_id")
    percentage = fields.Float(string="Percentual")
    base_amount = fields.Monetary(string="Valor Base", currency_field="currency_id")
    start_date = fields.Date(string="Data Inicial", required=True)
    end_date = fields.Date(string="Data Final")
    due_day = fields.Integer(string="Dia de Vencimento")
    billing_frequency = fields.Selection([
        ("monthly", "Mensal"),
        ("quarterly", "Trimestral"),
        ("semiannual", "Semestral"),
        ("annual", "Anual"),
        ("one_time", "Única"),
    ], string="Frequência de Cobrança", default="monthly")
    billing_period_type = fields.Selection([
        ("competence", "Competência"),
        ("advance", "Antecipado"),
        ("arrears", "Vencido/Subsequente"),
    ], string="Tipo de Período", default="competence")
    is_base_rent = fields.Boolean(string="É Aluguel-base", default=False)
    is_discount = fields.Boolean(string="É Desconto", default=False)
    is_extra_charge = fields.Boolean(string="É Acréscimo", default=False)
    is_temporary = fields.Boolean(string="Temporário", default=False)
    is_recurring = fields.Boolean(string="Recorrente", default=True)
    is_retroactive = fields.Boolean(string="Retroativo", default=False)
    is_proratable = fields.Boolean(string="Calcula Pró-rata", default=True)
    proration_method = fields.Selection([
        ("daily", "Pro rata dia"),
        ("monthly", "Mês cheio"),
        ("none", "Sem pró-rata"),
    ], string="Método de Pró-rata", default="daily")
    tax_included = fields.Boolean(string="Impostos Incluídos", default=False)
    account_id = fields.Many2one("account.account", string="Conta Contábil")
    analytic_account_id = fields.Many2one("account.analytic.account", string="Conta Analítica")
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("active", "Ativo"),
        ("superseded", "Substituído"),
        ("cancelled", "Cancelado"),
    ], string="Status", default="draft", tracking=True)
    notes = fields.Text(string="Observações")
    company_id = fields.Many2one(related="contract_id.company_id", string="Empresa", store=True, readonly=True)
    currency_id = fields.Many2one(related="contract_id.currency_id", string="Moeda", store=True, readonly=True)

    @api.onchange("charge_type")
    def _onchange_charge_type(self):
        for rec in self:
            rec.is_base_rent = rec.charge_type in ("base_rent", "minimum_rent")
            rec.is_discount = rec.charge_type in ("discount", "rent_free_period", "grace_period", "credit")
            rec.is_extra_charge = rec.charge_type not in ("base_rent", "minimum_rent", "discount", "rent_free_period", "grace_period", "credit")

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for rec in self:
            if rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(_("A data final da linha de valor não pode ser anterior à data inicial."))

    @api.constrains("contract_id", "charge_type", "start_date", "end_date", "status")
    def _check_overlapping_base_rent(self):
        for rec in self.filtered(lambda r: r.status == "active" and r.charge_type in ("base_rent", "minimum_rent")):
            domain = [
                ("id", "!=", rec.id),
                ("contract_id", "=", rec.contract_id.id),
                ("status", "=", "active"),
                ("charge_type", "in", ["base_rent", "minimum_rent"]),
                ("start_date", "<=", rec.end_date or "9999-12-31"),
                "|", ("end_date", "=", False), ("end_date", ">=", rec.start_date),
            ]
            if self.search_count(domain):
                raise ValidationError(_("Existe sobreposição de aluguel-base ativo no mesmo período."))

    def _is_date_in_range(self, date):
        self.ensure_one()
        return self.start_date <= date and (not self.end_date or self.end_date >= date)
