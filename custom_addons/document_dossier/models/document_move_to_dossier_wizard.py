from odoo import fields, models, _
from odoo.exceptions import ValidationError


class DocumentMoveToDossierWizard(models.TransientModel):
    _name = "document.move.to.dossier.wizard"
    _description = "Vincular Documento ao Dossiê"

    document_id = fields.Many2one(
        "document.document",
        string="Documento",
        required=True,
        readonly=True,
    )
    dossier_id = fields.Many2one(
        "dossier.dossier",
        string="Dossiê de Destino",
        required=True,
    )

    def action_link(self):
        self.ensure_one()
        if self.document_id in self.dossier_id.document_ids:
            raise ValidationError(_("O documento já está neste dossiê."))

        # Add document to dossier using M2M relationship
        self.dossier_id.write({
            "document_ids": [(4, self.document_id.id)],
        })
        return {"type": "ir.actions.act_window_close"}


    def action_move(self):
        # Compatibilidade com botões antigos.
        return self.action_link()
