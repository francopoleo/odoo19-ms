from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class GovernanceCaseObligation(models.Model):
    _name = "governance.case.obligation"
    _description = "Obrigação do Caso de Governança"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, due_date, id"

    name = fields.Char(
        string="O que precisa ser feito",
        required=True,
        tracking=True,
        help="Compromisso formal de uma parte ou responsável, com prazo, cobrança e eventual resposta. Ações internas simples devem ser Pendências.",
    )
    reference = fields.Char(string="Referência", readonly=True, copy=False, default="Nova")
    case_id = fields.Many2one("governance.case", string="Caso", required=True, ondelete="cascade", tracking=True)
    company_id = fields.Many2one(related="case_id.company_id", store=True, readonly=True)
    partner_id = fields.Many2one("res.partner", string="Parte que deve cumprir", tracking=True)
    participant_id = fields.Many2one("governance.case.participant", string="Participante relacionado")
    responsible_id = fields.Many2one("res.users", string="Responsável interno", required=True, default=lambda self: self.env.user, tracking=True)
    source_communication_id = fields.Many2one("governance.case.communication", string="Comunicação de origem", ondelete="set null")
    response_id = fields.Many2one("governance.case.response", string="Resposta formal", ondelete="set null", tracking=True)
    obligation_type = fields.Selection([
        ("information", "Fornecer informação"),
        ("document", "Fornecer documento"),
        ("response", "Enviar resposta"),
        ("action", "Executar providência"),
        ("approval", "Obter aprovação"),
        ("review", "Realizar análise"),
        ("other", "Outra obrigação"),
    ], string="Tipo de obrigação", required=True, default="information", tracking=True)
    state = fields.Selection([
        ("draft", "Rascunho"),
        ("sent", "Enviada"),
        ("waiting", "Aguardando cumprimento"),
        ("due_soon", "Prazo próximo"),
        ("overdue", "Atrasada"),
        ("received", "Recebida"),
        ("in_review", "Em análise"),
        ("fulfilled", "Cumprida"),
        ("not_fulfilled", "Não cumprida"),
        ("cancelled", "Cancelada"),
    ], string="Situação", default="draft", required=True, tracking=True, index=True)
    priority = fields.Selection([
        ("0", "Baixa"), ("1", "Média"), ("2", "Alta"), ("3", "Crítica"),
    ], string="Prioridade", default="1", required=True, tracking=True)
    description = fields.Html(string="Instruções e critérios de aceite")
    requested_date = fields.Date(string="Solicitada em", default=fields.Date.today, required=True, tracking=True)
    due_date = fields.Date(string="Prazo", tracking=True, index=True)
    fulfilled_date = fields.Date(string="Cumprida em", readonly=True, tracking=True)
    is_required = fields.Boolean(string="Obrigatória", default=True, tracking=True)
    escalation_level = fields.Integer(string="Nível de escalonamento", default=0, readonly=True)
    last_followup_date = fields.Date(string="Última cobrança", readonly=True)
    next_followup_date = fields.Date(string="Próxima cobrança", readonly=True)
    age_days = fields.Integer(string="Idade (dias)", compute="_compute_metrics", store=True)
    is_overdue = fields.Boolean(string="Atrasada", compute="_compute_metrics", store=True, index=True)
    deadline_bucket = fields.Selection([
        ("none", "Sem prazo"), ("today", "Hoje"), ("next_7", "Próximos 7 dias"),
        ("future", "Futura"), ("overdue", "Vencida"), ("closed", "Encerrada"),
    ], string="Faixa de prazo", compute="_compute_metrics", store=True)

    @api.depends("requested_date", "due_date", "state")
    def _compute_metrics(self):
        today = fields.Date.today()
        open_states = {"sent", "waiting", "due_soon", "overdue", "received", "in_review"}
        for record in self:
            record.age_days = max((today - record.requested_date).days, 0) if record.requested_date else 0
            record.is_overdue = bool(record.due_date and record.state in open_states and record.due_date < today)
            if record.state in {"fulfilled", "not_fulfilled", "cancelled"}:
                record.deadline_bucket = "closed"
            elif not record.due_date:
                record.deadline_bucket = "none"
            elif record.due_date < today:
                record.deadline_bucket = "overdue"
            elif record.due_date == today:
                record.deadline_bucket = "today"
            elif record.due_date <= today + timedelta(days=7):
                record.deadline_bucket = "next_7"
            else:
                record.deadline_bucket = "future"

    @api.constrains("due_date", "requested_date")
    def _check_dates(self):
        for record in self:
            if record.due_date and record.requested_date and record.due_date < record.requested_date:
                raise ValidationError(_("O prazo da obrigação não pode ser anterior à data da solicitação."))

    @api.constrains("case_id", "participant_id")
    def _check_participant_case(self):
        for record in self:
            if record.participant_id and record.participant_id.case_id != record.case_id:
                raise ValidationError(_("O participante precisa pertencer ao mesmo caso da obrigação."))

    @api.constrains("reference")
    def _check_unique_reference(self):
        for record in self:
            if record.reference and self.search_count([("id", "!=", record.id), ("reference", "=", record.reference)]):
                raise ValidationError(_("A referência da obrigação precisa ser única."))

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["common.sequence"].sudo()
        for vals in vals_list:
            if vals.get("reference", "Nova") == "Nova":
                vals["reference"] = sequence.next_by_code("governance.case.obligation") or "OBR-NOVA"
            if not vals.get("responsible_id") and vals.get("case_id"):
                case = self.env["governance.case"].browse(vals["case_id"])
                vals["responsible_id"] = case.responsible_id.id or self.env.user.id
            if vals.get("state") == "draft" and vals.get("requested_date"):
                vals["state"] = "waiting"
        return super().create(vals_list)

    def action_mark_sent(self):
        self.write({"state": "waiting"})
        return True

    def action_mark_received(self):
        self.write({"state": "received"})
        return True

    def action_start_review(self):
        self.write({"state": "in_review"})
        return True

    def action_mark_fulfilled(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Uma obrigação cancelada não pode ser cumprida."))
            record.write({"state": "fulfilled", "fulfilled_date": fields.Date.today()})
        return True

    def action_mark_not_fulfilled(self):
        self.write({"state": "not_fulfilled", "fulfilled_date": False})
        return True

    def action_reopen(self):
        self.write({"state": "waiting", "fulfilled_date": False})
        return True

    def action_cancel(self):
        self.write({"state": "cancelled"})
        return True

    @api.model
    def action_cron_update_deadlines(self):
        """Atualiza a fila de obrigações e cria uma atividade por responsável."""
        today = fields.Date.today()
        open_states = ("sent", "waiting", "due_soon", "overdue", "received", "in_review")
        records = self.search([("state", "in", open_states)])
        activity_type = self.env.ref("governance.activity_type_required_pending", raise_if_not_found=False)
        for obligation in records:
            if obligation.due_date and obligation.due_date < today and obligation.state not in ("overdue", "received", "in_review"):
                obligation.write({"state": "overdue", "escalation_level": obligation.escalation_level + 1})
            elif obligation.due_date and obligation.due_date <= today + timedelta(days=7) and obligation.state in ("sent", "waiting"):
                obligation.write({"state": "due_soon"})
            if obligation.is_overdue and activity_type and obligation.responsible_id:
                existing = self.env["mail.activity"].search([
                    ("res_model", "=", self._name), ("res_id", "=", obligation.id),
                    ("activity_type_id", "=", activity_type.id), ("date_deadline", "=", today),
                ], limit=1)
                if not existing:
                    obligation.activity_schedule(
                        activity_type_id=activity_type.id, user_id=obligation.responsible_id.id,
                        date_deadline=today, summary=_("Cobrar obrigação em atraso"),
                        note=_("A obrigação %s está vencida e precisa de providência.") % obligation.name,
                    )
        return True

    def action_open_case(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "name": _("Caso"), "res_model": "governance.case", "res_id": self.case_id.id, "view_mode": "form"}
