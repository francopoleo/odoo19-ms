from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class PropertyCommission(models.Model):
    _name = "property.commission"
    _description = "Comissão de Corretor"
    _inherit = ["mail.thread"]
    _order = "create_date desc"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Descrição", compute="_compute_name", store=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")

    # ==================== Tipo ====================
    commission_type = fields.Selection([
        ("sale", "Venda"),
        ("rental", "Locação"),
    ], string="Tipo", required=True, default="sale", tracking=True)

    # ==================== Vínculos ====================
    broker_id = fields.Many2one(
        "res.partner", string="Corretor",
        required=True, ondelete="restrict", tracking=True,
        domain=[("category_id.name", "ilike", "Corretor")],
    )
    acquisition_id = fields.Many2one(
        "property.acquisition", string="Aquisição",
        ondelete="set null", tracking=True
    )
    contract_id = fields.Many2one(
        "property.contract", string="Contrato",
        ondelete="set null", tracking=True
    )
    asset_id = fields.Many2one(
        "property.asset", string="Imóvel",
        compute="_compute_asset", store=True
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, index=True
    )

    # ==================== Financeiro ====================
    currency_id = fields.Many2one(
        "res.currency", related="company_id.currency_id", store=True
    )
    base_value = fields.Monetary(
        "Valor Base do Negócio", currency_field="currency_id",
        required=True, tracking=True
    )
    commission_rate = fields.Float(
        "Taxa de Comissão (%)", digits=(5, 2),
        tracking=True
    )
    commission_value = fields.Monetary(
        "Valor da Comissão", currency_field="currency_id",
        compute="_compute_commission", store=True, readonly=False,
        tracking=True
    )

    # ==================== Datas ====================
    deal_date = fields.Date(
        "Data do Negócio", default=fields.Date.today, tracking=True
    )
    due_date = fields.Date("Vencimento da Comissão", tracking=True)
    payment_date = fields.Date("Data de Pagamento", tracking=True)

    # ==================== Status ====================
    status = fields.Selection([
        ("pending", "A Pagar"),
        ("paid", "Pago"),
        ("cancelled", "Cancelado"),
    ], default="pending", tracking=True, required=True)

    notes = fields.Text("Observações")

    # ==================== Computed ====================

    @api.depends("broker_id", "acquisition_id", "contract_id", "commission_type", "deal_date")
    def _compute_name(self):
        type_label = {"sale": "Venda", "rental": "Locação"}
        for comm in self:
            broker = comm.broker_id.name or "Corretor"
            tipo = type_label.get(comm.commission_type, "")
            ref = comm.acquisition_id.name or comm.contract_id.name or ""
            if ref:
                comm.name = "Comissão %s (%s) — %s" % (broker, tipo, ref)
            else:
                comm.name = "Comissão %s (%s)" % (broker, tipo)

    @api.depends("acquisition_id", "contract_id")
    def _compute_asset(self):
        for comm in self:
            if comm.acquisition_id and comm.acquisition_id.asset_id:
                comm.asset_id = comm.acquisition_id.asset_id
            elif comm.contract_id:
                comm.asset_id = comm.contract_id.asset_id
            else:
                comm.asset_id = False

    @api.depends("base_value", "commission_rate")
    def _compute_commission(self):
        for comm in self:
            if comm.base_value and comm.commission_rate:
                comm.commission_value = comm.base_value * comm.commission_rate / 100
            elif not comm.commission_value:
                comm.commission_value = 0.0

    # ==================== Onchange ====================

    @api.onchange("broker_id")
    def _onchange_broker_id(self):
        if self.broker_id:
            self.commission_rate = self.broker_id.commission_rate

    @api.onchange("acquisition_id")
    def _onchange_acquisition_id(self):
        if self.acquisition_id:
            self.commission_type = "sale"
            self.base_value = (
                self.acquisition_id.agreed_price
                or self.acquisition_id.offer_price
                or self.acquisition_id.asking_price
            )
            if self.acquisition_id.broker_id and not self.broker_id:
                self.broker_id = self.acquisition_id.broker_id

    @api.onchange("contract_id")
    def _onchange_contract_id(self):
        if self.contract_id:
            self.commission_type = "rental"
            self.base_value = self.contract_id.total_value

    # ==================== Actions ====================

    def action_pay(self):
        self.ensure_one()
        if self.status != "pending":
            raise UserError(_("Esta comissão não está pendente de pagamento."))
        if not self.payment_date:
            self.payment_date = date.today()
        self.status = "paid"
        self.message_post(
            body=_("Comissão de %s paga em %s: R$ %.2f") % (
                self.broker_id.name, self.payment_date, self.commission_value
            )
        )

    def action_cancel(self):
        self.ensure_one()
        self.status = "cancelled"

    # ==================== Constraints ====================

    @api.constrains("commission_rate")
    def _check_rate(self):
        for comm in self:
            if comm.commission_rate < 0 or comm.commission_rate > 100:
                raise ValidationError(_("Taxa de comissão deve ser entre 0% e 100%."))

    # ==================== Cron ====================

    @api.model
    def action_cron_commission_reminder(self):
        """Weekly cron: post chatter reminder on pending commissions older than 7 days."""
        from datetime import timedelta
        cutoff = fields.Date.today() - timedelta(days=7)
        pending = self.search([
            ("status", "=", "pending"),
            ("create_date", "<=", cutoff),
        ])
        for comm in pending:
            comm.message_post(
                body=_("🔔 Lembrete: comissão %s de R$ %.2f ainda está pendente de pagamento.") % (
                    comm.reference, comm.commission_value
                )
            )

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.commission") or "New"
                )
        return super().create(vals_list)