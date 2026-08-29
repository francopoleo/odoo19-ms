from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PropertyMediaBulkWizardDocumentExt(models.Model):
    _inherit = "property.media.bulk.wizard"

    document_id = fields.Many2one("document.document", string="Documento")

    @api.onchange("context_selection", "asset_id", "inspection_id", "maintenance_id", "document_id")
    def _onchange_context_document(self):
        super()._onchange_context()

    def _validate_context(self):
        super()._validate_context()
        self.ensure_one()
        if self.context_selection == "document_support" and not (self.document_id or self.asset_id):
            raise ValidationError(_("Selecione um documento ou imóvel."))

    def action_create_media(self):
        """Enhanced action_create_media to handle document_id."""
        self.ensure_one()
        self._validate_context()
        if not self.image_ids:
            raise ValidationError(_("Selecione pelo menos uma imagem ou arquivo."))

        Media = self.env["property.media"]
        for index, attachment in enumerate(self.image_ids):
            content_kind = self._content_kind_for_attachment(attachment)
            vals = {
                "name": (attachment.name or _("Mídia")).rsplit(".", 1)[0],
                "purpose": self.purpose,
                "category_id": self.category_id.id if self.category_id else False,
                "content_kind": content_kind,
                "visibility_level": self.visibility_level,
                "website_published": self.website_published if self.purpose == "asset_gallery" else False,
                "publication_state": self.publication_state,
                "allow_download": self.allow_download,
                "sequence": (index + 1) * 10,
                "company_id": self.env.company.id,
                "file_name": attachment.name,
            }
            if content_kind == "image":
                vals["image_1920"] = attachment.datas
            else:
                vals["file_data"] = attachment.datas

            if self.purpose in ("asset_gallery", "other"):
                vals["asset_id"] = self.asset_id.id
            elif self.purpose == "inspection":
                vals["inspection_id"] = self.inspection_id.id
                vals["asset_id"] = self.inspection_id.asset_id.id
            elif self.purpose == "maintenance":
                vals["maintenance_id"] = self.maintenance_id.id
                vals["asset_id"] = self.maintenance_id.asset_id.id
            elif self.purpose == "document_support":
                vals["document_id"] = self.document_id.id if self.document_id else False
                vals["asset_id"] = self.asset_id.id if self.asset_id else (self.document_id.asset_id.id if self.document_id and getattr(self.document_id, "asset_id", False) else False)

            Media.create(vals)

        return {"type": "ir.actions.act_window_close"}
