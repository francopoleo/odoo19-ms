# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models


class HelpSuggestionRule(models.Model):
    _name = "help.suggestion.rule"
    _description = "Regra de Sugestão Inteligente da Central de Ajuda"
    _order = "sequence, name"

    name = fields.Char(string="Nome", required=True)
    code = fields.Char(string="Código", index=True)
    rule_type = fields.Selection([
        ("error", "Erro / Exceção"),
        ("missing_required", "Campo obrigatório faltante"),
        ("state_flow", "Fluxo por situação"),
        ("context", "Contexto geral"),
    ], string="Tipo de Regra", default="context", required=True, index=True)
    pattern = fields.Char(string="Padrão / Regex")
    module_name = fields.Char(string="Módulo")
    model_name = fields.Char(string="Model")
    field_name = fields.Char(string="Campo")
    state_value = fields.Char(string="Situação / Status")
    tip_text = fields.Text(string="Sugestão curta")
    article_ids = fields.Many2many("help.article", "help_suggestion_article_rel", "rule_id", "article_id", string="Artigos sugeridos")
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativo", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = self.browse()
        for vals in vals_list:
            code = vals.get("code")
            if code:
                existing = self.search([("code", "=", code)], limit=1)
                if existing:
                    existing.write(vals)
                    records |= existing
                    continue
            records |= super(HelpSuggestionRule, self).create([vals])
        return records

    def _matches_text(self, text):
        self.ensure_one()
        if not self.pattern:
            return False
        try:
            return bool(re.search(self.pattern, text or "", re.IGNORECASE | re.MULTILINE))
        except re.error:
            return (self.pattern or "").lower() in (text or "").lower()
