# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HelpTip(models.Model):
    _name = "help.tip"
    _description = "Dica Contextual da Central de Ajuda"
    _order = "sequence, name"

    name = fields.Char(string="Título", required=True)
    code = fields.Char(string="Código", index=True)
    content = fields.Text(string="Dica", required=True)
    module_name = fields.Char(string="Módulo")
    model_name = fields.Char(string="Model")
    view_type = fields.Selection([
        ("form", "Formulário"),
        ("list", "Lista"),
        ("kanban", "Kanban"),
        ("calendar", "Calendário"),
        ("search", "Pesquisa"),
        ("pivot", "Tabela Dinâmica"),
        ("graph", "Gráfico"),
        ("activity", "Atividades"),
        ("gantt", "Gantt"),
        ("cohort", "Coorte"),
        ("map", "Mapa"),
        ("dashboard", "Dashboard"),
        ("other", "Outro"),
    ], string="Tipo de View")
    field_name = fields.Char(string="Campo")
    audience = fields.Selection([
        ("all", "Todos"),
        ("user", "Usuário"),
        ("admin", "Administrador"),
        ("technical", "Técnico"),
    ], string="Público", default="all", required=True)
    article_id = fields.Many2one("help.article", string="Artigo relacionado", ondelete="set null")
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
            records |= super(HelpTip, self).create([vals])
        return records
