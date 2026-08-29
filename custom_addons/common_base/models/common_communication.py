# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import uuid
import logging

_logger = logging.getLogger(__name__)


class CommonCommunicationBase(models.AbstractModel):
    """
    Base abstrata para comunicações rastreáveis em todos os módulos.
    Permite correlacionar emails, mensagens e documentos através de um token único.

    Herdada por:
    - governance.case.communication
    - property.asset.communication
    - document.communication

    NOTA: Os campos Many2many são adicionados nos modelos concretos para evitar
    dependências circulares. Este modelo abstrato contém apenas campos genéricos.
    """
    _name = 'common.communication.base'
    _description = 'Base para Comunicações Rastreáveis'

    # ==================== Rastreamento ====================
    tracking_token = fields.Char(
        "Token de Rastreamento",
        copy=False,
        index=True,
        readonly=True,
        default=lambda self: str(uuid.uuid4())[:32],
        help="ID único para correlacionar emails, mensagens e documentos entre módulos"
    )

    # ==================== Email ====================
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
        help="Message-ID do e-mail externo (para correlação com servidores IMAP/SMTP)"
    )
    email_from = fields.Char("Remetente", readonly=True, copy=False)
    email_to = fields.Char("Destinatário", readonly=True, copy=False)
    email_cc = fields.Char("CC", readonly=True, copy=False)

    # ==================== Canal ====================
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
        help="Identifica o módulo/canal de origem: 'governance', 'property_support', 'document_upload', etc."
    )

    # ==================== Metadados ====================
    sent_by_odoo = fields.Boolean(
        "Enviado pelo Odoo",
        readonly=True,
        copy=False,
        help="Indica se a comunicação foi originada no Odoo ou importada de fonte externa"
    )
    communication_date = fields.Datetime(
        "Data da Comunicação",
        readonly=True,
        copy=False,
        default=fields.Datetime.now,
        index=True
    )

    def _get_tracking_token(self):
        """Retorna o token de rastreamento, gerando um se não existir."""
        self.ensure_one()
        if not self.tracking_token:
            self.write({'tracking_token': str(uuid.uuid4())[:32]})
        return self.tracking_token