# -*- coding: utf-8 -*-
from odoo import fields, models, _


class GovernanceCaseExt(models.Model):
    """Extend governance.case with document dossier support"""
    _inherit = "governance.case"

    # ── Document Dossier Integration ──────────────────────────────────
    dossier_id = fields.Many2one(
        comodel_name="dossier.dossier",
        string="Document Dossier",
        ondelete="set null",
        help="Link to a document dossier for managing required documentation",
    )

    # Readonly computed field showing dossier status
    dossier_completion_percent = fields.Float(
        string="Dossier Completion %",
        related="dossier_id.completion_percent",
        readonly=True,
    )

    dossier_complete = fields.Boolean(
        string="Dossier Complete",
        related="dossier_id.dossier_complete",
        readonly=True,
    )

    dossier_document_count = fields.Integer(
        string="Required Documents",
        related="dossier_id.document_count",
        readonly=True,
    )

    dossier_missing_requirements = fields.Integer(
        string="Missing Fields",
        related="dossier_id.missing_requirements",
        readonly=True,
    )

    # ── Action Methods ────────────────────────────────────────────────
    def action_assign_dossier_template(self):
        """Abre o wizard único de atribuição de dossiê."""
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
                "default_process_xmlid": "document_dossier.process_governance_audit",
            },
        }

    def action_view_dossier(self):
        """Open the attached dossier"""
        if not self.dossier_id:
            return
        return {
            "type": "ir.actions.act_window",
            "name": self.dossier_id.name,
            "res_model": "dossier.dossier",
            "res_id": self.dossier_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_view_dossier_documents(self):
        """Open documents within the dossier"""
        if not self.dossier_id or not self.dossier_id.document_ids:
            return
        return {
            "type": "ir.actions.act_window",
            "name": _("Documentos do Dossiê"),
            "res_model": "document.document",
            "view_mode": "kanban,list,form",
            "domain": [("id", "in", self.dossier_id.document_ids.ids)],
        }
