# -*- coding: utf-8 -*-
from odoo import fields, models


class HelpFeedback(models.Model):
    _name = "help.feedback"
    _description = "Feedback da Central de Ajuda"
    _order = "create_date desc"

    article_id = fields.Many2one("help.article", string="Artigo", required=True, ondelete="cascade")
    user_id = fields.Many2one("res.users", string="Usuário", default=lambda self: self.env.user, required=True)
    rating = fields.Selection([("useful", "Útil"), ("not_useful", "Não útil")], string="Avaliação", required=True)
    comment = fields.Text(string="Comentário")
    model_name = fields.Char(string="Model de Origem")
    record_id = fields.Integer(string="Registro de Origem")
