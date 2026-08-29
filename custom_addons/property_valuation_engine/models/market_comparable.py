# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyMarketComparable(models.Model):
    _name = "property.market.comparable"
    _description = "Imóvel Comparável de Mercado"
    _order = "date_observed desc, city, neighborhood, id desc"
    _check_company_auto = True

    name = fields.Char(string="Título", required=True, index=True)
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
    asset_id = fields.Many2one(
        "property.asset",
        string="Imóvel interno relacionado",
        index=True,
        ondelete="set null",
    )
    source_id = fields.Many2one("property.valuation.source", string="Fonte", check_company=True)
    external_reference = fields.Char(string="Referência externa")
    url = fields.Char(string="URL do anúncio / pesquisa")
    date_observed = fields.Date(string="Data da pesquisa", default=fields.Date.context_today, required=True)
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
    conservation = fields.Selection(
        [
            ("new", "Novo / reformado"),
            ("good", "Bom"),
            ("regular", "Regular"),
            ("needs_renovation", "Necessita reforma"),
        ],
        string="Conservação",
        default="good",
    )
    city = fields.Char(string="Cidade", required=True, index=True)
    neighborhood = fields.Char(string="Bairro / Região", index=True)
    address = fields.Char(string="Endereço / referência")
    area_m2 = fields.Float(string="Área m²", required=True, digits=(16, 2))
    total_price = fields.Monetary(string="Valor total", required=True, currency_field="currency_id")
    price_m2 = fields.Monetary(
        string="Valor m²",
        compute="_compute_price_m2",
        store=True,
        currency_field="currency_id",
    )
    weight = fields.Float(
        string="Peso manual",
        default=1.0,
        digits=(16, 4),
        help="Peso adicional para esse comparável. Use 1,0 como padrão.",
    )
    is_internal_closed_deal = fields.Boolean(
        string="Negócio fechado interno",
        help="Marque quando o comparável representa preço realmente contratado, não apenas preço anunciado.",
    )
    notes = fields.Text(string="Observações")

    _area_positive = models.Constraint('CHECK(area_m2 > 0)', 'A área deve ser maior que zero.')
    _price_positive = models.Constraint('CHECK(total_price > 0)', 'O valor total deve ser maior que zero.')
    _weight_positive = models.Constraint('CHECK(weight > 0)', 'O peso deve ser maior que zero.')

    @api.depends("area_m2", "total_price")
    def _compute_price_m2(self):
        for rec in self:
            rec.price_m2 = rec.total_price / rec.area_m2 if rec.area_m2 else 0.0

    @api.constrains("area_m2", "total_price", "weight")
    def _check_positive_values(self):
        for rec in self:
            if rec.area_m2 <= 0:
                raise ValidationError("A área deve ser maior que zero.")
            if rec.total_price <= 0:
                raise ValidationError("O valor total deve ser maior que zero.")
            if rec.weight <= 0:
                raise ValidationError("O peso deve ser maior que zero.")
