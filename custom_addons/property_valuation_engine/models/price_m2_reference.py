# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyPriceM2Reference(models.Model):
    _name = "property.price.m2.reference"
    _description = "Referência de Valor por m²"
    _order = "city, neighborhood, valuation_type, standard, valid_from desc, id desc"
    _check_company_auto = True

    name = fields.Char(string="Descrição", compute="_compute_name", store=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        default=lambda self: self.env.company,
        index=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Moeda",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    valuation_type = fields.Selection(
        [("rent", "Locação"), ("sale", "Venda")],
        string="Finalidade",
        required=True,
        default="rent",
        index=True,
    )
    asset_use_type = fields.Selection(
        [
            ("commercial", "Comercial"),
            ("residential", "Residencial"),
            ("industrial", "Industrial / Galpão"),
            ("land", "Terreno"),
            ("mixed", "Misto"),
            ("other", "Outro"),
        ],
        string="Tipo de uso",
        default="commercial",
        required=True,
        index=True,
    )
    standard = fields.Selection(
        [
            ("low", "Simples"),
            ("medium", "Médio"),
            ("high", "Alto"),
            ("premium", "Premium"),
        ],
        string="Padrão",
        default="medium",
        required=True,
        index=True,
    )
    city = fields.Char(string="Cidade", required=True, index=True)
    neighborhood = fields.Char(string="Bairro / Região", index=True)
    price_m2 = fields.Monetary(string="Valor m²", required=True, currency_field="currency_id")
    valid_from = fields.Date(string="Válido a partir de", default=fields.Date.context_today, required=True)
    valid_to = fields.Date(string="Válido até")
    source_id = fields.Many2one("property.valuation.source", string="Fonte", check_company=True)
    confidence_score = fields.Float(
        string="Confiança (%)",
        default=70.0,
        help="Confiança gerencial dessa referência, entre 0 e 100.",
    )
    notes = fields.Text(string="Observações")

    _price_m2_positive = models.Constraint('CHECK(price_m2 > 0)', 'O valor por m² deve ser maior que zero.')
    _confidence_range = models.Constraint(
        'CHECK(confidence_score >= 0 AND confidence_score <= 100)',
        'A confiança deve estar entre 0 e 100.',
    )

    @api.depends("valuation_type", "asset_use_type", "standard", "city", "neighborhood", "price_m2")
    def _compute_name(self):
        label_type = dict(self._fields["valuation_type"].selection)
        label_use = dict(self._fields["asset_use_type"].selection)
        label_standard = dict(self._fields["standard"].selection)
        for rec in self:
            region = rec.city or "Sem cidade"
            if rec.neighborhood:
                region = "%s / %s" % (region, rec.neighborhood)
            rec.name = "%s - %s - %s - %s" % (
                region,
                label_type.get(rec.valuation_type, rec.valuation_type or ""),
                label_use.get(rec.asset_use_type, rec.asset_use_type or ""),
                label_standard.get(rec.standard, rec.standard or ""),
            )

    @api.constrains("price_m2", "confidence_score", "valid_from", "valid_to")
    def _check_values(self):
        for rec in self:
            if rec.price_m2 <= 0:
                raise ValidationError("O valor por m² deve ser maior que zero.")
            if rec.confidence_score < 0 or rec.confidence_score > 100:
                raise ValidationError("A confiança deve estar entre 0 e 100.")
            if rec.valid_to and rec.valid_from and rec.valid_to < rec.valid_from:
                raise ValidationError("A data final não pode ser anterior à data inicial.")
