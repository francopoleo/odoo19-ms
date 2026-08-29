from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PropertyMediaBulkWizard(models.TransientModel):
    _name = "property.media.bulk.wizard"
    _description = "Adicionar Múltiplas Mídias"

    context_selection = fields.Selection([
        ("asset_gallery", "Galeria do Imóvel"),
        ("inspection", "Vistoria"),
        ("maintenance", "Manutenção"),
        ("asset_other", "Outras Mídias do Imóvel"),
        ("document_support", "Apoio Documental"),
    ], string="Fluxo", required=True, default="asset_gallery")

    asset_id = fields.Many2one("property.asset", string="Imóvel")
    inspection_id = fields.Many2one("property.inspection", string="Vistoria")
    maintenance_id = fields.Many2one("property.maintenance", string="Manutenção")

    purpose = fields.Selection([
        ("asset_gallery", "Galeria do Imóvel"),
        ("inspection", "Vistoria"),
        ("maintenance", "Manutenção"),
        ("other", "Outras Mídias"),
        ("document_support", "Apoio Documental"),
    ], string="Finalidade", required=True, default="asset_gallery")

    category_id = fields.Many2one(
        "property.media.category",
        string="Categoria",
        domain="['|', ('applicable_purpose', '=', purpose), ('applicable_purpose', '=', 'all')]",
    )
    upload_kind = fields.Selection([
        ("auto", "Detectar automaticamente"),
        ("image", "Salvar como Foto / Imagem"),
        ("document", "Salvar como Arquivo / Documento"),
    ], string="Enviar como", default="auto", required=True)

    visibility_level = fields.Selection([
        ("internal", "Somente Interno"),
        ("restricted_internal", "Interno Restrito"),
        ("authorized_brokers", "Corretores Autorizados"),
        ("portal", "Somente Logado"),
        ("public", "Público"),
    ], string="Visibilidade", required=True, default="internal")
    website_published = fields.Boolean("Publicar no Site", default=False)
    publication_state = fields.Selection([
        ("draft", "Rascunho"),
        ("review", "Em Revisão"),
        ("approved", "Aprovado"),
        ("published", "Publicado"),
        ("archived", "Arquivado"),
    ], string="Status Editorial", default="draft")
    allow_download = fields.Boolean("Permitir Download", default=True)

    image_ids = fields.Many2many(
        "ir.attachment",
        relation="property_media_bulk_wizard_attachment_rel",
        column1="wizard_id",
        column2="attachment_id",
        string="Imagens / Arquivos",
        help="Selecione múltiplos arquivos para criar registros de mídia de uma vez.",
    )

    step = fields.Selection([
        ("select_context", "Selecionar Contexto"),
        ("upload_files", "Enviar Arquivos"),
        ("confirm", "Confirmar"),
    ], string="Etapa", default="select_context", readonly=True)

    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        context_selection = vals.get("context_selection") or self.env.context.get("default_context_selection")
        if context_selection:
            vals["context_selection"] = context_selection
        return vals

    @api.onchange("context_selection", "asset_id", "inspection_id", "maintenance_id")
    def _onchange_context(self):
        for wiz in self:
            if wiz.context_selection == "asset_gallery":
                wiz.purpose = "asset_gallery"
                wiz.upload_kind = "image"
                wiz.visibility_level = "public"
                wiz.website_published = True
                wiz.publication_state = "approved"
            elif wiz.context_selection == "inspection":
                wiz.purpose = "inspection"
                wiz.upload_kind = self.env.context.get("default_upload_kind") or "auto"
                wiz.visibility_level = "internal"
                wiz.website_published = False
                if wiz.inspection_id and wiz.inspection_id.asset_id:
                    wiz.asset_id = wiz.inspection_id.asset_id
            elif wiz.context_selection == "maintenance":
                wiz.purpose = "maintenance"
                wiz.upload_kind = self.env.context.get("default_upload_kind") or "auto"
                wiz.visibility_level = "internal"
                wiz.website_published = False
                if wiz.maintenance_id and wiz.maintenance_id.asset_id:
                    wiz.asset_id = wiz.maintenance_id.asset_id
            elif wiz.context_selection == "asset_other":
                wiz.purpose = "other"
                wiz.upload_kind = "auto"
                wiz.visibility_level = "internal"
                wiz.website_published = False
            elif wiz.context_selection == "document_support":
                wiz.purpose = "document_support"
                wiz.upload_kind = "document"
                wiz.visibility_level = "internal"
                wiz.website_published = False

    def action_next_step(self):
        self.ensure_one()
        if self.step == "select_context":
            self._validate_context()
            self.step = "upload_files"
        elif self.step == "upload_files":
            if not self.image_ids:
                raise ValidationError(_("Selecione pelo menos uma imagem ou arquivo."))
            self.step = "confirm"
        return self._reload()

    def action_previous_step(self):
        self.ensure_one()
        if self.step == "confirm":
            self.step = "upload_files"
        elif self.step == "upload_files":
            self.step = "select_context"
        return self._reload()

    def _reload(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "property.media.bulk.wizard",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
            "views": [(False, "form")],
        }

    def _validate_context(self):
        self.ensure_one()
        if self.context_selection in ("asset_gallery", "asset_other") and not self.asset_id:
            raise ValidationError(_("Selecione um imóvel."))
        if self.context_selection == "inspection" and not self.inspection_id:
            raise ValidationError(_("Selecione uma vistoria."))
        if self.context_selection == "maintenance" and not self.maintenance_id:
            raise ValidationError(_("Selecione uma manutenção."))
        if self.context_selection == "document_support" and not self.asset_id:
            raise ValidationError(_("Selecione um imóvel."))

    def _content_kind_for_attachment(self, attachment):
        self.ensure_one()
        if self.upload_kind in ("image", "document"):
            return self.upload_kind
        mimetype = attachment.mimetype or ""
        return "image" if mimetype.startswith("image/") else "document"

    def action_create_media(self):
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
                vals["asset_id"] = self.asset_id.id if self.asset_id else False

            Media.create(vals)

        return {"type": "ir.actions.act_window_close"}


class PropertyMediaBulkWizardLine(models.TransientModel):
    _name = "property.media.bulk.wizard.line"
    _description = "Linha do Wizard de Múltiplas Mídias"
    _order = "sequence"

    wizard_id = fields.Many2one("property.media.bulk.wizard", ondelete="cascade")
    attachment_id = fields.Many2one("ir.attachment", string="Arquivo", ondelete="cascade")
    name = fields.Char("Nome da Mídia")
    caption = fields.Char("Legenda")
    location_note = fields.Char("Ambiente / Local")
    sequence = fields.Integer(default=10)

    def init(self):
        # Defensive cleanup for databases that received earlier wizard versions
        # where these transient columns were NOT NULL. The new wizard does not
        # depend on this line model during upload, but old schema constraints can
        # still block temporary saves in Odoo.
        self.env.cr.execute("""
            ALTER TABLE IF EXISTS property_media_bulk_wizard_line
            ALTER COLUMN attachment_id DROP NOT NULL,
            ALTER COLUMN name DROP NOT NULL,
            ALTER COLUMN wizard_id DROP NOT NULL
        """)
