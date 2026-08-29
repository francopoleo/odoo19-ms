# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HelpMetric(models.Model):
    _name = "help.metric"
    _description = "Métrica de Uso da Central de Ajuda"
    _order = "create_date desc"

    event_type = fields.Selection([
        ("drawer_open", "Abertura do painel"),
        ("article_open", "Abertura de artigo"),
        ("search", "Busca"),
        ("feedback", "Feedback"),
        ("error_suggest", "Sugestão por erro"),
        ("checklist", "Checklist"),
    ], string="Tipo de Evento", default="drawer_open", required=True, index=True)
    article_id = fields.Many2one("help.article", string="Artigo", ondelete="set null")
    user_id = fields.Many2one("res.users", string="Usuário", default=lambda self: self.env.user, required=True, index=True)
    model_name = fields.Char(string="Model")
    view_type = fields.Char(string="Tipo de View")
    menu_xmlid = fields.Char(string="XML ID do Menu")
    action_xmlid = fields.Char(string="XML ID da Ação")
    record_id = fields.Integer(string="ID do Registro")
    query = fields.Char(string="Busca")
    error_text = fields.Text(string="Erro / Texto analisado")

    @api.model
    def log_event(self, values=None):
        values = dict(values or {})
        values.setdefault("user_id", self.env.user.id)
        return self.sudo().create(values).id
