# -*- coding: utf-8 -*-
from odoo import fields, models, _


class DocumentDocumentDossierExt(models.Model):
    _inherit = "document.document"

    dossier_ids = fields.Many2many(
        comodel_name="dossier.dossier",
        relation="dossier_dossier_document_rel",
        column1="document_id",
        column2="dossier_id",
        string="Dossiês",
        readonly=True,
        copy=False,
        help="Dossiês nos quais este documento está incluído.",
    )
    dossier_count = fields.Integer(
        string="Qtd. Dossiês",
        compute="_compute_dossier_count",
    )

    def _compute_dossier_count(self):
        for document in self:
            document.dossier_count = len(document.dossier_ids)

    def action_view_dossiers(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Dossiês do Documento"),
            "res_model": "dossier.dossier",
            "view_mode": "kanban,list,form",
            "domain": [("id", "in", self.dossier_ids.ids)],
            "context": {"create": False},
        }

    def action_add_to_dossier(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Vincular ao Dossiê"),
            "res_model": "document.move.to.dossier.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_document_id": self.id},
        }
