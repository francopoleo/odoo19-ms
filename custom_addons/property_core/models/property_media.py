from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import base64
import mimetypes


MEDIA_PURPOSE_SELECTION = [
    ("asset_gallery", "Galeria do Imóvel"),
    ("inspection", "Vistoria"),
    ("maintenance", "Manutenção"),
    ("other", "Outras Mídias"),
    ("document_support", "Apoio Documental"),
]


class PropertyMediaCategory(models.Model):
    _name = "property.media.category"
    _description = "Categoria de Mídia Imobiliária"
    _order = "applicable_purpose, sequence, name"

    name = fields.Char("Categoria", required=True, translate=True)
    code = fields.Char("Código", required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    applicable_purpose = fields.Selection(
        MEDIA_PURPOSE_SELECTION + [("all", "Todos os Fluxos")],
        string="Aplicável em",
        default="other",
        required=True,
        help="Define em quais fluxos esta categoria aparece. Evita misturar categorias de galeria, vistoria, manutenção e outras mídias.",
    )
    default_content_kind = fields.Selection(
        [("image", "Foto / Imagem"), ("document", "Arquivo / Documento")],
        string="Tipo Padrão",
        default="image",
        required=True,
    )
    publishable_default = fields.Boolean(
        "Pode ir para Site",
        default=False,
        help="Indica se essa categoria costuma ser publicável. A publicação real ainda depende da mídia estar na Galeria do Imóvel e aprovada.",
    )
    description = fields.Text("Descrição")

    _sql_constraints = [
        ("property_media_category_code_uniq", "unique(code)", "O código da categoria de mídia deve ser único."),
    ]


class PropertyMedia(models.Model):
    _name = "property.media"
    _description = "Mídia do Imóvel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "purpose, sequence, id"
    _rec_name = "display_name"

    # ==================== Identificação ====================
    name = fields.Char(
        "Título",
        required=True,
        tracking=True,
        help="Nome curto para identificar a mídia. Ex.: Fachada principal, Sala 01, Vazamento cozinha, Antes da pintura.",
    )
    display_name = fields.Char(compute="_compute_display_name", store=True)
    sequence = fields.Integer("Sequência", default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, index=True)

    # ==================== Organização Enterprise ====================
    purpose = fields.Selection(
        MEDIA_PURPOSE_SELECTION,
        string="Finalidade",
        default="asset_gallery",
        required=True,
        tracking=True,
        help="Fluxo principal da mídia. Use Galeria para site/comercial, Vistoria para evidências de vistoria, Manutenção para histórico técnico e Outras Mídias para imagens complementares do imóvel.",
    )
    category_id = fields.Many2one(
        "property.media.category",
        string="Categoria",
        tracking=True,
        domain="['|', ('applicable_purpose', '=', purpose), ('applicable_purpose', '=', 'all')]",
        help="Classificação dentro da finalidade. As categorias são configuráveis, mas filtradas por fluxo para manter consistência.",
    )
    content_kind = fields.Selection(
        [("image", "Foto / Imagem"), ("document", "Arquivo / Documento")],
        string="Tipo de Conteúdo",
        default="image",
        required=True,
        tracking=True,
        help="Controla qual campo de upload aparece no formulário e evita que uma mídia seja foto e documento ao mesmo tempo.",
    )

    # Campo técnico mantido apenas para compatibilidade interna de views/controladores antigos.
    # A organização nova deve usar purpose + category_id.
    media_role = fields.Selection([
        ("gallery", "Galeria do Imóvel"),
        ("inspection", "Vistoria"),
        ("maintenance", "Manutenção"),
        ("document_support", "Apoio a Documento"),
        ("technical", "Imagem Técnica"),
        ("marketing", "Material Comercial"),
        ("before", "Antes"),
        ("after", "Depois"),
        ("evidence", "Evidência Fotográfica"),
        ("scan", "Digitalização / Scan"),
    ], string="Uso Técnico", default="gallery", required=True)

    # ==================== Publicação / Acesso ====================
    visibility_level = fields.Selection([
        ("internal", "Somente Interno"),
        ("restricted_internal", "Interno Restrito"),
        ("authorized_brokers", "Corretores Autorizados"),
        ("portal", "Somente Logado"),
        ("public", "Público"),
    ], string="Visibilidade", default="internal", required=True, tracking=True)
    website_published = fields.Boolean("Publicar no Site", default=False, tracking=True)
    publication_state = fields.Selection([
        ("draft", "Rascunho"),
        ("review", "Em Revisão"),
        ("approved", "Aprovado"),
        ("published", "Publicado"),
        ("archived", "Arquivado"),
    ], string="Status Editorial", default="draft", tracking=True)
    allow_download = fields.Boolean("Permitir Download", default=True, tracking=True)
    is_cover = fields.Boolean("Imagem de Capa", tracking=True)

    # ==================== Vínculos ====================
    asset_id = fields.Many2one("property.asset", string="Imóvel", ondelete="cascade", tracking=True)
    inspection_id = fields.Many2one("property.inspection", string="Vistoria", ondelete="cascade", tracking=True)
    maintenance_id = fields.Many2one("property.maintenance", string="Manutenção", ondelete="cascade", tracking=True)

    # ==================== Arquivo / Imagem ====================
    image_1920 = fields.Image("Foto / Imagem", max_width=1920, max_height=1920)
    image_512 = fields.Image("Miniatura", related="image_1920", max_width=512, max_height=512, store=True)
    file_data = fields.Binary("Arquivo / Documento", attachment=True)
    file_name = fields.Char("Nome Original do Arquivo")
    file_mimetype = fields.Char("MIME Type", compute="_compute_file_meta", store=True, readonly=True)
    file_size = fields.Integer("Tamanho (bytes)", compute="_compute_file_meta", store=True, readonly=True)
    file_size_human = fields.Char("Tamanho", compute="_compute_file_meta", store=True, readonly=True)

    # ==================== Detalhes ====================
    caption = fields.Char("Legenda")
    description = fields.Text("Descrição")
    location_note = fields.Char("Ambiente / Local")
    date_taken = fields.Datetime("Data do Registro")
    taken_by = fields.Many2one("res.users", string="Registrado por", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(
        "common.tag",
        relation="common_tag_property_media_rel",
        column1="media_id",
        column2="tag_id",
        string="Tags",
    )

    def init(self):
        """Binary/image fields must never be tracked by mail.thread.

        Older development versions may have left tracking enabled in
        ir.model.fields for image_1920/image_512/file_data. Odoo cannot
        create chatter tracking values for binary fields, so replacing
        images/files would crash with: Unsupported tracking on field ...
        This cleanup runs on module update and is intentionally defensive.
        """
        self.env.cr.execute("""
            UPDATE ir_model_fields
               SET tracking = 0
             WHERE model IN ('property.media', 'property.asset', 'property.complex')
               AND ttype = 'binary'
               AND COALESCE(tracking, 0) <> 0
        """)

    @api.depends("name", "purpose", "asset_id", "inspection_id", "maintenance_id")
    def _compute_display_name(self):
        purpose_map = dict(self._fields["purpose"].selection)
        for rec in self:
            parts = [rec.name]
            context = rec.asset_id.display_name_full or rec.asset_id.name if rec.asset_id else False
            if not context and rec.inspection_id:
                context = rec.inspection_id.reference or rec.inspection_id.name
            if not context and rec.maintenance_id:
                context = rec.maintenance_id.reference or rec.maintenance_id.name
            if context:
                parts.append(context)
            parts.append(purpose_map.get(rec.purpose, rec.purpose))
            rec.display_name = " • ".join([p for p in parts if p])

    @api.depends("file_name", "file_data", "image_1920", "content_kind")
    def _compute_file_meta(self):
        for rec in self:
            rec.file_mimetype = mimetypes.guess_type(rec.file_name or "")[0] or False
            binary_data = rec.file_data or rec.image_1920
            size = 0
            if binary_data:
                try:
                    size = len(base64.b64decode(binary_data))
                except Exception:
                    size = 0
            rec.file_size = size
            if not size:
                rec.file_size_human = False
            elif size < 1024:
                rec.file_size_human = "%s B" % size
            elif size < 1024 * 1024:
                rec.file_size_human = "%.1f KB" % (size / 1024.0)
            else:
                rec.file_size_human = "%.1f MB" % (size / 1024.0 / 1024.0)

    @api.onchange("purpose")
    def _onchange_purpose(self):
        for rec in self:
            if rec.purpose == "asset_gallery":
                rec.content_kind = "image"
                rec.visibility_level = "public"
                rec.media_role = "gallery"
            elif rec.purpose == "inspection":
                rec.media_role = "inspection"
            elif rec.purpose == "maintenance":
                rec.media_role = "maintenance"
            elif rec.purpose == "document_support":
                rec.content_kind = "document"
                rec.media_role = "document_support"
            elif rec.purpose == "other":
                rec.media_role = "technical"
            if rec.category_id and rec.category_id.applicable_purpose not in (rec.purpose, "all"):
                rec.category_id = False

    @api.onchange("category_id")
    def _onchange_category_id(self):
        for rec in self:
            if rec.category_id and rec.category_id.default_content_kind:
                rec.content_kind = rec.category_id.default_content_kind

    @api.onchange("content_kind")
    def _onchange_content_kind(self):
        for rec in self:
            if rec.content_kind == "image":
                rec.file_data = False
            elif rec.content_kind == "document":
                rec.image_1920 = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._normalize_binary_vals(vals)
            self._normalize_role_vals(vals)
        return super().create(vals_list)

    def write(self, vals):
        vals = dict(vals)
        self._normalize_binary_vals(vals)
        self._normalize_role_vals(vals)
        return super().write(vals)

    @api.model
    def _normalize_binary_vals(self, vals):
        """Keep media binary fields mutually exclusive.

        Odoo's image/file widgets can update only the binary field that changed.
        When replacing a photo on an old/conflicting record, the previous
        document binary may remain in the database unless we explicitly clear it.
        The same applies when replacing a document on a record that used to be an
        image.  Normalize the incoming values before create/write so users can
        safely change the uploaded media from the form.
        """
        content_kind = vals.get("content_kind")
        has_new_image = bool(vals.get("image_1920"))
        has_new_file = bool(vals.get("file_data"))

        if content_kind == "image":
            vals["file_data"] = False
        elif content_kind == "document":
            vals["image_1920"] = False

        if has_new_image and has_new_file:
            if vals.get("content_kind") == "document":
                vals["image_1920"] = False
            else:
                vals["file_data"] = False
                vals["content_kind"] = "image"
        elif has_new_image:
            vals["content_kind"] = "image"
            vals["file_data"] = False
        elif has_new_file:
            vals["content_kind"] = "document"
            vals["image_1920"] = False

    @api.model
    def _normalize_role_vals(self, vals):
        purpose = vals.get("purpose")
        if not purpose:
            return
        mapping = {
            "asset_gallery": "gallery",
            "inspection": "inspection",
            "maintenance": "maintenance",
            "document_support": "document_support",
            "other": "technical",
        }
        vals.setdefault("media_role", mapping.get(purpose, "gallery"))

    @api.constrains("asset_id", "inspection_id", "maintenance_id", "purpose")
    def _check_context_link(self):
        for rec in self:
            if rec.purpose in ("asset_gallery", "other") and not rec.asset_id:
                raise ValidationError(_("Mídias de Galeria e Outras Mídias precisam estar vinculadas a um imóvel."))
            if rec.purpose == "inspection" and not rec.inspection_id:
                raise ValidationError(_("Mídias de vistoria precisam estar vinculadas a uma vistoria."))
            if rec.purpose == "maintenance" and not rec.maintenance_id:
                raise ValidationError(_("Mídias de manutenção precisam estar vinculadas a uma manutenção."))
            if rec.purpose == "document_support" and not rec.asset_id:
                raise ValidationError(_("Mídias de apoio documental precisam estar vinculadas a um imóvel."))

    @api.constrains("content_kind", "image_1920", "file_data")
    def _check_binary_consistency(self):
        for rec in self:
            if rec.content_kind == "image":
                if not rec.image_1920:
                    raise ValidationError(_("Informe a Foto / Imagem."))
                if rec.file_data:
                    raise ValidationError(_("Uma mídia do tipo Foto / Imagem não pode ter Arquivo / Documento preenchido."))
            if rec.content_kind == "document":
                if not rec.file_data:
                    raise ValidationError(_("Informe o Arquivo / Documento."))
                if rec.image_1920:
                    raise ValidationError(_("Uma mídia do tipo Arquivo / Documento não pode ter Foto / Imagem preenchida."))

    @api.constrains("purpose", "website_published", "visibility_level", "content_kind", "publication_state")
    def _check_publication_rules(self):
        for rec in self:
            if rec.website_published and rec.purpose != "asset_gallery":
                raise ValidationError(_("Somente mídias da Galeria do Imóvel podem ser publicadas no site."))
            if rec.website_published and rec.content_kind != "image":
                raise ValidationError(_("Somente fotos/imagens podem ser publicadas no site."))
            if rec.website_published and rec.visibility_level != "public":
                raise ValidationError(_("Para publicar no site, a visibilidade da mídia precisa ser Pública."))

    @api.constrains("is_cover", "asset_id", "purpose")
    def _check_is_cover_unique(self):
        for rec in self:
            if rec.is_cover and rec.asset_id and rec.purpose == "asset_gallery":
                duplicates = self.search([
                    ("id", "!=", rec.id),
                    ("asset_id", "=", rec.asset_id.id),
                    ("purpose", "=", "asset_gallery"),
                    ("is_cover", "=", True),
                ], limit=1)
                if duplicates:
                    raise ValidationError(_("Este imóvel já possui uma imagem de capa na galeria. Desmarque a capa anterior antes de definir uma nova."))

    @api.model
    def action_disable_binary_tracking(self):
        """Disable chatter tracking for all image/file binary fields.

        Kept as a callable XML/data migration so upgrades clean stale
        ir.model.fields metadata even if the Python field definition was
        corrected later.
        """
        self.env.cr.execute("""
            UPDATE ir_model_fields
               SET tracking = 0
             WHERE model IN ('property.asset', 'property.media', 'property.complex')
               AND ttype = 'binary'
               AND COALESCE(tracking, 0) <> 0
        """)
        return True

    @api.model
    def action_cleanup_binary_conflicts(self):
        cr = self.env.cr
        # Check if columns exist before trying to use them
        cr.execute("""
            SELECT EXISTS(
                SELECT FROM information_schema.columns
                WHERE table_name = 'property_media' AND column_name = 'image_1920'
            )
        """)
        if not cr.fetchone()[0]:
            return {"cleaned_count": 0}

        cr.execute("""
            UPDATE property_media
               SET file_data = NULL,
                   content_kind = 'image'
             WHERE image_1920 IS NOT NULL
               AND image_1920 != ''::bytea
               AND file_data IS NOT NULL
               AND file_data != ''::bytea
        """)
        return {"cleaned_count": cr.rowcount}
