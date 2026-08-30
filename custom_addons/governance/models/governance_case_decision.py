from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class GovernanceCaseDecision(models.Model):
    _name = "governance.case.decision"
    _description = "Decisão do Caso de Governança"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "decision_date desc, id desc"

    name = fields.Char(string="Decisão", required=True, tracking=True)
    case_id = fields.Many2one("governance.case", string="Caso", required=True, ondelete="cascade", tracking=True)
    company_id = fields.Many2one(related="case_id.company_id", store=True, readonly=True)
    decision_type = fields.Selection([
        ("accept", "Aceitar"), ("reject", "Rejeitar"), ("exception", "Aceitar exceção"),
        ("risk_acceptance", "Aceitar risco"), ("close", "Autorizar encerramento"), ("other", "Outra decisão"),
    ], string="Tipo", required=True, default="other", tracking=True)
    state = fields.Selection([
        ("draft", "Rascunho"), ("pending", "Aguardando aprovação"),
        ("approved", "Aprovada"), ("rejected", "Rejeitada"), ("cancelled", "Cancelada"),
    ], string="Situação", required=True, default="draft", tracking=True)
    requested_by_id = fields.Many2one("res.users", string="Solicitada por", default=lambda self: self.env.user, readonly=True)
    approver_id = fields.Many2one("res.users", string="Aprovador", tracking=True)
    decision_date = fields.Date(string="Data", default=fields.Date.today, required=True, tracking=True)
    rationale = fields.Html(string="Fundamentação", required=True)
    response_id = fields.Many2one("governance.case.response", string="Resposta analisada", ondelete="set null")
    evidence_document_ids = fields.Many2many("document.document", string="Evidências")

    @api.constrains("case_id", "response_id")
    def _check_case_links(self):
        for record in self:
            if record.response_id and record.response_id.case_id != record.case_id:
                raise ValidationError(_("A resposta precisa pertencer ao mesmo caso da decisão."))

    def action_submit(self):
        for record in self:
            if not record.rationale or not record.rationale.strip():
                raise UserError(_("A fundamentação é obrigatória para enviar uma decisão."))
            record.write({"state": "pending"})
        return True

    def action_approve(self):
        for record in self:
            if record.requested_by_id == self.env.user:
                raise UserError(_("A pessoa que solicitou a decisão não pode aprová-la."))
        self.write({"state": "approved", "approver_id": self.env.user.id, "decision_date": fields.Date.today()})
        return True

    def action_reject(self):
        self.write({"state": "rejected", "approver_id": self.env.user.id, "decision_date": fields.Date.today()})
        return True

    def action_cancel(self):
        self.write({"state": "cancelled"})
        return True

    def action_open_case(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "name": _("Caso"), "res_model": "governance.case", "res_id": self.case_id.id, "view_mode": "form"}
