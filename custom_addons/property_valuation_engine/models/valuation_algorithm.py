# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyValuationAlgorithm(models.Model):
    _name = "property.valuation.algorithm"
    _description = "Algoritmo de Valuation Imobiliário"
    _order = "sequence, name"

    name = fields.Char(string="Algoritmo", required=True, translate=True)
    code = fields.Selection(
        [
            ("simple_m2", "Regra simples por m²"),
            ("comparables", "Comparáveis ponderados"),
            ("hybrid", "Híbrido: m² + comparáveis"),
        ],
        string="Código técnico",
        required=True,
        index=True,
    )
    version = fields.Char(string="Versão", required=True, default="1.0")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    description = fields.Text(string="Descrição")
    formula = fields.Text(string="Fórmula / lógica")
