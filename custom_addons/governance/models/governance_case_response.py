from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GovernanceCaseResponse(models.Model):
    _name = "governance.case.response"
    _description = "Resposta do Caso de Governança"
    _inherit = ["mail.thread"]
    _order = "response_date desc, id desc"

    name = fields.Char(string="Resumo", required=True, tracking=True)
    case_id = fields.Many2one("governance.case", string="Caso", required=True, ondelete="cascade", tracking=True)
    company_id = fields.Many2one(related="case_id.company_id", store=True, readonly=True)
    communication_id = fields.Many2one("governance.case.communication", string="Comunicação de Origem")
    obligation_id = fields.Many2one("governance.case.obligation", string="Obrigação atendida", ondelete="set null", tracking=True)
    participant_id = fields.Many2one("governance.case.participant", string="Participante")
    partner_id = fields.Many2one("res.partner", string="Contato", tracking=True)
    responsible_id = fields.Many2one("res.users", string="Responsável", default=lambda self: self.env.user, tracking=True)
    response_date = fields.Date(string="Data da Resposta", default=fields.Date.today, required=True, tracking=True)
    response_type = fields.Selection([
        ("formal", "Formal"),
        ("partial", "Parcial"),
        ("refusal", "Negativa"),
        ("compliance", "Cumprimento"),
        ("clarification", "Esclarecimento"),
        ("other", "Outra"),
    ], string="Tipo", default="formal", required=True, tracking=True)
    outcome = fields.Selection([
        ("received", "Recebida"),
        ("accepted", "Aceita"),
        ("pending_analysis", "Pendente de Análise"),
        ("rejected", "Rejeitada"),
    ], string="Resultado", default="received", tracking=True)
    state = fields.Selection([
        ("received", "Recebida"), ("in_review", "Em análise"), ("clarification", "Aguardando esclarecimento"),
        ("approved", "Aprovada"), ("partial", "Parcialmente aceita"), ("rejected", "Rejeitada"),
        ("closed", "Encerrada"),
    ], string="Situação do processo", default="received", required=True, tracking=True)
    decision_id = fields.Many2one("governance.case.decision", string="Decisão", ondelete="set null")
    document_ids = fields.Many2many("document.document", string="Documentos e evidências")
    close_open_pendings = fields.Boolean(string="Concluir Pendências Abertas")
    note = fields.Html(string="Detalhes")

    @api.constrains("case_id", "communication_id", "obligation_id", "decision_id")
    def _check_related_case(self):
        for record in self:
            for related in (record.communication_id, record.obligation_id, record.decision_id):
                if related and related.case_id != record.case_id:
                    raise ValidationError(_("Todos os vínculos da resposta devem pertencer ao mesmo caso."))

    @api.onchange("participant_id")
    def _onchange_participant_id(self):
        for rec in self:
            if rec.participant_id and not rec.partner_id:
                rec.partner_id = rec.participant_id.partner_id

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_case_from_response()
        return records

    def write(self, vals):
        res = super().write(vals)
        if any(k in vals for k in ["response_date", "response_type", "outcome", "close_open_pendings", "case_id", "communication_id"]):
            self._sync_case_from_response()
        return res

    def _sync_case_from_response(self):
        partial_stage = self.env.ref("governance.stage_partial", raise_if_not_found=False)
        done_stage = self.env.ref("governance.stage_done", raise_if_not_found=False)
        for rec in self.filtered("case_id"):
            case = rec.case_id
            vals = {"response_date": rec.response_date or fields.Date.today()}
            if rec.response_type in ("compliance",) or rec.outcome in ("accepted",):
                stage = case._get_stage_by_type_or_default("done") if hasattr(case, "_get_stage_by_type_or_default") else done_stage
                if stage:
                    vals["stage_id"] = stage.id
            else:
                stage = partial_stage
                if stage:
                    vals["stage_id"] = stage.id
            case.write(vals)
            if rec.communication_id:
                rec.communication_id.write({"response_received": True, "response_id": rec.id})
            if rec.obligation_id:
                rec.obligation_id.write({"response_id": rec.id, "state": "received"})
            partner = rec.partner_id or rec.participant_id.partner_id
            if partner and partner not in case.partner_ids:
                case.write({"partner_ids": [(4, partner.id)]})
            if rec.close_open_pendings:
                case.pending_ids.filtered(lambda p: p.state == "open").write({"state": "done", "date_done": rec.response_date or fields.Date.today()})

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

    def action_start_review(self):
        self.write({"state": "in_review", "outcome": "pending_analysis"})
        if self.obligation_id:
            self.obligation_id.action_start_review()
        return True

    def action_mark_approved(self):
        self.write({"state": "approved", "outcome": "accepted"})
        if self.obligation_id:
            self.obligation_id.action_mark_fulfilled()
        return True

    def action_mark_partial(self):
        self.write({"state": "partial", "outcome": "pending_analysis"})
        if self.obligation_id:
            self.obligation_id.write({"state": "received"})
        return True

    def action_mark_rejected(self):
        self.write({"state": "rejected", "outcome": "rejected"})
        if self.obligation_id:
            self.obligation_id.action_mark_not_fulfilled()
        return True
