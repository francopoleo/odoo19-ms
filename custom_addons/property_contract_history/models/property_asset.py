# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PropertyAsset(models.Model):
    _inherit = "property.asset"

    # Contract history tracking
    contract_history_count = fields.Integer(
        "Qtd. Contratos",
        compute="_compute_contract_history_count",
        help="Número de contratos sincronizados com este imóvel",
    )

    contract_history_ids = fields.One2many(
        "property.contract.history",
        "synced_to_asset_id",
        string="Histórico de Contratos",
        readonly=True,
        help="Contratos sincronizados a partir do módulo property_contract_history",
    )

    last_contract_sync = fields.Datetime(
        "Última Sincronização de Contrato",
        readonly=True,
        help="Quando foi feita a última sincronização de contrato?",
    )

    last_contract_source_id = fields.Many2one(
        "property.contract.history",
        string="Última Fonte",
        readonly=True,
        help="Qual contrato foi a última fonte de atualização de dados?",
    )

    @api.depends("contract_history_ids")
    def _compute_contract_history_count(self):
        for asset in self:
            asset.contract_history_count = len(asset.contract_history_ids)

    def action_view_contract_history(self):
        """View all contract history records linked to this asset."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Histórico de Contratos",
            "res_model": "property.contract.history",
            "view_mode": "list,form",
            "domain": [("synced_to_asset_id", "=", self.id)],
            "context": {"default_asset_id": self.id},
            "target": "current",
        }

    def action_import_contract_history(self):
        """Open dialog to import a contract."""
        return {
            "type": "ir.actions.act_window",
            "name": "Importar Contrato Histórico",
            "res_model": "property.contract.history",
            "view_mode": "form",
            "target": "new",
            "context": {"default_asset_id": self.id},
        }
