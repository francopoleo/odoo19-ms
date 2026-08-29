from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DocumentPropertyExt(models.Model):
    _inherit = "document.document"

    # ==================== Auditoria ====================
    created_in_property_id = fields.Many2one(
        "property.asset",
        string="Criado a partir de",
        readonly=True,
        help="Imóvel a partir do qual este documento foi criado"
    )

    # ==================== Vínculos com Imóveis ====================
    complex_id = fields.Many2one("property.complex", string="Complexo", ondelete="set null", tracking=True)
    asset_ids = fields.Many2many(
        "property.asset",
        "document_asset_rel",
        "document_id",
        "asset_id",
        string="Imóveis Vinculados",
        tracking=True,
        help="Imóveis relacionados a este documento"
    )
    asset_count = fields.Integer("Qtd. Imóveis", compute="_compute_asset_count")
    contract_id = fields.Many2one("property.contract", string="Contrato", ondelete="set null", tracking=True)
    owner_id = fields.Many2one("property.owner", string="Proprietário", ondelete="set null", tracking=True)
    broker_id = fields.Many2one("property.broker", string="Corretor Responsável", ondelete="set null", tracking=True)

    # ==================== Vínculos com Governança ====================
    case_ids = fields.Many2many(
        "governance.case",
        "document_case_rel",
        "document_id",
        "case_id",
        string="Casos de Governança",
        tracking=True,
        help="Casos de governança relacionados a este documento"
    )
    case_count = fields.Integer("Qtd. Casos", compute="_compute_case_count")

    # ==================== Segurança & Autorização ====================
    authorized_broker_ids = fields.Many2many(
        "property.broker",
        "document_broker_rel",
        "document_id",
        "broker_id",
        string="Corretores Autorizados",
    )

    # ==================== Mídias & Apoio ====================
    media_ids = fields.One2many("property.media", "document_id", string="Mídias de Apoio")
    media_count = fields.Integer("Qtd. Mídias", compute="_compute_media_count")

    # ==================== Computed Fields ====================
    @api.depends("media_ids")
    def _compute_media_count(self):
        for doc in self:
            doc.media_count = len(doc.media_ids)

    @api.depends("asset_ids")
    def _compute_asset_count(self):
        for doc in self:
            doc.asset_count = len(doc.asset_ids)

    @api.depends("case_ids")
    def _compute_case_count(self):
        for doc in self:
            doc.case_count = len(doc.case_ids)

    @api.depends("asset_ids", "case_ids", "asset_ids.name", "asset_ids.reference", "case_ids.name")
    def _compute_linked_entities_summary(self):
        for doc in self:
            parts = []
            if doc.asset_ids:
                asset_names = ", ".join([f"{a.reference}" for a in doc.asset_ids])
                parts.append(f"Imóveis: {asset_names}")
            if doc.case_ids:
                case_names = ", ".join([c.name for c in doc.case_ids])
                parts.append(f"Casos: {case_names}")
            doc.linked_entities_summary = " • ".join(parts) if parts else "Sem vínculos"

    # ==================== Métodos de Auditoria ====================
    @api.model_create_multi
    def create(self, vals_list):
        """Override create para auto-detectar context type e rastrear propriedade de origem."""
        for vals in vals_list:
            # Auto-detect context type based on links
            if not vals.get("created_context_type"):
                if vals.get("asset_ids"):
                    vals["created_context_type"] = "property"
                    vals["document_context_type"] = "property"
                elif vals.get("case_ids"):
                    vals["created_context_type"] = "governance"
                    vals["document_context_type"] = "governance"
                else:
                    vals["created_context_type"] = "generic"
                    vals["document_context_type"] = "generic"

            # Store which property this was created from (first in list)
            if not vals.get("created_in_property_id") and vals.get("asset_ids"):
                asset_ids = vals.get("asset_ids", [])
                if asset_ids:
                    first_asset = None
                    if isinstance(asset_ids[0], (list, tuple)):
                        for cmd_type, cmd_id, cmd_data in asset_ids:
                            if cmd_type == 4:
                                first_asset = cmd_id
                                break
                    if first_asset:
                        vals["created_in_property_id"] = first_asset

        return super().create(vals_list)

    def _get_broker_for_user(self, user=None):
        user = user or self.env.user
        if not user or not user.exists() or user._is_public():
            return self.env["property.broker"]
        return self.env["property.broker"].sudo().search([("user_id", "=", user.id)], limit=1)

    def _get_user_accessible_asset_ids(self, user=None):
        user = user or self.env.user
        asset_domain = []
        if user.has_group("property_core.group_property_manager"):
            return user.env["property.asset"].search([])
        assets = user.env["property.asset"].search(asset_domain)
        return assets

    def _get_user_accessible_case_ids(self, user=None):
        user = user or self.env.user
        if user.has_group("governance.group_governance_user"):
            return user.env["governance.case"].search([])
        return user.env["governance.case"]

    def can_user_view_document(self, user=None, broker=None):
        self.ensure_one()
        user = user or self.env.user
        broker = broker or self._get_broker_for_user(user)

        if user.has_group("property_core.group_property_manager"):
            return True
        if self.access_level == "public":
            return True
        if self.access_level == "portal":
            return not user._is_public()
        if self.access_level == "authorized_brokers":
            return bool(broker and broker in self.authorized_broker_ids)
        if self.access_level == "internal":
            return bool(user and not user._is_public() and user.has_group("base.group_user"))
        if self.access_level in ("legal", "finance"):
            return bool(user and not user._is_public() and user.has_group("property_core.group_property_manager"))
        if self.access_level == "governance":
            return bool(user and not user._is_public() and user.has_group("governance.group_governance_user"))
        return False

    @api.depends("access_level", "website_published", "website_visibility", "authorized_broker_ids", "allowed_group_ids", "asset_ids", "case_ids")
    def _compute_access_summary(self):
        """Enhance access summary with property and governance link counts."""
        super()._compute_access_summary()
        for rec in self:
            parts = [rec.access_summary] if rec.access_summary else []
            if rec.asset_ids:
                parts.append("Imóveis: %s" % len(rec.asset_ids))
            if rec.case_ids:
                parts.append("Casos: %s" % len(rec.case_ids))
            if rec.authorized_broker_ids:
                parts.append("Corretores: %s" % len(rec.authorized_broker_ids))
            rec.access_summary = " • ".join([p for p in parts if p])
