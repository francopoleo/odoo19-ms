from odoo import fields, models


class CondominiumRelationship(models.Model):
    _name = "property.condominium.relationship"
    _description = "Vínculo do Condomínio"
    _order = "complex_id, asset_id, partner_id"

    complex_id = fields.Many2one("property.complex", string="Condomínio", ondelete="cascade")
    asset_id = fields.Many2one("property.asset", string="Unidade", ondelete="cascade")
    partner_id = fields.Many2one("res.partner", string="Pessoa", required=True, ondelete="cascade")
    role = fields.Selection(
        [
            ("owner", "Proprietário"),
            ("tenant", "Locatário"),
            ("financial_responsible", "Responsável Financeiro"),
            ("manager", "Administrador"),
            ("syndic", "Síndico"),
            ("occupant", "Morador"),
        ],
        required=True,
        default="tenant",
        string="Papel",
    )
    active = fields.Boolean(default=True)
