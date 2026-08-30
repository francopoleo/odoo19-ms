from odoo import api, fields, models, _
from datetime import timedelta


class GovernanceCasePending(models.Model):
    _name = "governance.case.pending"
    _description = "Pendência do Caso de Governança"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "state, due_date, id"

    name = fields.Char(string="Pendência", required=True, tracking=True)
    case_id = fields.Many2one("governance.case", string="Caso", required=True, ondelete="cascade", tracking=True)
    company_id = fields.Many2one(related="case_id.company_id", store=True, readonly=True)
    participant_id = fields.Many2one("governance.case.participant", string="Participante")
    partner_id = fields.Many2one("res.partner", string="Contato")
    communication_id = fields.Many2one("governance.case.communication", string="Comunicação")
    template_id = fields.Many2one(
        "governance.case.type.pending.template",
        string="Modelo de checklist",
        help="Modelo que originou esta ação. Documentos devem ir para o dossiê; compromissos formais devem usar uma Obrigação.",
    )
    response_id = fields.Many2one("governance.case.response", string="Resposta")
    stage_id = fields.Many2one("governance.stage", string="Etapa Relacionada")
    responsible_id = fields.Many2one("res.users", string="Responsável", default=lambda self: self.env.user, tracking=True)
    description = fields.Html(string="Descrição")
    due_date = fields.Date(string="Prazo", tracking=True)
    required = fields.Boolean(string="Obrigatória", default=False, tracking=True)
    priority = fields.Selection([
        ("0", "Baixa"),
        ("1", "Média"),
        ("2", "Alta"),
        ("3", "Crítica"),
    ], string="Prioridade", default="1", tracking=True)
    state = fields.Selection([
        ("open", "Aberta"),
        ("done", "Concluída"),
        ("cancel", "Cancelada"),
    ], string="Status", default="open", tracking=True)
    date_done = fields.Date(string="Concluída em", tracking=True)
    is_overdue = fields.Boolean(string="Atrasada", compute="_compute_pending_metrics", store=True)
    age_days = fields.Integer(string="Idade (dias)", compute="_compute_pending_metrics", store=True)
    deadline_bucket = fields.Selection([
        ("today", "Hoje"),
        ("next_7", "Próx. 7 dias"),
        ("overdue", "Vencida"),
        ("future", "Futura"),
        ("none", "Sem Prazo"),
    ], string="Faixa de Prazo", compute="_compute_pending_metrics", store=True)

    @api.depends("due_date", "state", "create_date")
    def _compute_pending_metrics(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_overdue = bool(rec.due_date and rec.state == "open" and rec.due_date < today)
            create_date = fields.Date.to_date(rec.create_date) if rec.create_date else today
            rec.age_days = (today - create_date).days if create_date else 0
            if not rec.due_date:
                rec.deadline_bucket = "none"
            elif rec.state != "open":
                rec.deadline_bucket = "future"
            elif rec.due_date < today:
                rec.deadline_bucket = "overdue"
            elif rec.due_date == today:
                rec.deadline_bucket = "today"
            elif rec.due_date <= today + timedelta(days=7):
                rec.deadline_bucket = "next_7"
            else:
                rec.deadline_bucket = "future"

    @api.onchange("participant_id")
    def _onchange_participant_id(self):
        for rec in self:
            if rec.participant_id and not rec.partner_id:
                rec.partner_id = rec.participant_id.partner_id

    def action_mark_done(self):
        for rec in self:
            rec.write({"state": "done", "date_done": fields.Date.today()})
        return True

    def action_reopen(self):
        for rec in self:
            rec.write({"state": "open", "date_done": False})
        return True

    def action_cancel(self):
        self.write({"state": "cancel"})
        return True

    def action_open_case(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Caso"),
            "res_model": "governance.case",
            "res_id": self.case_id.id,
            "view_mode": "form",
            "target": "current",
        }
