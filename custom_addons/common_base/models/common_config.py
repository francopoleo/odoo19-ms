from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CommonConfig(models.Model):
    """
    Configurações por empresa (singleton por empresa).
    Cada empresa tem o seu próprio registro de configuração.
    Acessível via Configurações > Geral.
    """
    _name = "common.config"
    _description = "Configurações Gerais"

    name = fields.Char(default="Configurações Gerais", readonly=True)

    company_id = fields.Many2one(
        'res.company',
        string="Empresa",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )

    # ========== CONFIGURAÇÕES DE GOVERNANÇA ==========
    governance_followup_days = fields.Integer(
        string="Dias para Follow-up",
        default=3,
        help="Dias após envio para primeiro follow-up"
    )

    governance_reminder_days = fields.Integer(
        string="Dias para Lembrete",
        default=7,
        help="Dias após follow-up para lembrete"
    )

    governance_silence_days = fields.Integer(
        string="Dias para Silêncio",
        default=15,
        help="Dias sem resposta para marcar como silêncio"
    )

    # ========== CONFIGURAÇÕES DE FINANCEIRO ==========
    default_late_fee = fields.Float(
        string="Multa Padrão (%)",
        default=2.0,
        help="Percentual padrão de multa por atraso"
    )

    default_interest_per_day = fields.Float(
        string="Juros por Dia (%)",
        default=0.033,
        help="Juros diários padrão por atraso"
    )

    # ========== CONFIGURAÇÕES DE NOTIFICAÇÃO ==========
    enable_auto_followup = fields.Boolean(
        string="Ativar Follow-up Automático",
        default=True,
        help="Cria atividades de follow-up automaticamente"
    )

    enable_email_notifications = fields.Boolean(
        string="Ativar Notificações por E-mail",
        default=True,
        help="Envia notificações por e-mail automaticamente"
    )

    _company_unique = models.Constraint(
        'UNIQUE(company_id)',
        'Apenas um registro de configuração por empresa é permitido.',
    )

    def unlink(self):
        raise ValidationError("O registro de configuração geral não pode ser removido.")

    @api.model
    def get_config(self):
        """Retorna as configurações da empresa atual (cria se não existir)."""
        company = self.env.company
        config = self.sudo().search([('company_id', '=', company.id)], limit=1)
        if not config:
            config = self.sudo().create({'company_id': company.id})
        return config