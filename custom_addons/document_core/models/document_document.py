from datetime import date
from html import escape as html_escape

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DocumentDocument(models.Model):
    _name = "document.document"
    _description = "Documento"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, expiry_date, name"
    _rec_name = "name"

    _MANAGER_ONLY_FIELDS = {
        "access_level",
        "allowed_group_ids",
        "website_published",
        "website_visibility",
        "allow_download",
        "is_sensitive",
        "validated_by",
        "validation_date",
    }

    def _is_document_manager(self):
        return self.env.user.has_group("document_core.group_document_manager") or self.env.su

    def _sanitize_operator_vals(self, vals):
        """Remove campos de governança que o perfil operacional não deve definir na criação."""
        if self.env.context.get("document_core_system_defaults") or self._is_document_manager():
            return vals
        clean_vals = dict(vals)
        for field_name in self._MANAGER_ONLY_FIELDS:
            clean_vals.pop(field_name, None)
        return clean_vals

    def _check_operator_write_vals(self, vals):
        """Impede alteração manual de campos sensíveis por usuário operacional."""
        if self.env.context.get("document_core_system_defaults") or self._is_document_manager():
            return
        blocked = sorted(set(vals) & self._MANAGER_ONLY_FIELDS)
        if blocked:
            labels = [self._fields[name].string for name in blocked if name in self._fields]
            raise ValidationError(_("Seu perfil operacional não permite alterar estes campos: %s.") % ", ".join(labels))

    def name_get(self):
        return super().name_get()

    active = fields.Boolean(default=True)
    sequence = fields.Integer("Sequência", default=10)
    color = fields.Integer("Cor")
    name = fields.Char("Título", required=True, tracking=True)
    description = fields.Char("Descrição Curta", tracking=True)
    content = fields.Html("Conteúdo / Texto do Documento")
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")
    document_number = fields.Char("Número / Protocolo", tracking=True)
    version = fields.Char("Versão", default="1.0", tracking=True)
    version_number = fields.Integer("Número da Versão", compute="_compute_version_number", store=True)
    parent_document_id = fields.Many2one("document.document", string="Documento Original", ondelete="cascade", readonly=True, help="Documento pai - apenas preenchido em cópias")
    document_version_ids = fields.One2many("document.document", "parent_document_id", string="Histórico de Versões")
    document_state = fields.Selection([
        ("draft", "Rascunho"),
        ("active", "Vigente"),
        ("replaced", "Substituído"),
        ("archived", "Arquivado"),
        ("cancelled", "Cancelado"),
    ], string="Estado do Documento", default="active", tracking=True, required=True)
    responsible_id = fields.Many2one("res.users", string="Responsável", tracking=True,
                                     help="Responsável por manter este documento atualizado e renovado")
    document_type_id = fields.Many2one("document.type", string="Tipo de Documento", tracking=True, ondelete="restrict")
    category_id = fields.Many2one("document.category", string="Categoria", related="document_type_id.category_id", store=True, readonly=True)
    category_code = fields.Char(related="category_id.code", store=True, readonly=True)
    is_sensitive = fields.Boolean("Documento Sensível", tracking=True)
    source = fields.Selection([
        ("internal", "Interno"),
        ("owner", "Proprietário"),
        ("broker", "Corretor"),
        ("tenant", "Locatário"),
        ("registry", "Cartório"),
        ("city_hall", "Prefeitura"),
        ("fire_department", "Bombeiros"),
        ("legal", "Jurídico"),
        ("other", "Outro"),
    ], string="Origem", default="internal", tracking=True)
    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.company, index=True)
    issue_date = fields.Date("Data de Emissão")
    effective_date = fields.Date("Data de Vigência")
    expiry_date = fields.Date("Data de Vencimento", tracking=True)
    review_date = fields.Date("Data de Revisão", tracking=True)
    next_review_date = fields.Date("Próxima Revisão", compute="_compute_next_review_date", store=True)
    review_status = fields.Selection([
        ("no_review", "Sem revisão"),
        ("up_to_date", "Atualizado"),
        ("due_soon", "Revisão próxima"),
        ("overdue", "Revisão atrasada"),
    ], string="Situação de Revisão", compute="_compute_review_status", store=True)
    received_date = fields.Date("Data de Recebimento")
    alert_days = fields.Integer("Alertar com (dias)", default=30)
    issuer = fields.Char("Emitido por")
    validated_by = fields.Many2one("res.users", string="Validado por", tracking=True)
    validation_date = fields.Date("Data da Validação", tracking=True)
    requires_issue_date = fields.Boolean("Exige Data de Emissão", related="document_type_id.requires_issue_date", readonly=True)
    requires_expiry = fields.Boolean("Exige Data de Vencimento", related="document_type_id.requires_expiry", readonly=True)
    requires_review = fields.Boolean("Exige Data de Revisão", related="document_type_id.requires_review", readonly=True)
    requires_validation = fields.Boolean("Exige Validação", related="document_type_id.requires_validation", readonly=True)
    is_validated = fields.Boolean("Validado", compute="_compute_is_validated", store=True)
    superseded_by_id = fields.Many2one("document.document", string="Substituído por", ondelete="set null")
    document_complete = fields.Boolean(
        "Documento Completo",
        compute="_compute_document_complete",
        store=True,
        compute_sudo=True,
    )
    document_completion_state = fields.Selection([
        ("not_required", "Opcional"),
        ("missing", "Pendente"),
        ("incomplete", "Incompleto"),
        ("complete", "Completo"),
    ], string="Completude", compute="_compute_document_completion_state", store=True, compute_sudo=True)
    missing_requirements = fields.Char(
        "Pendências",
        compute="_compute_missing_requirements",
        store=True,
        compute_sudo=True,
    )
    missing_requirements_count = fields.Integer(
        "Qtd. Pendências",
        compute="_compute_missing_requirements_count",
        store=True,
        compute_sudo=True,
    )
    missing_requirements_html = fields.Html(
        "Aviso de Pendências",
        compute="_compute_missing_requirements_html",
        store=True,
        sanitize=False,
        compute_sudo=True,
    )

    notes = fields.Text("Observações")
    has_physical_original = fields.Boolean("Possui Original Físico", tracking=True)
    physical_location_id = fields.Many2one("document.location", string="Localização Física", ondelete="set null", tracking=True)
    physical_reference = fields.Char("Referência Física")
    requires_physical_original = fields.Boolean("Exige Original Físico", related="document_type_id.requires_physical_original", readonly=True)
    access_level = fields.Selection([
        ("internal", "Interno"),
        ("legal", "Jurídico"),
        ("finance", "Financeiro"),
        ("authorized_brokers", "Corretores Autorizados"),
        ("portal", "Portal / Logado"),
        ("public", "Público"),
    ], string="Nível de Acesso", default="internal", required=True, tracking=True)
    allowed_group_ids = fields.Many2many("res.groups", "document_res_groups_rel", "document_id", "group_id", string="Grupos Internos Autorizados")
    website_published = fields.Boolean("Disponível no Site", default=False, tracking=True)
    website_visibility = fields.Selection([
        ("portal", "Somente Logado"),
        ("public", "Público"),
        ("authorized_brokers", "Corretores Autorizados"),
        ("internal", "Somente Interno"),
    ], string="Visibilidade no Site", default="portal", tracking=True)
    allow_download = fields.Boolean("Permitir Download", default=True, tracking=True)

    # ==================== Workflow & Auditoria ====================
    portal_uploadable = fields.Boolean("Permitir Upload no Portal", default=False, tracking=True, help="Se ativado, usuários do portal podem fazer upload deste tipo de documento")
    document_workflow_state = fields.Selection([
        ("draft", "Rascunho"),
        ("pending_approval", "Pendente de Aprovação"),
        ("validated", "Validado"),
        ("rejected", "Rejeitado"),
        ("archived", "Arquivado/Obsoleto"),
    ], string="Status do Workflow", default="draft", tracking=True, required=True)
    created_by_id = fields.Many2one("res.users", string="Criado por", ondelete="restrict", readonly=True)
    approved_by_id = fields.Many2one("res.users", string="Aprovado por", ondelete="restrict", readonly=True, tracking=True)
    approval_date = fields.Date("Data de Aprovação", readonly=True, tracking=True)
    approval_notes = fields.Text("Observações da Aprovação", tracking=True, help="Comentários sobre a aprovação ou rejeição")
    attachment_ids = fields.Many2many("ir.attachment", relation="document_attachment_rel", column1="document_id", column2="attachment_id", string="Arquivos")
    attachment_count = fields.Integer("Qtd. Arquivos", compute="_compute_attachment_count")
    preview_attachment_id = fields.Many2one(
        "ir.attachment",
        string="Arquivo para Visualizar",
        help="Selecione qual anexo deve aparecer na pré-visualização desta tela.",
    )
    primary_attachment_id = fields.Many2one("ir.attachment", string="Arquivo em Prévia", compute="_compute_preview_fields", readonly=True)
    primary_attachment_name = fields.Char("Nome do Arquivo Principal", compute="_compute_preview_fields", readonly=True)
    primary_attachment_mimetype = fields.Char("Tipo MIME do Arquivo Principal", compute="_compute_preview_fields", readonly=True)
    preview_available = fields.Boolean("Pré-visualização Disponível", compute="_compute_preview_fields", readonly=True)
    preview_kind = fields.Selection([("none", "Sem arquivo"), ("pdf", "PDF"), ("image", "Imagem"), ("text", "Texto"), ("other", "Outro")], string="Tipo de Pré-visualização", compute="_compute_preview_fields", readonly=True)
    preview_html = fields.Html("Pré-visualização", compute="_compute_preview_fields", sanitize=False, readonly=True)
    status = fields.Selection([
        ("valid", "Válido"),
        ("expiring", "A Vencer"),
        ("expired", "Vencido"),
        ("no_expiry", "Sem Vencimento"),
    ], string="Situação", compute="_compute_status", store=True)
    access_summary = fields.Char("Resumo de Acesso", compute="_compute_access_summary")

    # ==================== Contexto & Multi-Referência ====================
    document_context_type = fields.Selection(
        [("property", "Imóvel"), ("generic", "Genérico")],
        string="Tipo de Contexto",
        default="generic",
        tracking=True,
        help="Indica o tipo principal de vínculo do documento"
    )
    created_context_type = fields.Selection(
        [("property", "Imóvel"), ("generic", "Genérico")],
        string="Contexto de Criação",
        readonly=True,
        tracking=True,
        help="Tipo de contexto quando o documento foi criado"
    )
    linked_entities_summary = fields.Char(
        "Resumo de Vínculos",
        compute="_compute_linked_entities_summary",
        store=True,
        help="Mostra todos os imóveis e casos vinculados"
    )
    context_type_display = fields.Char(
        "Contexto",
        compute="_compute_context_type_display",
        store=True,
    )

    # ==================== Comunicações ====================
    communication_ids = fields.One2many("document.communication", "document_id", string="Comunicações")

    @api.depends("attachment_ids")
    def _compute_attachment_count(self):
        for doc in self:
            doc.attachment_count = len(doc.attachment_ids)

    def _ordered_attachments(self):
        """Retorna anexos em ordem estável.

        O widget many2many_binary não garante visualmente qual arquivo será o
        primeiro quando há mais de um anexo. Por isso ordenamos pelo ID e,
        quando possível, escolhemos o primeiro arquivo pré-visualizável.
        """
        self.ensure_one()
        return self.attachment_ids.sorted(lambda attachment: attachment.id or 0)

    @api.model
    def _attachment_preview_kind(self, attachment):
        name = (attachment.name or _("Arquivo")).lower()
        mimetype = attachment.mimetype or ""
        if mimetype == "application/pdf" or name.endswith(".pdf"):
            return "pdf"
        if mimetype.startswith("image/") or name.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
            return "image"
        if mimetype.startswith("text/") or name.endswith((".txt", ".csv", ".xml", ".json", ".log")):
            return "text"
        return "other"

    def _attachment_content_url(self, attachment, download=False):
        """URL estável e segura para pré-visualizar anexo deste documento."""
        self.ensure_one()
        if not self.id or not isinstance(self.id, int) or not attachment or not attachment.id:
            return "#"
        return "/document_core/document/%s/attachment/%s?download=%s" % (
            self.id,
            attachment.id,
            "1" if download else "0",
        )

    def _select_primary_attachment(self):
        """Escolhe o arquivo exibido na prévia.

        Se o usuário selecionou um arquivo no campo "Arquivo para Visualizar",
        ele tem prioridade. Caso contrário, prioriza PDF/imagem/texto.
        """
        self.ensure_one()
        attachments = self._ordered_attachments()
        if not attachments:
            return self.env["ir.attachment"]
        if self.preview_attachment_id and self.preview_attachment_id in attachments:
            return self.preview_attachment_id
        previewable = attachments.filtered(lambda attachment: self._attachment_preview_kind(attachment) in ("pdf", "image", "text"))
        return (previewable or attachments)[:1]

    @api.depends("attachment_ids", "attachment_ids.name", "attachment_ids.mimetype", "preview_attachment_id", "preview_attachment_id.name", "preview_attachment_id.mimetype")
    def _compute_preview_fields(self):
        for doc in self:
            attachments = doc._ordered_attachments()
            attachment = doc._select_primary_attachment()

            if not attachment:
                doc.primary_attachment_id = False
                doc.primary_attachment_name = False
                doc.primary_attachment_mimetype = False
                doc.preview_available = False
                doc.preview_kind = "none"
                doc.preview_html = '<div class="alert alert-light mb-0">Nenhum arquivo anexado.</div>'
                continue

            name = attachment.name or _("Arquivo")
            mimetype = attachment.mimetype or ""
            preview_kind = doc._attachment_preview_kind(attachment)

            doc.primary_attachment_id = attachment.id
            doc.primary_attachment_name = name
            doc.primary_attachment_mimetype = mimetype
            doc.preview_kind = preview_kind
            doc.preview_available = preview_kind in ("pdf", "image", "text")

            if not doc.id or not isinstance(doc.id, int):
                doc.preview_html = (
                    '<div class="alert alert-info mb-0">'
                    '<strong>Salve o documento para liberar a pré-visualização.</strong><br/>'
                    'Os arquivos já foram selecionados, mas o visualizador precisa do documento salvo para gerar um link seguro.'
                    '</div>'
                )
                continue

            content_url = doc._attachment_content_url(attachment, download=False)
            download_url = doc._attachment_content_url(attachment, download=True)

            rows = []
            if len(attachments) > 1:
                for item in attachments:
                    item_name = html_escape(item.name or _("Arquivo"))
                    item_kind = doc._attachment_preview_kind(item)
                    item_mimetype = html_escape(item.mimetype or item_kind or _("Arquivo"))
                    item_url = doc._attachment_content_url(item, download=False)
                    item_download_url = doc._attachment_content_url(item, download=True)
                    rows.append(
                        '<tr>'
                        '<td style="width:45%%;vertical-align:middle;">%s</td>'
                        '<td style="width:20%%;vertical-align:middle;">%s</td>'
                        '<td style="width:35%%;vertical-align:middle;text-align:right;">'
                        '<a class="btn btn-sm btn-outline-primary me-1" href="%s" target="_blank">Visualizar</a>'
                        '<a class="btn btn-sm btn-outline-secondary" href="%s">Baixar</a>'
                        '</td>'
                        '</tr>' % (item_name, item_mimetype, item_url, item_download_url)
                    )

            file_list_html = ""
            if rows:
                file_list_html = (
                    '<div class="mb-3">'
                    '<div class="fw-bold mb-2">Arquivos anexados (%s)</div>'
                    '<div class="table-responsive">'
                    '<table class="table table-sm table-hover align-middle mb-0">'
                    '<thead><tr><th>Arquivo</th><th>Tipo</th><th class="text-end">Ações</th></tr></thead>'
                    '<tbody>%s</tbody>'
                    '</table>'
                    '</div>'
                    '<div class="text-muted small mt-2">Selecione acima o arquivo que deseja visualizar nesta mesma tela. Sem seleção, o sistema prioriza PDF, imagem ou texto.</div>'
                    '</div>'
                ) % (len(attachments), "".join(rows))

            safe_name = html_escape(name)
            if preview_kind == "pdf":
                preview = (
                    '<div class="o_document_preview_wrapper">'
                    '<div class="d-flex justify-content-between align-items-center mb-2">'
                    '<strong>Pré-visualização: %s</strong>'
                    '<a class="btn btn-sm btn-outline-primary" href="%s" target="_blank">Abrir em nova aba</a>'
                    '</div>'
                    '<iframe src="%s" style="width:100%%;height:680px;border:1px solid #dee2e6;border-radius:8px;background:#fff;"></iframe>'
                    '</div>'
                ) % (safe_name, content_url, content_url)
            elif preview_kind == "image":
                preview = (
                    '<div class="o_document_preview_wrapper text-center">'
                    '<div class="d-flex justify-content-between align-items-center mb-2 text-start">'
                    '<strong>Pré-visualização: %s</strong>'
                    '<a class="btn btn-sm btn-outline-primary" href="%s" target="_blank">Abrir em nova aba</a>'
                    '</div>'
                    '<img src="%s" style="max-width:100%%;max-height:680px;border:1px solid #dee2e6;border-radius:8px;background:#fff;object-fit:contain;"/>'
                    '</div>'
                ) % (safe_name, content_url, content_url)
            elif preview_kind == "text":
                preview = (
                    '<div class="o_document_preview_wrapper">'
                    '<div class="d-flex justify-content-between align-items-center mb-2">'
                    '<strong>Pré-visualização: %s</strong>'
                    '<a class="btn btn-sm btn-outline-primary" href="%s" target="_blank">Abrir em nova aba</a>'
                    '</div>'
                    '<iframe src="%s" style="width:100%%;height:520px;border:1px solid #dee2e6;border-radius:8px;background:#fff;"></iframe>'
                    '</div>'
                ) % (safe_name, content_url, content_url)
            else:
                preview = (
                    '<div class="alert alert-warning mb-0">'
                    '<strong>Pré-visualização direta não disponível para este tipo de arquivo.</strong><br/>'
                    'Arquivo principal: %s<br/>'
                    '<a class="btn btn-sm btn-outline-primary mt-2" href="%s" target="_blank">Tentar abrir</a> '
                    '<a class="btn btn-sm btn-outline-secondary mt-2" href="%s">Baixar arquivo</a>'
                    '</div>'
                ) % (safe_name, content_url, download_url)

            doc.preview_html = file_list_html + preview


    @api.onchange("attachment_ids")
    def _onchange_attachment_ids_preview_selection(self):
        for doc in self:
            if doc.preview_attachment_id and doc.preview_attachment_id not in doc.attachment_ids:
                doc.preview_attachment_id = False
            if not doc.preview_attachment_id and doc.attachment_ids:
                doc.preview_attachment_id = doc._select_primary_attachment()

    @api.depends("validated_by", "validation_date")
    def _compute_is_validated(self):
        for doc in self:
            doc.is_validated = bool(doc.validated_by and doc.validation_date)


    def _get_missing_requirements(self):
        self.ensure_one()
        missing = []
        dtype = self.document_type_id
        if not self.attachment_ids:
            missing.append(_("Arquivo"))
        if dtype:
            if dtype.requires_issue_date and not self.issue_date:
                missing.append(_("Data de emissão"))
            if dtype.requires_expiry and not self.expiry_date:
                missing.append(_("Data de vencimento"))
            if dtype.requires_review and not self.review_date:
                missing.append(_("Data de revisão"))
            if dtype.requires_physical_original and not self.has_physical_original:
                missing.append(_("Original físico"))
            if dtype.requires_validation and not self.is_validated:
                missing.append(_("Validação"))
        return missing

    def _document_completion_depends():
        return (
            "attachment_ids",
            "document_type_id.requires_issue_date", "document_type_id.requires_expiry",
            "document_type_id.requires_review", "document_type_id.requires_physical_original",
            "document_type_id.requires_validation", "issue_date", "expiry_date",
            "review_date", "has_physical_original", "validated_by", "validation_date", "is_validated",
        )

    @api.depends(*_document_completion_depends())
    def _compute_document_complete(self):
        for doc in self:
            doc.document_complete = not bool(doc._get_missing_requirements())

    @api.depends(*_document_completion_depends())
    def _compute_document_completion_state(self):
        for doc in self:
            missing = doc._get_missing_requirements()
            if not missing:
                doc.document_completion_state = "complete"
            elif not doc.attachment_ids:
                doc.document_completion_state = "missing"
            else:
                doc.document_completion_state = "incomplete"

    @api.depends(*_document_completion_depends())
    def _compute_missing_requirements(self):
        for doc in self:
            missing = doc._get_missing_requirements()
            doc.missing_requirements = ", ".join(missing) if missing else False

    @api.depends(*_document_completion_depends())
    def _compute_missing_requirements_count(self):
        for doc in self:
            doc.missing_requirements_count = len(doc._get_missing_requirements())

    @api.depends(*_document_completion_depends())
    def _compute_missing_requirements_html(self):
        for doc in self:
            missing = doc._get_missing_requirements()
            if not missing:
                doc.missing_requirements_html = False
                continue

            title = _("Documento incompleto")

            missing_items = "".join(
                "<li><strong>%s</strong></li>" % html_escape(str(item))
                for item in missing
            )
            doc.missing_requirements_html = (
                '<div class="alert alert-danger mb-3 o_document_missing_requirements">'
                '<div class="d-flex align-items-start gap-2">'
                '<span class="fa fa-exclamation-triangle mt-1" aria-hidden="true"></span>'
                '<div>'
                '<div class="fw-bold">%s</div>'
                '<div>Este documento ainda não está completo porque faltam campos/arquivos exigidos pelas regras do tipo documental ou pelo template do dossiê:</div>'
                '<ul class="mb-2 mt-2">%s</ul>'
                '<div class="small text-muted">Preencha estes itens para que o documento e o dossiê sejam considerados completos.</div>'
                '</div>'
                '</div>'
                '</div>'
            ) % (html_escape(str(title)), missing_items)

    @api.depends("review_date", "document_type_id.review_cycle_days")
    def _compute_next_review_date(self):
        for doc in self:
            if not doc.review_date or not doc.document_type_id.review_cycle_days:
                doc.next_review_date = False
                continue
            from datetime import timedelta
            doc.next_review_date = doc.review_date + timedelta(days=doc.document_type_id.review_cycle_days)

    @api.depends("next_review_date", "review_date")
    def _compute_review_status(self):
        today = date.today()
        for doc in self:
            if not doc.next_review_date:
                doc.review_status = "no_review"
            elif (doc.next_review_date - today).days < 0:
                doc.review_status = "overdue"
            elif (doc.next_review_date - today).days <= 30:
                doc.review_status = "due_soon"
            else:
                doc.review_status = "up_to_date"

    @api.depends("expiry_date", "alert_days")
    def _compute_status(self):
        today = date.today()
        for doc in self:
            if not doc.expiry_date:
                doc.status = "no_expiry"
            elif doc.expiry_date < today:
                doc.status = "expired"
            elif (doc.expiry_date - today).days <= (doc.alert_days or 30):
                doc.status = "expiring"
            else:
                doc.status = "valid"

    @api.depends("access_level", "website_published", "website_visibility", "allowed_group_ids")
    def _compute_access_summary(self):
        access_map = dict(self._fields["access_level"].selection)
        website_map = dict(self._fields["website_visibility"].selection)
        for rec in self:
            parts = [access_map.get(rec.access_level, "")]
            if rec.website_published:
                parts.append("Site: %s" % website_map.get(rec.website_visibility, ""))
            if rec.allowed_group_ids:
                parts.append("Grupos: %s" % len(rec.allowed_group_ids))
            rec.access_summary = " • ".join([p for p in parts if p])

    @api.depends("document_context_type")
    def _compute_context_type_display(self):
        context_map = dict(self._fields["document_context_type"].selection)
        for doc in self:
            doc.context_type_display = context_map.get(doc.document_context_type, "")

    @api.depends("document_context_type")
    def _compute_linked_entities_summary(self):
        for doc in self:
            doc.linked_entities_summary = "Sem vínculos específicos"

    def _apply_default_rules_from_type(self):
        for rec in self:
            dtype = rec.document_type_id
            if not dtype:
                continue
            vals = {}
            if not rec.access_level or rec.access_level == "internal":
                vals["access_level"] = dtype.default_access_level or "internal"
            if not rec.website_published and dtype.allow_website_publish:
                vals["website_visibility"] = dtype.website_default_visibility or "portal"
            if dtype.is_sensitive and not rec.is_sensitive:
                vals["is_sensitive"] = True
            if vals:
                rec.with_context(document_core_system_defaults=True).write(vals)

    @api.onchange("document_type_id")
    def _onchange_document_type_id(self):
        for rec in self:
            dtype = rec.document_type_id
            if not dtype:
                continue
            rec.access_level = dtype.default_access_level or "internal"
            rec.is_sensitive = dtype.is_sensitive
            if dtype.allow_website_publish:
                rec.website_visibility = dtype.website_default_visibility or "portal"
            else:
                rec.website_published = False
                rec.website_visibility = "internal"


    def action_open_attachments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Arquivos de %s") % (self.name or self.reference),
            "res_model": "ir.attachment",
            "view_mode": "list,form",
            "domain": [("id", "in", self.attachment_ids.ids)],
            "context": {
                "default_res_model": self._name,
                "default_res_id": self.id,
            },
        }

    def action_preview_primary_attachment(self):
        self.ensure_one()
        self._sync_attachment_ownership()
        attachment = self._select_primary_attachment()
        if not attachment:
            raise ValidationError(_("Este documento ainda não possui arquivo anexado para visualizar."))
        return {
            "type": "ir.actions.act_url",
            "name": _("Visualizar Arquivo"),
            "url": self._attachment_content_url(attachment, download=False),
            "target": "new",
        }

    @api.constrains("issue_date", "expiry_date", "review_date")
    def _check_dates(self):
        for doc in self:
            if doc.issue_date and doc.expiry_date and doc.expiry_date < doc.issue_date:
                raise ValidationError(_("A data de vencimento não pode ser anterior à data de emissão."))
            if doc.review_date and doc.issue_date and doc.review_date < doc.issue_date:
                raise ValidationError(_("A data de revisão não pode ser anterior à data de emissão."))

    @api.constrains("document_state", "document_type_id", "validated_by", "validation_date")
    def _check_validation_required(self):
        for doc in self:
            if doc.document_state == "active" and doc.document_type_id.requires_validation and not doc.is_validated:
                raise ValidationError(_("Documento '%s' exige validação formal antes de ser ativado.") % doc.name)

    @api.constrains("document_type_id", "issue_date", "expiry_date", "review_date", "has_physical_original", "website_published", "website_visibility")
    def _check_document_rules(self):
        for doc in self:
            dtype = doc.document_type_id
            if not dtype:
                continue
            if doc.document_state != "active":
                # Documentos não ativos podem ficar incompletos.
                # Ao ativar, as regras de completude passam a ser obrigatórias.
                continue
            if dtype.requires_issue_date and not doc.issue_date:
                raise ValidationError(_("O tipo documental '%s' exige Data de Emissão.") % dtype.name)
            if dtype.requires_expiry and not doc.expiry_date:
                raise ValidationError(_("O tipo documental '%s' exige Data de Vencimento.") % dtype.name)
            if dtype.requires_review and not doc.review_date:
                raise ValidationError(_("O tipo documental '%s' exige Data de Revisão.") % dtype.name)
            if dtype.requires_physical_original and not doc.has_physical_original:
                raise ValidationError(_("O tipo documental '%s' exige guarda do original físico.") % dtype.name)
            if doc.website_published and not dtype.allow_website_publish:
                raise ValidationError(_("O tipo documental '%s' não está autorizado para publicação no site.") % dtype.name)
            if doc.website_published and doc.website_visibility == "public" and doc.access_level not in ("public", "portal"):
                raise ValidationError(_("Documentos públicos no site devem ter nível de acesso Público ou Portal / Logado."))

    def _schedule_expiry_activity(self):
        """Agenda atividade quando documento está próximo de vencer."""
        today = date.today()
        for doc in self:
            if not doc.expiry_date:
                continue
            days_left = (doc.expiry_date - today).days
            if not (0 <= days_left <= (doc.alert_days or 30)):
                continue
            already = doc.activity_ids.filtered(lambda a: "vencimento" in (a.summary or "").lower())
            if already:
                continue
            activity_type = self.env.ref("document_core.mail_activity_type_document_expiry", raise_if_not_found=False)
            if not activity_type:
                continue
            user_id = (doc.responsible_id or doc.create_uid).id
            doc.activity_schedule(
                activity_type_id=activity_type.id,
                date_deadline=doc.expiry_date,
                summary=_("Vence em %s dias — %s") % (days_left, doc.name),
                note=_("O documento '%s' (tipo: %s) vence em %s. Providencie renovação.") % (
                    doc.name,
                    doc.document_type_id.name or _("Sem tipo definido"),
                    doc.expiry_date,
                ),
                user_id=user_id,
            )

    def _schedule_validation_activity(self):
        """Agenda atividade quando documento exige validação."""
        for doc in self:
            if not doc.requires_validation or doc.is_validated:
                continue
            already = doc.activity_ids.filtered(lambda a: "validação" in (a.summary or "").lower())
            if already:
                continue
            activity_type = self.env.ref("document_core.mail_activity_type_document_validation", raise_if_not_found=False)
            if not activity_type:
                continue
            user_id = (doc.responsible_id or doc.create_uid).id
            doc.activity_schedule(
                activity_type_id=activity_type.id,
                date_deadline=date.today(),
                summary=_("Validar documento — %s") % doc.name,
                note=_("O documento '%s' (tipo: %s) exige validação formal. Aprove ou rejeite.") % (
                    doc.name,
                    doc.document_type_id.name or _("Sem tipo definido"),
                ),
                user_id=user_id,
            )

    def _schedule_review_activity(self):
        """Agenda atividade quando documento exige revisão periódica."""
        today = date.today()
        for doc in self:
            if not doc.next_review_date or doc.review_status not in ("due_soon", "overdue"):
                continue
            already = doc.activity_ids.filtered(lambda a: "revisão" in (a.summary or "").lower())
            if already:
                continue
            activity_type = self.env.ref("document_core.mail_activity_type_document_review", raise_if_not_found=False)
            if not activity_type:
                continue
            days_overdue = (today - doc.next_review_date).days
            user_id = (doc.responsible_id or doc.create_uid).id
            doc.activity_schedule(
                activity_type_id=activity_type.id,
                date_deadline=doc.next_review_date,
                summary=_("Revisar documento — %s") % doc.name,
                note=_("O documento '%s' exige revisão (ciclo: %s dias). Última revisão: %s. Próxima: %s.") % (
                    doc.name,
                    doc.document_type_id.review_cycle_days or "N/A",
                    doc.review_date or "Nunca",
                    doc.next_review_date,
                ),
                user_id=user_id,
            )

    @api.model
    def action_cron_check_expiry(self):
        """Cron diário: verifica vencimentos e alerta."""
        docs = self.search([("expiry_date", "!=", False), ("status", "in", ["valid", "expiring"])])
        docs._schedule_expiry_activity()

    @api.model
    def action_cron_check_validation(self):
        """Cron diário: verifica documentos que exigem validação."""
        docs = self.search([("document_type_id.requires_validation", "=", True), ("is_validated", "=", False)])
        docs._schedule_validation_activity()

    @api.model
    def action_cron_check_review(self):
        """Cron diário: verifica ciclos de revisão."""
        docs = self.search([("next_review_date", "!=", False)])
        docs._schedule_review_activity()

    def _sync_attachment_ownership(self):
        """Garante vínculo técnico dos anexos com o documento.

        Em alguns cenários do widget many2many_binary, principalmente com mais
        de um arquivo, o anexo pode ficar sem res_model/res_id definitivo.
        Isso faz o /web/content/<id> retornar Not Found por regra de acesso.
        """
        for doc in self:
            for attachment in doc.attachment_ids.sudo():
                vals = {}
                if attachment.res_model != doc._name:
                    # Não sobrescreve anexos claramente pertencentes a outro modelo.
                    if attachment.res_model and attachment.res_id:
                        continue
                    vals["res_model"] = doc._name
                if not attachment.res_id:
                    vals["res_id"] = doc.id
                if vals:
                    attachment.write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        sanitized_vals_list = []
        for vals in vals_list:
            vals = self._sanitize_operator_vals(vals)
            if vals.get("reference", "New") == "New":
                seq = self.env["common.sequence"].sudo().next_by_code("document.document")
                vals["reference"] = seq or "New"
            if "created_by_id" not in vals:
                vals["created_by_id"] = self.env.user.id
            sanitized_vals_list.append(vals)
        docs = super().create(sanitized_vals_list)
        docs._sync_attachment_ownership()
        docs._apply_default_rules_from_type()
        docs._schedule_expiry_activity()
        docs._schedule_validation_activity()
        docs._schedule_review_activity()
        return docs

    def write(self, vals):
        self._check_operator_write_vals(vals)
        vals = dict(vals)
        res = super().write(vals)
        if "attachment_ids" in vals:
            self._sync_attachment_ownership()
            for doc in self:
                if doc.preview_attachment_id and doc.preview_attachment_id not in doc.attachment_ids:
                    doc.preview_attachment_id = False
        if "document_type_id" in vals:
            self._apply_default_rules_from_type()
        if "expiry_date" in vals or "alert_days" in vals:
            self._schedule_expiry_activity()
        if "document_type_id" in vals or "validated_by" in vals or "validation_date" in vals:
            self._schedule_validation_activity()
        if "review_date" in vals or "next_review_date" in vals:
            self._schedule_review_activity()
        return res

    # ==================== Workflow & Transitions ====================

    @api.onchange("document_workflow_state")
    def _onchange_workflow_state(self):
        """Valida transições de estado quando mudado via statusbar."""
        if not self.id:
            return

        old_state = self._origin.document_workflow_state if self._origin else "draft"
        new_state = self.document_workflow_state

        # Validar transições permitidas
        allowed_transitions = {
            "draft": ["pending_approval"],
            "pending_approval": ["validated", "rejected"],
            "validated": ["archived"],  # Bloqueado após validação - apenas arquivar
            "rejected": ["pending_approval"],  # Pode reenviar após rejeição
            "archived": [],  # Fim do fluxo - sem volta
        }

        if new_state not in allowed_transitions.get(old_state, []):
            self.document_workflow_state = old_state
            raise ValidationError(
                _("Transição inválida de %s para %s") % (old_state, new_state)
            )

        # Se aprovando via statusbar, registrar
        if new_state == "validated" and old_state == "pending_approval":
            self.approved_by_id = self.env.user.id
            self.approval_date = fields.Date.today()

    def action_submit_for_approval(self):
        for doc in self:
            if doc.document_workflow_state != "draft":
                raise ValidationError(_("Apenas documentos em rascunho podem ser submetidos para aprovação"))
            doc.document_workflow_state = "pending_approval"

    def action_approve(self):
        for doc in self:
            if doc.document_workflow_state != "pending_approval":
                raise ValidationError(_("Apenas documentos pendentes podem ser aprovados"))
            doc.write({
                "document_workflow_state": "validated",
                "approved_by_id": self.env.user.id,
                "approval_date": fields.Date.today(),
                "website_published": True,
            })
            # Log activity
            doc.message_post(
                body=_("Documento aprovado por %s") % self.env.user.name,
                message_type="notification",
            )

    def action_reject(self):
        """Abre diálogo para rejeitar com notas."""
        return {
            "type": "ir.actions.act_window",
            "res_model": "document.reject.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_document_id": self.id},
        }

    def action_reset_to_draft(self):
        for doc in self:
            if doc.document_workflow_state == "rejected":
                doc.write({
                    "document_workflow_state": "draft",
                    "approved_by_id": False,
                    "approval_date": False,
                    "approval_notes": False,
                })

    def action_archive(self):
        """Arquiva/marca como obsoleto um documento validado."""
        for doc in self:
            if doc.document_workflow_state != "validated":
                raise ValidationError(_("Apenas documentos validados podem ser arquivados"))
            doc.document_workflow_state = "archived"
            doc.message_post(
                body=_("Documento arquivado por %s") % self.env.user.name,
                message_type="notification",
            )

    @api.depends("version")
    def _compute_version_number(self):
        """Extrai o número da versão (1 de '1.0')."""
        for doc in self:
            try:
                doc.version_number = int(float(doc.version or "1.0"))
            except (ValueError, TypeError):
                doc.version_number = 1

    def action_create_new_version(self):
        """Cria uma nova versão de um documento validado."""
        for doc in self:
            if doc.document_workflow_state not in ("validated", "archived"):
                raise ValidationError(
                    _("Apenas documentos validados ou arquivados podem ter nova versão")
                )

            # Calcular novo número de versão
            next_version = (doc.version_number or 1) + 1
            new_version_str = f"{next_version}.0"

            # Copiar documento
            new_doc = doc.copy(
                default={
                    "version": new_version_str,
                    "version_number": next_version,
                    "document_workflow_state": "draft",
                    "parent_document_id": doc.parent_document_id.id or doc.id,
                    "approved_by_id": False,
                    "approval_date": False,
                    "approval_notes": False,
                    "created_by_id": self.env.user.id,
                }
            )

            # Log no documento original
            doc.message_post(
                body=_("Nova versão criada: %s") % new_version_str,
                message_type="notification",
            )

            return {
                "type": "ir.actions.act_window",
                "res_model": "document.document",
                "res_id": new_doc.id,
                "view_mode": "form",
                "target": "current",
            }

    def action_view_versions(self):
        """Abre a visualização de histórico de versões."""
        self.ensure_one()
        parent = self.parent_document_id or self
        return {
            "type": "ir.actions.act_window",
            "res_model": "document.document",
            "domain": [("id", "in", ([parent.id] + parent.document_version_ids.ids))],
            "view_mode": "list,form",
            "target": "current",
            "name": _("Histórico de Versões: %s") % parent.name,
            "context": {"search_default_parent": parent.id},
        }
