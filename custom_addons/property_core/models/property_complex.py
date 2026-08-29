from odoo import api, fields, models, _
import requests
import logging

_logger = logging.getLogger(__name__)


class PropertyComplex(models.Model):
    _name = "property.complex"
    _description = "Complexo / Edifício"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Nome", required=True, tracking=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")
    active = fields.Boolean(default=True)

    complex_type = fields.Selection([
        ("strip", "Galeria / Strip Mall"),
        ("office", "Edifício Corporativo"),
        ("mixed", "Uso Misto"),
        ("residential", "Residencial"),
        ("industrial", "Industrial / Galpão"),
        ("mall", "Shopping / Mall"),
        ("other", "Outro"),
    ], string="Tipo de Complexo", required=True, default="strip", tracking=True)

    owner_id = fields.Many2one(
        "res.partner", string="Proprietário",
        tracking=True, ondelete="set null",
        domain=[("category_id.name", "ilike", "Proprietário")]
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, index=True
    )

    # ==================== Localização ====================
    address = fields.Char("Logradouro", tracking=True)
    address_number = fields.Char("Número")
    neighborhood = fields.Char("Bairro")
    city = fields.Char("Cidade", tracking=True)
    state_name = fields.Char("Estado")
    zip_code = fields.Char("CEP")
    country_id = fields.Many2one(
        "res.country", string="País",
        default=lambda self: self.env.ref("base.br", raise_if_not_found=False)
    )
    latitude = fields.Float("Latitude", digits=(10, 6))
    longitude = fields.Float("Longitude", digits=(10, 6))


    # ==================== Dados Físicos ====================
    land_area = fields.Float("Área do Terreno (m²)", digits=(10, 2))
    total_gla = fields.Float(
        "ABL Total (m²)", digits=(10, 2),
        help="Área Bruta Locável total do complexo"
    )
    construction_year = fields.Integer("Ano de Construção")
    floors = fields.Integer("Número de Andares", default=1)
    parking_total = fields.Integer("Total de Vagas", default=0)
    construction_standard = fields.Selection([
        ("simple", "Simples"),
        ("medium", "Médio"),
        ("high", "Alto"),
        ("luxury", "Luxo"),
    ], string="Padrão Construtivo", default="medium")

    # ==================== Dados Legais ====================
    def init(self):
        """Ensure image/binary fields are not tracked in chatter."""
        self.env.cr.execute("""
            UPDATE ir_model_fields
               SET tracking = 0
             WHERE model IN ('property.complex', 'property.asset', 'property.media')
               AND ttype = 'binary'
               AND COALESCE(tracking, 0) <> 0
        """)

    registration = fields.Char("Matrícula", tracking=True,
                                help="Matrícula do terreno no cartório de registro de imóveis")
    iptu_number = fields.Char("Número IPTU")
    legal_description = fields.Text("Descrição Legal")

    # ==================== Custos do Complexo ====================
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    asset_value = fields.Monetary(
        "Valor de Avaliação", currency_field="currency_id", tracking=True
    )
    iptu_annual = fields.Monetary(
        "IPTU Anual", currency_field="currency_id",
        help="IPTU do conjunto / terreno"
    )
    foro_annual = fields.Monetary(
        "Foro/Enfiteuse Anual", currency_field="currency_id"
    )
    condominium_monthly = fields.Monetary(
        "Condomínio Mensal", currency_field="currency_id"
    )
    total_annual_costs = fields.Monetary(
        "Custo Operacional Anual", currency_field="currency_id",
        compute="_compute_financials", store=True
    )

    # ==================== KPIs Computados das Unidades ====================
    unit_count = fields.Integer(
        "Total de Unidades", compute="_compute_financials", store=True
    )
    units_rented = fields.Integer(
        "Unidades Alugadas", compute="_compute_financials", store=True
    )
    units_available = fields.Integer(
        "Unidades Disponíveis", compute="_compute_financials", store=True
    )
    occupancy_rate = fields.Float(
        "Taxa de Ocupação (%)", digits=(5, 1),
        compute="_compute_financials", store=True
    )
    total_monthly_rent = fields.Monetary(
        "Receita Mensal Total", currency_field="currency_id",
        compute="_compute_financials", store=True,
        help="Soma dos aluguéis dos contratos ativos de todas as unidades"
    )
    noi_monthly = fields.Monetary(
        "NOI Mensal", currency_field="currency_id",
        compute="_compute_financials", store=True,
        help="Net Operating Income: Receita mensal − custos fixos mensais"
    )

    # ==================== Relações ====================
    asset_ids = fields.One2many("property.asset", "complex_id", string="Unidades")

    tag_ids = fields.Many2many(
        "common.tag",
        relation="common_tag_property_complex_rel",
        column1="complex_id",
        column2="tag_id",
        string="Tags",
    )

    notes = fields.Html("Observações")

    # ==================== Computed ====================

    @api.depends(
        "iptu_annual", "foro_annual", "condominium_monthly",
        "asset_ids", "asset_ids.status",
        "asset_ids.contract_ids", "asset_ids.contract_ids.status",
        "asset_ids.contract_ids.monthly_rent",
    )
    def _compute_financials(self):
        for cx in self:
            assets = cx.asset_ids
            total = len(assets)
            rented = len(assets.filtered(lambda a: a.status == "rented"))
            available = len(assets.filtered(lambda a: a.status == "available"))

            active_contracts = self.env["property.contract"].search([
                ("asset_id", "in", assets.ids),
                ("status", "=", "active"),
            ])
            monthly_rent = sum(active_contracts.mapped("monthly_rent"))
            annual_costs = (
                cx.iptu_annual
                + cx.foro_annual
                + (cx.condominium_monthly * 12)
            )

            cx.unit_count = total
            cx.units_rented = rented
            cx.units_available = available
            cx.occupancy_rate = (rented / total * 100) if total else 0.0
            cx.total_monthly_rent = monthly_rent
            cx.total_annual_costs = annual_costs
            cx.noi_monthly = monthly_rent - (annual_costs / 12)

    # ==================== CEP / ZIP CODE ====================

    @api.onchange("zip_code")
    def _onchange_zip_code(self):
        """Auto-fetch address data when zip code is changed"""
        for cx in self:
            if cx.zip_code:
                self._search_zip_code_data(cx)

    def _search_zip_code_data(self, cx):
        """Fetch address data from ViaCEP API using zip code"""
        if not cx.zip_code:
            return

        # Clean zip code (remove special characters)
        clean_zip = cx.zip_code.replace("-", "").replace(" ", "").strip()

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

            # Map ViaCEP fields to property.complex fields
            cx.address = data.get("logradouro", "")
            cx.neighborhood = data.get("bairro", "")
            cx.city = data.get("localidade", "")
            cx.state_name = data.get("uf", "")

        except requests.RequestException as e:
            _logger.warning(f"Error fetching CEP {clean_zip}: {str(e)}")
        except Exception as e:
            _logger.error(f"Unexpected error in CEP lookup: {str(e)}")

    def action_search_zip_code(self):
        """Action button to manually trigger zip code search"""
        self.ensure_one()
        if self.zip_code:
            self._search_zip_code_data(self)
            return {"type": "ir.actions.client", "tag": "reload"}
        return {"type": "ir.actions.client", "tag": "display_notification", "params": {"message": "Informe o CEP", "type": "warning"}}

    # ==================== Actions ====================

    def action_view_units(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Unidades",
            "res_model": "property.asset",
            "view_mode": "list,kanban,form",
            "domain": [("complex_id", "=", self.id)],
            "context": {"default_complex_id": self.id},
        }

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.complex") or "New"
                )
        return super().create(vals_list)

    def write(self, vals):
        """Update linked assets when complex address is changed"""
        # Check if any address fields were modified
        address_fields = {'address', 'address_number', 'city', 'state_name', 'zip_code'}
        modified_fields = address_fields & set(vals.keys())

        # If address fields were modified, update linked assets
        if modified_fields:
            for complex_rec in self:
                # Find all assets linked to this complex
                assets = self.env['property.asset'].search([('complex_id', '=', complex_rec.id)])

                # Prepare update values for assets
                asset_vals = {}
                if 'address' in modified_fields:
                    asset_vals['address'] = vals.get('address')
                if 'address_number' in modified_fields:
                    asset_vals['address_number'] = vals.get('address_number')
                if 'city' in modified_fields:
                    asset_vals['city'] = vals.get('city')
                if 'state_name' in modified_fields:
                    asset_vals['state_name'] = vals.get('state_name')
                if 'zip_code' in modified_fields:
                    asset_vals['zip_code'] = vals.get('zip_code')

                # Update all linked assets
                if asset_vals and assets:
                    assets.write(asset_vals)

        return super().write(vals)