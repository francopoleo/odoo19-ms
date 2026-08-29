# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HelpChecklistTemplate(models.Model):
    _name = "help.checklist.template"
    _description = "Template de Checklist da Central de Ajuda"
    _order = "sequence, name"

    name = fields.Char(string="Nome", required=True)
    code = fields.Char(string="Código", index=True)
    description = fields.Text(string="Descrição")
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
    audience = fields.Selection([
        ("all", "Todos"),
        ("user", "Usuário"),
        ("admin", "Administrador"),
        ("technical", "Técnico"),
    ], string="Público", default="user", required=True)
    item_ids = fields.One2many("help.checklist.item", "template_id", string="Itens")
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
            records |= super(HelpChecklistTemplate, self).create([vals])
        return records


class HelpChecklistItem(models.Model):
    _name = "help.checklist.item"
    _description = "Item de Checklist da Central de Ajuda"
    _order = "sequence, id"

    template_id = fields.Many2one("help.checklist.template", string="Checklist", required=True, ondelete="cascade")
    name = fields.Char(string="Item", required=True)
    description = fields.Text(string="Descrição")
    article_id = fields.Many2one("help.article", string="Artigo relacionado", ondelete="set null")
    sequence = fields.Integer(string="Sequência", default=10)
    required = fields.Boolean(string="Obrigatório")
    active = fields.Boolean(string="Ativo", default=True)


class HelpChecklistProgress(models.Model):
    _name = "help.checklist.progress"
    _description = "Progresso de Checklist da Central de Ajuda"
    _order = "write_date desc"

    user_id = fields.Many2one("res.users", string="Usuário", default=lambda self: self.env.user, required=True, index=True)
    template_id = fields.Many2one("help.checklist.template", string="Checklist", required=True, ondelete="cascade")
    item_id = fields.Many2one("help.checklist.item", string="Item", required=True, ondelete="cascade")
    model_name = fields.Char(string="Model")
    record_id = fields.Integer(string="Registro")
    done = fields.Boolean(string="Concluído", default=False)

    @api.model
    def toggle_progress(self, item_id, model_name=None, record_id=None, done=None):
        item = self.env["help.checklist.item"].browse(int(item_id)).exists()
        if not item:
            return False
        domain = [
            ("user_id", "=", self.env.user.id),
            ("item_id", "=", item.id),
            ("model_name", "=", model_name or False),
            ("record_id", "=", int(record_id or 0)),
        ]
        progress = self.search(domain, limit=1)
        values = {
            "user_id": self.env.user.id,
            "template_id": item.template_id.id,
            "item_id": item.id,
            "model_name": model_name or False,
            "record_id": int(record_id or 0),
        }
        if progress:
            progress.done = bool(done) if done is not None else not progress.done
            return progress.done
        values["done"] = bool(done) if done is not None else True
        self.create(values)
        return values["done"]
