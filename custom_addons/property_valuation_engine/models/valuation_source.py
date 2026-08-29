# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyValuationSource(models.Model):
    _name = "property.valuation.source"
    _description = "Fonte de Dados de Valuation Imobiliário"
    _order = "sequence, name"
    _check_company_auto = True

    name = fields.Char(string="Fonte", required=True, index=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        default=lambda self: self.env.company,
        index=True,
    )
    source_type = fields.Selection(
        [
            ("internal_contract", "Contrato interno"),
            ("internal_offer", "Proposta interna"),
            ("manual_research", "Pesquisa manual"),
            ("market_index", "Índice de mercado"),
            ("portal", "Portal imobiliário"),
            ("spreadsheet", "Planilha importada"),
            ("api", "API/parceiro de dados"),
            ("other", "Outra"),
        ],
        string="Tipo",
        default="manual_research",
        required=True,
    )
    url = fields.Char(string="URL / Referência")
    reliability_score = fields.Float(
        string="Confiabilidade (%)",
        default=70.0,
        help="Nota de 0 a 100 usada no cálculo de confiança da estimativa.",
    )
    notes = fields.Text(string="Observações")

    _source_reliability_range = models.Constraint(
        'CHECK(reliability_score >= 0 AND reliability_score <= 100)',
        'A confiabilidade da fonte deve estar entre 0 e 100.',
    )

    @api.constrains("reliability_score")
    def _check_reliability_score(self):
        for rec in self:
            if rec.reliability_score < 0 or rec.reliability_score > 100:
                raise ValidationError("A confiabilidade da fonte deve estar entre 0 e 100.")
