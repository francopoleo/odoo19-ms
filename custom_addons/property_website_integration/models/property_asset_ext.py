from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PropertyAssetExt(models.Model):
    _inherit = "property.asset"

    # ==================== Imagens ====================
    image_1920 = fields.Image("Foto Principal", max_width=1920, max_height=1920, help="Imagem principal do imóvel, usada como destaque em listagens, detalhes e site.")
    image_512 = fields.Image("Thumbnail", related="image_1920", max_width=512, max_height=512, store=True, help="Miniatura automática gerada a partir da foto principal.")

    # ==================== Publicação e Acesso ====================
    website_published = fields.Boolean(
        "Publicado no Site", default=False, tracking=True,
        help="Nada aparece no site sem esta opção habilitada."
    )
    website_visibility = fields.Selection([
        ("public", "Público"),
        ("portal", "Somente Logado"),
        ("restricted_brokers", "Somente Corretores Autorizados"),
        ("internal_only", "Somente Interno"),
    ], string="Visibilidade no Site", default="public", required=True, tracking=True, help="Define quem pode visualizar o imóvel no site: público, somente logado, corretores autorizados ou somente interno.")
    website_lead_policy = fields.Selection([
        ("open", "Formulário Aberto"),
        ("portal_only", "Somente Logado"),
        ("authorized_brokers_only", "Somente Corretores Autorizados"),
        ("disabled", "Formulário Desabilitado"),
    ], string="Política do Formulário", default="open", required=True, tracking=True, help="Controla quem pode enviar interesse pelo site para este imóvel.")
    authorized_broker_ids = fields.Many2many(
        "property.broker",
        "property_asset_broker_rel",
        "asset_id",
        "broker_id",
        string="Corretores Autorizados",
        help="Corretores que podem visualizar e operar imóveis restritos."
    )
    exclusive_broker_id = fields.Many2one("property.broker", string="Corretor Exclusivo", tracking=True, help="Corretor principal quando o imóvel estiver em regime de exclusividade.")
    is_exclusive = fields.Boolean("Imóvel Exclusivo", default=False, tracking=True, help="Marque quando a operação comercial do imóvel for exclusiva de um corretor ou grupo restrito.")
    hide_when_unavailable = fields.Boolean(
        "Ocultar quando indisponível", default=True, tracking=True,
        help="Quando marcado, imóveis alugados, em negociação, em manutenção ou inativos não aparecem no site."
    )
    show_unavailable_on_website = fields.Boolean(
        "Mostrar indisponível no site", default=False, tracking=True,
        help="Permite manter imóveis indisponíveis visíveis no site, sem liberar automaticamente o formulário."
    )
    publish_start_date = fields.Date("Publicar a partir de", tracking=True, help="Data inicial para disponibilizar o imóvel no site.")
    publish_end_date = fields.Date("Publicar até", tracking=True, help="Data limite para manter o imóvel publicado no site.")
    website_access_summary = fields.Char("Resumo de Acesso", compute="_compute_website_access_summary", help="Resumo calculado das regras de publicação, visibilidade e formulário do imóvel.")

    @api.depends("website_published", "website_visibility", "website_lead_policy", "status", "is_exclusive", "exclusive_broker_id", "authorized_broker_ids")
    def _compute_website_access_summary(self):
        visibility_map = dict(self._fields["website_visibility"].selection)
        lead_map = dict(self._fields["website_lead_policy"].selection)
        status_map = dict(self._fields["status"].selection)
        for asset in self:
            parts = []
            parts.append("Publicado" if asset.website_published else "Oculto")
            parts.append(visibility_map.get(asset.website_visibility, ""))
            parts.append(lead_map.get(asset.website_lead_policy, ""))
            parts.append(status_map.get(asset.status, ""))
            if asset.is_exclusive and asset.exclusive_broker_id:
                parts.append(f"Exclusivo: {asset.exclusive_broker_id.name}")
            elif asset.authorized_broker_ids:
                parts.append(f"Corretores: {len(asset.authorized_broker_ids)}")
            asset.website_access_summary = " • ".join([p for p in parts if p])

    def _is_in_publication_window(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        if self.publish_start_date and today < self.publish_start_date:
            return False
        if self.publish_end_date and today > self.publish_end_date:
            return False
        return True

    def _is_status_website_eligible(self):
        self.ensure_one()
        if self.status in {"available", "for_sale"}:
            return True
        if self.show_unavailable_on_website and not self.hide_when_unavailable:
            return self.status != "inactive"
        return False

    def _get_brokers_allowed_to_view(self):
        self.ensure_one()
        brokers = self.authorized_broker_ids
        if self.is_exclusive and self.exclusive_broker_id:
            brokers |= self.exclusive_broker_id
        return brokers

    def _get_broker_for_user(self, user=None):
        self.ensure_one()
        user = user or self.env.user
        if not user or not user.exists() or user._is_public():
            return self.env["property.broker"]
        return self.env["property.broker"].sudo().search([("user_id", "=", user.id)], limit=1)

    def can_user_view_on_website(self, user=None, broker=None):
        self.ensure_one()
        user = user or self.env.user
        broker = broker or self._get_broker_for_user(user)

        if user.has_group("property_core.group_property_manager"):
            return True
        if not self.website_published or not self._is_in_publication_window() or not self._is_status_website_eligible():
            return False

        visibility = self.website_visibility or "public"
        if visibility == "public":
            return True
        if visibility == "portal":
            return not user._is_public()
        if visibility == "internal_only":
            return bool(user and not user._is_public() and user.has_group("base.group_user"))
        if visibility == "restricted_brokers":
            return bool(broker and broker in self._get_brokers_allowed_to_view())
        return False

    def can_user_submit_interest(self, user=None, broker=None):
        self.ensure_one()
        user = user or self.env.user
        broker = broker or self._get_broker_for_user(user)

        if not self.can_user_view_on_website(user=user, broker=broker):
            return False
        policy = self.website_lead_policy or "disabled"
        if policy == "disabled":
            return False
        if policy == "open":
            return True
        if policy == "portal_only":
            return not user._is_public()
        if policy == "authorized_brokers_only":
            return bool(broker and broker in self._get_brokers_allowed_to_view())
        return False

    @api.onchange("is_exclusive", "exclusive_broker_id")
    def _onchange_exclusive_broker(self):
        for asset in self:
            if asset.is_exclusive and asset.exclusive_broker_id and asset.exclusive_broker_id not in asset.authorized_broker_ids:
                asset.authorized_broker_ids |= asset.exclusive_broker_id

    @api.constrains("publish_start_date", "publish_end_date")
    def _check_publication_dates(self):
        for asset in self:
            if asset.publish_start_date and asset.publish_end_date and asset.publish_end_date < asset.publish_start_date:
                raise ValidationError(_("A data final de publicação não pode ser menor que a data inicial."))

    @api.depends(
        "complex_id", "complex_id.name", "unit_identifier", "neighborhood", "city",
        "maintenance_open_count",
        "status", "website_published", "publish_end_date", "active_contract_count"
    )
    def _compute_kanban_indicators(self):
        """Override parent method to include website-specific alerts."""
        today = fields.Date.context_today(self)
        for asset in self:
            location_parts = []
            if asset.complex_id:
                location_parts.append(asset.complex_id.name)
            if asset.unit_identifier:
                location_parts.append(asset.unit_identifier)
            if asset.neighborhood:
                location_parts.append(asset.neighborhood)
            if asset.city:
                location_parts.append(asset.city)
            asset.kanban_location = " • ".join([part for part in location_parts if part])

            alerts = []
            if asset.maintenance_open_count:
                alerts.append(_("%s manutenção(ões) aberta(s)") % asset.maintenance_open_count)
            if asset.status == "inactive":
                alerts.append(_("imóvel inativo"))
            if asset.website_published and asset.publish_end_date and asset.publish_end_date < today:
                alerts.append(_("publicação vencida"))

            asset.kanban_alert_count = len(alerts)
            asset.kanban_alert_summary = " • ".join(alerts[:3]) if alerts else _("Operação sem alertas relevantes")

            if asset.maintenance_open_count >= 3 or asset.status == "inactive":
                asset.kanban_alert_level = "danger"
            elif alerts:
                asset.kanban_alert_level = "warning"
            else:
                asset.kanban_alert_level = "success"
