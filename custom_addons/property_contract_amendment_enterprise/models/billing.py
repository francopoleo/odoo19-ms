# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PropertyContractBillingPlan(models.Model):
    _name = "property.contract.billing.plan"
    _description = "Plano de Cobrança do Contrato"
    _order = "contract_id, period_start, id"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade")
    period_start = fields.Date(string="Início do Período", required=True)
    period_end = fields.Date(string="Fim do Período", required=True)
    due_date = fields.Date(string="Data de Vencimento", required=True)
    base_rent_amount = fields.Monetary(string="Aluguel-base", currency_field="currency_id")
    discount_amount = fields.Monetary(string="Desconto", currency_field="currency_id")
    extra_charge_amount = fields.Monetary(string="Acréscimo", currency_field="currency_id")
    tax_amount = fields.Monetary(string="Impostos/Taxas", currency_field="currency_id")
    total_amount = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total", store=True)
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("calculated", "Calculado"),
        ("approved", "Aprovado"),
        ("invoiced", "Faturado"),
        ("paid", "Pago"),
        ("cancelled", "Cancelado"),
        ("superseded", "Substituído"),
    ], string="Status", default="draft")
    invoice_id = fields.Many2one("account.move", string="Fatura")
    source_amendment_ids = fields.Many2many("property.contract.amendment", string="Aditivos de Origem")
    amendment_adjustment_ids = fields.One2many("property.contract.billing.impact", "billing_plan_id", string="Ajustes por Aditivo")
    line_ids = fields.One2many("property.contract.billing.line", "billing_plan_id", string="Linhas")
    original_total_amount = fields.Monetary(string="Valor Original Antes dos Aditivos", currency_field="currency_id", readonly=True, copy=False)
    amendment_delta_amount = fields.Monetary(string="Diferença por Aditivos", currency_field="currency_id", compute="_compute_amendment_amounts", store=True)
    amended_total_amount = fields.Monetary(string="Valor Após Aditivos", currency_field="currency_id", compute="_compute_amendment_amounts", store=True)
    has_amendment_adjustment = fields.Boolean(string="Alterada por Aditivo", copy=False)
    amendment_applied_date = fields.Datetime(string="Aditivo Aplicado em", readonly=True, copy=False)
    amendment_effective_date = fields.Date(string="Data de Efeito do Aditivo", readonly=True, copy=False)
    company_id = fields.Many2one(related="contract_id.company_id", string="Empresa", store=True, readonly=True)
    currency_id = fields.Many2one(related="contract_id.currency_id", string="Moeda", store=True, readonly=True)

    @api.depends("base_rent_amount", "discount_amount", "extra_charge_amount", "tax_amount")
    def _compute_total(self):
        for rec in self:
            rec.total_amount = (rec.base_rent_amount or 0.0) - (rec.discount_amount or 0.0) + (rec.extra_charge_amount or 0.0) + (rec.tax_amount or 0.0)

    @api.depends("total_amount", "original_total_amount", "has_amendment_adjustment")
    def _compute_amendment_amounts(self):
        for rec in self:
            original = rec.original_total_amount if rec.original_total_amount not in (False, None, 0.0) else rec.total_amount
            rec.amended_total_amount = rec.total_amount
            rec.amendment_delta_amount = (rec.total_amount or 0.0) - (original or 0.0) if rec.has_amendment_adjustment else 0.0


class PropertyContractBillingLine(models.Model):
    _name = "property.contract.billing.line"
    _description = "Linha do Plano de Cobrança"
    _order = "billing_plan_id, sequence, id"

    billing_plan_id = fields.Many2one("property.contract.billing.plan", string="Plano de Cobrança", required=True, ondelete="cascade")
    contract_id = fields.Many2one(related="billing_plan_id.contract_id", string="Contrato", store=True, readonly=True)
    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo")
    rent_schedule_id = fields.Many2one("property.contract.rent.schedule", string="Linha da Tabela de Valores")
    sequence = fields.Integer(string="Sequência", default=10)
    line_type = fields.Selection([
        ("base_rent", "Aluguel-base"),
        ("discount", "Desconto"),
        ("extra_charge", "Acréscimo"),
        ("iptu", "IPTU"),
        ("condominium", "Condomínio"),
        ("cam", "Despesas comuns"),
        ("insurance", "Seguro"),
        ("utility", "Utilidade"),
        ("penalty", "Multa"),
        ("interest", "Juros"),
        ("adjustment", "Ajuste"),
        ("credit", "Crédito"),
    ], string="Tipo de Linha", default="base_rent")
    name = fields.Char(string="Descrição", required=True)
    amount = fields.Monetary(string="Valor", currency_field="currency_id")
    quantity = fields.Float(string="Quantidade", default=1.0)
    percentage = fields.Float(string="Percentual")
    period_start = fields.Date(string="Início do Período")
    period_end = fields.Date(string="Fim do Período")
    account_id = fields.Many2one("account.account", string="Conta Contábil")
    analytic_account_id = fields.Many2one("account.analytic.account", string="Conta Analítica")
    company_id = fields.Many2one(related="contract_id.company_id", string="Empresa", store=True, readonly=True)
    currency_id = fields.Many2one(related="contract_id.currency_id", string="Moeda", store=True, readonly=True)
