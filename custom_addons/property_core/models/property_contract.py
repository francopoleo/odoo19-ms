from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PropertyContract(models.Model):
    _name = "property.contract"
    _description = "Contrato de Locação"
    _inherit = ["mail.thread", "mail.activity.mixin", "common.mixin"]
    _order = "start_date desc"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Nome do Contrato", required=True, tracking=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")
    original_filename = fields.Char(
        "Nome do Arquivo Original",
        readonly=True,
        copy=False,
        help="Nome do arquivo de onde foi extraído este contrato (via OCR)"
    )

    contract_type = fields.Selection([
        ("residential", "Residencial"),
        ("commercial", "Comercial"),
        ("comodato", "Comodato"),
        ("arrendamento", "Arrendamento"),
    ], string="Tipo de Contrato", default="residential", tracking=True, required=True)

    # ==================== Partes ====================
    asset_id = fields.Many2one(
        "property.asset", required=True, string="Imóvel",
        tracking=True, ondelete="restrict"
    )
    partner_id = fields.Many2one(
        "res.partner", required=True, string="Locatário",
        tracking=True,
        domain=[("category_id.name", "ilike", "Inquilino")],
        help="Contato mestre do locatário.",
    )
    broker_id = fields.Many2one(
        "res.partner", string="Corretor da Locação",
        tracking=True,
        domain=[("category_id.name", "ilike", "Corretor")],
        help="Corretor responsável por esta locação"
    )
    assignment_id = fields.Many2one(
        "property.broker.assignment", string="Mandato",
        tracking=True, help="Mandato que originou este contrato"
    )
    commission_id = fields.Many2one(
        "property.commission", string="Comissão",
        readonly=True, copy=False
    )

    guarantor_ids = fields.Many2many(
        "res.partner",
        relation="property_contract_guarantor_rel",
        column1="contract_id",
        column2="partner_id",
        string="Fiadores",
    )

    asset_link_count = fields.Integer("Qtd. Imóveis", compute="_compute_relation_button_counts")
    tenant_profile_count = fields.Integer("Qtd. Perfis do Locatário", compute="_compute_relation_button_counts")
    broker_link_count = fields.Integer("Qtd. Corretores", compute="_compute_relation_button_counts")
    assignment_link_count = fields.Integer("Qtd. Mandatos", compute="_compute_relation_button_counts")

    # ==================== Datas ====================
    sign_date = fields.Date("Data de Assinatura", default=fields.Date.today)
    start_date = fields.Date("Início", required=True, tracking=True)
    end_date = fields.Date("Fim", required=True, tracking=True)
    duration_months = fields.Integer(
        "Duração (meses)", compute="_compute_duration", store=True
    )

    # ==================== Financeiro ====================
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    monthly_rent = fields.Monetary(
        "Aluguel Mensal", currency_field="currency_id",
        tracking=True, required=True
    )
    deposit_value = fields.Monetary(
        "Caução", currency_field="currency_id",
        help="Valor do depósito caução"
    )
    total_value = fields.Monetary(
        "Valor Total do Contrato", currency_field="currency_id",
        compute="_compute_total_value", store=True
    )

    # ==================== Contabilidade ====================
    journal_id = fields.Many2one(
        "account.journal",
        string="Diário Contábil",
        domain="[('company_id','=',company_id)]",
        help="Diário usado para os lançamentos de recebimento deste contrato. Se vazio, usa o padrão configurado na empresa.",
    )
    income_account_id = fields.Many2one(
        "account.account",
        string="Conta de Receita",
        domain="[('account_type','in',['income','income_other'])]",
        help="Conta contábil de receita deste contrato. Se vazia, usa o padrão configurado nas Configurações.",
    )

    # ==================== Reajuste ====================
    adjustment_index = fields.Selection([
        ("none", "Sem Reajuste"),
        ("igpm", "IGP-M"),
        ("ipca", "IPCA"),
        ("incc", "INCC"),
        ("fixed", "Percentual Fixo"),
    ], string="Índice de Reajuste", default="none")
    adjustment_rate = fields.Float(
        "Taxa Fixa (%)", digits=(5, 2),
        help="Usado quando índice = Percentual Fixo"
    )
    adjustment_period_months = fields.Integer(
        "Período de Reajuste (meses)", default=12
    )
    last_adjustment_date = fields.Date(
        "Último Reajuste Aplicado",
        help="Atualizado automaticamente ao aplicar cada reajuste. Define a base para o cálculo do próximo reajuste."
    )
    next_adjustment_date = fields.Date(
        "Próximo Reajuste", compute="_compute_next_adjustment", store=True
    )

    # ==================== Status e Alertas ====================
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("active", "Ativo"),
        ("expiring", "A Vencer"),
        ("renewing", "Em Renovação"),
        ("late", "Atrasado/Vencido"),
        ("defaulting", "Inadimplente"),
        ("closed", "Encerrado"),
    ], default="draft", tracking=True, required=True)

    alert_days = fields.Integer(
        "Alertar (dias antes do vencimento)", default=60,
        help="Quantos dias antes do vencimento gerar alerta"
    )
    days_to_expiry = fields.Integer("Dias para Vencer", compute="_compute_expiry_info")
    months_active = fields.Integer("Meses Ativos", compute="_compute_expiry_info")
    is_expiring = fields.Boolean("A Vencer", compute="_compute_is_expiring", store=True)

    # ==================== Parcelas ====================
    rent_ids = fields.One2many("property.rent", "contract_id", string="Parcelas")
    rent_count = fields.Integer("Total Parcelas", compute="_compute_rent_stats", store=True)
    rent_open_count = fields.Integer("Parcelas em Aberto", compute="_compute_rent_stats", store=True)
    rent_late_count = fields.Integer("Parcelas Atrasadas", compute="_compute_rent_stats", store=True)
    total_received = fields.Monetary("Total Recebido", currency_field="currency_id", compute="_compute_rent_stats", store=True)
    total_pending = fields.Monetary("Total Pendente", currency_field="currency_id", compute="_compute_rent_stats", store=True)

    # ==================== Reajustes ====================
    adjustment_ids = fields.One2many("property.rent.adjustment", "contract_id", string="Reajustes")
    adjustment_count = fields.Integer("Qtd. Reajustes", compute="_compute_adjustment_count")

    # ==================== Assinatura e Foro ====================
    jurisdiction = fields.Char(
        "Foro de Eleição",
        default="Barueri",
        help="Comarca eleita para dirimir questões do contrato"
    )
    witness_ids = fields.Many2many(
        "res.partner",
        relation="property_contract_witness_rel",
        column1="contract_id",
        column2="partner_id",
        string="Testemunhas",
    )
    additional_clauses = fields.Html(
        "Cláusulas Adicionais",
        help="Cláusulas extras a serem inseridas no contrato"
    )

    # ==================== Fase 4 ====================
    inspection_count = fields.Integer("Vistorias", compute="_compute_phase4_counts")
    maintenance_count = fields.Integer("Manutenções", compute="_compute_phase4_counts")

    @api.model
    def _auto_init(self):
        """Compatibiliza tabela legado de tags com o esquema derivado do common.mixin no Odoo 19."""
        cr = self.env.cr
        cr.execute(
            """
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'common_tag_property_contract_rel'
            """
        )
        if cr.fetchone():
            cr.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'common_tag_property_contract_rel'
                """
            )
            cols = {r[0] for r in cr.fetchall()}
            if 'contract_id' in cols and 'property_contract_id' not in cols:
                cr.execute('ALTER TABLE common_tag_property_contract_rel RENAME COLUMN contract_id TO property_contract_id')
            if 'tag_id' in cols and 'common_tag_id' not in cols:
                cr.execute('ALTER TABLE common_tag_property_contract_rel RENAME COLUMN tag_id TO common_tag_id')
        return super()._auto_init()

    @api.depends("asset_id", "broker_id", "assignment_id")
    def _compute_relation_button_counts(self):
        for contract in self:
            contract.asset_link_count = 1 if contract.asset_id else 0
            contract.broker_link_count = 1 if contract.broker_id else 0
            contract.assignment_link_count = 1 if contract.assignment_id else 0

    def action_open_asset(self):
        self.ensure_one()
        if not self.asset_id:
            return False
        return {
            "type": "ir.actions.act_window",
            "res_model": "property.asset",
            "res_id": self.asset_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_open_broker(self):
        self.ensure_one()
        if not self.broker_id:
            return False
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "res_id": self.broker_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_open_assignment(self):
        self.ensure_one()
        if not self.assignment_id:
            return False
        return {
            "type": "ir.actions.act_window",
            "res_model": "property.broker.assignment",
            "res_id": self.assignment_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def _compute_adjustment_count(self):
        Adj = self.env["property.rent.adjustment"]
        for contract in self:
            contract.adjustment_count = Adj.search_count([("contract_id", "=", contract.id)])

    def action_view_adjustments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Reajustes",
            "res_model": "property.rent.adjustment",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {
                "default_contract_id": self.id,
                "default_previous_rent": self.monthly_rent,
            },
        }

    @api.depends("rent_ids", "rent_ids.status", "rent_ids.amount_paid", "rent_ids.amount_due")
    def _compute_rent_stats(self):
        for contract in self:
            rents = contract.rent_ids
            contract.rent_count = len(rents)
            contract.rent_open_count = len(rents.filtered(lambda r: r.status in ("open", "partial")))
            contract.rent_late_count = len(rents.filtered(lambda r: r.status == "late"))
            contract.total_received = sum(rents.filtered(lambda r: r.status == "paid").mapped("amount_paid"))
            contract.total_pending = sum(
                rents.filtered(lambda r: r.status in ("open", "late", "partial")).mapped("amount_due")
            )

    def action_view_rents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Parcelas",
            "res_model": "property.rent",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id},
        }

    def action_generate_rents(self):
        """Gera parcelas mensais para todo o período do contrato."""
        self.ensure_one()
        if not self.start_date or not self.end_date:
            return
        self.rent_ids.filtered(lambda r: r.status == "draft").unlink()

        current = self.start_date
        end = self.end_date
        Rent = self.env["property.rent"]
        while current <= end:
            due = current.replace(day=5) if current.day < 5 else current + relativedelta(months=1, day=5)
            Rent.create({
                "contract_id": self.id,
                "due_date": due,
                "competence_month": current.month,
                "competence_year": current.year,
                "amount": self.monthly_rent,
                "status": "open",
            })
            current = current + relativedelta(months=1)


    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for contract in self:
            if contract.start_date and contract.end_date:
                delta = relativedelta(contract.end_date + relativedelta(days=1), contract.start_date)
                contract.duration_months = delta.years * 12 + delta.months
            else:
                contract.duration_months = 0

    @api.depends("start_date", "end_date", "monthly_rent")
    def _compute_total_value(self):
        for contract in self:
            contract.total_value = contract.monthly_rent * contract.duration_months

    @api.depends("start_date", "last_adjustment_date", "adjustment_period_months")
    def _compute_next_adjustment(self):
        for contract in self:
            base = contract.last_adjustment_date or contract.start_date
            if base and contract.adjustment_period_months > 0:
                contract.next_adjustment_date = base + relativedelta(months=contract.adjustment_period_months)
            else:
                contract.next_adjustment_date = False

    @api.depends("end_date", "start_date", "status", "alert_days")
    def _compute_expiry_info(self):
        today = date.today()
        for contract in self:
            if contract.end_date and contract.status in ("active", "expiring", "renewing"):
                contract.days_to_expiry = (contract.end_date - today).days
            else:
                contract.days_to_expiry = 0

            if contract.start_date and contract.status in ("active", "expiring", "renewing", "defaulting"):
                delta = relativedelta(today, contract.start_date)
                contract.months_active = delta.years * 12 + delta.months
            else:
                contract.months_active = 0

    @api.depends("end_date", "status", "alert_days")
    def _compute_is_expiring(self):
        today = date.today()
        for contract in self:
            if contract.end_date and contract.status in ("active", "expiring", "renewing"):
                days = (contract.end_date - today).days
                contract.is_expiring = 0 <= days <= (contract.alert_days or 60)
            else:
                contract.is_expiring = False

    @api.onchange("asset_id")
    def _onchange_asset_id(self):
        if self.asset_id and self.asset_id.rental_value and not self.monthly_rent:
            self.monthly_rent = self.asset_id.rental_value

    @api.onchange("assignment_id")
    def _onchange_assignment_id(self):
        if self.assignment_id:
            self.broker_id = self.assignment_id.broker_id

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for contract in self:
            if contract.start_date and contract.end_date and contract.end_date <= contract.start_date:
                raise ValidationError(_("A data de fim deve ser posterior à data de início."))

    @api.constrains("monthly_rent", "deposit_value")
    def _check_values(self):
        for contract in self:
            if contract.monthly_rent < 0:
                raise ValidationError(_("O aluguel mensal não pode ser negativo."))
            if contract.deposit_value < 0:
                raise ValidationError(_("O valor da caução não pode ser negativo."))

    def action_activate(self):
        self.ensure_one()
        self.status = "active"
        self.asset_id.status = "rented"
        self.action_generate_rents()

        if self.broker_id and not self.commission_id:
            commission = self.env["property.commission"].create({
                "broker_id": self.broker_id.id,
                "contract_id": self.id,
                "commission_type": "rental",
                "base_value": self.total_value,
                "commission_rate": self.broker_id.commission_rate,
                "deal_date": date.today(),
            })
            self.commission_id = commission.id
            if self.assignment_id and not self.assignment_id.commission_id:
                self.assignment_id.commission_id = commission.id
                self.assignment_id.contract_id = self.id

        self.message_post(body=_("Contrato ativado em %s. Parcelas geradas automaticamente.") % date.today())

    def action_set_renewing(self):
        self.ensure_one()
        self.status = "renewing"
        self.message_post(body=_("Contrato em processo de renovação desde %s.") % date.today())

    def action_set_defaulting(self):
        self.ensure_one()
        self.status = "defaulting"
        self.message_post(body=_("Contrato marcado como Inadimplente em %s.") % date.today())

    def action_set_late(self):
        self.ensure_one()
        self.status = "late"
        self.message_post(body=_("Contrato marcado como Atrasado/Vencido em %s.") % date.today())

    def action_close(self):
        self.ensure_one()
        self.status = "closed"
        other_active = self.asset_id.contract_ids.filtered(lambda c: c.status == "active" and c.id != self.id)
        if not other_active:
            self.asset_id.status = "available"
        self.message_post(body=_("Contrato encerrado em %s.") % date.today())

    def action_view_commission(self):
        self.ensure_one()
        if not self.commission_id:
            return False
        return {
            "type": "ir.actions.act_window",
            "name": "Comissão",
            "res_model": "property.commission",
            "res_id": self.commission_id.id,
            "view_mode": "form",
        }

    def action_print_contract(self):
        self.ensure_one()
        return self.env.ref("property_core.action_report_property_contract").report_action(self)

    @api.model
    def action_cron_check_late(self):
        today = date.today()

        late = self.search([
            ("status", "in", ["active", "expiring"]),
            ("end_date", "<", today),
        ])
        for contract in late:
            contract.status = "late"
            contract.message_post(body=_("Contrato vencido automaticamente em %s.") % today)

        template = self.env.ref("property_core.email_template_contrato_vencendo", raise_if_not_found=False)
        active = self.search([("status", "=", "active")])
        for contract in active:
            if contract.end_date and contract.is_expiring:
                contract.status = "expiring"
                contract.message_post(body=_("Contrato vence em %s dias (%s).") % (contract.days_to_expiry, contract.end_date))
                already = contract.activity_ids.filtered(lambda a: "vence" in (a.summary or "").lower())
                if not already:
                    contract.activity_schedule(
                        "property_core.mail_activity_type_contract_expiry",
                        date_deadline=contract.end_date,
                        summary=_("Contrato vence em %s dias — %s") % (contract.days_to_expiry, contract.partner_id.name),
                        note=_("O contrato '%s' com '%s' vence em %s. Avalie renovação ou encerramento.") % (
                            contract.name, contract.partner_id.name, contract.end_date
                        ),
                        user_id=contract.create_uid.id,
                    )
                if template and contract.partner_id and contract.partner_id.email:
                    try:
                        template.send_mail(contract.id, force_send=False)
                    except Exception:
                        pass

    @api.model
    def action_cron_check_adjustment_due(self):
        today = date.today()
        index_map = {
            "igpm": "igpm",
            "ipca": "ipca",
            "incc": "inpc",
            "fixed": "fixed",
        }
        contracts = self.search([
            ("status", "in", ["active", "expiring"]),
            ("adjustment_index", "!=", "none"),
            ("next_adjustment_date", "<=", today),
        ])
        Adj = self.env["property.rent.adjustment"]
        for contract in contracts:
            pending = Adj.search([("contract_id", "=", contract.id), ("status", "=", "draft")], limit=1)
            if pending:
                continue
            index_type = index_map.get(contract.adjustment_index, "igpm")
            adj = Adj.create({
                "contract_id": contract.id,
                "index_type": index_type,
                "period_months": contract.adjustment_period_months or 12,
                "adjustment_date": contract.next_adjustment_date,
                "effective_date": contract.next_adjustment_date,
                "previous_rent": contract.monthly_rent,
            })
            if index_type in ("igpm", "ipca", "inpc") and adj.index_id:
                try:
                    adj.action_fetch_rate()
                except Exception:
                    pass
            already = contract.activity_ids.filtered(lambda a: "reajuste" in (a.summary or "").lower())
            if not already:
                contract.activity_schedule(
                    "property_core.mail_activity_type_rent_adjustment",
                    date_deadline=contract.next_adjustment_date,
                    summary=_("Reajuste pendente — %s") % contract.partner_id.name,
                    note=_("Reajuste automático criado (ref: %s). Acesse Reajustes para revisar e aplicar.") % adj.reference,
                    user_id=contract.create_uid.id,
                )

    def _compute_phase4_counts(self):
        Insp = self.env["property.inspection"]
        Maint = self.env["property.maintenance"]
        for contract in self:
            contract.inspection_count = Insp.search_count([("contract_id", "=", contract.id)])
            contract.maintenance_count = Maint.search_count([("contract_id", "=", contract.id)])

    def action_view_inspections(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Vistorias",
            "res_model": "property.inspection",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id, "default_asset_id": self.asset_id.id},
        }

    def action_view_maintenance(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Manutenções",
            "res_model": "property.maintenance",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id, "default_asset_id": self.asset_id.id},
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = self.env["common.sequence"].sudo().next_by_code("property.contract") or "New"
        return super().create(vals_list)
