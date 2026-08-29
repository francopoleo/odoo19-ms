# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round
from datetime import date
import calendar
from dateutil.relativedelta import relativedelta


class PropertyRentLine(models.Model):
    _name = "property.rent.line"
    _description = "Composição da Parcela de Aluguel"
    _order = "rent_id, sequence, id"

    rent_id = fields.Many2one("property.rent", string="Parcela", required=True, ondelete="cascade", index=True)
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one(related="rent_id.company_id", store=True)
    currency_id = fields.Many2one(related="rent_id.currency_id", store=True)
    partner_id = fields.Many2one(related="rent_id.partner_id", store=True)
    contract_id = fields.Many2one(related="rent_id.contract_id", store=True)
    charge_type = fields.Selection([
        ("rent", "Aluguel"),
        ("prorata", "Pró-rata"),
        ("penalty", "Multa"),
        ("interest", "Juros de Mora"),
        ("discount", "Desconto"),
        ("condo", "Condomínio"),
        ("iptu", "IPTU"),
        ("other", "Outro"),
    ], string="Tipo", required=True, default="rent", index=True)
    name = fields.Char("Descrição", required=True)
    amount = fields.Monetary("Valor", currency_field="currency_id", required=True)
    account_id = fields.Many2one("account.account", string="Conta Contábil")
    origin = fields.Selection([
        ("auto", "Automático"),
        ("manual", "Manual"),
        ("adjustment", "Reajuste"),
    ], string="Origem", default="manual", required=True)
    calculation_base = fields.Monetary("Base de Cálculo", currency_field="currency_id")
    days = fields.Integer("Dias")
    calculation_note = fields.Text("Memória de Cálculo")

    @api.constrains("amount", "charge_type")
    def _check_amount_sign(self):
        for line in self:
            if line.charge_type == "discount" and line.amount > 0:
                raise ValidationError(_("Linhas de desconto devem ser gravadas com valor negativo."))
            if line.charge_type != "discount" and line.amount < 0:
                raise ValidationError(_("Somente linhas de desconto podem ter valor negativo."))


class PropertyRentPayment(models.Model):
    _name = "property.rent.payment"
    _description = "Recebimento de Parcela de Aluguel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "payment_date desc, id desc"

    name = fields.Char("Referência", readonly=True, copy=False, default="New")
    rent_id = fields.Many2one("property.rent", string="Parcela", required=True, ondelete="cascade", index=True)
    contract_id = fields.Many2one(related="rent_id.contract_id", store=True)
    asset_id = fields.Many2one(related="rent_id.asset_id", store=True)
    partner_id = fields.Many2one(related="rent_id.partner_id", store=True)
    company_id = fields.Many2one(related="rent_id.company_id", store=True)
    currency_id = fields.Many2one(related="rent_id.currency_id", store=True)
    payment_date = fields.Date("Data do Recebimento", required=True, default=fields.Date.today, tracking=True)
    amount = fields.Monetary("Valor Recebido", required=True, currency_field="currency_id", tracking=True)
    payment_method = fields.Selection([
        ("pix", "PIX"),
        ("transfer", "Transferência Bancária"),
        ("boleto", "Boleto"),
        ("cash", "Dinheiro"),
        ("check", "Cheque"),
    ], string="Forma de Pagamento", tracking=True)
    journal_id = fields.Many2one("account.journal", string="Diário", domain="[('company_id','=',company_id)]")
    account_move_id = fields.Many2one("account.move", string="Lançamento Contábil", readonly=True, copy=False)
    notes = fields.Text("Observações")
    state = fields.Selection([
        ("draft", "Rascunho"),
        ("posted", "Confirmado"),
        ("cancelled", "Cancelado"),
    ], string="Status", default="posted", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].sudo().next_by_code("property.rent.payment") or "REC-PGTO"
        return super().create(vals_list)

    def action_view_account_move(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Lançamento Contábil"),
            "res_model": "account.move",
            "res_id": self.account_move_id.id,
            "view_mode": "form",
        }


class PropertyContract(models.Model):
    _inherit = "property.contract"

    rent_due_day = fields.Integer(
        "Dia de Vencimento do Aluguel",
        default=5,
        tracking=True,
        help="Dia base para vencimento/ciclo das parcelas. Se o dia não existir no mês, usa o último dia do mês.",
    )
    late_fee_percent = fields.Float("Multa por Atraso (%)", default=2.0, digits=(6, 4), tracking=True)
    late_interest_percent_month = fields.Float("Juros de Mora ao Mês (%)", default=1.0, digits=(6, 4), tracking=True)
    late_grace_days = fields.Integer("Carência para Mora (dias)", default=0, tracking=True)
    penalty_account_id = fields.Many2one("account.account", string="Conta de Receita de Multa", domain="[('account_type','in',['income','income_other'])]")
    interest_account_id = fields.Many2one("account.account", string="Conta de Receita de Juros", domain="[('account_type','in',['income','income_other'])]")
    discount_account_id = fields.Many2one("account.account", string="Conta de Descontos Concedidos")

    @api.constrains("rent_due_day")
    def _check_rent_due_day(self):
        for contract in self:
            if contract.rent_due_day < 1 or contract.rent_due_day > 31:
                raise ValidationError(_("O dia de vencimento deve estar entre 1 e 31."))

    @api.onchange("rent_due_day")
    def _onchange_rent_due_day_warning(self):
        if self.rent_due_day in (29, 30, 31):
            return {
                "warning": {
                    "title": _("Atenção ao dia de vencimento"),
                    "message": _("Os dias 29, 30 e 31 podem não existir em todos os meses. O sistema usará automaticamente o último dia válido do mês."),
                }
            }

    def _safe_due_date(self, year, month, day):
        return date(year, month, min(day, calendar.monthrange(year, month)[1]))

    def _next_due_after(self, base_date):
        self.ensure_one()
        candidate = self._safe_due_date(base_date.year, base_date.month, self.rent_due_day or 5)
        if candidate <= base_date:
            next_month = base_date + relativedelta(months=1)
            candidate = self._safe_due_date(next_month.year, next_month.month, self.rent_due_day or 5)
        return candidate

    def _prorata_amount(self, period_start, period_end, cycle_start, cycle_end):
        self.ensure_one()
        days_charged = max((period_end - period_start).days + 1, 0)
        cycle_days = max((cycle_end - cycle_start).days + 1, 1)
        amount = (self.monthly_rent or 0.0) / cycle_days * days_charged
        return float_round(amount, precision_rounding=self.currency_id.rounding), days_charged, cycle_days

    def action_generate_rents(self):
        """Gera parcelas com ciclo configurável, pró-rata inicial/final e memória de cálculo."""
        self.ensure_one()
        if not self.start_date or not self.end_date:
            return
        self.rent_ids.filtered(lambda r: r.status == "draft").unlink()
        today = date.today()

        Rent = self.env["property.rent"]
        current_start = self.start_date
        first_due = self._next_due_after(self.start_date)
        previous_due = first_due - relativedelta(months=1)
        first_period_end = min(first_due - relativedelta(days=1), self.end_date)

        vals_list = []
        while current_start <= self.end_date:
            if current_start == self.start_date and current_start != previous_due:
                period_start = current_start
                period_end = first_period_end
                due_date = first_due
                cycle_start = previous_due
                cycle_end = first_due - relativedelta(days=1)
            else:
                due_date = current_start
                next_due = self._next_due_after(due_date)
                period_start = due_date
                period_end = min(next_due - relativedelta(days=1), self.end_date)
                cycle_start = due_date
                cycle_end = next_due - relativedelta(days=1)

            is_prorata = period_start != cycle_start or period_end != cycle_end
            if is_prorata:
                amount, days_charged, cycle_days = self._prorata_amount(period_start, period_end, cycle_start, cycle_end)
                rent_type = "prorata_initial" if period_start == self.start_date else "prorata_final"
                note = _("Pró-rata: %(days)s dias cobrados de %(cycle)s dias do ciclo. Período: %(start)s a %(end)s.") % {
                    "days": days_charged,
                    "cycle": cycle_days,
                    "start": period_start,
                    "end": period_end,
                }
            else:
                amount = self.monthly_rent
                days_charged = (period_end - period_start).days + 1
                cycle_days = days_charged
                rent_type = "normal"
                note = _("Parcela mensal cheia. Período: %(start)s a %(end)s.") % {"start": period_start, "end": period_end}

            vals_list.append({
                "contract_id": self.id,
                "due_date": due_date,
                "period_start": period_start,
                "period_end": period_end,
                "rent_type": rent_type,
                "days_charged": days_charged,
                "cycle_days": cycle_days,
                "calculation_note": note,
                "competence_month": period_start.month,
                "competence_year": period_start.year,
                "amount": amount,
                "status": "late" if due_date < today else "open",
            })

            if period_end >= self.end_date:
                break
            current_start = period_end + relativedelta(days=1)

        total = len(vals_list)
        for seq, vals in enumerate(vals_list, start=1):
            vals["installment_ref"] = f"{seq:02d}/{total:02d}"
        Rent.create(vals_list)


class PropertyRent(models.Model):
    _inherit = "property.rent"

    period_start = fields.Date("Início do Período", tracking=True)
    period_end = fields.Date("Fim do Período", tracking=True)
    rent_type = fields.Selection([
        ("normal", "Normal"),
        ("prorata_initial", "Pró-rata Inicial"),
        ("prorata_final", "Pró-rata Final"),
        ("manual", "Manual"),
    ], string="Tipo de Parcela", default="normal", tracking=True)
    days_charged = fields.Integer("Dias Cobrados")
    cycle_days = fields.Integer("Dias do Ciclo")
    calculation_note = fields.Text("Memória de Cálculo")
    installment_ref = fields.Char("Parcela", readonly=True, copy=False, help="Referência sequencial: 01/37, 02/37...")
    line_ids = fields.One2many("property.rent.line", "rent_id", string="Composição da Parcela")
    payment_ids = fields.One2many("property.rent.payment", "rent_id", string="Recebimentos")
    payment_count = fields.Integer("Qtd. Recebimentos", compute="_compute_payment_count")
    amount_rent = fields.Monetary("Aluguel/Pró-rata", currency_field="currency_id", compute="_compute_enterprise_totals", store=True)
    amount_penalty = fields.Monetary("Multa Calculada", currency_field="currency_id", compute="_compute_enterprise_totals", store=True)
    amount_interest = fields.Monetary("Juros Calculados", currency_field="currency_id", compute="_compute_enterprise_totals", store=True)
    amount_discount = fields.Monetary("Descontos", currency_field="currency_id", compute="_compute_enterprise_totals", store=True)
    residual_amount = fields.Monetary("Saldo em Aberto", currency_field="currency_id", compute="_compute_enterprise_totals", store=True)
    last_charge_calculation_date = fields.Date("Último Cálculo de Encargos", readonly=True)

    @api.depends("payment_ids.state")
    def _compute_payment_count(self):
        for rent in self:
            rent.payment_count = len(rent.payment_ids.filtered(lambda p: p.state == "posted"))

    @api.depends("line_ids.amount", "line_ids.charge_type", "payment_ids.amount", "payment_ids.state", "amount")
    def _compute_enterprise_totals(self):
        for rent in self:
            positive_lines = rent.line_ids.filtered(lambda l: l.charge_type != "discount")
            discount_lines = rent.line_ids.filtered(lambda l: l.charge_type == "discount")
            rent.amount_rent = sum(positive_lines.filtered(lambda l: l.charge_type in ("rent", "prorata")).mapped("amount")) or rent.amount
            rent.amount_penalty = sum(positive_lines.filtered(lambda l: l.charge_type == "penalty").mapped("amount"))
            rent.amount_interest = sum(positive_lines.filtered(lambda l: l.charge_type == "interest").mapped("amount"))
            rent.amount_discount = abs(sum(discount_lines.mapped("amount")))
            total_due = sum(positive_lines.mapped("amount")) + sum(discount_lines.mapped("amount"))
            if not rent.line_ids:
                total_due = rent.amount - rent.discount + rent.fine + rent.interest
            total_paid = sum(rent.payment_ids.filtered(lambda p: p.state == "posted").mapped("amount"))
            rent.residual_amount = max(total_due - total_paid, 0.0)

    @api.depends("amount", "discount", "fine", "interest", "line_ids.amount", "line_ids.charge_type")
    def _compute_amount_due(self):
        for rent in self:
            if rent.line_ids:
                rent.amount_due = sum(rent.line_ids.mapped("amount"))
            else:
                rent.amount_due = rent.amount - rent.discount + rent.fine + rent.interest

    def _ensure_base_rent_line(self):
        for rent in self:
            if rent.line_ids.filtered(lambda l: l.charge_type in ("rent", "prorata") and l.origin == "auto"):
                continue
            charge_type = "prorata" if rent.rent_type in ("prorata_initial", "prorata_final") else "rent"
            self.env["property.rent.line"].create({
                "rent_id": rent.id,
                "sequence": 10,
                "charge_type": charge_type,
                "name": _("Aluguel") if charge_type == "rent" else _("Aluguel pró-rata"),
                "amount": rent.amount,
                "origin": "auto",
                "calculation_base": rent.contract_id.monthly_rent,
                "days": rent.days_charged,
                "calculation_note": rent.calculation_note,
            })

    def _get_config_account(self, key):
        value = self.env["ir.config_parameter"].sudo().get_param(key, 0)
        return self.env["account.account"].browse(int(value)) if value else self.env["account.account"]

    def _get_account_for_charge(self, charge_type):
        self.ensure_one()
        contract = self.contract_id
        if charge_type in ("rent", "prorata", "condo", "iptu", "other"):
            return contract.income_account_id or self._get_config_account("property_core.rent_income_account_id")
        if charge_type == "penalty":
            return contract.penalty_account_id or self._get_config_account("property_core.rent_penalty_account_id") or contract.income_account_id or self._get_config_account("property_core.rent_income_account_id")
        if charge_type == "interest":
            return contract.interest_account_id or self._get_config_account("property_core.rent_interest_account_id") or contract.income_account_id or self._get_config_account("property_core.rent_income_account_id")
        if charge_type == "discount":
            return contract.discount_account_id or self._get_config_account("property_core.rent_discount_account_id")
        return contract.income_account_id or self._get_config_account("property_core.rent_income_account_id")

    def _calculate_late_charges(self, payment_date=None):
        for rent in self:
            rent._ensure_base_rent_line()
            calc_date = payment_date or fields.Date.today()
            if isinstance(calc_date, str):
                calc_date = fields.Date.from_string(calc_date)

            grace_days = rent.contract_id.late_grace_days or 0
            days_late = 0
            if rent.due_date and calc_date > rent.due_date:
                days_late = max((calc_date - rent.due_date).days - grace_days, 0)

            rent.line_ids.filtered(lambda l: l.origin == "auto" and l.charge_type in ("penalty", "interest")).unlink()
            rent.fine = 0.0
            rent.interest = 0.0
            if days_late <= 0:
                rent.last_charge_calculation_date = calc_date
                continue

            base_amount = sum(rent.line_ids.filtered(lambda l: l.charge_type in ("rent", "prorata", "condo", "iptu", "other")).mapped("amount")) or rent.amount
            penalty = float_round(base_amount * (rent.contract_id.late_fee_percent or 0.0) / 100.0, precision_rounding=rent.currency_id.rounding)
            interest = float_round(base_amount * ((rent.contract_id.late_interest_percent_month or 0.0) / 100.0) / 30.0 * days_late, precision_rounding=rent.currency_id.rounding)

            vals_to_create = []
            if penalty:
                vals_to_create.append({
                    "rent_id": rent.id,
                    "sequence": 80,
                    "charge_type": "penalty",
                    "name": _("Multa por atraso (%s%%)") % (rent.contract_id.late_fee_percent or 0.0),
                    "amount": penalty,
                    "origin": "auto",
                    "calculation_base": base_amount,
                    "days": days_late,
                    "calculation_note": _("Multa calculada sobre R$ %.2f após %s dia(s) de atraso.") % (base_amount, days_late),
                })
            if interest:
                vals_to_create.append({
                    "rent_id": rent.id,
                    "sequence": 90,
                    "charge_type": "interest",
                    "name": _("Juros de mora (%s%% ao mês)") % (rent.contract_id.late_interest_percent_month or 0.0),
                    "amount": interest,
                    "origin": "auto",
                    "calculation_base": base_amount,
                    "days": days_late,
                    "calculation_note": _("Juros de mora: R$ %.2f x %.4f%%/30 x %s dia(s).") % (base_amount, rent.contract_id.late_interest_percent_month or 0.0, days_late),
                })
            if vals_to_create:
                self.env["property.rent.line"].create(vals_to_create)
            rent.fine = penalty
            rent.interest = interest
            rent.last_charge_calculation_date = calc_date

    def action_recalculate_late_charges(self):
        for rent in self:
            rent._calculate_late_charges(fields.Date.today())
            rent.message_post(body=_("Encargos recalculados em %s.") % fields.Date.today())

    def action_open(self):
        res = super().action_open()
        self._ensure_base_rent_line()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        rents = super().create(vals_list)
        rents._ensure_base_rent_line()
        return rents

    def action_view_payments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Recebimentos"),
            "res_model": "property.rent.payment",
            "view_mode": "list,form",
            "domain": [("rent_id", "=", self.id)],
            "context": {"default_rent_id": self.id},
        }

    def action_register_payment(self):
        self.ensure_one()
        if self.status not in ("open", "late", "partial"):
            raise UserError(_("Esta parcela não está disponível para pagamento."))
        if not self.amount_paid:
            raise UserError(_("Informe o valor pago antes de confirmar."))
        if not self.payment_date:
            self.payment_date = fields.Date.today()

        self._calculate_late_charges(self.payment_date)
        payment = self.env["property.rent.payment"].create({
            "rent_id": self.id,
            "payment_date": self.payment_date,
            "amount": self.amount_paid,
            "payment_method": self.payment_method,
            "notes": self.payment_notes,
            "journal_id": self.contract_id.journal_id.id if self.contract_id.journal_id else False,
            "state": "posted",
        })
        self._create_accounting_entry(payment=payment)

        total_paid = sum(self.payment_ids.filtered(lambda p: p.state == "posted").mapped("amount"))
        if total_paid >= self.amount_due:
            self.status = "paid"
            self._issue_rent_receipt()
            self.message_post(body=_("Pagamento total confirmado: R$ %.2f. Recibo %s emitido.") % (total_paid, self.receipt_number or "-"))
            try:
                return self.action_print_receipt()
            except Exception as e:
                _logger.warning("Pagamento registrado com sucesso, mas falha ao gerar PDF do recibo: %s", e)
                return False

        self.status = "partial"
        self.message_post(body=_("Pagamento parcial registrado: R$ %.2f de R$ %.2f.") % (total_paid, self.amount_due))

    def _prepare_credit_lines_for_payment(self, amount_to_allocate):
        self.ensure_one()
        lines = []
        remaining = amount_to_allocate
        charge_order = ["penalty", "interest", "rent", "prorata", "condo", "iptu", "other"]
        for charge_type in charge_order:
            for line in self.line_ids.filtered(lambda l: l.charge_type == charge_type and l.amount > 0):
                if remaining <= 0:
                    break
                amount = min(line.amount, remaining)
                account = line.account_id or self._get_account_for_charge(charge_type)
                if not account:
                    raise UserError(_("Configure a conta contábil para '%s'.") % line.name)
                lines.append((line.name, account, amount))
                remaining -= amount
        return lines

    def _create_accounting_entry(self, payment=None):
        self.ensure_one()
        self._ensure_base_rent_line()
        contract = self.contract_id
        params = self.env["ir.config_parameter"].sudo()
        journal = (payment and payment.journal_id) or contract.journal_id
        if not journal:
            jid = int(params.get_param("property_core.rent_journal_id", 0))
            journal = self.env["account.journal"].browse(jid) if jid else self.env["account.journal"]

        if not journal or not journal.default_account_id:
            raise UserError(_("Configure um diário de recebimento com conta padrão para aluguéis."))

        amount_received = payment.amount if payment else self.amount_paid
        if amount_received <= 0:
            raise UserError(_("O valor recebido deve ser maior que zero."))

        move_lines = [(0, 0, {
            "account_id": journal.default_account_id.id,
            "name": payment.name if payment else self.name,
            "debit": amount_received,
            "credit": 0.0,
            "partner_id": self.partner_id.id if self.partner_id else False,
        })]

        discount_total = abs(sum(self.line_ids.filtered(lambda l: l.charge_type == "discount").mapped("amount")))
        if discount_total:
            discount_account = self._get_account_for_charge("discount")
            if not discount_account:
                raise UserError(_("Configure a conta de descontos concedidos."))
            move_lines.append((0, 0, {
                "account_id": discount_account.id,
                "name": _("Desconto concedido - %s") % self.name,
                "debit": discount_total,
                "credit": 0.0,
                "partner_id": self.partner_id.id if self.partner_id else False,
            }))

        amount_to_credit = amount_received + discount_total
        for name, account, amount in self._prepare_credit_lines_for_payment(amount_to_credit):
            move_lines.append((0, 0, {
                "account_id": account.id,
                "name": name,
                "debit": 0.0,
                "credit": amount,
                "partner_id": self.partner_id.id if self.partner_id else False,
            }))

        debit_total = sum(line[2].get("debit", 0.0) for line in move_lines)
        credit_total = sum(line[2].get("credit", 0.0) for line in move_lines)
        diff = float_round(debit_total - credit_total, precision_rounding=self.currency_id.rounding)
        if diff:
            for line in reversed(move_lines):
                if line[2].get("credit"):
                    line[2]["credit"] += diff
                    break

        move = self.env["account.move"].create({
            "move_type": "entry",
            "journal_id": journal.id,
            "date": (payment.payment_date if payment else self.payment_date) or fields.Date.today(),
            "ref": (payment.name if payment else self.reference),
            "narration": _("Recebimento de aluguel – %s") % self.name,
            "line_ids": move_lines,
        })
        move.action_post()
        if payment:
            payment.account_move_id = move.id
        self.account_move_id = move.id


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    property_rent_penalty_account_id = fields.Many2one(
        "account.account",
        string="Conta de Receita de Multa por Atraso",
        config_parameter="property_core.rent_penalty_account_id",
        domain="[('account_type','in',['income','income_other'])]",
    )
    property_rent_interest_account_id = fields.Many2one(
        "account.account",
        string="Conta de Receita de Juros de Mora",
        config_parameter="property_core.rent_interest_account_id",
        domain="[('account_type','in',['income','income_other'])]",
    )
    property_rent_discount_account_id = fields.Many2one(
        "account.account",
        string="Conta de Descontos Concedidos",
        config_parameter="property_core.rent_discount_account_id",
    )
