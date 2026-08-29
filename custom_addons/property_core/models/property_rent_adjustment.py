from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class PropertyRentAdjustment(models.Model):
    _name = "property.rent.adjustment"
    _description = "Reajuste de Aluguel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "adjustment_date desc"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Descrição", compute="_compute_name", store=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")

    # ==================== Vínculos ====================
    contract_id = fields.Many2one(
        "property.contract", string="Contrato",
        required=True, ondelete="cascade", tracking=True
    )
    asset_id = fields.Many2one(
        "property.asset", string="Imóvel",
        related="contract_id.asset_id", store=True
    )
    partner_id = fields.Many2one(
        "res.partner", string="Locatário",
        related="contract_id.partner_id", store=True
    )
    company_id = fields.Many2one(
        "res.company", related="contract_id.company_id", store=True
    )
    currency_id = fields.Many2one(
        "res.currency", related="contract_id.currency_id", store=True
    )

    # ==================== Índice ====================
    index_type = fields.Selection([
        ("igpm", "IGP-M"),
        ("ipca", "IPCA"),
        ("inpc", "INPC"),
        ("ivar", "IVAR"),
        ("fixed", "Taxa Fixa"),
        ("negotiated", "Negociado"),
    ], string="Índice", required=True, default="igpm", tracking=True)

    index_id = fields.Many2one(
        "property.index", string="Índice BCB",
        compute="_compute_index_id", store=True, readonly=False,
        help="Vínculo com o índice cadastrado para busca automática de taxas"
    )
    period_months = fields.Integer(
        "Meses Acumulados", default=12,
        help="Quantidade de meses para cálculo da taxa acumulada"
    )
    period_start = fields.Date(
        "Início do Período", compute="_compute_period_start", store=True,
        help="Calculado automaticamente: data do reajuste menos período em meses"
    )
    index_period = fields.Char(
        "Período de Referência", compute="_compute_index_period", store=True,
        tracking=True, help="Ex: Abr/2025 a Mar/2026 (12 meses)"
    )
    index_rate = fields.Float(
        "Taxa Acumulada (%)", digits=(6, 4), tracking=True,
        help="Taxa acumulada no período. Calculada automaticamente ou informada manualmente."
    )
    months_found = fields.Integer(
        "Meses encontrados", readonly=True,
        help="Quantidade de meses com dados disponíveis usados no cálculo"
    )

    # ==================== Valores ====================
    previous_rent = fields.Monetary(
        "Aluguel Anterior", currency_field="currency_id",
        required=True, tracking=True
    )
    new_rent = fields.Monetary(
        "Novo Aluguel", currency_field="currency_id",
        compute="_compute_new_rent", store=True, readonly=False,
        tracking=True,
        help="Calculado automaticamente. Pode ser ajustado manualmente."
    )
    adjustment_value = fields.Monetary(
        "Variação (R$)", currency_field="currency_id",
        compute="_compute_adjustment_value", store=True
    )
    adjustment_pct = fields.Float(
        "Variação (%)", digits=(5, 2),
        compute="_compute_adjustment_value", store=True
    )

    # ==================== Datas ====================
    adjustment_date = fields.Date(
        "Data do Reajuste", default=fields.Date.today, tracking=True
    )
    effective_date = fields.Date(
        "Data de Vigência", tracking=True,
        help="Data a partir da qual o novo valor passa a vigorar"
    )

    # ==================== Status ====================
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("applied", "Aplicado"),
        ("cancelled", "Cancelado"),
    ], default="draft", tracking=True, required=True)

    notes = fields.Text("Observações")

    # ==================== Computed ====================

    @api.depends("index_type")
    def _compute_index_id(self):
        """Auto-vincula ao registro property.index quando o tipo tem BCB."""
        BCB_CODES = ("igpm", "ipca", "inpc")
        for adj in self:
            if adj.index_type in BCB_CODES:
                idx = self.env["property.index"].search(
                    [("code", "=", adj.index_type)], limit=1
                )
                adj.index_id = idx or False
            else:
                adj.index_id = False

    @api.depends("adjustment_date", "period_months")
    def _compute_period_start(self):
        for adj in self:
            if adj.adjustment_date and adj.period_months > 0:
                adj.period_start = adj.adjustment_date - relativedelta(months=adj.period_months - 1)
            else:
                adj.period_start = False

    @api.depends("period_start", "adjustment_date")
    def _compute_index_period(self):
        labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                  "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        for adj in self:
            if adj.period_start and adj.adjustment_date:
                s = adj.period_start
                e = adj.adjustment_date
                adj.index_period = "%s/%s a %s/%s (%s meses)" % (
                    labels[s.month - 1], s.year,
                    labels[e.month - 1], e.year,
                    adj.period_months,
                )
            else:
                adj.index_period = ""

    @api.depends("contract_id", "index_type", "adjustment_date")
    def _compute_name(self):
        index_labels = {
            "igpm": "IGP-M", "ipca": "IPCA", "inpc": "INPC",
            "ivar": "IVAR", "fixed": "Fixa", "negotiated": "Negociado",
        }
        for adj in self:
            label = index_labels.get(adj.index_type, "")
            if adj.contract_id and adj.adjustment_date:
                adj.name = "Reajuste %s – %s (%s)" % (
                    label, adj.contract_id.name or "", adj.adjustment_date.strftime("%m/%Y")
                )
            else:
                adj.name = "Reajuste %s" % label

    @api.depends("previous_rent", "index_rate")
    def _compute_new_rent(self):
        for adj in self:
            if adj.previous_rent and adj.index_rate:
                adj.new_rent = adj.previous_rent * (1 + adj.index_rate / 100)
            elif not adj.new_rent:
                adj.new_rent = adj.previous_rent

    @api.depends("previous_rent", "new_rent")
    def _compute_adjustment_value(self):
        for adj in self:
            adj.adjustment_value = adj.new_rent - adj.previous_rent
            if adj.previous_rent:
                adj.adjustment_pct = (adj.adjustment_value / adj.previous_rent) * 100
            else:
                adj.adjustment_pct = 0.0

    # ==================== Onchange ====================

    @api.onchange("contract_id")
    def _onchange_contract_id(self):
        if self.contract_id:
            self.previous_rent = self.contract_id.monthly_rent

    # ==================== Actions ====================

    def action_fetch_rate(self):
        """Busca a taxa acumulada do período nos dados locais (sincronizados do BCB)."""
        self.ensure_one()
        if not self.index_id:
            raise UserError(_(
                "Selecione um índice BCB (IGP-M, IPCA ou INPC) para buscar a taxa automaticamente."
            ))
        if not self.period_start or not self.adjustment_date:
            raise UserError(_("Defina a data do reajuste e o período de meses."))

        # Garante que o período começa no 1º dia do mês
        from datetime import date as dt
        period_start = dt(self.period_start.year, self.period_start.month, 1)
        period_end = dt(self.adjustment_date.year, self.adjustment_date.month, 1)

        rate, months = self.index_id.get_accumulated_rate(period_start, period_end)

        if months == 0:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": _(
                        "Nenhum dado encontrado para %s no período %s. "
                        "Sincronize o índice primeiro."
                    ) % (self.index_id.name, self.index_period),
                    "type": "warning",
                    "sticky": True,
                },
            }

        self.index_rate = rate
        self.months_found = months

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": _("%s acumulado (%s meses): %.4f%%") % (
                    self.index_id.name, months, rate
                ),
                "type": "success",
                "sticky": False,
            },
        }

    def action_apply(self):
        """Aplica o reajuste: atualiza o aluguel mensal e avança o próximo reajuste."""
        self.ensure_one()
        if self.status != "draft":
            raise UserError(_("Este reajuste já foi aplicado ou cancelado."))
        if not self.new_rent or self.new_rent <= 0:
            raise UserError(_("O novo aluguel deve ser um valor positivo."))

        old = self.contract_id.monthly_rent
        self.contract_id.write({
            "monthly_rent": self.new_rent,
            "last_adjustment_date": self.adjustment_date,
        })
        self.status = "applied"

        # Marcar atividade de reajuste como concluída
        self.contract_id.activity_ids.filtered(
            lambda a: "reajuste" in (a.summary or "").lower()
        ).action_done()

        self.contract_id.message_post(
            body=_("Reajuste aplicado em %s: R$ %.2f → R$ %.2f (%s %.4f%% — %s). "
                   "Próximo reajuste: %s") % (
                self.adjustment_date,
                old,
                self.new_rent,
                self.index_type.upper(),
                self.index_rate,
                self.index_period or "",
                self.contract_id.next_adjustment_date,
            )
        )
        self.message_post(body=_("Reajuste aplicado ao contrato %s.") % self.contract_id.name)

    def action_create_renewal(self):
        """Cria um novo contrato em rascunho com o valor reajustado para revisão."""
        self.ensure_one()
        if self.status != "applied":
            raise UserError(_("Aplique o reajuste antes de gerar a renovação."))

        new_contract = self.contract_id.copy({
            "status": "draft",
            "monthly_rent": self.new_rent,
            "start_date": self.effective_date or self.adjustment_date,
            "last_adjustment_date": False,
            "name": _("%s (Renovação)") % self.contract_id.name,
        })
        new_contract.message_post(
            body=_("Renovação gerada a partir do reajuste %s (%.4f%% — %s).") % (
                self.reference, self.index_rate, self.index_period or ""
            )
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Novo Contrato"),
            "res_model": "property.contract",
            "res_id": new_contract.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_cancel(self):
        self.ensure_one()
        if self.status == "applied":
            raise UserError(
                _("Reajuste já aplicado. Para reverter, ajuste o valor do contrato manualmente.")
            )
        self.status = "cancelled"

    def action_reset_draft(self):
        self.ensure_one()
        if self.status != "cancelled":
            raise UserError(_("Apenas reajustes cancelados podem ser reabertos."))
        self.status = "draft"

    # ==================== Constraints ====================

    @api.constrains("index_rate")
    def _check_index_rate(self):
        for adj in self:
            if adj.index_rate < -50 or adj.index_rate > 100:
                raise ValidationError(_("A taxa do índice parece inválida (entre -50% e 100%)."))

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.rent.adjustment") or "New"
                )
        records = super().create(vals_list)
        # Auto-calcular taxa BCB ao criar
        for rec in records:
            if rec.index_id and rec.index_type in ("igpm", "ipca", "inpc"):
                try:
                    rec.action_fetch_rate()
                except Exception:
                    pass
        return records