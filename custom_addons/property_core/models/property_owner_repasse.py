from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date


class PropertyOwnerRepasse(models.Model):
    _name = "property.owner.repasse"
    _description = "Repasse Mensal ao Proprietário"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "period_year desc, period_month desc, id desc"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Descrição", compute="_compute_name", store=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")

    # ==================== Proprietário e Período ====================
    owner_id = fields.Many2one(
        "res.partner", string="Proprietário",
        required=True, tracking=True, ondelete="restrict",
        domain=[("category_id.name", "ilike", "Proprietário")],
    )
    period_month = fields.Integer("Mês", required=True)
    period_year = fields.Integer("Ano", required=True)
    date_from = fields.Date("De", required=True)
    date_to = fields.Date("Até", required=True)

    # ==================== Estado ====================
    state = fields.Selection([
        ("draft", "Rascunho"),
        ("confirmed", "Confirmado"),
        ("paid", "Pago"),
        ("cancelled", "Cancelado"),
    ], string="Estado", default="draft", tracking=True, required=True)

    # ==================== Registros Vinculados ====================
    rent_ids = fields.Many2many(
        "property.rent", "repasse_rent_rel", "repasse_id", "rent_id",
        string="Parcelas Pagas",
    )
    commission_ids = fields.Many2many(
        "property.commission", "repasse_commission_rel", "repasse_id", "commission_id",
        string="Comissões Pagas",
    )
    maintenance_ids = fields.Many2many(
        "property.maintenance", "repasse_maintenance_rel", "repasse_id", "maintenance_id",
        string="Manutenções Realizadas",
    )

    # ==================== Financeiro ====================
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )
    management_fee_pct = fields.Float(
        "Taxa de Administração (%)", default=10.0,
        help="Percentual retido pela administradora sobre o aluguel bruto recebido",
        tracking=True,
    )

    rent_total = fields.Monetary(
        "Aluguéis Recebidos", currency_field="currency_id",
        compute="_compute_totals", store=True,
    )
    commission_total = fields.Monetary(
        "Total Comissões", currency_field="currency_id",
        compute="_compute_totals", store=True,
    )
    maintenance_total = fields.Monetary(
        "Manutenções", currency_field="currency_id",
        compute="_compute_totals", store=True,
    )
    management_fee = fields.Monetary(
        "Taxa de Administração", currency_field="currency_id",
        compute="_compute_totals", store=True,
    )
    gross_amount = fields.Monetary(
        "Valor Bruto ao Proprietário", currency_field="currency_id",
        compute="_compute_totals", store=True,
        help="Aluguéis − Comissões − Manutenções",
    )
    net_amount = fields.Monetary(
        "Valor Líquido a Repassar", currency_field="currency_id",
        compute="_compute_totals", store=True,
        help="Valor Bruto − Taxa de Administração",
    )

    # ==================== Pagamento ====================
    payment_date = fields.Date("Data do Repasse", tracking=True)
    account_move_id = fields.Many2one(
        "account.move", string="Lançamento Contábil",
        readonly=True, copy=False,
    )

    notes = fields.Text("Observações")
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, index=True
    )

    # ==================== Computed ====================

    @api.depends("owner_id", "period_month", "period_year")
    def _compute_name(self):
        for r in self:
            if r.owner_id and r.period_month and r.period_year:
                r.name = "Repasse %02d/%d — %s" % (
                    r.period_month, r.period_year, r.owner_id.name
                )
            else:
                r.name = "Repasse (Rascunho)"

    @api.depends("rent_ids", "commission_ids", "maintenance_ids", "management_fee_pct")
    def _compute_totals(self):
        for r in self:
            rent_total = sum(r.rent_ids.mapped("amount_paid"))
            commission_total = sum(r.commission_ids.mapped("commission_value"))
            maintenance_total = sum(r.maintenance_ids.mapped("cost_actual"))
            management_fee = rent_total * (r.management_fee_pct / 100.0)
            gross = rent_total - commission_total - maintenance_total
            net = gross - management_fee

            r.rent_total = rent_total
            r.commission_total = commission_total
            r.maintenance_total = maintenance_total
            r.management_fee = management_fee
            r.gross_amount = gross
            r.net_amount = max(net, 0.0)

    # ==================== Onchange ====================

    @api.onchange("period_month", "period_year")
    def _onchange_period(self):
        if self.period_month and self.period_year:
            import calendar
            last_day = calendar.monthrange(self.period_year, self.period_month)[1]
            self.date_from = date(self.period_year, self.period_month, 1)
            self.date_to = date(self.period_year, self.period_month, last_day)

    # ==================== Actions ====================

    def action_load_data(self):
        """Auto-popula parcelas, comissões e manutenções do período."""
        self.ensure_one()
        assets = self.env["property.asset"].search([("owner_id", "=", self.owner_id.id)])
        if not assets:
            raise UserError(_("O proprietário não possui imóveis cadastrados."))
        if not self.date_from or not self.date_to:
            raise UserError(_("Defina o período (De / Até) antes de carregar os dados."))

        asset_ids = assets.ids

        rents = self.env["property.rent"].search([
            ("asset_id", "in", asset_ids),
            ("status", "=", "paid"),
            ("payment_date", ">=", self.date_from),
            ("payment_date", "<=", self.date_to),
        ])
        commissions = self.env["property.commission"].search([
            ("asset_id", "in", asset_ids),
            ("status", "=", "paid"),
            ("payment_date", ">=", self.date_from),
            ("payment_date", "<=", self.date_to),
        ])
        maintenances = self.env["property.maintenance"].search([
            ("asset_id", "in", asset_ids),
            ("status", "=", "done"),
            ("completion_date", ">=", self.date_from),
            ("completion_date", "<=", self.date_to),
        ])

        self.write({
            "rent_ids": [(6, 0, rents.ids)],
            "commission_ids": [(6, 0, commissions.ids)],
            "maintenance_ids": [(6, 0, maintenances.ids)],
        })
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "message": _(
                    "Dados carregados: %d parcelas, %d comissões, %d manutenções."
                ) % (len(rents), len(commissions), len(maintenances)),
                "next": {"type": "ir.actions.act_window_close"},
            },
        }

    def action_confirm(self):
        self.ensure_one()
        if self.state != "draft":
            raise UserError(_("Apenas repasses em Rascunho podem ser confirmados."))
        if not self.rent_ids and not self.maintenance_ids:
            raise UserError(_(
                "Carregue os dados do período antes de confirmar "
                "(use o botão 'Carregar Dados do Período')."
            ))
        self.state = "confirmed"
        self.message_post(
            body=_("Repasse confirmado. Valor líquido a repassar: R$ %.2f") % self.net_amount
        )
        self._send_repasse_email("property_core.email_template_repasse_confirmado")

    def action_register_payment(self):
        """Marca como pago e cria lançamento contábil se configurado."""
        self.ensure_one()
        if self.state != "confirmed":
            raise UserError(_("Apenas repasses confirmados podem ser marcados como pagos."))
        if not self.payment_date:
            self.payment_date = date.today()
        self._create_repasse_move()
        self.state = "paid"
        self.message_post(
            body=_("Repasse realizado em %s. Valor: R$ %.2f") % (self.payment_date, self.net_amount)
        )
        self._send_repasse_email("property_core.email_template_repasse_pago")

    def _send_repasse_email(self, template_xmlid):
        """Envia e-mail ao proprietário se houver endereço configurado."""
        email_to = self.owner_id.email
        if not email_to:
            return
        template = self.env.ref(template_xmlid, raise_if_not_found=False)
        if template:
            try:
                template.send_mail(self.id, force_send=False)
            except Exception:
                pass  # não bloqueia a operação principal

    def action_cancel(self):
        self.ensure_one()
        if self.state == "paid":
            raise UserError(_(
                "Repasses pagos não podem ser cancelados diretamente. "
                "Estorne o lançamento contábil primeiro."
            ))
        self.state = "cancelled"
        self.message_post(body=_("Repasse cancelado."))

    def action_reset_draft(self):
        self.ensure_one()
        if self.state not in ("cancelled",):
            raise UserError(_("Apenas repasses cancelados podem ser redefinidos para Rascunho."))
        self.state = "draft"

    def action_view_account_move(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Lançamento Contábil"),
            "res_model": "account.move",
            "res_id": self.account_move_id.id,
            "view_mode": "form",
        }

    # ==================== Accounting ====================

    def _create_repasse_move(self):
        """Cria lançamento contábil de saída para o repasse ao proprietário.
        Débito: conta de repasse (passivo/obrigação) | Crédito: conta bancária.
        """
        params = self.env["ir.config_parameter"].sudo()

        jid = int(params.get_param("property_core.repasse_journal_id", 0))
        journal = self.env["account.journal"].browse(jid) if jid else self.env["account.journal"]

        aid = int(params.get_param("property_core.repasse_account_id", 0))
        account = self.env["account.account"].browse(aid) if aid else self.env["account.account"]

        if not journal or not account:
            self.message_post(
                body=_(
                    "⚠️ Lançamento contábil não gerado: configure o Diário de Repasse e a "
                    "Conta de Repasse em Configurações → Contabilidade → Imóveis."
                ),
                subtype_xmlid="mail.mt_note",
            )
            return

        if not journal.default_account_id:
            self.message_post(
                body=_("⚠️ O diário '%s' não possui conta padrão configurada.") % journal.name,
                subtype_xmlid="mail.mt_note",
            )
            return

        partner_id = self.owner_id.id

        move = self.env["account.move"].create({
            "move_type": "entry",
            "journal_id": journal.id,
            "date": self.payment_date or fields.Date.today(),
            "ref": self.reference,
            "narration": _("Repasse ao proprietário – %s") % self.name,
            "line_ids": [
                # Débito: obrigação com proprietário (liquidação)
                (0, 0, {
                    "account_id": account.id,
                    "name": self.name,
                    "debit": self.net_amount,
                    "credit": 0.0,
                    "partner_id": partner_id,
                }),
                # Crédito: banco/caixa (saída de recursos)
                (0, 0, {
                    "account_id": journal.default_account_id.id,
                    "name": self.name,
                    "debit": 0.0,
                    "credit": self.net_amount,
                    "partner_id": partner_id,
                }),
            ],
        })
        move.action_post()
        self.account_move_id = move.id

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.owner.repasse")
                    or "New"
                )
        return super().create(vals_list)