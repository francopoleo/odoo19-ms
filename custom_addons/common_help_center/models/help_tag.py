# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HelpTag(models.Model):
    _name = "help.tag"
    _description = "Tag da Central de Ajuda"
    _order = "name"

    name = fields.Char(string="Nome", required=True, translate=True)
    color = fields.Integer(string="Cor")
    active = fields.Boolean(string="Ativo", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = self.browse()
        for vals in vals_list:
            name = vals.get("name")
            if name:
                existing = self.search([("name", "=", name)], limit=1)
                if existing:
                    existing.write(vals)
                    records |= existing
                    continue
            records |= super(HelpTag, self).create([vals])
        return records
