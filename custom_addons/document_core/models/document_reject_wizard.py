from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DocumentRejectWizard(models.TransientModel):
    _name = "document.reject.wizard"
    _description = "Assistente de Rejeição de Documento"

    document_id = fields.Many2one("document.document", string="Documento", required=True, ondelete="cascade")
    rejection_notes = fields.Text("Motivo da Rejeição", required=True, placeholder="Explique por que o documento está sendo rejeitado...")

    def action_confirm_reject(self):
        """Rejeita o documento com as notas."""
        self.ensure_one()

        if not self.rejection_notes.strip():
            raise ValidationError(_("Você deve informar o motivo da rejeição"))

        self.document_id.write({
            "document_workflow_state": "rejected",
            "approval_notes": self.rejection_notes,
        })

        # Log activity
        self.document_id.message_post(
            body=_("Documento rejeitado por %s.<br/>Motivo: %s") % (
                self.env.user.name,
                self.rejection_notes,
            ),
            message_type="notification",
        )

        return {"type": "ir.actions.act_window_close"}