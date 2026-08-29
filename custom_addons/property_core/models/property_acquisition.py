from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
import requests
import logging

_logger = logging.getLogger(__name__)


class PropertyAcquisition(models.Model):
    _name = "property.acquisition"
    _description = "Aquisição de Imóvel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "expected_close_date, name"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Oportunidade", required=True, tracking=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")
    color = fields.Integer("Cor Kanban", default=0)
    priority = fields.Selection([
        ("0", "Normal"),
        ("1", "Importante"),
        ("2", "Urgente"),
    ], default="0", tracking=True)

    # ==================== Tipo e Localização ====================
    asset_type = fields.Selection([
        ("residential", "Residencial"),
        ("commercial", "Comercial"),
        ("land", "Terreno"),
        ("industrial", "Industrial"),
        ("mixed", "Uso Misto"),
    ], string="Tipo de Imóvel", default="residential", tracking=True)

    address = fields.Char("Endereço")
    city = fields.Char("Cidade", tracking=True)
    state_name = fields.Char("Estado")
    neighborhood = fields.Char("Bairro")
    zip_code = fields.Char("CEP")

    total_area = fields.Float("Área Total (m²)", digits=(10, 2))
    useful_area = fields.Float("Área Útil (m²)", digits=(10, 2))

    # ==================== Partes ====================
    seller_partner_id = fields.Many2one(
        "res.partner", string="Vendedor (Contato)", tracking=True,
        domain=[("category_id.name", "ilike", "Vendedor")],
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Comprador", tracking=True,
        domain=[("category_id.name", "ilike", "Comprador")],
    )
    investor_id = fields.Many2one(
        "res.partner", string="Investidor", tracking=True,
        domain=[("category_id.name", "ilike", "Investidor")],
    )
    developer_id = fields.Many2one(
        "res.partner", string="Incorporadora", tracking=True,
        domain=[("category_id.name", "ilike", "Construtora")],
    )
    broker_id = fields.Many2one(
        "res.partner", string="Corretor", tracking=True,
        domain=[("category_id.name", "ilike", "Corretor")],
    )
    responsible_id = fields.Many2one(
        "res.users", string="Responsável",
        default=lambda self: self.env.user, tracking=True
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, index=True
    )

    # ==================== Financeiro ====================
    currency_id = fields.Many2one(
        "res.currency", related="company_id.currency_id", store=True
    )
    asking_price = fields.Monetary(
        "Preço Pedido", currency_field="currency_id", tracking=True
    )
    offer_price = fields.Monetary(
        "Nossa Oferta", currency_field="currency_id", tracking=True
    )
    agreed_price = fields.Monetary(
        "Valor Acordado", currency_field="currency_id", tracking=True
    )
    estimated_renovation = fields.Monetary(
        "Custo de Reforma Estimado", currency_field="currency_id"
    )
    estimated_rent = fields.Monetary(
        "Aluguel Estimado/mês", currency_field="currency_id", tracking=True
    )
    total_investment = fields.Monetary(
        "Investimento Total", currency_field="currency_id",
        compute="_compute_financials", store=True
    )
    roi_annual = fields.Float(
        "ROI Anual (%)", compute="_compute_financials", store=True,
        digits=(5, 2), help="Renda anual / Investimento total × 100"
    )
    discount_pct = fields.Float(
        "Desconto (%)", compute="_compute_financials", store=True,
        digits=(5, 2), help="Desconto obtido sobre o preço pedido"
    )

    # ==================== Datas ====================
    prospect_date = fields.Date(
        "Data de Prospecção", default=fields.Date.today, tracking=True
    )
    expected_close_date = fields.Date("Previsão de Fechamento", tracking=True)
    close_date = fields.Date("Data de Fechamento", tracking=True)

    # ==================== Due Diligence ====================
    dd_legal_docs = fields.Boolean("Documentação Legal OK")
    dd_registration = fields.Boolean("Matrícula Atualizada OK")
    dd_iptu_clear = fields.Boolean("IPTU Quitado OK")
    dd_environmental = fields.Boolean("Licença Ambiental OK")
    dd_structural = fields.Boolean("Laudo Estrutural OK")
    dd_notes = fields.Text("Observações de Due Diligence")

    dd_progress = fields.Integer(
        "Progresso DD (%)", compute="_compute_dd_progress"
    )

    # ==================== Descrição ====================
    description = fields.Text("Descrição do Imóvel")
    notes = fields.Html("Notas e Observações")

    # ==================== Resultado ====================
    asset_id = fields.Many2one(
        "property.asset", string="Imóvel Criado",
        readonly=True, copy=False
    )
    cancellation_reason = fields.Char("Motivo do Cancelamento")

    # ==================== Estágio ====================
    stage = fields.Selection([
        ("prospecting", "Prospecção"),
        ("analysis", "Análise"),
        ("negotiation", "Negociação"),
        ("due_diligence", "Due Diligence"),
        ("closing", "Fechamento"),
        ("closed", "Concluído"),
        ("cancelled", "Cancelado"),
    ], default="prospecting", tracking=True, required=True, group_expand="_expand_stages")

    # ==================== Computed ====================

    @api.depends("asking_price", "agreed_price", "estimated_renovation")
    def _compute_financials(self):
        for acq in self:
            base = acq.agreed_price or acq.offer_price or acq.asking_price
            acq.total_investment = base + acq.estimated_renovation

            if acq.asking_price and acq.agreed_price:
                acq.discount_pct = (
                    (acq.asking_price - acq.agreed_price) / acq.asking_price * 100
                )
            else:
                acq.discount_pct = 0.0

            if acq.total_investment and acq.estimated_rent:
                acq.roi_annual = (acq.estimated_rent * 12) / acq.total_investment * 100
            else:
                acq.roi_annual = 0.0

    def _compute_dd_progress(self):
        checks = ["dd_legal_docs", "dd_registration", "dd_iptu_clear", "dd_environmental", "dd_structural"]
        for acq in self:
            done = sum(1 for c in checks if getattr(acq, c))
            acq.dd_progress = int(done / len(checks) * 100)

    @api.model
    def _expand_stages(self, states, domain):
        return [
            "prospecting", "analysis", "negotiation",
            "due_diligence", "closing", "closed", "cancelled",
        ]

    # ==================== Actions ====================

    def action_set_analysis(self):
        self.ensure_one()
        self.stage = "analysis"
        self.message_post(body=_("Oportunidade movida para Análise."))

    def action_set_negotiation(self):
        self.ensure_one()
        self.stage = "negotiation"
        self.message_post(body=_("Oportunidade movida para Negociação."))

    def action_set_due_diligence(self):
        self.ensure_one()
        self.stage = "due_diligence"
        self.message_post(body=_("Oportunidade movida para Due Diligence."))

    def action_set_closing(self):
        self.ensure_one()
        self.stage = "closing"
        self.message_post(body=_("Oportunidade movida para Fechamento."))

    def action_close(self):
        """Fecha o negócio e cria automaticamente o property.asset."""
        self.ensure_one()
        if self.asset_id:
            raise UserError(_("Este negócio já foi concluído e o imóvel já foi criado."))

        asset = self.env["property.asset"].create({
            "name": self.name,
            "asset_type": self.asset_type,
            "address": self.address,
            "city": self.city,
            "state_name": self.state_name,
            "neighborhood": self.neighborhood,
            "total_area": self.total_area,
            "useful_area": self.useful_area,
            "market_value": self.agreed_price or self.offer_price,
            "status": "available",
        })
        self.asset_id = asset.id
        self.stage = "closed"
        self.close_date = date.today()

        # Auto-create commission if broker is set
        if self.broker_id:
            base = self.agreed_price or self.offer_price or self.asking_price
            self.env["property.commission"].create({
                "broker_id": self.broker_id.id,
                "acquisition_id": self.id,
                "commission_type": "sale",
                "base_value": base,
                "commission_rate": self.broker_id.commission_rate,
                "deal_date": self.close_date,
            })

        self.message_post(
            body=_("Negócio fechado em %s. Imóvel %s criado automaticamente.") % (
                self.close_date, asset.reference
            )
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Imóvel Criado",
            "res_model": "property.asset",
            "res_id": asset.id,
            "view_mode": "form",
        }

    def action_view_asset(self):
        self.ensure_one()
        if not self.asset_id:
            return
        return {
            "type": "ir.actions.act_window",
            "name": "Imóvel",
            "res_model": "property.asset",
            "res_id": self.asset_id.id,
            "view_mode": "form",
        }

    def action_cancel(self):
        self.ensure_one()
        self.stage = "cancelled"
        self.message_post(body=_("Oportunidade cancelada."))

    def action_reset(self):
        self.ensure_one()
        if self.stage != "cancelled":
            raise UserError(_("Apenas oportunidades canceladas podem ser reabertas."))
        self.stage = "prospecting"

    # ==================== CEP / ZIP CODE ====================

    @api.onchange("zip_code")
    def _onchange_zip_code(self):
        """Auto-fetch address data when zip code is changed"""
        for acq in self:
            if acq.zip_code:
                self._search_zip_code_data(acq)

    def _search_zip_code_data(self, acq):
        """Fetch address data from ViaCEP API using zip code"""
        if not acq.zip_code:
            return

        # Clean zip code (remove special characters)
        clean_zip = acq.zip_code.replace("-", "").replace(" ", "").strip()

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

            # Map ViaCEP fields to property.acquisition fields
            acq.address = data.get("logradouro", "")
            acq.neighborhood = data.get("bairro", "")
            acq.city = data.get("localidade", "")
            acq.state_name = data.get("uf", "")

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

    # ==================== Constraints ====================

    @api.constrains("asking_price", "offer_price", "agreed_price")
    def _check_prices(self):
        for acq in self:
            for field, label in [
                ("asking_price", "Preço Pedido"),
                ("offer_price", "Nossa Oferta"),
                ("agreed_price", "Valor Acordado"),
            ]:
                if getattr(acq, field) < 0:
                    raise ValidationError(_("%s não pode ser negativo.") % label)

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.acquisition") or "New"
                )
        return super().create(vals_list)