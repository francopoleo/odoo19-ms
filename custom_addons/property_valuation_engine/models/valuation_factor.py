# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyValuationFactor(models.Model):
    _name = "property.valuation.factor"
    _description = "Fator de Ajuste de Valuation Imobiliário"
    _order = "factor_type, sequence, name"
    _check_company_auto = True

    name = fields.Char(string="Fator", required=True, translate=True)
    code = fields.Char(string="Código", required=True, index=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        default=lambda self: self.env.company,
        index=True,
    )
    factor_type = fields.Selection(
        [
            ("standard", "Padrão construtivo"),
            ("conservation", "Conservação"),
            ("location", "Localização"),
            ("liquidity", "Liquidez"),
            ("vacancy", "Vacância"),
            ("custom", "Personalizado"),
        ],
        string="Tipo",
        required=True,
        index=True,
    )
    multiplier = fields.Float(
        string="Multiplicador",
        required=True,
        default=1.0,
        digits=(16, 4),
        help="Ex.: 1,15 aumenta 15%; 0,90 reduz 10%.",
    )
    description = fields.Text(string="Descrição")

    _code_type_company_unique = models.Constraint(
        'UNIQUE(code, factor_type, company_id)',
        'Já existe um fator com esse código, tipo e empresa.',
    )
    _multiplier_positive = models.Constraint(
        'CHECK(multiplier > 0)',
        'O multiplicador deve ser maior que zero.',
    )

    @api.constrains("multiplier")
    def _check_multiplier(self):
        for rec in self:
            if rec.multiplier <= 0:
                raise ValidationError("O multiplicador deve ser maior que zero.")
