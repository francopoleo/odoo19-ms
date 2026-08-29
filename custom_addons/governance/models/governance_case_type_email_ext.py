# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class GovernanceCaseType(models.Model):
    _inherit = "governance.case.type"

    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        index=True,
        help="Deixe vazio para tipo global. Preencha quando o tipo pertencer a uma empresa específica.",
    )
    default_responsible_id = fields.Many2one(
        "res.users",
        string="Responsável Padrão",
        help="Responsável sugerido para casos deste tipo. Pode ser sobrescrito no caso.",
    )

    response_sla_days = fields.Integer(
        string="SLA de Resposta Padrão (dias)",
        default=2,
        help="Prazo padrão de resposta para este tipo. Usado como fallback quando não houver regra específica em Regras de SLA.",
    )
    resolution_sla_days = fields.Integer(
        string="SLA de Resolução Padrão (dias)",
        default=15,
        help="Prazo padrão de resolução para este tipo. Usado como fallback quando não houver regra específica em Regras de SLA.",
    )
    followup_sla_days = fields.Integer(
        string="Follow-up Padrão (dias)",
        default=0,
        help="Prazo padrão de follow-up para este tipo. Mantém compatibilidade com telas de SLA e evita duplicidade de regra operacional.",
    )

    # Compatibilidade com telas anteriores que configuravam SLA por prioridade no Tipo de Caso.
    # A regra efetiva continua sendo governance.sla.rule; estes campos são fallback/default.
    sla_low_days = fields.Integer(
        string="SLA Baixo (dias)",
        default=30,
        help="Fallback para prioridade Baixa quando não houver regra específica de SLA.",
    )
    sla_medium_days = fields.Integer(
        string="SLA Médio (dias)",
        default=15,
        help="Fallback para prioridade Média quando não houver regra específica de SLA.",
    )
    sla_high_days = fields.Integer(
        string="SLA Alto (dias)",
        default=7,
        help="Fallback para prioridade Alta quando não houver regra específica de SLA.",
    )
    sla_critical_days = fields.Integer(
        string="SLA Crítico (dias)",
        default=3,
        help="Fallback para prioridade Crítica quando não houver regra específica de SLA.",
    )


    # Configurações de e-mail por tipo de caso.
    # Mantém o tipo de caso como regra de negócio, enquanto o canal de e-mail permanece apenas como porta de entrada.

    default_email_alias = fields.Char(
        string="Alias de E-mail Padrão",
        help="Alias legado/sugerido para este tipo de caso. A configuração operacional deve ficar em Canais de E-mail.",
    )
    default_email_from = fields.Char(
        string="Remetente Padrão",
        help="Remetente sugerido para comunicações deste tipo, quando aplicável.",
    )
    default_email_reply_to = fields.Char(
        string="Responder Para Padrão",
        help="Endereço de resposta sugerido. Use preferencialmente o canal institucional.",
    )
    default_email_to = fields.Char(
        string="Destinatário Padrão",
        help="Destinatário sugerido para comunicações recorrentes deste tipo, quando aplicável.",
    )

    email_subject_prefix = fields.Char(
        string="Prefixo do Assunto",
        help="Prefixo sugerido para assuntos de e-mail deste tipo de caso. Ex.: [Jurídico], [Documental].",
    )
    email_template_id = fields.Many2one(
        "mail.template",
        string="Modelo de E-mail Padrão",
        domain="[('model', '=', 'governance.case')]",
        help="Modelo padrão usado ao enviar comunicação formal a partir de casos deste tipo.",
    )
    email_default_cc = fields.Char(
        string="CC Padrão",
        help="Destinatários em cópia sugeridos para comunicações deste tipo. Separe múltiplos e-mails por vírgula.",
    )
    email_default_body = fields.Html(
        string="Corpo Padrão de E-mail",
        help="Texto base sugerido para comunicações formais deste tipo de caso.",
    )
    require_email_response = fields.Boolean(
        string="Exigir Resposta por E-mail",
        help="Indica que casos deste tipo normalmente exigem resposta formal por e-mail antes da conclusão.",
    )

    email_channel_ids = fields.One2many(
        "governance.email.channel",
        "case_type_id",
        string="Canais de E-mail",
    )
    email_channel_count = fields.Integer(
        string="Qtd Canais",
        compute="_compute_email_channel_count",
    )

    @api.depends("email_channel_ids")
    def _compute_email_channel_count(self):
        for rec in self:
            rec.email_channel_count = len(rec.email_channel_ids)

    def action_open_email_channels(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Canais de E-mail"),
            "res_model": "governance.email.channel",
            "view_mode": "list,form",
            "domain": [("case_type_id", "=", self.id)],
            "context": {"default_case_type_id": self.id},
        }


    @api.constrains("response_sla_days", "resolution_sla_days", "followup_sla_days", "sla_low_days", "sla_medium_days", "sla_high_days", "sla_critical_days")
    def _check_sla_defaults_non_negative(self):
        for rec in self:
            if any(v < 0 for v in [rec.response_sla_days, rec.resolution_sla_days, rec.followup_sla_days, rec.sla_low_days, rec.sla_medium_days, rec.sla_high_days, rec.sla_critical_days]):
                from odoo.exceptions import ValidationError
                raise ValidationError(_("Os prazos padrão de SLA não podem ser negativos."))

    @api.onchange("resolution_sla_days")
    def _onchange_resolution_sla_days_sync_legacy(self):
        for rec in self:
            if rec.resolution_sla_days and not rec.sla_days:
                rec.sla_days = rec.resolution_sla_days

    @api.onchange("followup_sla_days")
    def _onchange_followup_sla_days_sync_legacy(self):
        for rec in self:
            if rec.followup_sla_days and not rec.auto_followup_days:
                rec.auto_followup_days = rec.followup_sla_days
