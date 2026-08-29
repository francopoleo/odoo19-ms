from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyStakeholderType(models.Model):
    _name = "property.stakeholder.type"
    _description = "Tipo de Stakeholder Imobiliário"
    _order = "sequence, name"

    name = fields.Char("Nome", required=True, translate=True, help="Nome exibido para o tipo de stakeholder.")
    code = fields.Char("Código", required=True, index=True, help="Código técnico estável para integrações e regras.")
    category_group = fields.Selection([
        ("core", "Partes Principais"),
        ("intermediation", "Intermediação e Vendas"),
        ("development", "Desenvolvimento e Obra"),
        ("operations", "Operação e Suporte"),
        ("institutional", "Institucional"),
    ], string="Grupo", default="core", required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    is_person_role = fields.Boolean("Aceita Pessoa Física", default=True)
    is_company_role = fields.Boolean("Aceita Pessoa Jurídica", default=True)
    can_receive_commission = fields.Boolean("Pode Receber Comissão")
    can_have_portal_access = fields.Boolean("Pode Ter Acesso Portal")
    can_be_website_actor = fields.Boolean("Pode Atuar no Website")
    default_partner_tag_id = fields.Many2one("res.partner.category", string="Tag Padrão do Contato")
    description = fields.Text("Descrição")

    @api.constrains("code")
    def _check_unique_code(self):
        for rec in self:
            if not rec.code:
                continue
            duplicate = self.search([("id", "!=", rec.id), ("code", "=", rec.code)], limit=1)
            if duplicate:
                raise ValidationError("O código do tipo de stakeholder deve ser único.")
