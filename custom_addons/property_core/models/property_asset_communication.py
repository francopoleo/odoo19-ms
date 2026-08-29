# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class PropertyAssetCommunication(models.Model):
    """
    Comunicação rastreável para imóveis.
    Implementa os mesmos campos de rastreamento de common.communication.base.
    """
    _name = 'property.asset.communication'
    _description = 'Comunicação de Imóvel'
    _inherit = 'mail.thread'
    _order = 'communication_date desc, id desc'

    # ==================== Rastreamento (de common.communication.base) ====================
    tracking_token = fields.Char(
        "Token de Rastreamento",
        copy=False,
        index=True,
        readonly=True,
        default=lambda self: str(__import__('uuid').uuid4())[:32],
        help="ID único para correlacionar emails, mensagens e documentos entre módulos"
    )
    email_message_id = fields.Many2one(
        "mail.message",
        string="Mensagem de E-mail",
        readonly=True,
        copy=False,
        ondelete="set null",
        index=True,
        help="Vinculação com sistema de email do Odoo"
    )
    external_message_id = fields.Char(
        "Message-ID Externo",
        readonly=True,
        copy=False,
        index=True,
        help="Message-ID do e-mail externo"
    )
    email_from = fields.Char("Remetente", readonly=True, copy=False)
    email_to = fields.Char("Destinatário", readonly=True, copy=False)
    email_cc = fields.Char("CC", readonly=True, copy=False)
    channel_type = fields.Selection([
        ('email', 'E-mail'),
        ('call', 'Ligação'),
        ('chat', 'Chat/Mensagem'),
        ('meeting', 'Reunião'),
        ('task', 'Tarefa'),
        ('document', 'Documento'),
    ], string="Tipo de Comunicação", default='email')
    channel_origin = fields.Char(
        "Canal de Origem",
        readonly=True,
        copy=False,
        default='property',
        help="Origem: property"
    )
    sent_by_odoo = fields.Boolean(
        "Enviado pelo Odoo",
        readonly=True,
        copy=False,
        default=True
    )
    communication_date = fields.Datetime(
        "Data da Comunicação",
        readonly=True,
        copy=False,
        default=fields.Datetime.now,
        index=True
    )

    # ==================== Relações ====================
    asset_id = fields.Many2one(
        'property.asset',
        string='Imóvel',
        required=True,
        ondelete='cascade',
        index=True,
        tracking=True
    )
    contract_id = fields.Many2one(
        'property.contract',
        string='Contrato',
        ondelete='set null',
        index=True,
        tracking=True,
        help='Contrato relacionado a esta comunicação'
    )

    # ==================== Básico ====================
    name = fields.Char(
        string='Assunto',
        required=True,
        tracking=True
    )
    description = fields.Html(
        string='Descrição',
        tracking=True
    )

    # ==================== Participantes ====================
    partner_id = fields.Many2one(
        'res.partner',
        string='Contato',
        tracking=True,
        help='Pessoa com quem houve a comunicação'
    )
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsável',
        default=lambda self: self.env.user,
        tracking=True
    )

    # ==================== Status ====================
    status = fields.Selection([
        ('draft', 'Rascunho'),
        ('registered', 'Registrada'),
    ], string='Status', default='registered', tracking=True)

    requires_action = fields.Boolean(
        string='Requer Ação',
        default=False,
        tracking=True
    )
    action_deadline = fields.Date(
        string='Prazo',
        help='Data limite para ação relacionada'
    )


    def _get_tracking_token(self):
        """Retorna o token de rastreamento, gerando um se não existir."""
        self.ensure_one()
        if not self.tracking_token:
            self.write({'tracking_token': str(__import__('uuid').uuid4())[:32]})
        return self.tracking_token

    def _normalize_subject(self, subject):
        """Remove prefixos de resposta/encaminhamento do assunto."""
        if not subject:
            return subject
        import re
        # Remove prefixos comuns: Re:, RE:, Fwd:, FWD:, Fw:, etc.
        cleaned = re.sub(r'^(Re|RE|Fwd|FWD|Fw|fwd|re|fw):\s*', '', subject).strip()
        return cleaned

    @api.model_create_multi
    def create(self, vals_list):
        # Define channel_origin e auto-link asset
        for vals in vals_list:
            if 'channel_origin' not in vals:
                vals['channel_origin'] = 'property'
            if 'sent_by_odoo' not in vals:
                vals['sent_by_odoo'] = True
            # Normalizar assunto removendo prefixos de resposta (Re:, Fwd:, etc)
            # Apenas para comunicações de saída (enviadas pelo Odoo)
            if 'name' in vals and vals.get('direction') == 'out':
                vals['name'] = self._normalize_subject(vals['name'])

        records = super().create(vals_list)
        return records

    def action_mark_done(self):
        """Marca a comunicação como concluída."""
        self.ensure_one()
        self.write({
            'status': 'registered',
            'requires_action': False,
        })
        self.message_post(body=_("Comunicação registrada."))

    def action_create_task(self):
        """Cria uma tarefa relacionada a esta comunicação."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Nova Tarefa'),
            'res_model': 'mail.activity',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_res_id': self.asset_id.id,
                'default_res_model': 'property.asset',
                'default_summary': _('Ação: %s') % self.name,
                'default_user_id': self.responsible_id.id,
            },
        }
