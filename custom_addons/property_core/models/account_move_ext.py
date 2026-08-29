from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    maintenance_id = fields.Many2one(
        "property.maintenance",
        string="Manutenção",
        ondelete="set null",
        help="Manutenção de imóvel que originou esta fatura de compra.",
        copy=False,
        index=True,
    )
