# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PropertyContractHistoryLine(models.Model):
    _name = "property.contract.history.line"
    _description = "Campo Extraído de Contrato"
    _order = "sequence asc, id asc"

    history_id = fields.Many2one(
        "property.contract.history",
        string="Contrato",
        required=True,
        ondelete="cascade",
    )
    field_name = fields.Char(
        "Nome do Campo",
        help="Identificador do campo (ex: party1_name, start_date)",
    )
    label = fields.Char(
        "Rótulo",
        compute="_compute_label",
        help="Descrição legível do campo",
    )
    raw_value = fields.Text(
        "Valor Extraído",
        help="Texto bruto conforme extraído do PDF/OCR",
    )
    parsed_value = fields.Char(
        "Valor Parseado",
        help="Valor limpo e normalizado",
    )
    field_type = fields.Selection(
        [
            ("char", "Texto"),
            ("date", "Data"),
            ("monetary", "Valor Monetário"),
            ("selection", "Seleção"),
            ("text", "Texto Longo"),
        ],
        string="Tipo",
        default="char",
    )
    confidence = fields.Float(
        "Confiança (%)",
        default=80.0,
        help="Score de confiança da extração (0-100)",
    )
    notes = fields.Text(
        "Notas",
        help="Observações do revisor durante validação",
    )
    accepted = fields.Boolean(
        "Aceito",
        default=False,
        help="Marcar como aceito para incluir na sincronização",
    )
    sequence = fields.Integer("Ordem", default=0)

    @api.depends("field_name")
    def _compute_label(self):
        """Map field names to readable labels."""
        label_map = {
            "party1_name": "Parte 1 - Nome",
            "party1_vat": "Parte 1 - CPF/CNPJ",
            "party2_name": "Parte 2 - Nome",
            "party2_vat": "Parte 2 - CPF/CNPJ",
            "sign_date": "Data da Assinatura",
            "start_date": "Data de Início",
            "end_date": "Data de Término",
            "monthly_amount": "Valor Mensal",
            "total_value": "Valor Total",
            "deposit_value": "Caução/Depósito",
            "address": "Endereço do Imóvel",
            "neighborhood": "Bairro",
            "city": "Cidade",
            "zip_code": "CEP",
            "property_description": "Descrição do Imóvel",
        }
        for line in self:
            line.label = label_map.get(line.field_name, line.field_name)

    def action_accept(self):
        """Accept this field for sync."""
        self.write({"accepted": True})

    def action_reject(self):
        """Reject this field for sync."""
        self.write({"accepted": False})
