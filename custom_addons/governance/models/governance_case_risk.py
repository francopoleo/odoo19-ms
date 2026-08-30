from odoo import api, fields, models, _
from odoo.exceptions import UserError


class GovernanceCaseRisk(models.Model):
    _name = "governance.case.risk"
    _description = "Risco do Caso de Governança"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "risk_level desc, id desc"

    name = fields.Char(string="Risco", required=True, tracking=True)
    case_id = fields.Many2one("governance.case", string="Caso", required=True, ondelete="cascade", tracking=True)
    company_id = fields.Many2one(related="case_id.company_id", store=True, readonly=True)
    category = fields.Selection([
        ("legal", "Jurídico"), ("financial", "Financeiro"), ("operational", "Operacional"),
        ("documental", "Documental"), ("reputational", "Reputacional"), ("compliance", "Conformidade"),
        ("other", "Outro"),
    ], string="Categoria", required=True, default="operational", tracking=True)
    state = fields.Selection([
        ("identified", "Identificado"), ("assessing", "Em avaliação"), ("accepted", "Aceito"),
        ("treating", "Em tratamento"), ("mitigated", "Mitigado"), ("closed", "Encerrado"), ("reopened", "Reaberto"),
    ], string="Situação", default="identified", required=True, tracking=True)
    likelihood = fields.Selection([("1", "Baixa"), ("2", "Média"), ("3", "Alta")], string="Probabilidade", default="1", required=True)
    impact = fields.Selection([("1", "Baixo"), ("2", "Médio"), ("3", "Alto")], string="Impacto", default="1", required=True)
    risk_level = fields.Integer(string="Nível", compute="_compute_risk_level", store=True)
    owner_id = fields.Many2one("res.users", string="Responsável", required=True, default=lambda self: self.env.user, tracking=True)
    description = fields.Html(string="Descrição e causa")
    treatment_plan = fields.Html(string="Plano de tratamento")
    review_date = fields.Date(string="Próxima revisão", tracking=True)
    residual_risk = fields.Selection([("low", "Baixo"), ("medium", "Médio"), ("high", "Alto")], string="Risco residual")
    control_ids = fields.Many2many("governance.control", string="Controles relacionados")
    decision_id = fields.Many2one("governance.case.decision", string="Decisão de aceitação", ondelete="set null")

    @api.depends("likelihood", "impact")
    def _compute_risk_level(self):
        for record in self:
            record.risk_level = int(record.likelihood or 1) * int(record.impact or 1)

    def action_start_assessment(self):
        self.write({"state": "assessing"})
        return True

    def action_accept(self):
        for record in self:
            if record.risk_level >= 6 and (not record.decision_id or record.decision_id.state != "approved"):
                raise UserError(_("Risco alto ou crítico só pode ser aceito após decisão aprovada."))
        self.write({"state": "accepted"})
        return True

    def action_start_treatment(self):
        self.write({"state": "treating"})
        return True

    def action_mitigate(self):
        self.write({"state": "mitigated"})
        return True

    def action_close(self):
        self.write({"state": "closed"})
        return True

    def action_reopen(self):
        self.write({"state": "reopened"})
        return True
