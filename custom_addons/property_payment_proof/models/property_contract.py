# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyContract(models.Model):
    _inherit = "property.contract"

    authorized_payer_ids = fields.One2many(
        "property.payment.authorized.payer",
        "contract_id",
        string="Pagadores Autorizados",
        help="Pessoas/empresas autorizadas a pagar parcelas deste contrato, mesmo que o comprovante venha em nome diferente do locatário.",
    )
