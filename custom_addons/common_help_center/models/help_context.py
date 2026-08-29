# -*- coding: utf-8 -*-
from odoo import fields, models


class HelpContext(models.Model):
    _name = "help.context"
    _description = "Contexto de Ajuda"
    _order = "priority, name"

    name = fields.Char(string="Nome", required=True)
    category_id = fields.Many2one("help.category", string="Categoria/Área", ondelete="set null")
    context_kind = fields.Selection([
        ("screen", "Ajuda de Tela"),
        ("flow", "Fluxo Operacional"),
        ("field", "Ajuda de Campo"),
        ("checklist", "Checklist"),
        ("admin", "Administração"),
        ("technical", "Técnico"),
        ("troubleshooting", "Troubleshooting"),
    ], string="Tipo de Contexto", default="screen", required=True)
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
    menu_xmlid = fields.Char(string="XML ID do Menu")
    action_xmlid = fields.Char(string="XML ID da Ação")
    article_ids = fields.Many2many("help.article", "help_context_article_rel", "context_id", "article_id", string="Artigos")
    priority = fields.Integer(string="Prioridade", default=10)
    active = fields.Boolean(string="Ativo", default=True)
    description = fields.Text(string="Descrição")

    def action_open_articles(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Artigos de Ajuda",
            "res_model": "help.article",
            "view_mode": "list,form",
            "domain": [("id", "in", self.article_ids.ids)],
            "context": {"default_model_name": self.model_name, "default_module_name": self.module_name},
        }
