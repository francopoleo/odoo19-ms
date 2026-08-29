# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PropertyContract(models.Model):
    _inherit = "property.contract"

    # Campos de compatibilidade com diferentes versões do property_core.
    # Algumas views empresariais do property_core usam esses campos; se o modelo
    # base ainda não os tiver, este módulo os fornece para evitar erro de view.
    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        default=lambda self: self.env.company,
        index=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Moeda",
        default=lambda self: self.env.company.currency_id,
    )
    issuer = fields.Char(
        string="Emitido por",
        help="Compatibilidade para views de contrato que exibem o emissor do instrumento/documento.",
    )

    original_partner_id = fields.Many2one("res.partner", string="Locatário Original")
    current_partner_id = fields.Many2one("res.partner", string="Locatário Atual")

    original_monthly_rent = fields.Monetary(string="Aluguel Original", currency_field="currency_id")
    current_base_rent = fields.Monetary(string="Aluguel Base Atual", currency_field="currency_id")
    current_effective_rent = fields.Monetary(string="Aluguel Efetivo Atual", currency_field="currency_id", compute="_compute_current_financials", store=True)
    current_discount_amount = fields.Monetary(string="Desconto Atual", currency_field="currency_id", compute="_compute_current_financials", store=True)
    current_extra_charge_amount = fields.Monetary(string="Acréscimos Atuais", currency_field="currency_id", compute="_compute_current_financials", store=True)
    current_discount_until = fields.Date(string="Desconto Até")

    current_start_date = fields.Date(string="Início Vigente")
    current_end_date = fields.Date(string="Fim Vigente")
    current_guarantee_type = fields.Char(string="Garantia Vigente")
    current_adjustment_index = fields.Selection([
        ("none", "Sem reajuste"),
        ("igpm", "IGP-M"),
        ("ipca", "IPCA"),
        ("incc", "INCC"),
        ("fixed", "Fixo"),
        ("other", "Outro"),
    ], string="Índice Vigente")
    current_payment_day = fields.Integer(string="Dia de Vencimento Vigente")
    current_purpose = fields.Char(string="Finalidade Vigente")
    current_jurisdiction = fields.Char(string="Foro Vigente")
    consolidated_terms_html = fields.Html(string="Termos Consolidados")

    legal_status = fields.Selection([
        ("draft", "Rascunho"),
        ("under_review", "Em revisão"),
        ("signed", "Assinado"),
        ("amended", "Aditado"),
        ("terminated", "Encerrado"),
        ("expired", "Expirado"),
        ("cancelled", "Cancelado"),
    ], string="Status Jurídico", default="draft")

    operational_status = fields.Selection([
        ("pending_start", "Aguardando início"),
        ("active", "Ativo"),
        ("suspended", "Suspenso"),
        ("ending_soon", "Próximo do fim"),
        ("ended", "Encerrado"),
        ("cancelled", "Cancelado"),
    ], string="Status Operacional", default="pending_start")

    amendment_ids = fields.One2many("property.contract.amendment", "contract_id", string="Aditivos")
    version_ids = fields.One2many("property.contract.version", "contract_id", string="Versões")
    rent_schedule_ids = fields.One2many("property.contract.rent.schedule", "contract_id", string="Tabela de Valores")
    billing_plan_ids = fields.One2many("property.contract.billing.plan", "contract_id", string="Plano de Cobrança")
    financial_adjustment_ids = fields.One2many("property.contract.financial.adjustment", "contract_id", string="Ajustes Financeiros")
    document_ids = fields.One2many("property.contract.document", "contract_id", string="Documentos")
    obligation_ids = fields.One2many("property.contract.obligation", "contract_id", string="Obrigações")
    option_ids = fields.One2many("property.contract.option", "contract_id", string="Opções")
    term_history_ids = fields.One2many("property.contract.term.history", "contract_id", string="Histórico de Termos")

    current_version_id = fields.Many2one("property.contract.version", string="Versão Vigente")
    amendment_count = fields.Integer(compute="_compute_contract_counts", string="Qtd. Aditivos")
    document_count = fields.Integer(compute="_compute_contract_counts", string="Qtd. Documentos")
    last_amendment_date = fields.Date(string="Último Aditivo")
    has_pending_amendments = fields.Boolean(compute="_compute_contract_counts", string="Aditivos Pendentes")
    has_unapplied_amendments = fields.Boolean(compute="_compute_contract_counts", string="Aditivos Não Aplicados")
    next_rent_change_date = fields.Date(string="Próxima Alteração de Valor", compute="_compute_next_rent_change_date", store=True)

    @api.depends("amendment_ids.status", "amendment_ids.is_applied", "document_ids")
    def _compute_contract_counts(self):
        for contract in self:
            contract.amendment_count = len(contract.amendment_ids)
            contract.document_count = len(contract.document_ids)
            contract.has_pending_amendments = any(a.status not in ("applied", "cancelled", "archived") for a in contract.amendment_ids)
            contract.has_unapplied_amendments = any(a.status == "signed" and not a.is_applied for a in contract.amendment_ids)

    @api.depends("rent_schedule_ids.amount", "rent_schedule_ids.start_date", "rent_schedule_ids.end_date", "rent_schedule_ids.charge_type", "rent_schedule_ids.status")
    def _compute_current_financials(self):
        today = fields.Date.context_today(self)
        for contract in self:
            base = 0.0
            discount = 0.0
            extra = 0.0
            for line in contract.rent_schedule_ids.filtered(lambda r: r.status == "active" and r._is_date_in_range(today)):
                if line.is_base_rent or line.charge_type in ("base_rent", "minimum_rent"):
                    base += line.amount
                elif line.is_discount or line.charge_type in ("discount", "rent_free_period", "grace_period", "credit"):
                    discount += abs(line.amount)
                elif line.is_extra_charge or line.charge_type not in ("base_rent", "discount", "rent_free_period", "grace_period", "credit"):
                    extra += line.amount
            contract.current_base_rent = base or contract.current_base_rent
            contract.current_discount_amount = discount
            contract.current_extra_charge_amount = extra
            contract.current_effective_rent = (base or contract.current_base_rent or 0.0) - discount + extra

    @api.depends("rent_schedule_ids.start_date", "rent_schedule_ids.status")
    def _compute_next_rent_change_date(self):
        today = fields.Date.context_today(self)
        for contract in self:
            future = contract.rent_schedule_ids.filtered(lambda r: r.status == "active" and r.start_date and r.start_date > today).mapped("start_date")
            contract.next_rent_change_date = min(future) if future else False

    def action_open_amendments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Aditivos"),
            "res_model": "property.contract.amendment",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id},
        }

    def action_open_rent_schedule(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Tabela de Valores"),
            "res_model": "property.contract.rent.schedule",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id},
        }
