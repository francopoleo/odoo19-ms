# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PropertyAssetExt(models.Model):
    """Extend property.asset with document dossier support"""
    _inherit = "property.asset"

    # ── Document Dossier Integration ──────────────────────────────────
    dossier_ids = fields.Many2many(
        comodel_name="dossier.dossier",
        relation="property_asset_dossier_rel",
        column1="asset_id",
        column2="dossier_id",
        string="Document Dossiérs",
        help="Link to document dossiérs for property acquisition, sale, lease, or inspection documentation",
    )

    dossier_count = fields.Integer(
        string="Dossiér Count",
        compute="_compute_dossier_count",
        store=True,
    )

    # ── Computed Fields ───────────────────────────────────────────────
    @api.depends("dossier_ids")
    def _compute_dossier_count(self):
        """Count linked dossiérs"""
        for record in self:
            record.dossier_count = len(record.dossier_ids)

    # ── Action Methods ────────────────────────────────────────────────

    def action_assign_dossier_template(self):
        """Abre o wizard único de atribuição de dossiê para o imóvel."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Atribuir Dossiê de Documentação"),
            "res_model": "dossier.assign.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_target_model": self._name,
                "default_target_id": self.id,
                "default_process_xmlid": "document_dossier.process_property_lease",
            },
        }

    def action_view_dossiers(self):
        """Open dossiers linked to this property.

        If there is a single dossier, open it directly in form view to avoid
        an unnecessary Kanban/list intermediary. With multiple dossiers, open
        a list-first action that remains compatible with Odoo 19.
        """
        self.ensure_one()
        if len(self.dossier_ids) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": self.dossier_ids.name,
                "res_model": "dossier.dossier",
                "res_id": self.dossier_ids.id,
                "view_mode": "form",
                "target": "current",
            }
        return {
            "type": "ir.actions.act_window",
            "name": _("Dossiês do Imóvel"),
            "res_model": "dossier.dossier",
            "view_mode": "list,form,kanban",
            "domain": [("id", "in", self.dossier_ids.ids)],
            "context": {"default_domain": "property"},
        }

    def action_create_purchase_dossier(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Atribuir Dossiê de Documentação"),
            "res_model": "dossier.assign.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_target_model": self._name,
                "default_target_id": self.id,
                "default_process_xmlid": "document_dossier.process_property_purchase",
            },
        }

    def action_create_sale_dossier(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Atribuir Dossiê de Documentação"),
            "res_model": "dossier.assign.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_target_model": self._name,
                "default_target_id": self.id,
                "default_process_xmlid": "document_dossier.process_property_sale",
            },
        }

    def action_create_lease_dossier(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Atribuir Dossiê de Documentação"),
            "res_model": "dossier.assign.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_target_model": self._name,
                "default_target_id": self.id,
                "default_process_xmlid": "document_dossier.process_property_lease",
            },
        }
