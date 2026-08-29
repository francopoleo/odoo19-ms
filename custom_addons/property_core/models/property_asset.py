from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests
import logging

_logger = logging.getLogger(__name__)


class PropertyAsset(models.Model):
    _name = "property.asset"
    _description = "Imóvel"
    _inherit = ["mail.thread", "mail.activity.mixin", "common.mixin"]
    _order = "name"
    _rec_name = "display_name_full"

    # ==================== Identificação ====================
    name = fields.Char("Nome do Imóvel", required=True, tracking=True, help="Nome comercial ou interno do imóvel, usado em telas, relatórios e site.")
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")
    display_name_full = fields.Char(
        "Nome Completo", compute="_compute_display_name_full", store=True,
        help="Exibido em dropdowns: 'MALL - LOJA 1' ou apenas 'Nome do Imóvel'"
    )

    asset_type = fields.Selection([
        ("residential", "Residencial"),
        ("commercial", "Comercial"),
        ("land", "Terreno"),
        ("industrial", "Industrial"),
        ("mixed", "Uso Misto"),
    ], string="Tipo", default="residential", tracking=True, required=True)

    status = fields.Selection([
        ("available", "Disponível"),
        ("rented", "Alugado"),
        ("for_sale", "À Venda"),
        ("negotiating", "Em Negociação"),
        ("maintenance", "Em Manutenção"),
        ("inactive", "Inativo"),
    ], default="available", tracking=True, required=True)

    # ==================== Dados Legais ====================
    registration = fields.Char("Matrícula", tracking=True,
                                help="Número de matrícula no cartório de registro de imóveis")
    iptu_number = fields.Char("Número IPTU")
    legal_description = fields.Text("Descrição Legal")

    # ==================== Localização ====================
    address = fields.Char(
        "Endereço", tracking=True,
        help="Vem automaticamente do Complexo se vinculado. Somente editável para imóveis sem complexo."
    )
    address_number = fields.Char("Número")
    address_complement = fields.Char("Complemento")
    neighborhood = fields.Char("Bairro")
    city = fields.Char("Cidade", tracking=True)
    state_name = fields.Char("Estado")
    zip_code = fields.Char("CEP")
    country_id = fields.Many2one("res.country", string="País",
                                 default=lambda self: self.env.ref("base.br", raise_if_not_found=False))

    # Endereço computado do complexo (read-only)
    complex_address = fields.Char(
        "Endereço do Complexo", compute="_compute_complex_address", store=False,
        help="Endereço completo herdado do complexo vinculado"
    )

    # ==================== Geolocalização ====================
    latitude = fields.Float("Latitude", digits=(10, 6),
                           help="Vem automaticamente do Complexo se vinculado")
    longitude = fields.Float("Longitude", digits=(10, 6),
                            help="Vem automaticamente do Complexo se vinculado")

    def init(self):
        """Ensure image/binary fields are not tracked in chatter.

        Odoo mail tracking does not support binary fields such as image_512.
        This also fixes databases where a previous dev version left tracking
        enabled in ir.model.fields.
        """
        self.env.cr.execute("""
            UPDATE ir_model_fields
               SET tracking = 0
             WHERE model IN ('property.asset', 'property.media', 'property.complex')
               AND ttype = 'binary'
               AND COALESCE(tracking, 0) <> 0
        """)

    # ==================== Características Físicas ====================
    bedrooms = fields.Integer("Quartos", default=0)
    bathrooms = fields.Integer("Banheiros", default=0)
    parking_spots = fields.Integer("Vagas de Garagem", default=0)
    construction_year = fields.Integer("Ano de Construção")
    construction_standard = fields.Selection([
        ("simple", "Simples"),
        ("medium", "Médio"),
        ("high", "Alto"),
        ("luxury", "Luxo"),
    ], string="Padrão Construtivo", default="medium")
    permitted_use = fields.Selection([
        ("residential", "Residencial"),
        ("commercial", "Comercial"),
        ("mixed", "Uso Misto"),
    ], string="Uso Permitido", default="residential")

    # ==================== Áreas ====================
    total_area = fields.Float("Área Total (m²)", digits=(10, 2))
    useful_area = fields.Float("Área Útil (m²)", digits=(10, 2))
    land_area = fields.Float("Área do Terreno (m²)", digits=(10, 2))

    # ==================== Financeiro ====================
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    asset_value = fields.Monetary(
        "Valor de Avaliação", currency_field="currency_id", tracking=True,
        help="Valor venal ou de avaliação do imóvel"
    )
    market_value = fields.Monetary(
        "Valor de Mercado", currency_field="currency_id", tracking=True,
        help="Valor atual de mercado para venda"
    )
    rental_value = fields.Monetary(
        "Valor de Locação Esperado", currency_field="currency_id", tracking=True,
        help="Valor mensal de referência para novas locações"
    )
    current_monthly_rent = fields.Monetary(
        "Aluguel Atual", currency_field="currency_id",
        compute="_compute_contract_stats", store=True,
        help="Valor do contrato ativo atual"
    )

    # ==================== Custos Operacionais ====================
    iptu_annual = fields.Monetary(
        "IPTU Anual", currency_field="currency_id",
        help="Valor anual do IPTU"
    )
    foro_annual = fields.Monetary(
        "Foro/Enfiteuse Anual", currency_field="currency_id",
        help="Valor anual do foro ou enfiteuse"
    )
    condominium_monthly = fields.Monetary(
        "Condomínio Mensal", currency_field="currency_id",
        help="Custo mensal de condomínio"
    )
    total_annual_costs = fields.Monetary(
        "Custo Operacional Anual", currency_field="currency_id",
        compute="_compute_total_annual_costs", store=True,
        help="IPTU + Foro + (Condomínio × 12)"
    )

    # ==================== Notas ====================
    notes = fields.Html("Observações Internas")

    # ==================== Complexo ====================
    complex_id = fields.Many2one(
        "property.complex", string="Complexo / Edifício",
        tracking=True, ondelete="set null",
        help="Complexo ou edifício ao qual esta unidade pertence. "
             "Imóveis standalone ficam sem complexo."
    )
    unit_identifier = fields.Char(
        "Identificador da Unidade",
        help="Ex: Loja 1, Sala 601, Apto 2204, Estacionamento"
    )
    unit_type = fields.Selection([
        ("store", "Loja"),
        ("office", "Sala / Escritório"),
        ("apartment", "Apartamento"),
        ("parking", "Estacionamento"),
        ("warehouse", "Galpão / Depósito"),
        ("other", "Outro"),
    ], string="Tipo de Unidade")
    floor = fields.Char(
        "Andar / Pavimento",
        help="Ex: Térreo, 6º andar, Subsolo"
    )
    gla = fields.Float(
        "ABL (m²)", digits=(10, 2),
        help="Área Bruta Locável desta unidade"
    )

    # ==================== Proprietário ====================
    owner_id = fields.Many2one(
        "res.partner", string="Proprietário",
        tracking=True, ondelete="set null",
        domain=[("category_id.name", "ilike", "Proprietário")],
        help="Proprietário principal do imóvel para repasses, contratos e relatórios."    )

    # ==================== Relações ====================
    contract_ids = fields.One2many("property.contract", "asset_id", string="Contratos")
    inspection_ids = fields.One2many("property.inspection", "asset_id", string="Vistorias")
    maintenance_ids = fields.One2many("property.maintenance", "asset_id", string="Manutenções")
    media_ids = fields.One2many("property.media", "asset_id", string="Todas as Mídias")
    gallery_media_ids = fields.One2many(
        "property.media", "asset_id", string="Galeria do Imóvel",
        domain=[("purpose", "=", "asset_gallery")],
    )
    other_media_ids = fields.One2many(
        "property.media", "asset_id", string="Outras Mídias",
        domain=[("purpose", "=", "other")],
    )
    communication_ids = fields.One2many("property.asset.communication", "asset_id", string="Comunicações")
    contract_count = fields.Integer("Qtd Contratos", compute="_compute_contract_stats", store=True)
    active_contract_count = fields.Integer("Contratos Ativos", compute="_compute_contract_stats", store=True)
    active_contract_id = fields.Many2one(
        "property.contract", compute="_compute_contract_stats",
        string="Contrato Ativo", store=True
    )

    media_count = fields.Integer("Qtd. Mídias", compute="_compute_media_count")

    # ==================== Indicadores Kanban ====================
    kanban_location = fields.Char(
        "Localização Resumida",
        compute="_compute_kanban_indicators",
        help="Resumo da localização exibido no kanban.",
    )
    kanban_alert_count = fields.Integer(
        "Qtd. Alertas",
        compute="_compute_kanban_indicators",
        help="Quantidade de alertas relevantes para o card kanban.",
    )
    kanban_alert_level = fields.Selection([
        ("success", "Sucesso"),
        ("warning", "Atenção"),
        ("danger", "Crítico"),
    ], string="Nível do Alerta", compute="_compute_kanban_indicators")
    kanban_alert_summary = fields.Char(
        "Resumo dos Alertas",
        compute="_compute_kanban_indicators",
        help="Resumo textual dos alertas exibido no card kanban.",
    )

    def _compute_media_count(self):
        for asset in self:
            asset.media_count = len(asset.media_ids)

    @api.depends(
        "complex_id", "complex_id.name", "unit_identifier", "neighborhood", "city",
        "maintenance_open_count",
        "status", "active_contract_count"
    )
    def _compute_kanban_indicators(self):
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

            asset.kanban_alert_count = len(alerts)
            asset.kanban_alert_summary = " • ".join(alerts[:3]) if alerts else _("Operação sem alertas relevantes")

            if asset.maintenance_open_count >= 3 or asset.status == "inactive":
                asset.kanban_alert_level = "danger"
            elif alerts:
                asset.kanban_alert_level = "warning"
            else:
                asset.kanban_alert_level = "success"

    def action_view_media(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Mídias",
            "res_model": "property.media",
            "view_mode": "list,form",
            "domain": [("asset_id", "=", self.id)],
            "context": {"default_asset_id": self.id},
        }

    def action_open_bulk_media_wizard(self):
        """Compatibilidade: abre o upload da galeria do imóvel."""
        return self.action_open_gallery_media_wizard()

    def action_open_gallery_media_wizard(self):
        """Upload em lote para a Galeria do Imóvel / Site."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Adicionar Fotos à Galeria"),
            "res_model": "property.media.bulk.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_asset_id": self.id,
                "default_context_selection": "asset_gallery",
                "default_purpose": "asset_gallery",
                "default_upload_kind": "image",
                "default_visibility_level": "public",
                "default_website_published": True,
                "default_publication_state": "approved",
            },
        }

    def action_open_other_media_wizard(self):
        """Upload em lote para Outras Mídias do imóvel."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Adicionar Outras Mídias"),
            "res_model": "property.media.bulk.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_asset_id": self.id,
                "default_context_selection": "asset_other",
                "default_purpose": "other",
                "default_upload_kind": "auto",
                "default_visibility_level": "internal",
                "default_website_published": False,
            },
        }

    # ==================== Tags (relation explícita) ====================
    tag_ids = fields.Many2many(
        "common.tag",
        relation="common_tag_property_asset_rel",
        column1="asset_id",
        column2="tag_id",
        string="Tags",
    )

    # ==================== Computed ====================

    @api.depends("complex_id", "complex_id.name", "unit_identifier", "name")
    def _compute_display_name_full(self):
        for asset in self:
            if asset.complex_id and asset.unit_identifier:
                asset.display_name_full = f"{asset.complex_id.name} - {asset.unit_identifier}"
            elif asset.complex_id:
                asset.display_name_full = f"{asset.complex_id.name} - {asset.name}"
            else:
                asset.display_name_full = asset.name

    @api.depends("complex_id", "complex_id.address", "complex_id.address_number",
                 "complex_id.city", "unit_identifier")
    def _compute_complex_address(self):
        """Compute address from complex if asset belongs to one"""
        for asset in self:
            if asset.complex_id:
                parts = [asset.complex_id.address]
                if asset.complex_id.address_number:
                    parts.append(asset.complex_id.address_number)
                if asset.unit_identifier:
                    parts.append(f"- {asset.unit_identifier}")
                if asset.complex_id.city:
                    parts.append(asset.complex_id.city)
                asset.complex_address = ", ".join(p for p in parts if p)
            else:
                asset.complex_address = asset.address or ""

    @api.depends("iptu_annual", "foro_annual", "condominium_monthly")
    def _compute_total_annual_costs(self):
        for asset in self:
            asset.total_annual_costs = (
                asset.iptu_annual
                + asset.foro_annual
                + (asset.condominium_monthly * 12)
            )

    @api.depends("contract_ids", "contract_ids.status", "contract_ids.monthly_rent")
    def _compute_contract_stats(self):
        for asset in self:
            all_contracts = asset.contract_ids
            active = all_contracts.filtered(lambda c: c.status == "active")
            asset.contract_count = len(all_contracts)
            asset.active_contract_count = len(active)
            asset.active_contract_id = active[:1]
            asset.current_monthly_rent = sum(active.mapped("monthly_rent"))


    @api.onchange("complex_id")
    def _onchange_complex_id(self):
        """When complex is changed, update address and geolocation from complex"""
        for asset in self:
            if asset.complex_id:
                # Copy complete address from complex
                asset.address = asset.complex_id.address
                asset.address_number = asset.complex_id.address_number
                asset.neighborhood = asset.complex_id.neighborhood
                asset.city = asset.complex_id.city
                asset.state_name = asset.complex_id.state_name
                asset.zip_code = asset.complex_id.zip_code
                asset.country_id = asset.complex_id.country_id
                # Copy geolocation from complex
                asset.latitude = asset.complex_id.latitude
                asset.longitude = asset.complex_id.longitude
            else:
                # Clear address when complex is removed
                asset.address = False
                asset.address_number = False
                asset.neighborhood = False
                asset.city = False
                asset.state_name = False
                asset.zip_code = False
                asset.country_id = False
                asset.latitude = False
                asset.longitude = False
                # Note: address_complement remains always editable (unit-specific)

    @api.onchange("zip_code")
    def _onchange_zip_code(self):
        """Auto-fetch address data when zip code is changed (if not in complex)"""
        for asset in self:
            if asset.zip_code and not asset.complex_id:
                self._search_zip_code_data(asset)

    # ==================== Constraints ====================

    @api.constrains("useful_area", "total_area")
    def _check_areas(self):
        for asset in self:
            if asset.useful_area and asset.total_area and asset.useful_area > asset.total_area:
                raise ValidationError(_("A área útil não pode ser maior que a área total."))

    @api.constrains("bedrooms", "bathrooms", "parking_spots")
    def _check_characteristics(self):
        for asset in self:
            if asset.bedrooms < 0:
                raise ValidationError(_("O número de quartos não pode ser negativo."))
            if asset.bathrooms < 0:
                raise ValidationError(_("O número de banheiros não pode ser negativo."))
            if asset.parking_spots < 0:
                raise ValidationError(_("O número de vagas não pode ser negativo."))

    # ==================== CEP / ZIP CODE ====================

    def _search_zip_code_data(self, asset):
        """Fetch address data from ViaCEP API using zip code"""
        if not asset.zip_code:
            return

        # Clean zip code (remove special characters)
        clean_zip = asset.zip_code.replace("-", "").replace(" ", "").strip()

        if len(clean_zip) != 8 or not clean_zip.isdigit():
            return

        try:
            url = f"https://viacep.com.br/ws/{clean_zip}/json/"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Check for error response
            if data.get("erro"):
                _logger.warning(f"CEP {clean_zip} not found in ViaCEP")
                return

            # Map ViaCEP fields to property.asset fields
            asset.address = data.get("logradouro", "")
            asset.neighborhood = data.get("bairro", "")
            asset.city = data.get("localidade", "")
            asset.state_name = data.get("uf", "")

        except requests.RequestException as e:
            _logger.warning(f"Error fetching CEP {clean_zip}: {str(e)}")
        except Exception as e:
            _logger.error(f"Unexpected error in CEP lookup: {str(e)}")

    def action_search_zip_code(self):
        """Action button to manually trigger zip code search"""
        self.ensure_one()
        if self.zip_code and not self.complex_id:
            self._search_zip_code_data(self)
            return {"type": "ir.actions.client", "tag": "reload"}
        return {"type": "ir.actions.client", "tag": "display_notification", "params": {"message": "Informe o CEP e não vincule a um complexo", "type": "warning"}}

    # ==================== Actions ====================

    def action_set_available(self):
        self.ensure_one()
        self.status = "available"
        self.message_post(body=_("Imóvel marcado como Disponível."))

    def action_set_rented(self):
        self.ensure_one()
        self.status = "rented"
        self.message_post(body=_("Imóvel marcado como Alugado."))

    def action_set_for_sale(self):
        self.ensure_one()
        self.status = "for_sale"
        self.message_post(body=_("Imóvel colocado À Venda."))

    def action_set_negotiating(self):
        self.ensure_one()
        self.status = "negotiating"
        self.message_post(body=_("Imóvel marcado Em Negociação."))

    def action_set_maintenance(self):
        self.ensure_one()
        self.status = "maintenance"
        self.message_post(body=_("Imóvel colocado em Manutenção."))

    def action_set_inactive(self):
        self.ensure_one()
        self.status = "inactive"
        self.message_post(body=_("Imóvel marcado como Inativo."))

    def action_view_contracts(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Contratos",
            "res_model": "property.contract",
            "view_mode": "list,form",
            "domain": [("asset_id", "=", self.id)],
            "context": {"default_asset_id": self.id},
        }

    # ==================== Documentos / Vistorias / Manutenção ====================

    inspection_count = fields.Integer("Vistorias", compute="_compute_phase4_counts")
    maintenance_count = fields.Integer("Manutenções", compute="_compute_phase4_counts")
    maintenance_open_count = fields.Integer("Manutenções Abertas", compute="_compute_phase4_counts")

    def _compute_phase4_counts(self):
        Insp = self.env["property.inspection"]
        Maint = self.env["property.maintenance"]
        for asset in self:
            asset.inspection_count = Insp.search_count([("asset_id", "=", asset.id)])
            asset.maintenance_count = Maint.search_count([("asset_id", "=", asset.id)])
            asset.maintenance_open_count = Maint.search_count([
                ("asset_id", "=", asset.id),
                ("status", "not in", ["done", "cancelled"]),
            ])

    def action_view_inspections(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Vistorias",
            "res_model": "property.inspection",
            "view_mode": "list,form",
            "domain": [("asset_id", "=", self.id)],
            "context": {"default_asset_id": self.id},
        }

    def action_view_maintenance(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Manutenções",
            "res_model": "property.maintenance",
            "view_mode": "list,form",
            "domain": [("asset_id", "=", self.id)],
            "context": {"default_asset_id": self.id},
        }

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.asset") or "New"
                )
        return super().create(vals_list)