# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GovernanceSlaRule(models.Model):
    _name = "governance.sla.rule"
    _description = "Regra de SLA de Governança"
    _order = "sequence, company_id, case_type_id, priority"
    _rec_name = "name"

    name = fields.Char(string="Nome", compute="_compute_name", store=True)
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativa", default=True)
    company_id = fields.Many2one("res.company", string="Empresa", index=True)
    case_type_id = fields.Many2one("governance.case.type", string="Tipo de Caso", index=True)
    priority = fields.Selection(
        [("0", "Baixo"), ("1", "Médio"), ("2", "Alto"), ("3", "Crítico")],
        string="Prioridade",
        default="1",
        required=True,
        index=True,
    )
    response_sla_days = fields.Integer(string="SLA de Resposta (dias)", default=2)
    resolution_sla_days = fields.Integer(string="SLA de Resolução (dias)", default=15)
    followup_days = fields.Integer(string="Follow-up após (dias)", default=0)
    auto_create_followup_activity = fields.Boolean(string="Criar Atividade de Follow-up")
    notes = fields.Text(string="Observações")

    @api.depends("company_id", "case_type_id", "priority", "response_sla_days", "resolution_sla_days")
    def _compute_name(self):
        priority_map = dict(self._fields["priority"].selection)
        for rule in self:
            parts = [rule.company_id.name if rule.company_id else _("Global")]
            parts.append(rule.case_type_id.name if rule.case_type_id else _("Todos os tipos"))
            parts.append(priority_map.get(rule.priority, rule.priority))
            parts.append(_("Resp. %sd / Res. %sd") % (rule.response_sla_days, rule.resolution_sla_days))
            rule.name = " / ".join(parts)

    @api.constrains("response_sla_days", "resolution_sla_days", "followup_days")
    def _check_positive_days(self):
        for rule in self:
            if rule.response_sla_days < 0 or rule.resolution_sla_days < 0 or rule.followup_days < 0:
                raise ValidationError(_("Os prazos de SLA não podem ser negativos."))

    @api.model
    def get_effective_rule(self, company=None, case_type=None, priority=None):
        domain = [("active", "=", True), ("priority", "=", priority or "1")]
        if company:
            domain += ["|", ("company_id", "=", False), ("company_id", "=", company.id)]
        else:
            domain += [("company_id", "=", False)]
        if case_type:
            domain += ["|", ("case_type_id", "=", False), ("case_type_id", "=", case_type.id)]
        else:
            domain += [("case_type_id", "=", False)]
        rules = self.search(domain)
        if not rules:
            return self.browse()
        def score(rule):
            return (
                10 if company and rule.company_id == company else 0,
                10 if case_type and rule.case_type_id == case_type else 0,
                -rule.sequence,
            )
        return max(rules, key=score)
