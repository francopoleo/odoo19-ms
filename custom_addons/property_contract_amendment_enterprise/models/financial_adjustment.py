# -*- coding: utf-8 -*-
from odoo import models, fields


class PropertyContractFinancialAdjustment(models.Model):
    _name = "property.contract.financial.adjustment"
    _description = "Ajuste Financeiro Contratual"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "contract_id, reference_period_start desc, id desc"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade")
    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo", ondelete="set null")
    adjustment_type = fields.Selection([
        ("retroactive_credit", "Crédito retroativo"),
        ("retroactive_debit", "Débito retroativo"),
        ("overbilling_credit", "Crédito por cobrança a maior"),
        ("underbilling_debit", "Débito por cobrança a menor"),
        ("penalty_waiver", "Perdão de multa"),
        ("interest_waiver", "Perdão de juros"),
        ("settlement_credit", "Crédito de acordo"),
        ("settlement_debit", "Débito de acordo"),
    ], string="Tipo de Ajuste", required=True)
    financial_reason_id = fields.Many2one("property.contract.financial.reason", string="Motivo Financeiro")
    name = fields.Char(string="Descrição", required=True)
    amount = fields.Monetary(string="Valor", currency_field="currency_id", required=True)
    reference_period_start = fields.Date(string="Início do Período de Referência")
    reference_period_end = fields.Date(string="Fim do Período de Referência")
    apply_method = fields.Selection([
        ("next_invoice", "Próxima fatura"),
        ("credit_note", "Nota de crédito"),
        ("manual_journal", "Lançamento manual"),
        ("separate_invoice", "Fatura separada"),
    ], string="Forma de Aplicação", default="next_invoice")
    apply_to_invoice_id = fields.Many2one("account.move", string="Aplicar na Fatura")
    generated_invoice_id = fields.Many2one("account.move", string="Fatura Gerada")
    generated_credit_note_id = fields.Many2one("account.move", string="Nota de Crédito Gerada")
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("approved", "Aprovado"),
        ("applied", "Aplicado"),
        ("cancelled", "Cancelado"),
    ], string="Status", default="draft", tracking=True)
    notes = fields.Text(string="Observações")
    company_id = fields.Many2one(related="contract_id.company_id", string="Empresa", store=True, readonly=True)
    currency_id = fields.Many2one(related="contract_id.currency_id", string="Moeda", store=True, readonly=True)
