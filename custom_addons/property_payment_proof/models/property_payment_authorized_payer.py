# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


def normalize_doc(value):
    return re.sub(r"\D+", "", value or "")


class PropertyPaymentAuthorizedPayer(models.Model):
    _name = "property.payment.authorized.payer"
    _description = "Pagador Autorizado para Conciliação de Aluguel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "contract_id, priority, name"
    _rec_name = "name"

    active = fields.Boolean(default=True)
    priority = fields.Integer("Prioridade", default=10)
    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade", index=True)
    tenant_id = fields.Many2one(related="contract_id.partner_id", string="Locatário", store=True)
    company_id = fields.Many2one(related="contract_id.company_id", string="Empresa", store=True)
    partner_id = fields.Many2one("res.partner", string="Contato Relacionado")
    name = fields.Char("Nome do Pagador", required=True, tracking=True)
    vat = fields.Char("CPF/CNPJ do Pagador", tracking=True)
    normalized_vat = fields.Char("CPF/CNPJ Normalizado", compute="_compute_normalized_vat", store=True, index=True)
    pix_key = fields.Char("Chave PIX Autorizada", tracking=True)
    bank_name = fields.Char("Banco")
    bank_account_hint = fields.Char("Agência/Conta ou Identificador")
    relation_type = fields.Selection([
        ("tenant", "Próprio Locatário"),
        ("spouse", "Cônjuge/Familiar"),
        ("company", "Empresa Relacionada"),
        ("guarantor", "Fiador"),
        ("third_party", "Terceiro Autorizado"),
    ], string="Relação", default="tenant", required=True)
    notes = fields.Text("Observações")

    @api.depends("vat")
    def _compute_normalized_vat(self):
        for rec in self:
            rec.normalized_vat = normalize_doc(rec.vat)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
            self.name = self.partner_id.name
            self.vat = self.partner_id.vat

    @api.constrains("vat")
    def _check_vat_length(self):
        for rec in self:
            doc = normalize_doc(rec.vat)
            if doc and len(doc) not in (11, 14):
                raise ValidationError(_("CPF/CNPJ do pagador deve ter 11 ou 14 dígitos."))
