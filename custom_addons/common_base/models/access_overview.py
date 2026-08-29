# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccessOverview(models.Model):
    """Vista consolidada de todas as permissões agrupadas por módulo."""
    _name = 'access.overview'
    _description = 'Visão Geral de Permissões'
    _auto = False

    module = fields.Char('Módulo', readonly=True)
    model_name = fields.Char('Modelo', readonly=True)
    group_id = fields.Char('Grupo de Acesso', readonly=True)
    perm_read = fields.Boolean('Ler', readonly=True)
    perm_write = fields.Boolean('Escrever', readonly=True)
    perm_create = fields.Boolean('Criar', readonly=True)
    perm_unlink = fields.Boolean('Deletar', readonly=True)

    @api.model
    def _auto_init(self):
        # This is a read-only view, no table in database
        return True

    def init(self):
        """Cria a view SQL."""
        query = """
            DROP VIEW IF EXISTS access_overview CASCADE;
            CREATE VIEW access_overview AS
            SELECT
                row_number() OVER (ORDER BY imd_module.module, ima.model_id, ima.group_id) as id,
                COALESCE(imd_module.module, 'core'::text) as module,
                imd.model as model_name,
                COALESCE(rg.name::text, 'Sem grupo'::text) as group_id,
                ima.perm_read,
                ima.perm_write,
                ima.perm_create,
                ima.perm_unlink
            FROM ir_model_access ima
            JOIN ir_model imd ON ima.model_id = imd.id
            LEFT JOIN ir_model_data imd_module ON imd_module.model = 'ir.model.access'
                AND imd_module.res_id = ima.id
            LEFT JOIN res_groups rg ON ima.group_id = rg.id
        """
        self.env.cr.execute(query)