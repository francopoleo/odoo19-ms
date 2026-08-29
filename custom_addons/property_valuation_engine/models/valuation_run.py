# -*- coding: utf-8 -*-
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round


class PropertyValuationRun(models.Model):
    _name = "property.valuation.run"
    _description = "Execução de Estimativa de Valor Imobiliário"
    _order = "valuation_date desc, id desc"
    _check_company_auto = True

    name = fields.Char(string="Código", required=True, copy=False, default="Novo", readonly=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Moeda",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    asset_id = fields.Many2one(
        "property.asset",
        string="Imóvel",
        required=True,
        index=True,
        ondelete="cascade",
    )
    valuation_date = fields.Date(string="Data da estimativa", default=fields.Date.context_today, required=True)
    valuation_type = fields.Selection(
        [("rent", "Locação"), ("sale", "Venda")],
        string="Finalidade",
        required=True,
        default="rent",
        index=True,
    )
    state = fields.Selection(
        [
            ("draft", "Rascunho"),
            ("calculated", "Calculado"),
            ("reviewed", "Revisado"),
            ("approved", "Aprovado"),
            ("rejected", "Rejeitado"),
        ],
        string="Status",
        default="draft",
        required=True,
        index=True,
    )
    algorithm_id = fields.Many2one("property.valuation.algorithm", string="Algoritmo")
    algorithm_code = fields.Selection(
        [
            ("simple_m2", "Regra simples por m²"),
            ("comparables", "Comparáveis ponderados"),
            ("hybrid", "Híbrido: m² + comparáveis"),
        ],
        string="Método",
        default="hybrid",
        required=True,
    )
    algorithm_version = fields.Char(string="Versão do algoritmo", default="1.0")

    area_m2 = fields.Float(string="Área considerada m²", digits=(16, 2), required=True)
    city = fields.Char(string="Cidade", index=True)
    neighborhood = fields.Char(string="Bairro / Região", index=True)
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

    reference_id = fields.Many2one(
        "property.price.m2.reference",
        string="Referência m² principal",
        check_company=True,
    )
    source_ids = fields.Many2many(
        "property.valuation.source",
        "property_valuation_run_source_rel",
        "run_id",
        "source_id",
        string="Fontes utilizadas",
        check_company=True,
    )
    comparable_ids = fields.Many2many(
        "property.market.comparable",
        "property_valuation_run_comparable_rel",
        "run_id",
        "comparable_id",
        string="Comparáveis utilizados",
        check_company=True,
    )
    comparable_count = fields.Integer(string="Qtd. comparáveis", compute="_compute_comparable_count", store=True)

    base_price_m2 = fields.Monetary(string="Valor m² base", currency_field="currency_id")
    comparable_price_m2 = fields.Monetary(string="Valor m² comparáveis", currency_field="currency_id")
    adjusted_price_m2 = fields.Monetary(string="Valor m² ajustado", currency_field="currency_id", readonly=True)

    location_factor = fields.Float(string="Fator localização", default=1.0, digits=(16, 4))
    standard_factor = fields.Float(string="Fator padrão", default=1.0, digits=(16, 4))
    conservation_factor = fields.Float(string="Fator conservação", default=1.0, digits=(16, 4))
    liquidity_factor = fields.Float(string="Fator liquidez", default=1.0, digits=(16, 4))
    vacancy_factor = fields.Float(string="Fator vacância", default=1.0, digits=(16, 4))

    calculated_value = fields.Monetary(string="Valor sugerido", currency_field="currency_id", readonly=True)
    low_value = fields.Monetary(string="Faixa inferior", currency_field="currency_id", readonly=True)
    high_value = fields.Monetary(string="Faixa superior", currency_field="currency_id", readonly=True)
    confidence_score = fields.Float(string="Confiança (%)", readonly=True)
    margin_percent = fields.Float(string="Margem da faixa (%)", readonly=True)

    approved_value = fields.Monetary(string="Valor aprovado", currency_field="currency_id")
    approved_by_id = fields.Many2one("res.users", string="Aprovado por", readonly=True)
    approved_date = fields.Datetime(string="Data de aprovação", readonly=True)
    review_notes = fields.Text(string="Parecer / justificativa")
    calculation_notes = fields.Text(string="Memória de cálculo", readonly=True)

    _area_positive = models.Constraint('CHECK(area_m2 > 0)', 'A área considerada deve ser maior que zero.')
    _confidence_range = models.Constraint(
        'CHECK(confidence_score >= 0 AND confidence_score <= 100)',
        'A confiança deve estar entre 0 e 100.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Novo") == "Novo":
                vals["name"] = self.env["ir.sequence"].next_by_code("property.valuation.run") or "Novo"
        return super().create(vals_list)

    @api.depends("comparable_ids")
    def _compute_comparable_count(self):
        for rec in self:
            rec.comparable_count = len(rec.comparable_ids)

    @api.constrains(
        "area_m2",
        "base_price_m2",
        "comparable_price_m2",
        "location_factor",
        "standard_factor",
        "conservation_factor",
        "liquidity_factor",
        "vacancy_factor",
    )
    def _check_positive_numeric_values(self):
        for rec in self:
            if rec.area_m2 <= 0:
                raise ValidationError("A área considerada deve ser maior que zero.")
            for field_name in [
                "location_factor",
                "standard_factor",
                "conservation_factor",
                "liquidity_factor",
                "vacancy_factor",
            ]:
                if rec[field_name] <= 0:
                    raise ValidationError("Todos os fatores de ajuste devem ser maiores que zero.")

    @api.model
    def create_from_asset(self, asset, valuation_type="rent"):
        """Create, calculate and return a valuation run from a property.asset record."""
        asset.ensure_one()
        vals = self._prepare_values_from_asset(asset, valuation_type)
        run = self.create(vals)
        run.action_calculate()
        return run

    @api.model
    def _prepare_values_from_asset(self, asset, valuation_type):
        area_m2 = self._asset_value(asset, ["valuation_area_m2", "area_m2", "area", "built_area", "total_area"])
        if not area_m2:
            raise UserError(
                _(
                    "Informe a área de valuation do imóvel antes de calcular. "
                    "Use o campo 'Área para valuation m²' na aba de Valuation."
                )
            )

        company = self._asset_company(asset)
        algorithm = self.env["property.valuation.algorithm"].search(
            [("code", "=", "hybrid"), ("active", "=", True)], limit=1
        )
        raw_use_type = self._asset_value(asset, ["valuation_use_type", "asset_use_type", "permitted_use", "asset_type"])
        raw_standard = self._asset_value(asset, ["valuation_standard", "construction_standard", "standard"])
        raw_conservation = self._asset_value(asset, ["valuation_conservation", "conservation_state"])
        return {
            "asset_id": asset.id,
            "company_id": company.id,
            "currency_id": company.currency_id.id,
            "valuation_type": valuation_type,
            "algorithm_id": algorithm.id or False,
            "algorithm_code": algorithm.code if algorithm else "hybrid",
            "algorithm_version": algorithm.version if algorithm else "1.0",
            "area_m2": area_m2,
            "city": self._asset_value(asset, ["valuation_city", "city"]),
            "neighborhood": self._asset_value(asset, ["valuation_neighborhood", "neighborhood", "district"]),
            "asset_use_type": self._normalize_use_type(raw_use_type),
            "standard": self._normalize_standard(raw_standard),
            "conservation": self._normalize_conservation(raw_conservation),
            "location_factor": self._safe_float(self._asset_value(asset, ["valuation_location_factor"]) or 1.0),
            "liquidity_factor": self._safe_float(self._asset_value(asset, ["valuation_liquidity_factor"]) or 1.0),
            "vacancy_factor": self._safe_float(self._asset_value(asset, ["valuation_vacancy_factor"]) or 1.0),
        }

    def action_calculate(self):
        for rec in self:
            rec._calculate_values()
        return True

    def action_mark_reviewed(self):
        self.write({"state": "reviewed"})
        return True

    def action_approve(self):
        for rec in self:
            value = rec.approved_value or rec.calculated_value
            if not value:
                raise UserError(_("Calcule a estimativa antes de aprovar."))
            rec.write(
                {
                    "approved_value": value,
                    "approved_by_id": self.env.user.id,
                    "approved_date": fields.Datetime.now(),
                    "state": "approved",
                }
            )
        return True

    def action_reject(self):
        self.write({"state": "rejected"})
        return True

    def _calculate_values(self):
        self.ensure_one()
        if self.area_m2 <= 0:
            raise UserError(_("A área considerada deve ser maior que zero."))

        reference = self._select_best_reference()
        comparables = self._select_comparables()
        comparable_price_m2 = self._weighted_comparable_price(comparables)

        base_price_m2 = reference.price_m2 if reference else 0.0
        if self.algorithm_code == "simple_m2":
            selected_price_m2 = base_price_m2
        elif self.algorithm_code == "comparables":
            selected_price_m2 = comparable_price_m2
        else:
            selected_price_m2 = self._hybrid_price_m2(base_price_m2, comparable_price_m2)

        if not selected_price_m2:
            raise UserError(
                _(
                    "Não há dados suficientes para calcular. Cadastre uma referência de valor m² "
                    "ou imóveis comparáveis para a mesma finalidade."
                )
            )

        standard_factor = self._factor_multiplier("standard", self.standard) or 1.0
        conservation_factor = self._factor_multiplier("conservation", self.conservation) or 1.0
        adjusted_price_m2 = selected_price_m2
        adjusted_price_m2 *= self.location_factor or 1.0
        adjusted_price_m2 *= standard_factor
        adjusted_price_m2 *= conservation_factor
        adjusted_price_m2 *= self.liquidity_factor or 1.0
        adjusted_price_m2 *= self.vacancy_factor or 1.0

        calculated_value = adjusted_price_m2 * self.area_m2
        confidence_score = self._calculate_confidence(reference, comparables)
        margin_percent = self._range_margin(confidence_score)
        low_value = calculated_value * (1 - margin_percent / 100.0)
        high_value = calculated_value * (1 + margin_percent / 100.0)

        source_ids = []
        if reference and reference.source_id:
            source_ids.append(reference.source_id.id)
        source_ids += [c.source_id.id for c in comparables if c.source_id]

        notes = self._build_calculation_notes(
            reference=reference,
            comparables=comparables,
            selected_price_m2=selected_price_m2,
            adjusted_price_m2=adjusted_price_m2,
            confidence_score=confidence_score,
            margin_percent=margin_percent,
        )

        self.write(
            {
                "reference_id": reference.id if reference else False,
                "base_price_m2": base_price_m2,
                "comparable_price_m2": comparable_price_m2,
                "comparable_ids": [(6, 0, comparables.ids)],
                "source_ids": [(6, 0, list(set(source_ids)))],
                "standard_factor": standard_factor,
                "conservation_factor": conservation_factor,
                "adjusted_price_m2": float_round(adjusted_price_m2, precision_digits=2),
                "calculated_value": float_round(calculated_value, precision_digits=2),
                "low_value": float_round(low_value, precision_digits=2),
                "high_value": float_round(high_value, precision_digits=2),
                "approved_value": float_round(calculated_value, precision_digits=2),
                "confidence_score": float_round(confidence_score, precision_digits=2),
                "margin_percent": float_round(margin_percent, precision_digits=2),
                "calculation_notes": notes,
                "state": "calculated",
            }
        )


    def action_open_form(self):
        self.ensure_one()
        return {
            "name": _("Estimativa de Valor"),
            "type": "ir.actions.act_window",
            "res_model": "property.valuation.run",
            "view_mode": "form",
            "res_id": self.id,
            "target": "current",
        }

    def _select_best_reference(self):
        self.ensure_one()
        today = self.valuation_date or fields.Date.context_today(self)
        refs = self.env["property.price.m2.reference"].search(
            [
                ("active", "=", True),
                ("valuation_type", "=", self.valuation_type),
                ("price_m2", ">", 0),
                "|",
                ("company_id", "=", False),
                ("company_id", "=", self.company_id.id),
                "|",
                ("valid_to", "=", False),
                ("valid_to", ">=", today),
                ("valid_from", "<=", today),
            ]
        )
        if not refs:
            return self.env["property.price.m2.reference"]

        scored = []
        for ref in refs:
            score = 0
            if self._norm(ref.city) == self._norm(self.city):
                score += 40
            elif ref.city:
                score -= 10
            if ref.neighborhood and self._norm(ref.neighborhood) == self._norm(self.neighborhood):
                score += 35
            if ref.asset_use_type == self.asset_use_type:
                score += 15
            if ref.standard == self.standard:
                score += 15
            score += min(ref.confidence_score or 0, 100) / 10.0
            scored.append((score, ref))
        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[0][1] if scored and scored[0][0] > 0 else self.env["property.price.m2.reference"]

    def _select_comparables(self):
        self.ensure_one()
        comps = self.env["property.market.comparable"].search(
            [
                ("active", "=", True),
                ("valuation_type", "=", self.valuation_type),
                ("area_m2", ">", 0),
                ("price_m2", ">", 0),
                "|",
                ("company_id", "=", False),
                ("company_id", "=", self.company_id.id),
            ]
        )
        scored = []
        for comp in comps:
            score = self._comparable_similarity_score(comp)
            if score > 0:
                scored.append((score, comp))
        scored.sort(key=lambda item: item[0], reverse=True)
        return self.env["property.market.comparable"].browse([comp.id for _, comp in scored[:12]])

    def _comparable_similarity_score(self, comp):
        self.ensure_one()
        score = 0.0
        if self.city and self._norm(comp.city) == self._norm(self.city):
            score += 30.0
        if self.neighborhood and self._norm(comp.neighborhood) == self._norm(self.neighborhood):
            score += 35.0
        if comp.asset_use_type == self.asset_use_type:
            score += 15.0
        if comp.standard == self.standard:
            score += 10.0
        if comp.conservation == self.conservation:
            score += 5.0
        if self.area_m2 and comp.area_m2:
            ratio = abs(comp.area_m2 - self.area_m2) / self.area_m2
            if ratio <= 0.15:
                score += 15.0
            elif ratio <= 0.30:
                score += 8.0
            elif ratio <= 0.50:
                score += 3.0
            else:
                score -= 10.0
        if comp.is_internal_closed_deal:
            score += 10.0
        score *= comp.weight or 1.0
        return score

    def _weighted_comparable_price(self, comparables):
        self.ensure_one()
        total_weighted_price = 0.0
        total_weight = 0.0
        for comp in comparables:
            score = max(self._comparable_similarity_score(comp), 1.0)
            total_weighted_price += comp.price_m2 * score
            total_weight += score
        return total_weighted_price / total_weight if total_weight else 0.0

    def _hybrid_price_m2(self, base_price_m2, comparable_price_m2):
        if base_price_m2 and comparable_price_m2:
            return (base_price_m2 * 0.55) + (comparable_price_m2 * 0.45)
        return base_price_m2 or comparable_price_m2

    def _factor_multiplier(self, factor_type, code):
        if not code:
            return 1.0
        factor = self.env["property.valuation.factor"].search(
            [
                ("active", "=", True),
                ("factor_type", "=", factor_type),
                ("code", "=", code),
                "|",
                ("company_id", "=", False),
                ("company_id", "=", self.company_id.id),
            ],
            limit=1,
        )
        return factor.multiplier if factor else 1.0

    def _calculate_confidence(self, reference, comparables):
        score = 25.0
        if reference:
            score += min(reference.confidence_score or 0.0, 100.0) * 0.25
        if comparables:
            score += min(len(comparables) * 4.0, 24.0)
            internal_count = len(comparables.filtered("is_internal_closed_deal"))
            score += min(internal_count * 3.0, 12.0)
            source_scores = [c.source_id.reliability_score for c in comparables if c.source_id]
            if source_scores:
                score += min(sum(source_scores) / len(source_scores), 100.0) * 0.12
        if self.city:
            score += 5.0
        if self.neighborhood:
            score += 5.0
        if self.area_m2:
            score += 5.0
        if self.standard:
            score += 3.0
        if self.conservation:
            score += 3.0
        return max(0.0, min(score, 100.0))

    def _range_margin(self, confidence_score):
        if confidence_score >= 85:
            return 8.0
        if confidence_score >= 70:
            return 12.0
        if confidence_score >= 55:
            return 18.0
        return 28.0

    def _build_calculation_notes(self, reference, comparables, selected_price_m2, adjusted_price_m2, confidence_score, margin_percent):
        lines = []
        lines.append("Método: %s" % (dict(self._fields["algorithm_code"].selection).get(self.algorithm_code) or self.algorithm_code))
        lines.append("Área considerada: %.2f m²" % self.area_m2)
        if reference:
            lines.append("Referência m² principal: %s | %.2f" % (reference.display_name, reference.price_m2))
        else:
            lines.append("Referência m² principal: não utilizada")
        if comparables:
            lines.append("Comparáveis utilizados: %s" % len(comparables))
            lines.append("Valor m² médio ponderado dos comparáveis: %.2f" % (self._weighted_comparable_price(comparables)))
        else:
            lines.append("Comparáveis utilizados: 0")
        lines.append("Valor m² selecionado antes dos fatores: %.2f" % selected_price_m2)
        lines.append("Fatores: localização %.4f | padrão %.4f | conservação %.4f | liquidez %.4f | vacância %.4f" % (
            self.location_factor or 1.0,
            self.standard_factor or 1.0,
            self.conservation_factor or 1.0,
            self.liquidity_factor or 1.0,
            self.vacancy_factor or 1.0,
        ))
        lines.append("Valor m² ajustado: %.2f" % adjusted_price_m2)
        lines.append("Confiança: %.2f%% | Margem da faixa: %.2f%%" % (confidence_score, margin_percent))
        lines.append("Aviso: estimativa gerencial; não substitui laudo técnico de avaliação.")
        return "\n".join(lines)

    @api.model
    def _asset_company(self, asset):
        company = getattr(asset, "company_id", False)
        return company if company else self.env.company

    @api.model
    def _asset_value(self, asset, field_names):
        for field_name in field_names:
            if field_name in asset._fields:
                value = asset[field_name]
                if value:
                    # Convert Many2one records to display text when used as location/type.
                    if hasattr(value, "display_name") and not isinstance(value, (str, int, float, bool)):
                        return value.display_name
                    return value
        return False


    @api.model
    def _normalize_use_type(self, value):
        value = self._norm(value)
        mapping = {
            "commercial": "commercial",
            "comercial": "commercial",
            "residential": "residential",
            "residencial": "residential",
            "industrial": "industrial",
            "galpao": "industrial",
            "galpão": "industrial",
            "warehouse": "industrial",
            "land": "land",
            "terreno": "land",
            "mixed": "mixed",
            "misto": "mixed",
        }
        return mapping.get(value, "other" if value else "commercial")

    @api.model
    def _normalize_standard(self, value):
        value = self._norm(value)
        mapping = {
            "low": "low",
            "simple": "low",
            "simples": "low",
            "medium": "medium",
            "medio": "medium",
            "médio": "medium",
            "high": "high",
            "alto": "high",
            "premium": "premium",
            "luxo": "premium",
        }
        return mapping.get(value, "medium")

    @api.model
    def _normalize_conservation(self, value):
        value = self._norm(value)
        mapping = {
            "new": "new",
            "novo": "new",
            "reformado": "new",
            "good": "good",
            "bom": "good",
            "regular": "regular",
            "needs_renovation": "needs_renovation",
            "necessita reforma": "needs_renovation",
            "reformar": "needs_renovation",
            "ruim": "needs_renovation",
        }
        return mapping.get(value, "good")

    @api.model
    def _safe_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @api.model
    def _norm(self, value):
        return (value or "").strip().lower()
