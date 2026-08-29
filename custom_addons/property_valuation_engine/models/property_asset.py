# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class PropertyAsset(models.Model):
    _inherit = "property.asset"

    valuation_area_m2 = fields.Float(
        string="Área para valuation m²",
        digits=(16, 2),
        help="Área considerada no cálculo de valuation. Se não for preenchida, o motor tenta usar campos de área do imóvel.",
    )
    valuation_city = fields.Char(
        string="Cidade para valuation",
        help="Cidade usada para buscar referências de m² e comparáveis. Se vazio, o motor tenta usar o campo cidade do property_core.",
    )
    valuation_neighborhood = fields.Char(
        string="Bairro / região para valuation",
        help="Bairro/região usado para buscar referências de m² e comparáveis. Se vazio, o motor tenta usar o campo bairro do property_core.",
    )
    valuation_use_type = fields.Selection(
        [
            ("commercial", "Comercial"),
            ("residential", "Residencial"),
            ("industrial", "Industrial / Galpão"),
            ("land", "Terreno"),
            ("mixed", "Misto"),
            ("other", "Outro"),
        ],
        string="Tipo de uso para valuation",
        default="commercial",
    )
    valuation_standard = fields.Selection(
        [
            ("low", "Simples"),
            ("medium", "Médio"),
            ("high", "Alto"),
            ("premium", "Premium"),
        ],
        string="Padrão para valuation",
        default="medium",
    )
    valuation_conservation = fields.Selection(
        [
            ("new", "Novo / reformado"),
            ("good", "Bom"),
            ("regular", "Regular"),
            ("needs_renovation", "Necessita reforma"),
        ],
        string="Conservação para valuation",
        default="good",
    )
    valuation_location_factor = fields.Float(
        string="Fator localização",
        default=1.0,
        digits=(16, 4),
        help="Multiplicador manual de localização. Ex.: 1,10 aumenta 10%; 0,95 reduz 5%.",
    )
    valuation_liquidity_factor = fields.Float(
        string="Fator liquidez",
        default=1.0,
        digits=(16, 4),
        help="Multiplicador manual de liquidez/atratividade do imóvel.",
    )
    valuation_vacancy_factor = fields.Float(
        string="Fator vacância",
        default=1.0,
        digits=(16, 4),
        help="Multiplicador manual para risco de vacância ou ocupação da região.",
    )

    valuation_run_ids = fields.One2many("property.valuation.run", "asset_id", string="Estimativas")
    valuation_run_count = fields.Integer(string="Qtd. estimativas", compute="_compute_valuation_summary")
    latest_valuation_id = fields.Many2one(
        "property.valuation.run",
        string="Última estimativa",
        compute="_compute_valuation_summary",
    )
    latest_rent_valuation_id = fields.Many2one(
        "property.valuation.run",
        string="Última estimativa de locação",
        compute="_compute_valuation_summary",
    )
    latest_sale_valuation_id = fields.Many2one(
        "property.valuation.run",
        string="Última estimativa de venda",
        compute="_compute_valuation_summary",
    )
    estimated_rent_value = fields.Monetary(
        string="Valor sugerido de locação",
        compute="_compute_valuation_summary",
        currency_field="valuation_currency_id",
    )
    estimated_sale_value = fields.Monetary(
        string="Valor sugerido de venda",
        compute="_compute_valuation_summary",
        currency_field="valuation_currency_id",
    )
    valuation_confidence_score = fields.Float(
        string="Confiança da última estimativa (%)",
        compute="_compute_valuation_summary",
    )
    valuation_currency_id = fields.Many2one(
        "res.currency",
        string="Moeda do valuation",
        compute="_compute_valuation_currency",
    )

    def _compute_valuation_currency(self):
        for asset in self:
            company = getattr(asset, "company_id", False) or self.env.company
            asset.valuation_currency_id = company.currency_id

    def _compute_valuation_summary(self):
        Valuation = self.env["property.valuation.run"]
        for asset in self:
            all_runs = Valuation.search(
                [("asset_id", "=", asset.id)],
                order="valuation_date desc, id desc",
            )
            latest = all_runs[:1]
            rent = all_runs.filtered(lambda r: r.valuation_type == "rent")[:1]
            sale = all_runs.filtered(lambda r: r.valuation_type == "sale")[:1]
            asset.valuation_run_count = len(all_runs)
            asset.latest_valuation_id = latest.id if latest else False
            asset.latest_rent_valuation_id = rent.id if rent else False
            asset.latest_sale_valuation_id = sale.id if sale else False
            asset.estimated_rent_value = rent.approved_value or rent.calculated_value if rent else 0.0
            asset.estimated_sale_value = sale.approved_value or sale.calculated_value if sale else 0.0
            asset.valuation_confidence_score = latest.confidence_score if latest else 0.0

    def action_pve_calculate_rent(self):
        self.ensure_one()
        run = self.env["property.valuation.run"].create_from_asset(self, valuation_type="rent")
        return run.action_open_form()

    def action_pve_calculate_sale(self):
        self.ensure_one()
        run = self.env["property.valuation.run"].create_from_asset(self, valuation_type="sale")
        return run.action_open_form()

    def action_pve_open_valuation_runs(self):
        self.ensure_one()
        return {
            "name": _("Estimativas do Imóvel"),
            "type": "ir.actions.act_window",
            "res_model": "property.valuation.run",
            "view_mode": "list,form,pivot,graph",
            "domain": [("asset_id", "=", self.id)],
            "context": {
                "default_asset_id": self.id,
                "default_company_id": (getattr(self, "company_id", False) or self.env.company).id,
            },
        }
