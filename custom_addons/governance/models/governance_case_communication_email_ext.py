# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.addons.common_base.models.partner_resolution import MATCH_SOURCES


class GovernanceCaseCommunication(models.Model):
    _inherit = "governance.case.communication"

    partner_match_source = fields.Selection(
        MATCH_SOURCES,
        string="Identificação do Contato",
        readonly=True,
        copy=False,
        index=True,
        help=(
            "Como o contato foi identificado automaticamente ao receber o e-mail: "
            "'E-mail Exato' = match direto no banco (máxima confiança); "
            "'Contato Criado' = nenhum contato existente foi encontrado."
        ),
    )
    partner_match_confidence = fields.Integer(
        string="Confiança na Identificação (%)",
        readonly=True,
        copy=False,
        help=(
            "Nível de confiança da identificação automática do contato. "
            "100 = e-mail exato; 90 = e-mail normalizado; 95 = locatário/proprietário; "
            "75 = telefone; 0 = contato criado novo. "
            "Valores abaixo de 80 merecem revisão manual."
        ),
    )
