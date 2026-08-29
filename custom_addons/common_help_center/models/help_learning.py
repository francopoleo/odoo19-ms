# -*- coding: utf-8 -*-
from odoo import fields, models


class HelpLearningPath(models.Model):
    _name = "help.learning.path"
    _description = "Trilha de Aprendizado"
    _order = "sequence, name"

    name = fields.Char(string="Nome", required=True)
    module_name = fields.Char(string="Módulo")
    description = fields.Text(string="Descrição")
    audience = fields.Selection([
        ("all", "Todos"),
        ("user", "Usuário"),
        ("admin", "Administrador"),
        ("technical", "Técnico"),
    ], string="Público", default="user", required=True)
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativo", default=True)
    step_ids = fields.One2many("help.learning.step", "learning_path_id", string="Passos")


class HelpLearningStep(models.Model):
    _name = "help.learning.step"
    _description = "Passo da Trilha de Aprendizado"
    _order = "sequence, id"

    learning_path_id = fields.Many2one("help.learning.path", string="Trilha", required=True, ondelete="cascade")
    name = fields.Char(string="Nome", required=True)
    description = fields.Text(string="Descrição")
    article_id = fields.Many2one("help.article", string="Artigo")
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativo", default=True)
