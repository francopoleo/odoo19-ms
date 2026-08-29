# -*- coding: utf-8 -*-
import logging
import uuid
from email.utils import parseaddr

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class GovernanceEmailTest(models.Model):
    _name = "governance.email.test"
    _description = "Teste de E-mail da Governança"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"
    _rec_name = "name"

    name = fields.Char(string="Nome do Teste", required=True, default=lambda self: self._default_name(), tracking=True)
    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        default=lambda self: self.env.company,
        required=True,
        index=True,
        tracking=True,
    )
    state = fields.Selection([
        ("draft", "Preparação"),
        ("case_ready", "Caso Preparado"),
        ("sent", "Enviado"),
        ("waiting_reply", "Aguardando Resposta"),
        ("received", "Resposta Recebida"),
        ("bounced", "Bounce/Falha Detectada"),
        ("failed", "Falhou"),
        ("done", "Concluído"),
    ], string="Status", default="draft", tracking=True, index=True)

    external_email = fields.Char(
        string="E-mail Externo para Teste",
        default="francopoleo@gmail.com",
        required=True,
        tracking=True,
        help="E-mail externo que receberá a mensagem de teste e deverá responder mantendo o assunto.",
    )
    outbound_email = fields.Char(
        string="E-mail de Saída Esperado",
        default="governance@ogie.com.br",
        required=True,
        tracking=True,
        help="Endereço institucional que deve aparecer como remetente/reply-to do teste.",
    )
    reply_to_email = fields.Char(
        string="Reply-To Esperado",
        default="governance@ogie.com.br",
        help="Endereço para onde a resposta deve voltar. Por padrão usa o mesmo e-mail de saída.",
    )
    test_token = fields.Char(string="Token do Teste", readonly=True, copy=False, index=True)
    subject = fields.Char(string="Assunto do Teste")
    body_html = fields.Html(string="Corpo Enviado")

    channel_id = fields.Many2one(
        "governance.email.channel",
        string="Canal de Governança",
        domain="[('company_id', 'in', [False, company_id]), ('active', '=', True)]",
        tracking=True,
        help="Canal usado para criar o caso de teste. Normalmente Governança Geral / governance.",
    )
    case_type_id = fields.Many2one(
        "governance.case.type",
        string="Tipo de Caso",
        related="channel_id.case_type_id",
        readonly=True,
        store=True,
    )
    case_id = fields.Many2one("governance.case", string="Caso de Teste", readonly=True, copy=False, tracking=True)
    sent_message_id = fields.Many2one("mail.message", string="Mensagem Chatter", readonly=True, copy=False)
    sent_mail_id = fields.Many2one("mail.mail", string="E-mail Técnico", readonly=True, copy=False)

    sent_datetime = fields.Datetime(string="Enviado em", readonly=True, copy=False)
    last_check_datetime = fields.Datetime(string="Última Verificação", readonly=True, copy=False)
    received_datetime = fields.Datetime(string="Resposta Detectada em", readonly=True, copy=False)
    bounce_datetime = fields.Datetime(string="Bounce Detectado em", readonly=True, copy=False)
    fetch_executed_datetime = fields.Datetime(string="Última Busca IMAP", readonly=True, copy=False)

    inbound_found = fields.Boolean(string="Resposta Encontrada", readonly=True, copy=False)
    bounce_found = fields.Boolean(string="Bounce Encontrado", readonly=True, copy=False)
    outbound_sent_ok = fields.Boolean(string="Envio OK", readonly=True, copy=False)
    mail_state = fields.Char(string="Estado Técnico do E-mail", readonly=True, copy=False)
    failure_reason = fields.Text(string="Motivo Técnico da Falha", readonly=True, copy=False)
    result_summary = fields.Html(string="Resultado Alcançado", readonly=True, copy=False)
    diagnostic_log = fields.Text(string="Log Técnico", readonly=True, copy=False)

    @api.model
    def _default_name(self):
        return _("Teste de E-mail Governance")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            token = vals.setdefault("test_token", self._generate_token())
            vals.setdefault("reply_to_email", vals.get("outbound_email") or "governance@ogie.com.br")
            vals.setdefault("subject", self._build_subject(token))
        records = super().create(vals_list)
        for record in records:
            if not record.body_html:
                record.body_html = record._build_body_html(record.test_token)
        return records

    def _build_subject(self, token):
        return _("[GOV-EMAIL-TEST %s] Teste de envio e recebimento") % token

    def _build_body_html(self, token):
        self.ensure_one()
        return """
            <p>Este é um teste automático do módulo <strong>Governança</strong>.</p>
            <p><strong>Token:</strong> %s</p>
            <p><strong>Destino externo:</strong> %s</p>
            <p><strong>Remetente esperado:</strong> %s</p>
            <p><strong>Reply-To esperado:</strong> %s</p>
            <hr/>
            <p>Para validar o fluxo de recebimento, responda este e-mail mantendo o assunto original.</p>
            <p>O Odoo deverá registrar a resposta no caso de teste ou detectar que ela criou um caso novo.</p>
        """ % (token, self.external_email or "", self.outbound_email or "", self.reply_to_email or self.outbound_email or "")

    @api.model
    def _generate_token(self):
        return uuid.uuid4().hex[:10].upper()

    def _normalize_subject(self, subject):
        """Remove prefixos de resposta/encaminhamento do assunto."""
        if not subject:
            return subject
        import re
        # Remove prefixos comuns: Re:, RE:, Fwd:, FWD:, Fw:, etc.
        cleaned = re.sub(r'^(Re|RE|Fwd|FWD|Fw|fwd|re|fw):\s*', '', subject).strip()
        return cleaned

    def _append_log(self, message):
        self.ensure_one()
        now = fields.Datetime.to_string(fields.Datetime.now())
        current = self.diagnostic_log or ""
        self.diagnostic_log = "%s[%s] %s\n" % (current, now, message)

    def _find_default_channel(self):
        Channel = self.env["governance.email.channel"]
        domain = [("active", "=", True)]
        if self.company_id:
            domain += [("company_id", "=", self.company_id.id)]
        channel = Channel.search(domain + [("alias_name", "=", "governance")], limit=1)
        if not channel:
            channel = Channel.search(domain, order="sequence, id", limit=1)
        return channel

    def _get_or_create_external_partner(self):
        self.ensure_one()
        name, email = parseaddr(self.external_email or "")
        if not email:
            raise UserError(_("Informe um e-mail externo válido para o teste."))
        Partner = self.env["res.partner"].sudo()
        partner = Partner.search([("email", "=ilike", email)], limit=1)
        if not partner:
            partner = Partner.create({"name": name or email, "email": email})
        return partner

    def action_prepare_case(self):
        for rec in self:
            if not rec.channel_id:
                rec.channel_id = rec._find_default_channel()
            if not rec.channel_id:
                raise UserError(_("Nenhum canal de e-mail ativo encontrado. Cadastre o canal governance antes do teste."))
            if not rec.test_token:
                rec.test_token = rec._generate_token()
            if not rec.subject:
                rec.subject = rec._build_subject(rec.test_token)
            if not rec.body_html:
                rec.body_html = rec._build_body_html(rec.test_token)
            vals = {
                "name": rec.subject,
                "description": rec.body_html,
                "email_channel_id": rec.channel_id.id,
                "message_origin": "system",
                "requires_triage": rec.channel_id.requires_triage,
                "priority": rec.channel_id.priority or "1",
                "responsible_id": rec.channel_id.responsible_id.id or self.env.user.id,
            }
            if "company_id" in self.env["governance.case"]._fields:
                vals["company_id"] = rec.company_id.id
            if rec.channel_id.case_type_id:
                vals["case_type_id"] = rec.channel_id.case_type_id.id
            case = self.env["governance.case"].sudo().create(vals)
            rec.case_id = case.id
            rec.state = "case_ready"
            rec._append_log(_("Caso de teste criado: %s") % case.display_name)
            case.message_post(body=_("Caso criado para teste de e-mail. Token: %s") % rec.test_token)
        return True

    def _create_or_send_mail(self):
        self.ensure_one()
        partner = self._get_or_create_external_partner()
        case = self.case_id
        if not case:
            raise UserError(_("Prepare o caso de teste antes de enviar."))
        if not self.outbound_email:
            raise UserError(_("Informe o e-mail de saída esperado."))
        if not self.reply_to_email:
            self.reply_to_email = self.outbound_email

        body = self.body_html or ""
        subject = self.subject or (_("[GOV-EMAIL-TEST %s] Teste de envio e recebimento") % self.test_token)

        message = case.sudo().message_post(
            body=body,
            subject=subject,
            message_type="comment",
            subtype_xmlid="mail.mt_comment",
            email_from=self.outbound_email,
            reply_to=self.reply_to_email,
        )
        self.sent_message_id = message.id

        Mail = self.env["mail.mail"].sudo()
        mail_vals = {
            "subject": subject,
            "body_html": body,
            "email_from": self.outbound_email,
            "email_to": partner.email,
            "reply_to": self.reply_to_email,
            "auto_delete": False,
        }
        for key, value in {
            "model": "governance.case",
            "res_id": case.id,
            "mail_message_id": message.id,
        }.items():
            if key in Mail._fields:
                mail_vals[key] = value
        mail = Mail.create(mail_vals)
        self.sent_mail_id = mail.id
        try:
            mail.send(raise_exception=True)
            self.outbound_sent_ok = True
            self.mail_state = mail.state or "sent"
            self.sent_datetime = fields.Datetime.now()
            self.state = "waiting_reply"
            self._append_log(_("E-mail enviado para %s usando remetente %s.") % (partner.email, self.outbound_email))
        except Exception as exc:
            _logger.exception("Falha no envio do teste de e-mail da governança")
            self.outbound_sent_ok = False
            self.mail_state = mail.state or "exception"
            self.failure_reason = str(exc)
            self.state = "failed"
            self._append_log(_("Falha no envio: %s") % exc)
        return mail

    def action_send_test_email(self):
        for rec in self:
            if not rec.case_id:
                rec.action_prepare_case()
            rec._create_or_send_mail()
            rec.action_check_results()
        return True

    def action_fetch_incoming_mail(self):
        try:
            FetchServer = self.env["fetchmail.server"]
        except KeyError:
            FetchServer = False
        for rec in self:
            if not FetchServer:
                rec._append_log(_("Modelo fetchmail.server não encontrado. O módulo fetchmail pode não estar instalado."))
                continue
            servers = FetchServer.sudo().search([("active", "=", True)])
            if not servers:
                rec._append_log(_("Nenhum servidor de entrada ativo encontrado."))
                continue
            ok = 0
            for server in servers:
                try:
                    server.fetch_mail()
                    ok += 1
                    rec._append_log(_("Busca executada no servidor de entrada: %s") % server.display_name)
                except Exception as exc:
                    _logger.exception("Falha ao buscar e-mails no servidor %s", server.display_name)
                    rec._append_log(_("Falha ao buscar no servidor %s: %s") % (server.display_name, exc))
            rec.fetch_executed_datetime = fields.Datetime.now()
            rec._append_log(_("Busca IMAP finalizada. Servidores executados com sucesso: %s/%s") % (ok, len(servers)))
        return True

    def _search_token_in_mail_messages(self, token):
        Message = self.env["mail.message"].sudo()
        domain = ["|", ("subject", "ilike", token), ("body", "ilike", token)]
        return Message.search(domain, order="date desc, id desc", limit=20)

    def _search_token_in_communications(self, token):
        Communication = self.env["governance.case.communication"].sudo()
        # Procura tanto pelo token quanto comparando assuntos normalizados
        comms = Communication.search(["|", ("name", "ilike", token), ("note", "ilike", token)], order="communication_datetime desc, id desc", limit=20)

        # Filtra também por correspondência de assunto normalizado
        if self.subject:
            normalized_search = self._normalize_subject(self.subject)
            if normalized_search and normalized_search != self.subject:
                extra_comms = Communication.search([("name", "ilike", normalized_search)], order="communication_datetime desc", limit=20)
                comms = comms | extra_comms

        return comms

    def action_check_results(self):
        for rec in self:
            if not rec.test_token:
                raise UserError(_("Este teste não possui token."))
            rec.last_check_datetime = fields.Datetime.now()
            token = rec.test_token
            log_lines = []

            # Estado técnico do e-mail enviado
            if rec.sent_mail_id:
                rec.sent_mail_id.invalidate_recordset()
                rec.mail_state = rec.sent_mail_id.state or ""
                failure = ""
                for field_name in ("failure_reason", "failure_type"):
                    if field_name in rec.sent_mail_id._fields and rec.sent_mail_id[field_name]:
                        failure = "%s%s: %s\n" % (failure, field_name, rec.sent_mail_id[field_name])
                if failure:
                    rec.failure_reason = failure
                if rec.sent_mail_id.state == "exception":
                    rec.bounce_found = True
                    rec.bounce_datetime = rec.bounce_datetime or fields.Datetime.now()
                    rec.state = "bounced"
                    log_lines.append(_("Falha técnica detectada no mail.mail."))

            messages = rec._search_token_in_mail_messages(token)
            communications = rec._search_token_in_communications(token)

            inbound_comm = communications.filtered(lambda c: c.direction == "in" and (not rec.case_id or c.case_id == rec.case_id))[:1]
            inbound_msg = messages.filtered(lambda m: m.model == "governance.case" and m.res_id == rec.case_id.id and m.id != rec.sent_message_id.id)[:1] if rec.case_id else self.env["mail.message"].sudo().browse()

            if inbound_comm or inbound_msg:
                rec.inbound_found = True
                rec.received_datetime = rec.received_datetime or fields.Datetime.now()
                if rec.state not in ("bounced", "failed"):
                    rec.state = "received"
                log_lines.append(_("Resposta localizada no caso de teste."))

            # Caso a resposta tenha criado um novo caso por roteamento de alias, também mostrar isso.
            Case = self.env["governance.case"].sudo()
            extra_cases = Case.search([("id", "!=", rec.case_id.id or 0), "|", ("name", "ilike", token), ("description", "ilike", token)], limit=10)
            if extra_cases:
                rec.inbound_found = True
                rec.received_datetime = rec.received_datetime or fields.Datetime.now()
                log_lines.append(_("A resposta/entrada foi encontrada, mas criou outro caso: %s") % ", ".join(extra_cases.mapped("display_name")))

            bounce_keywords = ("undelivered", "delivery status", "mail delivery", "failure", "returned mail", "não entregue", "falha", "bounce")
            bounce_messages = messages.filtered(lambda m: any(k in ((m.subject or "") + " " + (m.body or "")).lower() for k in bounce_keywords))
            if bounce_messages:
                rec.bounce_found = True
                rec.bounce_datetime = rec.bounce_datetime or fields.Datetime.now()
                rec.state = "bounced"
                log_lines.append(_("Mensagem de bounce/falha localizada com o token do teste."))

            if rec.outbound_sent_ok and not rec.inbound_found and not rec.bounce_found:
                rec.state = "waiting_reply"
                log_lines.append(_("E-mail enviado; ainda não foi localizada resposta nem bounce."))
            elif rec.inbound_found and not rec.bounce_found:
                rec.state = "done"

            rec._set_result_summary(messages, communications, extra_cases if 'extra_cases' in locals() else self.env["governance.case"].browse())
            for line in log_lines:
                rec._append_log(line)
        return True

    def action_fetch_and_check(self):
        self.action_fetch_incoming_mail()
        self.action_check_results()
        return True

    def _set_result_summary(self, messages, communications, extra_cases):
        self.ensure_one()
        case_link = self.case_id.display_name if self.case_id else _("Não criado")
        summary = """
            <div class="o_governance_email_test_result">
                <h3>Resultado do Teste</h3>
                <ul>
                    <li><strong>Token:</strong> %s</li>
                    <li><strong>Remetente esperado:</strong> %s</li>
                    <li><strong>Destino externo:</strong> %s</li>
                    <li><strong>Caso:</strong> %s</li>
                    <li><strong>Estado técnico do e-mail:</strong> %s</li>
                    <li><strong>Envio OK:</strong> %s</li>
                    <li><strong>Resposta encontrada:</strong> %s</li>
                    <li><strong>Bounce/falha encontrada:</strong> %s</li>
                    <li><strong>Mensagens com token:</strong> %s</li>
                    <li><strong>Comunicações com token:</strong> %s</li>
                    <li><strong>Casos adicionais com token:</strong> %s</li>
                </ul>
            </div>
        """ % (
            self.test_token or "",
            self.outbound_email or "",
            self.external_email or "",
            case_link,
            self.mail_state or "",
            _("Sim") if self.outbound_sent_ok else _("Não"),
            _("Sim") if self.inbound_found else _("Não"),
            _("Sim") if self.bounce_found else _("Não"),
            len(messages),
            len(communications),
            len(extra_cases),
        )
        if self.failure_reason:
            summary += "<p><strong>Falha técnica:</strong><br/>%s</p>" % (self.failure_reason or "")
        self.result_summary = summary

    def action_open_case(self):
        self.ensure_one()
        if not self.case_id:
            raise UserError(_("Nenhum caso de teste foi criado ainda."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Caso de Teste"),
            "res_model": "governance.case",
            "res_id": self.case_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_reset_test(self):
        for rec in self:
            rec.write({
                "state": "draft",
                "test_token": rec._generate_token(),
                "case_id": False,
                "sent_message_id": False,
                "sent_mail_id": False,
                "sent_datetime": False,
                "last_check_datetime": False,
                "received_datetime": False,
                "bounce_datetime": False,
                "fetch_executed_datetime": False,
                "inbound_found": False,
                "bounce_found": False,
                "outbound_sent_ok": False,
                "mail_state": False,
                "failure_reason": False,
                "result_summary": False,
                "diagnostic_log": False,
            })
            rec.subject = rec._build_subject(rec.test_token)
            rec.body_html = rec._build_body_html(rec.test_token)
        return True
