# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HelpCategory(models.Model):
    _name = "help.category"
    _description = "Categoria da Central de Ajuda"
    _order = "sequence, name"

    name = fields.Char(string="Nome", required=True, translate=True)
    code = fields.Char(string="Código", required=True, index=True)
    parent_id = fields.Many2one("help.category", string="Categoria Pai", ondelete="restrict")
    child_ids = fields.One2many("help.category", "parent_id", string="Subcategorias")
    sequence = fields.Integer(string="Sequência", default=10)
    description = fields.Text(string="Descrição", translate=True)
    active = fields.Boolean(string="Ativo", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Criação idempotente para dados-base.

        Durante testes e reinstalações pode existir uma categoria criada por uma
        versão anterior sem o XML ID atual. Em vez de quebrar a instalação por
        código repetido, reutilizamos/atualizamos a categoria existente.
        """
        records = self.browse()
        for vals in vals_list:
            code = vals.get("code")
            if code:
                existing = self.search([("code", "=", code)], limit=1)
                if existing:
                    existing.write(vals)
                    records |= existing
                    continue
            records |= super(HelpCategory, self).create([vals])
        return records
