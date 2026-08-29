# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError


AMENDMENT_TYPES = [
    ("tenant_change", "Troca de locatário"),
    ("landlord_change", "Troca de locador"),
    ("guarantor_change", "Troca de fiador/garantidor"),
    ("assignment", "Cessão de posição contratual"),
    ("novation", "Novação"),
    ("rent_change", "Alteração de aluguel"),
    ("rent_increase", "Aumento de aluguel"),
    ("rent_reduction", "Redução de aluguel"),
    ("temporary_discount", "Desconto temporário"),
    ("permanent_discount", "Desconto permanente"),
    ("extra_charge", "Acréscimo/cobrança adicional"),
    ("charge_waiver", "Renúncia/perdão de cobrança"),
    ("billing_reschedule", "Reprogramação de cobrança"),
    ("debt_confession", "Confissão/parcelamento de dívida"),
    ("term_extension", "Prorrogação de prazo"),
    ("term_reduction", "Redução de prazo"),
    ("renewal", "Renovação"),
    ("early_termination", "Rescisão antecipada"),
    ("termination", "Encerramento"),
    ("partial_termination", "Encerramento parcial"),
    ("guarantee_change", "Alteração de garantia"),
    ("asset_area_change", "Alteração de imóvel/área"),
    ("purpose_change", "Alteração de finalidade"),
    ("index_change", "Alteração de índice"),
    ("payment_terms_change", "Alteração de pagamento"),
    ("expenses_change", "Alteração de encargos/despesas"),
    ("works_fitout", "Obras, benfeitorias ou adaptação/implantação"),
    ("sublocation_authorization", "Autorização de sublocação"),
    ("conformidade_update", "Ajuste jurídico/conformidade"),
    ("force_majeure", "Força maior / evento extraordinário"),
    ("rectification", "Retificação/Rerratificação"),
    ("other", "Outro"),
]


CONTROLLED_CONTRACT_FIELD_OPTIONS = [
    ("current_base_rent", "Aluguel base atual"),
    ("original_monthly_rent", "Aluguel original"),
    ("current_start_date", "Início vigente"),
    ("current_end_date", "Fim vigente"),
    ("current_discount_until", "Desconto até"),
    ("current_payment_day", "Dia de vencimento vigente"),
    ("current_adjustment_index", "Índice de reajuste vigente"),
    ("current_partner_id", "Locatário atual"),
    ("original_partner_id", "Locatário original"),
    ("current_guarantee_type", "Garantia vigente"),
    ("current_purpose", "Finalidade vigente"),
    ("current_jurisdiction", "Foro vigente"),
    ("legal_status", "Status jurídico"),
    ("operational_status", "Status operacional"),
    ("consolidated_terms_html", "Termos consolidados"),
    ("issuer", "Emitido por"),
]

CONTROLLED_CONTRACT_FIELD_META = {
    "current_base_rent": {"label": "Aluguel Base Atual", "category": "financial", "value_type": "float"},
    "original_monthly_rent": {"label": "Aluguel Original", "category": "financial", "value_type": "float"},
    "current_start_date": {"label": "Início Vigente", "category": "term", "value_type": "date"},
    "current_end_date": {"label": "Fim Vigente", "category": "term", "value_type": "date"},
    "current_discount_until": {"label": "Desconto Até", "category": "financial", "value_type": "date"},
    "current_payment_day": {"label": "Dia de Vencimento Vigente", "category": "billing", "value_type": "float"},
    "current_adjustment_index": {"label": "Índice de Reajuste Vigente", "category": "financial", "value_type": "char"},
    "current_partner_id": {"label": "Locatário Atual", "category": "party", "value_type": "partner"},
    "original_partner_id": {"label": "Locatário Original", "category": "party", "value_type": "partner"},
    "current_guarantee_type": {"label": "Garantia Vigente", "category": "guarantee", "value_type": "char"},
    "current_purpose": {"label": "Finalidade Vigente", "category": "asset", "value_type": "char"},
    "current_jurisdiction": {"label": "Foro Vigente", "category": "legal", "value_type": "char"},
    "legal_status": {"label": "Status Jurídico", "category": "legal", "value_type": "char"},
    "operational_status": {"label": "Status Operacional", "category": "operational", "value_type": "char"},
    "consolidated_terms_html": {"label": "Termos Consolidados", "category": "clause", "value_type": "char"},
    "issuer": {"label": "Emitido por", "category": "legal", "value_type": "char"},
}


class PropertyContractAmendment(models.Model):
    _name = "property.contract.amendment"
    _description = "Aditivo Contratual"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "contract_id, amendment_number, id"

    name = fields.Char(string="Nome", required=True, tracking=True, default=lambda self: _("Novo Aditivo"))
    sequence = fields.Char(string="Sequência", default=lambda self: self.env["ir.sequence"].next_by_code("property.contract.amendment"), copy=False, readonly=True)
    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade", index=True, tracking=True)
    amendment_number = fields.Integer(string="Número do Aditivo", tracking=True)
    amendment_type = fields.Selection(AMENDMENT_TYPES, string="Tipo de Aditivo", required=True, default="other", tracking=True)
    amendment_reason_id = fields.Many2one("property.contract.amendment.reason", string="Motivo")
    amendment_scope = fields.Selection([
        ("specific_clause", "Cláusula específica"),
        ("financial", "Financeiro"),
        ("term", "Prazo/vigência"),
        ("parties", "Partes"),
        ("asset", "Imóvel/área"),
        ("full_consolidation", "Consolidação ampla"),
    ], string="Escopo", default="specific_clause", tracking=True)
    economic_effect = fields.Selection([
        ("neutral", "Neutro"),
        ("increase", "Acréscimo/a mais"),
        ("decrease", "Desconto/a menos"),
        ("mixed", "Misto"),
    ], string="Efeito Econômico", default="neutral", tracking=True)
    risk_level = fields.Selection([
        ("low", "Baixo"),
        ("medium", "Médio"),
        ("high", "Alto"),
        ("critical", "Crítico"),
    ], string="Risco", default="medium", tracking=True)
    signature_method = fields.Selection([
        ("manual", "Manual"),
        ("digital", "Digital"),
        ("electronic", "Eletrônica"),
        ("notarial", "Reconhecimento/Cartório"),
        ("not_required", "Não exige assinatura"),
    ], string="Forma de Assinatura", default="digital")

    status = fields.Selection([
        ("draft", "Rascunho"),
        ("legal_review", "Revisão jurídica"),
        ("commercial_review", "Revisão comercial"),
        ("financial_review", "Revisão financeira"),
        ("risk_review", "Revisão de risco"),
        ("approved", "Aprovado"),
        ("sent_to_signature", "Enviado para assinatura"),
        ("partially_signed", "Parcialmente assinado"),
        ("signed", "Assinado"),
        ("ready_to_apply", "Pronto para aplicar"),
        ("applied", "Aplicado"),
        ("rejected", "Rejeitado"),
        ("cancelled", "Cancelado"),
        ("archived", "Arquivado"),
    ], string="Status", default="draft", tracking=True)

    instrument_date = fields.Date(string="Data do Instrumento", tracking=True)
    sign_date = fields.Date(string="Data de Assinatura", tracking=True)
    signature_completed_at = fields.Datetime(string="Conclusão da Assinatura")
    effective_date = fields.Date(string="Data de Efeito", required=True, tracking=True)
    retroactive_effect = fields.Boolean(string="Efeito Retroativo")
    retroactive_from = fields.Date(string="Retroativo Desde")
    retroactive_to = fields.Date(string="Retroativo Até")
    execution_date = fields.Date(string="Data de Execução")
    applied_date = fields.Datetime(string="Aplicado em", readonly=True)
    applied_by = fields.Many2one("res.users", string="Aplicado por", readonly=True)
    is_applied = fields.Boolean(string="Aplicado", default=False, readonly=True)

    requires_approval = fields.Boolean(string="Exige Aprovação", default=True)
    approval_state = fields.Selection([
        ("none", "Sem aprovação"),
        ("pending", "Pendente"),
        ("approved", "Aprovado"),
        ("rejected", "Rejeitado"),
    ], string="Status da Aprovação", default="pending")

    commercial_impact = fields.Boolean(string="Impacto Comercial")
    financial_impact = fields.Boolean(string="Impacto Financeiro")
    legal_impact = fields.Boolean(string="Impacto Jurídico", default=True)
    operational_impact = fields.Boolean(string="Impacto Operacional")
    requires_financial_update = fields.Boolean(string="Exige Atualização Financeira")
    requires_party_update = fields.Boolean(string="Exige Atualização de Partes")
    requires_term_update = fields.Boolean(string="Exige Atualização de Prazo")
    requires_guarantee_update = fields.Boolean(string="Exige Atualização de Garantia")
    requires_asset_update = fields.Boolean(string="Exige Atualização de Imóvel")
    requires_billing_recalculation = fields.Boolean(string="Exige Recálculo de Cobrança")
    requires_accounting_adjustment = fields.Boolean(string="Exige Ajuste Contábil")

    old_summary_html = fields.Html(string="Resumo Antes")
    new_summary_html = fields.Html(string="Resumo Depois")
    summary_html = fields.Html(string="Resumo do Aditivo")
    legal_basis = fields.Text(string="Base Legal/Contratual")
    clauses_affected = fields.Char(string="Cláusulas Afetadas")
    unchanged_clauses_html = fields.Html(string="Cláusulas Mantidas")
    changes_json = fields.Text(string="Alterações JSON")
    note = fields.Text(string="Observações")

    change_line_ids = fields.One2many("property.contract.amendment.change", "amendment_id", string="Alterações")
    document_ids = fields.One2many("property.contract.document", "amendment_id", string="Documentos")
    approval_ids = fields.One2many("property.contract.approval", "amendment_id", string="Aprovações")
    term_history_ids = fields.One2many("property.contract.term.history", "amendment_id", string="Histórico")
    rent_schedule_ids = fields.One2many("property.contract.rent.schedule", "amendment_id", string="Tabela de Valores")
    financial_adjustment_ids = fields.One2many("property.contract.financial.adjustment", "amendment_id", string="Ajustes Financeiros")
    billing_impact_ids = fields.One2many("property.contract.billing.impact", "amendment_id", string="Parcelas Afetadas")
    billing_impact_count = fields.Integer(string="Qtd. Parcelas Afetadas", compute="_compute_billing_impact_summary")
    billing_impact_total_delta = fields.Monetary(string="Diferença Total nas Parcelas", currency_field="currency_id", compute="_compute_billing_impact_summary")
    has_pending_billing_impacts = fields.Boolean(string="Possui Parcelas Pendentes", compute="_compute_billing_impact_summary")

    company_id = fields.Many2one(related="contract_id.company_id", string="Empresa", store=True, readonly=True)
    currency_id = fields.Many2one(related="contract_id.currency_id", string="Moeda", store=True, readonly=True)

    _contract_amendment_number_unique = models.Constraint(
        'UNIQUE(contract_id, amendment_number)',
        'Já existe aditivo com este número para este contrato.',
    )

    @api.depends("billing_impact_ids.status", "billing_impact_ids.delta_amount")
    def _compute_billing_impact_summary(self):
        for amendment in self:
            impacts = amendment.billing_impact_ids
            amendment.billing_impact_count = len(impacts)
            amendment.billing_impact_total_delta = sum(impacts.mapped("delta_amount"))
            amendment.has_pending_billing_impacts = any(i.status in ("draft", "simulated") for i in impacts)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("sequence"):
                vals["sequence"] = self.env["ir.sequence"].next_by_code("property.contract.amendment") or _("Novo")
            contract_id = vals.get("contract_id")
            if contract_id and not vals.get("amendment_number"):
                last = self.search(
                    [("contract_id", "=", contract_id)],
                    order="amendment_number desc, id desc",
                    limit=1,
                )
                vals["amendment_number"] = (last.amendment_number or 0) + 1
            if not vals.get("name") or vals.get("name") == _("Novo Aditivo"):
                number = vals.get("amendment_number") or 1
                vals["name"] = _("Aditivo %02d") % number
        return super().create(vals_list)

    @api.onchange("amendment_type", "amendment_reason_id")
    def _onchange_amendment_classification(self):
        financial_types = {
            "rent_change", "rent_increase", "rent_reduction", "temporary_discount",
            "permanent_discount", "extra_charge", "charge_waiver", "billing_reschedule",
            "debt_confession", "index_change", "payment_terms_change", "expenses_change",
        }
        party_types = {"tenant_change", "landlord_change", "guarantor_change", "assignment", "novation"}
        term_types = {"term_extension", "term_reduction", "renewal", "early_termination", "termination", "partial_termination"}
        asset_types = {"asset_area_change", "purpose_change", "works_fitout", "sublocation_authorization"}
        for rec in self:
            rec.financial_impact = rec.amendment_type in financial_types
            rec.commercial_impact = rec.amendment_type in financial_types | term_types | asset_types
            rec.requires_financial_update = rec.amendment_type in financial_types
            rec.requires_billing_recalculation = rec.amendment_type in financial_types
            rec.requires_accounting_adjustment = rec.amendment_type in {"debt_confession", "extra_charge", "charge_waiver"}
            rec.requires_party_update = rec.amendment_type in party_types
            rec.requires_term_update = rec.amendment_type in term_types
            rec.requires_guarantee_update = rec.amendment_type == "guarantor_change" or rec.amendment_type == "guarantee_change"
            rec.requires_asset_update = rec.amendment_type in asset_types
            if rec.amendment_type in {"rent_increase", "extra_charge", "underbilling_debit", "debt_confession"}:
                rec.economic_effect = "increase"
            elif rec.amendment_type in {"rent_reduction", "temporary_discount", "permanent_discount", "charge_waiver"}:
                rec.economic_effect = "decrease"
            elif rec.amendment_type in financial_types:
                rec.economic_effect = "mixed"
            else:
                rec.economic_effect = "neutral"
            if rec.amendment_type in financial_types:
                rec.amendment_scope = "financial"
            elif rec.amendment_type in party_types:
                rec.amendment_scope = "parties"
            elif rec.amendment_type in term_types:
                rec.amendment_scope = "term"
            elif rec.amendment_type in asset_types:
                rec.amendment_scope = "asset"

    def action_submit_legal(self):
        self.write({"status": "legal_review"})

    def action_approve(self):
        self.write({"status": "approved", "approval_state": "approved"})

    def action_send_to_signature(self):
        self.write({"status": "sent_to_signature"})

    def action_mark_signed(self):
        self.write({"status": "signed", "sign_date": fields.Date.context_today(self)})

    def action_ready_to_apply(self):
        self.write({"status": "ready_to_apply"})

    def action_cancel(self):
        self.write({"status": "cancelled"})

    def action_simulate_billing_impact(self):
        for amendment in self:
            amendment._simulate_billing_impacts()
        return True

    def action_apply_billing_impact(self):
        for amendment in self:
            amendment._apply_billing_impacts()
        return True

    def action_reverse_billing_impact(self):
        for amendment in self:
            amendment.billing_impact_ids.filtered(lambda i: i.status == "applied").action_reverse()
        return True

    def action_apply(self):
        for amendment in self:
            if amendment.is_applied:
                raise UserError(_("Este aditivo já foi aplicado."))
            if amendment.status not in ("signed", "ready_to_apply", "approved"):
                raise UserError(_("Somente aditivos assinados, aprovados ou prontos para aplicar podem ser aplicados."))
            amendment._apply_change_lines()
            amendment._apply_financial_lines()
            if amendment.requires_billing_recalculation or amendment.rent_schedule_ids or amendment.financial_adjustment_ids:
                if not amendment.billing_impact_ids:
                    amendment._simulate_billing_impacts()
                amendment._apply_billing_impacts()
            amendment._create_version_snapshot()
            amendment.write({
                "is_applied": True,
                "status": "applied",
                "applied_date": fields.Datetime.now(),
                "applied_by": self.env.user.id,
            })
            amendment.contract_id.write({
                "legal_status": "amended",
                "last_amendment_date": amendment.effective_date or fields.Date.context_today(self),
            })

    def _apply_change_lines(self):
        self.ensure_one()
        contract = self.contract_id
        for line in self.change_line_ids:
            field_name = line.field_name or line.field_key
            if not field_name or field_name not in contract._fields:
                raise UserError(_("O campo '%s' não existe no contrato e não pode ser aplicado.") % (field_name or ""))
            old_value = line._get_old_value_display()
            new_value = line._get_new_value_display()
            vals = line._get_contract_write_value()
            if vals:
                contract.write(vals)
            self.env["property.contract.term.history"].create({
                "contract_id": contract.id,
                "amendment_id": self.id,
                "source_type": "amendment",
                "source_id": "%s,%s" % (self._name, self.id),
                "field_name": field_name,
                "field_label": line.field_label or field_name,
                "old_value": old_value,
                "new_value": new_value,
                "effective_date": line.effective_date or self.effective_date,
                "applied_date": fields.Datetime.now(),
                "applied_by": self.env.user.id,
                "reason": self.amendment_reason_id.name or self.amendment_type,
            })
            line.write({"is_applied": True, "applied_at": fields.Datetime.now()})

    def _apply_financial_lines(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        for schedule in self.rent_schedule_ids:
            if schedule.status == "draft":
                schedule.status = "active"
        if self.effective_date and self.effective_date < today:
            self.retroactive_effect = True

    def _apply_billing_impacts(self):
        self.ensure_one()
        impacts = self.billing_impact_ids.filtered(lambda i: i.status in ("draft", "simulated"))
        for impact in impacts:
            impact.action_apply()

    def _simulate_billing_impacts(self):
        self.ensure_one()
        Impact = self.env["property.contract.billing.impact"]
        # Mantém impactos aplicados/revertidos como auditoria e recria somente simulações pendentes.
        self.billing_impact_ids.filtered(lambda i: i.status in ("draft", "simulated", "ignored")).unlink()
        for schedule in self.rent_schedule_ids:
            for plan in self._find_billing_plans_for_period(schedule.start_date, schedule.end_date):
                vals = self._prepare_billing_impact_from_schedule(schedule, plan)
                if vals:
                    Impact.create(vals)
        for adjustment in self.financial_adjustment_ids:
            plans = self._find_billing_plans_for_period(adjustment.reference_period_start, adjustment.reference_period_end)
            if not plans:
                plans = self._find_next_open_billing_plan()
            for plan in plans:
                vals = self._prepare_billing_impact_from_financial_adjustment(adjustment, plan)
                if vals:
                    Impact.create(vals)

    def _find_billing_plans_for_period(self, period_start, period_end):
        self.ensure_one()
        if not period_start:
            period_start = self.effective_date
        if not period_end:
            period_end = self.contract_id.current_end_date or "9999-12-31"
        domain = [
            ("contract_id", "=", self.contract_id.id),
            ("period_start", "<=", period_end),
            ("period_end", ">=", period_start),
            ("status", "!=", "cancelled"),
        ]
        return self.env["property.contract.billing.plan"].search(domain, order="period_start, due_date, id")

    def _find_next_open_billing_plan(self):
        self.ensure_one()
        domain = [
            ("contract_id", "=", self.contract_id.id),
            ("status", "in", ["draft", "calculated", "approved"]),
        ]
        return self.env["property.contract.billing.plan"].search(domain, order="due_date, period_start, id", limit=1)

    def _prepare_billing_impact_from_schedule(self, schedule, plan):
        self.ensure_one()
        original_total = plan.total_amount or 0.0
        original_base = plan.base_rent_amount or 0.0
        original_discount = plan.discount_amount or 0.0
        original_extra = plan.extra_charge_amount or 0.0
        signed_amount = self._get_schedule_signed_amount(schedule, plan)
        impact_type = self._get_schedule_impact_type(schedule)
        new_base = original_base
        new_discount = original_discount
        new_extra = original_extra
        if impact_type == "base_rent_change":
            delta = (schedule.amount or 0.0) - original_base
            new_base = schedule.amount or 0.0
        elif impact_type == "discount":
            delta = -abs(signed_amount)
            new_discount = original_discount + abs(signed_amount)
        else:
            delta = signed_amount
            new_extra = original_extra + signed_amount
        if not delta:
            return {}
        application_rule = self._get_application_rule(plan, delta)
        if application_rule == "ignored":
            new_total = original_total
        elif application_rule in ("complementary_debit", "credit_note"):
            new_total = original_total + delta
        else:
            new_total = original_total + delta
        return {
            "amendment_id": self.id,
            "billing_plan_id": plan.id,
            "rent_schedule_id": schedule.id,
            "impact_source_type": "rent_schedule",
            "impact_type": impact_type,
            "application_rule": application_rule,
            "period_start": plan.period_start,
            "period_end": plan.period_end,
            "due_date": plan.due_date,
            "original_amount": original_total,
            "new_amount": new_total,
            "delta_amount": delta,
            "original_base_rent_amount": original_base,
            "new_base_rent_amount": new_base,
            "original_discount_amount": original_discount,
            "new_discount_amount": new_discount,
            "original_extra_charge_amount": original_extra,
            "new_extra_charge_amount": new_extra,
            "is_retroactive": bool(self.effective_date and plan.period_start and plan.period_start < self.effective_date),
            "status": "simulated" if application_rule != "ignored" else "ignored",
            "notes": schedule.notes or "",
        }

    def _prepare_billing_impact_from_financial_adjustment(self, adjustment, plan):
        self.ensure_one()
        amount = abs(adjustment.amount or 0.0)
        if not amount:
            return {}
        credit_types = {"retroactive_credit", "overbilling_credit", "penalty_waiver", "interest_waiver", "settlement_credit"}
        debit_types = {"retroactive_debit", "underbilling_debit", "settlement_debit"}
        delta = -amount if adjustment.adjustment_type in credit_types else amount
        if adjustment.adjustment_type not in credit_types | debit_types:
            delta = amount
        impact_type = "retroactive_credit" if delta < 0 else "retroactive_debit"
        if adjustment.apply_method == "credit_note" and delta < 0:
            application_rule = "credit_note"
        elif adjustment.apply_method == "separate_invoice" and delta > 0:
            application_rule = "complementary_debit"
        else:
            application_rule = self._get_application_rule(plan, delta)
        original_total = plan.total_amount or 0.0
        original_extra = plan.extra_charge_amount or 0.0
        original_discount = plan.discount_amount or 0.0
        return {
            "amendment_id": self.id,
            "billing_plan_id": plan.id,
            "financial_adjustment_id": adjustment.id,
            "impact_source_type": "financial_adjustment",
            "impact_type": impact_type,
            "application_rule": application_rule,
            "period_start": plan.period_start,
            "period_end": plan.period_end,
            "due_date": plan.due_date,
            "original_amount": original_total,
            "new_amount": original_total + delta,
            "delta_amount": delta,
            "original_base_rent_amount": plan.base_rent_amount or 0.0,
            "new_base_rent_amount": plan.base_rent_amount or 0.0,
            "original_discount_amount": original_discount,
            "new_discount_amount": original_discount + abs(delta) if delta < 0 else original_discount,
            "original_extra_charge_amount": original_extra,
            "new_extra_charge_amount": original_extra + delta if delta > 0 else original_extra,
            "is_retroactive": True,
            "status": "simulated" if application_rule != "ignored" else "ignored",
            "notes": adjustment.notes or adjustment.name or "",
        }

    def _get_schedule_signed_amount(self, schedule, plan):
        self.ensure_one()
        amount = schedule.amount or 0.0
        if schedule.amount_type == "percentage":
            base = schedule.base_amount or plan.base_rent_amount or plan.total_amount or 0.0
            amount = base * (schedule.percentage or 0.0) / 100.0
        if schedule.charge_type in ("discount", "rent_free_period", "grace_period", "credit"):
            return -abs(amount)
        return amount

    def _get_schedule_impact_type(self, schedule):
        if schedule.charge_type in ("base_rent", "minimum_rent"):
            return "base_rent_change"
        if schedule.charge_type in ("discount", "rent_free_period", "grace_period", "credit"):
            return "discount"
        return "extra_charge"

    def _get_application_rule(self, plan, delta):
        self.ensure_one()
        if plan.status in ("cancelled", "superseded"):
            return "ignored"
        if plan.status == "paid":
            return "complementary_debit" if delta > 0 else "credit_note"
        if plan.status == "invoiced":
            return "complementary_debit" if delta > 0 else "credit_note"
        if plan.status == "approved":
            return "open_update"
        return "future_recalculation"

    def _create_version_snapshot(self):
        self.ensure_one()
        contract = self.contract_id
        snapshot = {
            "contract_name": contract.display_name,
            "current_partner_id": contract.current_partner_id.display_name if contract.current_partner_id else "",
            "current_base_rent": contract.current_base_rent,
            "current_effective_rent": contract.current_effective_rent,
            "current_start_date": str(contract.current_start_date or ""),
            "current_end_date": str(contract.current_end_date or ""),
            "source_amendment": self.display_name,
        }
        version = self.env["property.contract.version"].create({
            "contract_id": contract.id,
            "source_amendment_id": self.id,
            "effective_date": self.effective_date,
            "terms_snapshot_json": json.dumps(snapshot, ensure_ascii=False, indent=2),
            "terms_snapshot_html": "<pre>%s</pre>" % json.dumps(snapshot, ensure_ascii=False, indent=2),
            "is_current": True,
        })
        contract.version_ids.filtered(lambda v: v.id != version.id).write({"is_current": False})
        contract.current_version_id = version.id


class PropertyContractAmendmentChange(models.Model):
    _name = "property.contract.amendment.change"
    _description = "Alteração de Aditivo Contratual"
    _order = "amendment_id, sequence, id"

    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo", required=True, ondelete="cascade")
    contract_id = fields.Many2one(related="amendment_id.contract_id", string="Contrato", store=True, readonly=True)
    sequence = fields.Integer(string="Sequência", default=10)
    change_category = fields.Selection([
        ("party", "Partes"),
        ("financial", "Financeiro"),
        ("term", "Prazo"),
        ("asset", "Imóvel"),
        ("guarantee", "Garantia"),
        ("obligation", "Obrigação"),
        ("clause", "Cláusula"),
        ("billing", "Cobrança"),
        ("legal", "Jurídico"),
        ("operational", "Operacional"),
    ], string="Categoria da Alteração", required=True, default="legal", readonly=True)

    field_key = fields.Selection(
        CONTROLLED_CONTRACT_FIELD_OPTIONS,
        string="Campo do Contrato",
        required=True,
        index=True,
        help="Selecione o campo contratual controlado que será alterado. O campo técnico, rótulo e tipo são preenchidos automaticamente.",
    )
    field_name = fields.Char(
        string="Campo Técnico",
        readonly=True,
        copy=False,
        help="Nome técnico usado internamente pelo Odoo. É preenchido automaticamente pela seleção Campo do Contrato.",
    )
    field_label = fields.Char(
        string="Rótulo do Campo",
        readonly=True,
        copy=False,
        help="Nome amigável do campo alterado. É preenchido automaticamente.",
    )
    value_type = fields.Selection([
        ("char", "Texto"),
        ("float", "Número"),
        ("date", "Data"),
        ("partner", "Contato"),
        ("boolean", "Sim/Não"),
    ], string="Tipo de Valor", required=True, default="char", readonly=True)

    old_value_char = fields.Char(string="Valor Anterior (Texto)", readonly=True)
    new_value_char = fields.Char(string="Novo Valor (Texto)")
    old_value_float = fields.Float(string="Valor Anterior (Número)", readonly=True)
    new_value_float = fields.Float(string="Novo Valor (Número)")
    old_value_date = fields.Date(string="Valor Anterior (Data)", readonly=True)
    new_value_date = fields.Date(string="Novo Valor (Data)")
    old_value_partner_id = fields.Many2one("res.partner", string="Contato Anterior", readonly=True)
    new_value_partner_id = fields.Many2one("res.partner", string="Novo Contato")
    old_value_bool = fields.Boolean(string="Valor Anterior (Sim/Não)", readonly=True)
    new_value_bool = fields.Boolean(string="Novo Valor (Sim/Não)")
    effective_date = fields.Date(string="Data de Efeito")
    is_applied = fields.Boolean(string="Aplicada", default=False, readonly=True)
    applied_at = fields.Datetime(string="Aplicada em", readonly=True)

    @api.model
    def _controlled_field_values(self, field_key):
        """Return normalized values for the controlled contract field selection."""
        if not field_key:
            return {}
        meta = CONTROLLED_CONTRACT_FIELD_META.get(field_key)
        if not meta:
            raise UserError(_("O campo selecionado não está disponível na lista controlada de alterações."))
        return {
            "field_name": field_key,
            "field_label": meta["label"],
            "value_type": meta["value_type"],
            "change_category": meta["category"],
        }

    @api.model_create_multi
    def create(self, vals_list):
        normalized_vals_list = []
        for vals in vals_list:
            vals = dict(vals)
            field_key = vals.get("field_key") or vals.get("field_name")
            if field_key:
                vals["field_key"] = field_key
                vals.update(self._controlled_field_values(field_key))
            normalized_vals_list.append(vals)
        return super().create(normalized_vals_list)

    def write(self, vals):
        vals = dict(vals)
        field_key = vals.get("field_key")
        if field_key:
            vals.update(self._controlled_field_values(field_key))
        return super().write(vals)

    @api.onchange("field_key", "contract_id")
    def _onchange_field_key_fill_defaults(self):
        for line in self:
            if not line.field_key:
                continue
            values = line._controlled_field_values(line.field_key)
            line.field_name = values["field_name"]
            line.field_label = values["field_label"]
            line.value_type = values["value_type"]
            line.change_category = values["change_category"]
            line._fill_old_value_from_contract()

    def _fill_old_value_from_contract(self):
        for line in self:
            contract = line.contract_id
            field_name = line.field_name or line.field_key
            if not contract or not field_name or field_name not in contract._fields:
                continue
            value = contract[field_name]
            field = contract._fields[field_name]
            line.field_label = line.field_label or field.string
            if field.type in ("many2one",) or line.value_type == "partner":
                line.value_type = "partner"
                line.old_value_partner_id = value.id if field.comodel_name == "res.partner" and value else False
            elif field.type in ("float", "monetary", "integer") or line.value_type == "float":
                line.value_type = "float"
                line.old_value_float = float(value or 0.0)
            elif field.type == "date" or line.value_type == "date":
                line.value_type = "date"
                line.old_value_date = value or False
            elif field.type == "boolean" or line.value_type == "boolean":
                line.value_type = "boolean"
                line.old_value_bool = bool(value)
            else:
                line.value_type = "char"
                line.old_value_char = str(value or "")

    def _get_old_value_display(self):
        self.ensure_one()
        if self.value_type == "partner":
            return self.old_value_partner_id.display_name or ""
        if self.value_type == "float":
            return str(self.old_value_float or 0.0)
        if self.value_type == "date":
            return str(self.old_value_date or "")
        if self.value_type == "boolean":
            return str(bool(self.old_value_bool))
        return self.old_value_char or ""

    def _get_new_value_display(self):
        self.ensure_one()
        if self.value_type == "partner":
            return self.new_value_partner_id.display_name or ""
        if self.value_type == "float":
            return str(self.new_value_float or 0.0)
        if self.value_type == "date":
            return str(self.new_value_date or "")
        if self.value_type == "boolean":
            return str(bool(self.new_value_bool))
        return self.new_value_char or ""

    def _get_contract_write_value(self):
        self.ensure_one()
        contract = self.contract_id
        field_name = self.field_name or self.field_key
        if not field_name or field_name not in contract._fields:
            return {}
        if self.value_type == "partner":
            return {field_name: self.new_value_partner_id.id or False}
        if self.value_type == "float":
            field = contract._fields[field_name]
            if field.type == "integer":
                return {field_name: int(self.new_value_float or 0)}
            return {field_name: self.new_value_float}
        if self.value_type == "date":
            return {field_name: self.new_value_date}
        if self.value_type == "boolean":
            return {field_name: self.new_value_bool}
        return {field_name: self.new_value_char or False}


class PropertyContractVersion(models.Model):
    _name = "property.contract.version"
    _description = "Versão Consolidada do Contrato"
    _order = "contract_id, version_number desc, id desc"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade")
    version_number = fields.Integer(string="Número da Versão", default=1)
    source_amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo de Origem")
    effective_date = fields.Date(string="Data de Efeito")
    created_by = fields.Many2one("res.users", string="Criado por", default=lambda self: self.env.user, readonly=True)
    terms_snapshot_json = fields.Text(string="Registro JSON dos Termos")
    terms_snapshot_html = fields.Html(string="Registro dos Termos")
    is_current = fields.Boolean(string="Versão Vigente", default=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("contract_id") and not vals.get("version_number"):
                last = self.search([("contract_id", "=", vals["contract_id"])], order="version_number desc", limit=1)
                vals["version_number"] = (last.version_number or 0) + 1
        return super().create(vals_list)


class PropertyContractTermHistory(models.Model):
    _name = "property.contract.term.history"
    _description = "Histórico de Termos Contratuais"
    _order = "effective_date desc, id desc"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade")
    source_type = fields.Selection([
        ("original_contract", "Contrato original"),
        ("amendment", "Aditivo"),
        ("manual_adjustment", "Ajuste manual"),
        ("system_adjustment", "Ajuste sistêmico"),
        ("import", "Importação"),
    ], string="Origem", default="amendment")
    source_id = fields.Char(string="ID da Origem")
    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo")
    field_name = fields.Char(string="Campo Técnico", required=True)
    field_label = fields.Char(string="Rótulo do Campo")
    old_value = fields.Text(string="Valor Anterior")
    new_value = fields.Text(string="Novo Valor")
    effective_date = fields.Date(string="Data de Efeito")
    applied_date = fields.Datetime(string="Aplicado em")
    applied_by = fields.Many2one("res.users", string="Aplicado por")
    reason = fields.Char(string="Motivo")
