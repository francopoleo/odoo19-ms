# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class GovernanceDashboard(models.TransientModel):
    _name = "governance.dashboard"
    _description = "Painel Operacional de Governança"

    name = fields.Char(default="Painel Operacional", readonly=True)

    # ── Fila de Trabalho ─────────────────────────────────────────
    case_active_count = fields.Integer(readonly=True)
    case_urgent_count = fields.Integer(readonly=True)
    case_attention_count = fields.Integer(readonly=True)
    case_ok_count = fields.Integer(readonly=True)
    case_critical_count = fields.Integer(readonly=True)
    case_high_count = fields.Integer(readonly=True)

    # ── SLA ──────────────────────────────────────────────────────
    case_overdue_sla_count = fields.Integer(readonly=True)
    case_due_soon_sla_count = fields.Integer(readonly=True)
    case_on_track_sla_count = fields.Integer(readonly=True)

    # ── Respostas & Comunicação ───────────────────────────────────
    case_waiting_count = fields.Integer(readonly=True)
    case_no_response_count = fields.Integer(readonly=True)
    response_open_count = fields.Integer(readonly=True)

    # ── Pendências ────────────────────────────────────────────────
    pending_open_total = fields.Integer(readonly=True)
    pending_overdue_count = fields.Integer(readonly=True)
    pending_today_count = fields.Integer(readonly=True)
    pending_next7_count = fields.Integer(readonly=True)

    # ── Governança Enterprise ───────────────────────────────────
    obligation_open_total = fields.Integer(readonly=True)
    obligation_overdue_total = fields.Integer(readonly=True)
    decision_pending_total = fields.Integer(readonly=True)
    critical_risk_total = fields.Integer(readonly=True)
    deficient_control_total = fields.Integer(readonly=True)

    # ── Minha Operação ────────────────────────────────────────────
    case_my_count = fields.Integer(readonly=True)
    case_my_urgent_count = fields.Integer(readonly=True)
    pending_my_overdue_count = fields.Integer(readonly=True)
    pending_my_today_count = fields.Integer(readonly=True)

    # ── Pipeline por Status ───────────────────────────────────────
    case_planned_count = fields.Integer(readonly=True)
    case_sent_count = fields.Integer(readonly=True)
    case_waiting_status_count = fields.Integer(readonly=True)
    case_partial_count = fields.Integer(readonly=True)
    case_no_response_status_count = fields.Integer(readonly=True)
    case_done_count = fields.Integer(readonly=True)
    case_closed_count = fields.Integer(readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        Case = self.env["governance.case"]
        Pending = self.env["governance.case.pending"]
        Comm = self.env["governance.case.communication"]
        Obligation = self.env["governance.case.obligation"]
        Decision = self.env["governance.case.decision"]
        Risk = self.env["governance.case.risk"]
        Control = self.env["governance.control"]
        uid = self.env.user.id

        active = [("status", "not in", ["closed"])]

        res.update({
            # Fila
            "case_active_count": Case.search_count(active),
            "case_urgent_count": Case.search_count(active + [("work_queue_status", "=", "urgent")]),
            "case_attention_count": Case.search_count(active + [("work_queue_status", "=", "attention")]),
            "case_ok_count": Case.search_count(active + [("work_queue_status", "=", "ok")]),
            "case_critical_count": Case.search_count(active + [("priority", "=", "3")]),
            "case_high_count": Case.search_count(active + [("priority", "=", "2")]),
            # SLA
            "case_overdue_sla_count": Case.search_count(active + [("sla_status", "=", "overdue")]),
            "case_due_soon_sla_count": Case.search_count(active + [("sla_status", "=", "due_soon")]),
            "case_on_track_sla_count": Case.search_count(active + [("sla_status", "=", "on_track")]),
            # Respostas
            "case_waiting_count": Case.search_count([("status", "=", "waiting")]),
            "case_no_response_count": Case.search_count([("status", "=", "no_response")]),
            "response_open_count": Comm.search_count([
                ("requires_response", "=", True), ("response_received", "=", False),
            ]),
            # Pendências
            "pending_open_total": Pending.search_count([("state", "=", "open")]),
            "pending_overdue_count": Pending.search_count([("state", "=", "open"), ("is_overdue", "=", True)]),
            "pending_today_count": Pending.search_count([("state", "=", "open"), ("deadline_bucket", "=", "today")]),
            "pending_next7_count": Pending.search_count([("state", "=", "open"), ("deadline_bucket", "=", "next_7")]),
            "obligation_open_total": Obligation.search_count([("state", "not in", ("fulfilled", "not_fulfilled", "cancelled"))]),
            "obligation_overdue_total": Obligation.search_count([("is_overdue", "=", True)]),
            "decision_pending_total": Decision.search_count([("state", "=", "pending")]),
            "critical_risk_total": Risk.search_count([("risk_level", ">=", 6), ("state", "not in", ("closed", "mitigated"))]),
            "deficient_control_total": Control.search_count([("state", "=", "deficient")]),
            # Minha operação
            "case_my_count": Case.search_count(active + [("responsible_id", "=", uid)]),
            "case_my_urgent_count": Case.search_count(active + [("responsible_id", "=", uid), ("work_queue_status", "=", "urgent")]),
            "pending_my_overdue_count": Pending.search_count([("state", "=", "open"), ("is_overdue", "=", True), ("responsible_id", "=", uid)]),
            "pending_my_today_count": Pending.search_count([("state", "=", "open"), ("deadline_bucket", "=", "today"), ("responsible_id", "=", uid)]),
            # Pipeline
            "case_planned_count": Case.search_count([("status", "=", "planned")]),
            "case_sent_count": Case.search_count([("status", "=", "sent")]),
            "case_waiting_status_count": Case.search_count([("status", "=", "waiting")]),
            "case_partial_count": Case.search_count([("status", "=", "partial")]),
            "case_no_response_status_count": Case.search_count([("status", "=", "no_response")]),
            "case_done_count": Case.search_count([("status", "=", "done")]),
            "case_closed_count": Case.search_count([("status", "=", "closed")]),
        })
        return res

    def _case_action(self, domain, name="Casos"):
        return {
            "type": "ir.actions.act_window",
            "name": name,
            "res_model": "governance.case",
            "view_mode": "list,kanban,form",
            "domain": domain,
            "context": {},
        }

    def _pending_action(self, domain, name="Pendências"):
        return {
            "type": "ir.actions.act_window",
            "name": name,
            "res_model": "governance.case.pending",
            "view_mode": "list,form",
            "domain": domain,
            "context": {},
        }

    def _comm_action(self, domain, name="Comunicações"):
        return {
            "type": "ir.actions.act_window",
            "name": name,
            "res_model": "governance.case.communication",
            "view_mode": "list,form",
            "domain": domain,
            "context": {},
        }

    def action_refresh(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "governance.dashboard",
            "view_mode": "form",
            "target": "current",
        }

    # ── Fila de Trabalho ─────────────────────────────────────────
    def action_view_active(self):
        return self._case_action([("status", "not in", ["closed"])], _("Casos Ativos"))

    def action_view_urgent(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("work_queue_status", "=", "urgent")],
            _("Casos Urgentes"),
        )

    def action_view_attention(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("work_queue_status", "=", "attention")],
            _("Casos em Atenção"),
        )

    def action_view_ok(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("work_queue_status", "=", "ok")],
            _("Casos em Dia"),
        )

    def action_view_critical(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("priority", "=", "3")],
            _("Casos Críticos"),
        )

    def action_view_high(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("priority", "=", "2")],
            _("Casos Alta Prioridade"),
        )

    # ── SLA ──────────────────────────────────────────────────────
    def action_view_overdue_sla(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("sla_status", "=", "overdue")],
            _("SLA Vencido"),
        )

    def action_view_due_soon_sla(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("sla_status", "=", "due_soon")],
            _("SLA Próximo do Prazo"),
        )

    def action_view_on_track_sla(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("sla_status", "=", "on_track")],
            _("SLA em Dia"),
        )

    # ── Respostas ─────────────────────────────────────────────────
    def action_view_waiting(self):
        return self._case_action([("status", "=", "waiting")], _("Aguardando Resposta"))

    def action_view_no_response(self):
        return self._case_action([("status", "=", "no_response")], _("Sem Resposta"))

    def action_view_response_open(self):
        return self._comm_action(
            [("requires_response", "=", True), ("response_received", "=", False)],
            _("Solicitações sem Resposta"),
        )

    # ── Pendências ────────────────────────────────────────────────
    def action_view_pending_all(self):
        return self._pending_action([("state", "=", "open")], _("Todas as Pendências Abertas"))

    def action_view_pending_overdue(self):
        return self._pending_action(
            [("state", "=", "open"), ("is_overdue", "=", True)],
            _("Pendências Atrasadas"),
        )

    def action_view_pending_today(self):
        return self._pending_action(
            [("state", "=", "open"), ("deadline_bucket", "=", "today")],
            _("Pendências de Hoje"),
        )

    def action_view_pending_next7(self):
        return self._pending_action(
            [("state", "=", "open"), ("deadline_bucket", "=", "next_7")],
            _("Pendências Próx. 7 Dias"),
        )

    def action_view_obligations(self):
        return {"type": "ir.actions.act_window", "name": _("Obrigações em Aberto"), "res_model": "governance.case.obligation", "view_mode": "list,form", "domain": [("state", "not in", ("fulfilled", "not_fulfilled", "cancelled"))]}

    def action_view_obligations_overdue(self):
        return {"type": "ir.actions.act_window", "name": _("Obrigações Atrasadas"), "res_model": "governance.case.obligation", "view_mode": "list,form", "domain": [("is_overdue", "=", True)]}

    def action_view_pending_decisions(self):
        return {"type": "ir.actions.act_window", "name": _("Decisões Pendentes"), "res_model": "governance.case.decision", "view_mode": "list,form", "domain": [("state", "=", "pending")]}

    def action_view_critical_risks(self):
        return {"type": "ir.actions.act_window", "name": _("Riscos Críticos"), "res_model": "governance.case.risk", "view_mode": "list,form", "domain": [("risk_level", ">=", 6), ("state", "not in", ("closed", "mitigated"))]}

    def action_view_deficient_controls(self):
        return {"type": "ir.actions.act_window", "name": _("Controles com Deficiência"), "res_model": "governance.control", "view_mode": "list,form", "domain": [("state", "=", "deficient")]}

    # ── Minha Operação ────────────────────────────────────────────
    def action_view_my_cases(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("responsible_id", "=", self.env.user.id)],
            _("Meus Casos Ativos"),
        )

    def action_view_my_urgent(self):
        return self._case_action(
            [("status", "not in", ["closed"]), ("responsible_id", "=", self.env.user.id), ("work_queue_status", "=", "urgent")],
            _("Meus Casos Urgentes"),
        )

    def action_view_my_pending_overdue(self):
        return self._pending_action(
            [("state", "=", "open"), ("is_overdue", "=", True), ("responsible_id", "=", self.env.user.id)],
            _("Minhas Pendências Atrasadas"),
        )

    def action_view_my_pending_today(self):
        return self._pending_action(
            [("state", "=", "open"), ("deadline_bucket", "=", "today"), ("responsible_id", "=", self.env.user.id)],
            _("Minhas Pendências de Hoje"),
        )

    # ── Pipeline por Status ───────────────────────────────────────
    def action_view_status_planned(self):
        return self._case_action([("status", "=", "planned")], _("Planejados"))

    def action_view_status_sent(self):
        return self._case_action([("status", "=", "sent")], _("E-mail Enviado"))

    def action_view_status_waiting(self):
        return self._case_action([("status", "=", "waiting")], _("Aguardando Resposta"))

    def action_view_status_partial(self):
        return self._case_action([("status", "=", "partial")], _("Resposta Parcial"))

    def action_view_status_no_response(self):
        return self._case_action([("status", "=", "no_response")], _("Sem Resposta"))

    def action_view_status_done(self):
        return self._case_action([("status", "=", "done")], _("Concluídos"))

    def action_view_status_closed(self):
        return self._case_action([("status", "=", "closed")], _("Encerrados"))

    # ── Atalhos rápidos ───────────────────────────────────────────
    def action_shortcut_cases(self):
        return self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_case")

    def action_shortcut_work_queue(self):
        return self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_work_queue")

    def action_shortcut_my_queue(self):
        return self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_my_work_queue")

    def action_shortcut_pendings(self):
        return self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_case_pending")

    def action_shortcut_communications(self):
        return self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_case_communication")

    def action_shortcut_executive(self):
        return self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_executive_panel")
