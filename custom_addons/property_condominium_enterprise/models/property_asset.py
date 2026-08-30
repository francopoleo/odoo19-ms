from odoo import fields, models


class PropertyAsset(models.Model):
    _inherit = "property.asset"

    condo_fraction = fields.Float(
        "Fração Ideal",
        digits=(12, 6),
        default=1.0,
        help="Fração ideal usada no rateio de despesas do condomínio.",
    )
    condo_fee_override = fields.Monetary(
        "Taxa de Condomínio Manual",
        currency_field="currency_id",
        help="Valor manual de condomínio para esta unidade, se necessário.",
    )
    condo_billing_partner_id = fields.Many2one(
        "res.partner",
        string="Responsável pela Cobrança",
        help="Pessoa que recebe a cobrança do condomínio, se diferente do locatário.",
    )
