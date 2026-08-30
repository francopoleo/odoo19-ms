from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GovernanceCaseCommunication(models.Model):
    _name = "governance.case.communication"
    _description = "Comunicação do Caso de Governança"
    _inherit = ["mail.thread"]
    _order = "communication_datetime desc, id desc"

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
        default='governance',
        help="Origem: governance"
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

    name = fields.Char(string="Assunto", required=True, tracking=True)
    case_id = fields.Many2one("governance.case", string="Caso", required=True, ondelete="cascade", tracking=True)
    obligation_id = fields.Many2one("governance.case.obligation", string="Solicitação/Obrigação", ondelete="set null", tracking=True)
    response_id = fields.Many2one("governance.case.response", string="Resposta formal", ondelete="set null", tracking=True)
    company_id = fields.Many2one(related="case_id.company_id", store=True, readonly=True)
    communication_datetime = fields.Datetime(string="Data/Hora", default=fields.Datetime.now, required=True, tracking=True)
    communication_type = fields.Selection([
        ("notification", "Notificação"),
        ("email", "E-mail"),
        ("call", "Telefonema"),
        ("meeting", "Reunião"),
        ("message", "Mensagem"),
        ("response", "Resposta"),
        ("attempt", "Tentativa sem retorno"),
        ("other", "Outro"),
    ], string="Tipo", default="email", required=True, tracking=True)
    direction = fields.Selection([
        ("out", "Saída"),
        ("in", "Entrada"),
        ("internal", "Interna"),
    ], string="Direção", default="out", required=True, tracking=True)
    participant_id = fields.Many2one("governance.case.participant", string="Participante")
    partner_id = fields.Many2one("res.partner", string="Contato", tracking=True)
    responsible_id = fields.Many2one("res.users", string="Responsável", default=lambda self: self.env.user, tracking=True)
    note = fields.Html(string="Detalhes")
    requires_response = fields.Boolean(string="Exige Resposta")
    response_deadline = fields.Date(string="Prazo da Resposta")
    response_received = fields.Boolean(string="Resposta Recebida", tracking=True)
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("done", "Registrada"),
    ], string="Status", default="done", tracking=True)

    @api.constrains("case_id", "obligation_id", "response_id")
    def _check_related_case(self):
        for record in self:
            if record.obligation_id and record.obligation_id.case_id != record.case_id:
                raise ValidationError(_("A obrigação precisa pertencer ao mesmo caso da comunicação."))
            if record.response_id and record.response_id.case_id != record.case_id:
                raise ValidationError(_("A resposta precisa pertencer ao mesmo caso da comunicação."))

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

    @api.onchange("participant_id")
    def _onchange_participant_id(self):
        for rec in self:
            if rec.participant_id and not rec.partner_id:
                rec.partner_id = rec.participant_id.partner_id

    @api.model_create_multi
    def create(self, vals_list):
        # Define channel_origin como 'governance' e sent_by_odoo=True para criações locais
        for vals in vals_list:
            if 'channel_origin' not in vals:
                vals['channel_origin'] = 'governance'
            if 'sent_by_odoo' not in vals:
                vals['sent_by_odoo'] = True
            # Normalizar assunto removendo prefixos de resposta (Re:, Fwd:, etc)
            # Apenas para comunicações de saída (enviadas pelo Odoo)
            if 'name' in vals and vals.get('direction') == 'out':
                vals['name'] = self._normalize_subject(vals['name'])

        records = super().create(vals_list)
        records._sync_case_from_communication(on_create=True)
        return records

    def write(self, vals):
        res = super().write(vals)
        if any(k in vals for k in ["communication_datetime", "communication_type", "direction", "response_received", "case_id"]):
            self._sync_case_from_communication(on_create=False)
        return res

    def _sync_case_from_communication(self, on_create=False):
        sent_stage = self.env.ref("governance.stage_sent", raise_if_not_found=False)
        partial_stage = self.env.ref("governance.stage_partial", raise_if_not_found=False)
        for rec in self.filtered("case_id"):
            case = rec.case_id
            comm_date = fields.Date.to_date(rec.communication_datetime) if rec.communication_datetime else fields.Date.today()
            vals = {}
            if rec.direction == "out" and rec.communication_type in ("notification", "email"):
                if not case.email_sent_date or comm_date >= case.email_sent_date:
                    vals["email_sent_date"] = comm_date
                if sent_stage and case.stage_id.status == "planned":
                    vals["stage_id"] = sent_stage.id
            if rec.communication_type in ("attempt",) or (rec.direction == "out" and rec.communication_type in ("call", "message")):
                if not case.last_followup_date or comm_date >= case.last_followup_date:
                    vals["last_followup_date"] = comm_date
                if on_create:
                    vals["followup_count"] = (case.followup_count or 0) + 1
            if rec.direction == "in" or rec.communication_type == "response" or rec.response_received:
                if not case.response_date or comm_date >= case.response_date:
                    vals["response_date"] = comm_date
                if partial_stage and case.stage_id.status in ("waiting", "sent", "no_response"):
                    vals["stage_id"] = partial_stage.id
            if vals:
                case.write(vals)
            if rec.obligation_id and rec.response_received:
                rec.obligation_id.action_mark_received()
            partner = rec.partner_id or rec.participant_id.partner_id
            if partner and partner not in case.partner_ids:
                case.write({"partner_ids": [(4, partner.id)]})

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

    def action_register_response(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Registrar Resposta"),
            "res_model": "governance.case.response",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_case_id": self.case_id.id,
                "default_communication_id": self.id,
                "default_obligation_id": self.obligation_id.id,
                "default_participant_id": self.participant_id.id,
                "default_partner_id": self.partner_id.id,
                "default_responsible_id": self.responsible_id.id or self.env.user.id,
                "default_name": _("Resposta: %s") % self.name,
            },
        }

    def action_create_pending(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Nova Pendência"),
            "res_model": "governance.case.pending",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_case_id": self.case_id.id,
                "default_communication_id": self.id,
                "default_participant_id": self.participant_id.id,
                "default_partner_id": self.partner_id.id,
                "default_responsible_id": self.responsible_id.id or self.env.user.id,
                "default_name": _("Pendência: %s") % self.name,
            },
        }
