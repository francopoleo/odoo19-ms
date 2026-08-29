from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class PropertyRent(models.Model):
    _name = "property.rent"
    _description = "Parcela de Aluguel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "due_date"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Descrição", compute="_compute_name", store=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")

    # ==================== Relações ====================
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

    # ==================== Competência ====================
    competence_month = fields.Integer("Mês", tracking=True)
    competence_year = fields.Integer("Ano", tracking=True)

    # ==================== Datas ====================
    due_date = fields.Date("Vencimento", required=True, tracking=True)
    payment_date = fields.Date("Data de Pagamento", tracking=True)

    # ==================== Valores ====================
    currency_id = fields.Many2one(
        "res.currency", related="contract_id.currency_id", store=True
    )
    amount = fields.Monetary("Valor Base", required=True, currency_field="currency_id")
    discount = fields.Monetary("Desconto", currency_field="currency_id")
    fine = fields.Monetary("Multa", currency_field="currency_id")
    interest = fields.Monetary("Juros", currency_field="currency_id")
    amount_paid = fields.Monetary("Valor Pago", currency_field="currency_id", tracking=True)
    amount_due = fields.Monetary(
        "Valor a Pagar", currency_field="currency_id",
        compute="_compute_amount_due", store=True
    )

    # ==================== Contabilidade ====================
    account_move_id = fields.Many2one(
        "account.move",
        string="Lançamento Contábil",
        readonly=True, copy=False,
        help="Lançamento gerado automaticamente ao registrar o pagamento",
    )

    # ==================== Recibo de Aluguel ====================
    receipt_number = fields.Char(
        "Nº do Recibo",
        readonly=True,
        copy=False,
        tracking=True,
        help="Número do recibo emitido após a confirmação do recebimento do aluguel.",
    )
    receipt_date = fields.Date(
        "Data do Recibo",
        readonly=True,
        copy=False,
        tracking=True,
    )
    receipt_state = fields.Selection([
        ("none", "Não Emitido"),
        ("issued", "Emitido"),
        ("cancelled", "Cancelado"),
    ], string="Status do Recibo", default="none", readonly=True, copy=False, tracking=True)

    # ==================== Pagamento ====================
    payment_method = fields.Selection([
        ("pix", "PIX"),
        ("transfer", "Transferência Bancária"),
        ("boleto", "Boleto"),
        ("cash", "Dinheiro"),
        ("check", "Cheque"),
    ], string="Forma de Pagamento", tracking=True)
    payment_notes = fields.Text("Observações do Pagamento")

    # ==================== Status ====================
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("open", "Em Aberto"),
        ("partial", "Parcialmente Pago"),
        ("paid", "Pago"),
        ("late", "Atrasado"),
        ("cancelled", "Cancelado"),
    ], default="draft", tracking=True, required=True)

    days_late = fields.Integer("Dias em Atraso", compute="_compute_days_late")

    # ==================== Controle régua ====================
    notified_d1 = fields.Boolean("Notificado D+1", default=False)
    notified_d5 = fields.Boolean("Notificado D+5", default=False)
    notified_d15 = fields.Boolean("Notificado D+15", default=False)
    notified_d30 = fields.Boolean("Notificado D+30", default=False)

    # ==================== Computed ====================

    @api.depends("competence_month", "competence_year", "contract_id")
    def _compute_name(self):
        for rent in self:
            if rent.competence_month and rent.competence_year:
                rent.name = "Aluguel %02d/%d – %s" % (
                    rent.competence_month,
                    rent.competence_year,
                    rent.contract_id.name or "",
                )
            else:
                rent.name = rent.contract_id.name or "Parcela"

    @api.depends("amount", "discount", "fine", "interest")
    def _compute_amount_due(self):
        for rent in self:
            rent.amount_due = rent.amount - rent.discount + rent.fine + rent.interest

    def _compute_days_late(self):
        today = date.today()
        for rent in self:
            if rent.due_date and rent.status in ("late", "open") and rent.due_date < today:
                rent.days_late = (today - rent.due_date).days
            else:
                rent.days_late = 0

    # ==================== Constraints ====================

    @api.constrains("amount")
    def _check_amount(self):
        for rent in self:
            if rent.amount <= 0:
                raise ValidationError(_("O valor da parcela deve ser positivo."))

    @api.constrains("amount_paid")
    def _check_amount_paid(self):
        for rent in self:
            if rent.amount_paid < 0:
                raise ValidationError(_("O valor pago não pode ser negativo."))

    # ==================== Actions ====================

    def action_open(self):
        self.ensure_one()
        if self.status != "draft":
            raise UserError(_("Apenas parcelas em Rascunho podem ser abertas."))
        self.status = "open"
        self.message_post(body=_("Parcela aberta para cobrança."))

    def action_register_payment(self):
        """Registra pagamento total ou parcial e emite recibo após quitação."""
        self.ensure_one()
        if self.status not in ("open", "late", "partial"):
            raise UserError(_("Esta parcela não está disponível para pagamento."))
        if not self.amount_paid:
            raise UserError(_("Informe o valor pago antes de confirmar."))
        if not self.payment_date:
            self.payment_date = date.today()

        if self.amount_paid >= self.amount_due:
            self.status = "paid"
            self._create_accounting_entry()
            self._issue_rent_receipt()
            self.message_post(
                body=_("Pagamento total confirmado: R$ %.2f em %s. Recibo %s emitido.") % (
                    self.amount_paid, self.payment_date, self.receipt_number or "-"
                )
            )
            return self.action_print_receipt()

        self.status = "partial"
        self.message_post(
            body=_("Pagamento parcial registrado: R$ %.2f de R$ %.2f em %s.") % (
                self.amount_paid, self.amount_due, self.payment_date
            )
        )

    def _issue_rent_receipt(self):
        """Emite o recibo de aluguel após a confirmação do pagamento total."""
        for rent in self:
            if rent.status != "paid":
                continue
            if not rent.receipt_number:
                sequence = rent.env["ir.sequence"].sudo().next_by_code("property.rent.receipt")
                rent.receipt_number = sequence or "REC-%s" % rent.id
            if not rent.receipt_date:
                rent.receipt_date = rent.payment_date or fields.Date.today()
            rent.receipt_state = "issued"

    def action_print_receipt(self):
        self.ensure_one()
        if self.status != "paid" or self.receipt_state != "issued":
            raise UserError(_("O recibo só pode ser impresso após a confirmação do pagamento total."))
        return self.env.ref("property_core.action_report_property_rent_receipt").report_action(self)

    def action_cancel(self):
        self.ensure_one()
        # Reverter lançamento contábil se existir
        if self.account_move_id and self.account_move_id.state == "posted":
            self.account_move_id.button_cancel()
        if self.receipt_state == "issued":
            self.receipt_state = "cancelled"
            self.message_post(body=_("Recibo %s cancelado por cancelamento da parcela.") % (self.receipt_number or "-"))
        self.status = "cancelled"
        self.message_post(body=_("Parcela cancelada em %s.") % date.today())

    def action_view_account_move(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Lançamento Contábil",
            "res_model": "account.move",
            "res_id": self.account_move_id.id,
            "view_mode": "form",
        }

    # ==================== Accounting ====================

    def _create_accounting_entry(self):
        """Cria e posta lançamento contábil ao registrar pagamento total.
        Débito: conta do diário (caixa/banco) | Crédito: conta de receita de aluguel.
        Usa configuração do contrato; se vazia, usa padrão dos parâmetros do sistema.
        """
        contract = self.contract_id
        params = self.env["ir.config_parameter"].sudo()

        journal = contract.journal_id
        if not journal:
            jid = int(params.get_param("property_core.rent_journal_id", 0))
            journal = self.env["account.journal"].browse(jid) if jid else self.env["account.journal"]

        income_account = contract.income_account_id
        if not income_account:
            aid = int(params.get_param("property_core.rent_income_account_id", 0))
            income_account = self.env["account.account"].browse(aid) if aid else self.env["account.account"]

        if not journal or not income_account:
            # Contabilidade não configurada — registra aviso no chatter e segue
            self.message_post(
                body=_("⚠️ Lançamento contábil não gerado: configure o Diário e a Conta de Receita "
                       "em Contabilidade → Imóveis ou no contrato."),
                subtype_xmlid="mail.mt_note",
            )
            return

        if not journal.default_account_id:
            self.message_post(
                body=_("⚠️ Lançamento contábil não gerado: o diário '%s' não possui conta padrão.") % journal.name,
                subtype_xmlid="mail.mt_note",
            )
            return

        move = self.env["account.move"].create({
            "move_type": "entry",
            "journal_id": journal.id,
            "date": self.payment_date or fields.Date.today(),
            "ref": self.reference,
            "narration": _("Recebimento de aluguel – %s") % self.name,
            "line_ids": [
                # Débito: conta do diário (caixa ou banco)
                (0, 0, {
                    "account_id": journal.default_account_id.id,
                    "name": self.name,
                    "debit": self.amount_paid,
                    "credit": 0.0,
                    "partner_id": self.partner_id.id if self.partner_id else False,
                }),
                # Crédito: conta de receita de aluguel
                (0, 0, {
                    "account_id": income_account.id,
                    "name": self.name,
                    "debit": 0.0,
                    "credit": self.amount_paid,
                    "partner_id": self.partner_id.id if self.partner_id else False,
                }),
            ],
        })
        move.action_post()
        self.account_move_id = move.id

    def action_reset_draft(self):
        self.ensure_one()
        if self.status not in ("cancelled",):
            raise UserError(_("Apenas parcelas canceladas podem ser redefinidas."))
        self.status = "draft"

    # ==================== Cron — Régua de Inadimplência ====================

    @api.model
    def action_cron_check_late_rents(self):
        """Cron diário: régua de inadimplência D+1, D+5, D+15, D+30."""
        today = date.today()

        # Marcar como atrasadas as parcelas abertas vencidas
        overdue = self.search([
            ("status", "in", ["open", "partial"]),
            ("due_date", "<", today),
        ])
        overdue.filtered(lambda r: r.status == "open").write({"status": "late"})

        # Régua sobre parcelas atrasadas
        late = self.search([("status", "=", "late")])
        for rent in late:
            days = (today - rent.due_date).days

            # D+1 — nota interna
            if days >= 1 and not rent.notified_d1:
                rent.message_post(
                    body=_("⚠️ Parcela vencida há %s dia(s). Vencimento: %s.") % (days, rent.due_date),
                    subtype_xmlid="mail.mt_note",
                )
                rent.notified_d1 = True

            # D+5 — e-mail ao locatário via template
            if days >= 5 and not rent.notified_d5:
                if rent.partner_id and rent.partner_id.email:
                    template = self.env.ref(
                        "property_core.email_template_parcela_atrasada",
                        raise_if_not_found=False,
                    )
                    if template:
                        try:
                            template.send_mail(rent.id, force_send=False)
                        except Exception:
                            rent.message_post(
                                body=_("Parcela vencida há %s dias. Por favor, regularize o pagamento.") % days,
                                partner_ids=[rent.partner_id.id],
                                subtype_xmlid="mail.mt_comment",
                            )
                rent.notified_d5 = True

            # D+15 — atividade urgente para responsável
            if days >= 15 and not rent.notified_d15:
                rent.activity_schedule(
                    "property_core.mail_activity_type_rent_overdue",
                    date_deadline=today,
                    summary=_("Cobrança urgente: aluguel %s dias em atraso") % days,
                    note=_("Locatário: %s | Imóvel: %s | Valor: %s") % (
                        rent.partner_id.name, rent.asset_id.name, rent.amount_due
                    ),
                    user_id=rent.contract_id.company_id.user_ids[:1].id if rent.contract_id.company_id.user_ids else False,
                )
                rent.notified_d15 = True

            # D+30 — contrato para Inadimplente
            if days >= 30 and not rent.notified_d30:
                if rent.contract_id.status not in ("defaulting", "closed"):
                    rent.contract_id.action_set_defaulting()
                rent.notified_d30 = True

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.rent") or "New"
                )
        return super().create(vals_list)