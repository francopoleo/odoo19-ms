from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DocumentUploadWizard(models.TransientModel):
    _name = "document.upload.wizard"
    _description = "Assistente de Upload de Documentos"

    document_name = fields.Char("Nome do Documento", required=True)
    document_type_id = fields.Many2one(
        "document.type",
        string="Tipo de Documento",
        required=True,
        domain=[("portal_uploadable", "=", True)],
        help="Selecione um tipo de documento que permite upload no portal"
    )
    asset_reference_code = fields.Char("Código da Propriedade", required=True, help="Ex: MALL-LOJ001")
    description = fields.Text("Descrição (opcional)")
    attachment_file = fields.Binary("Arquivo", required=True, attachment=True)
    attachment_filename = fields.Char("Nome do Arquivo")
    issue_date = fields.Date("Data de Emissão")
    expiry_date = fields.Date("Data de Vencimento (opcional)")

    def action_create_document(self):
        """Cria um novo documento a partir do upload."""
        self.ensure_one()

        if not self.attachment_file:
            raise ValidationError(_("Arquivo é obrigatório"))

        # Criar documento em rascunho
        document_vals = {
            "name": self.document_name,
            "document_type_id": self.document_type_id.id,
            "asset_reference_code": self.asset_reference_code,
            "description": self.description,
            "issue_date": self.issue_date,
            "expiry_date": self.expiry_date,
            "document_workflow_state": "draft",
            "portal_uploadable": True,
            "access_level": "portal",
            "source": "tenant",
        }

        document = self.env["document.document"].create(document_vals)

        # Criar attachment
        attachment = self.env["ir.attachment"].create({
            "name": self.attachment_filename,
            "type": "binary",
            "datas": self.attachment_file,
            "res_model": "document.document",
            "res_id": document.id,
            "public": False,
        })

        # Associar attachment ao documento
        document.attachment_ids = [(4, attachment.id)]

        return {
            "type": "ir.actions.act_window",
            "res_model": "document.document",
            "res_id": document.id,
            "view_mode": "form",
            "target": "current",
        }