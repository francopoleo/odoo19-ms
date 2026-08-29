# -*- coding: utf-8 -*-
from email.utils import parseaddr
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GovernanceCase(models.Model):
    _inherit = "governance.case"

    email_channel_id = fields.Many2one(
        "governance.email.channel",
        string="Canal de E-mail",
        tracking=True,
        index=True,
        help="Canal institucional que originou ou roteou este caso.",
    )
    message_origin = fields.Selection(
        [("manual", "Manual"), ("email", "E-mail"), ("portal", "Portal"), ("system", "Sistema")],
        string="Origem",
        default="manual",
        tracking=True,
        index=True,
    )
    requires_triage = fields.Boolean(string="Exige Triagem", tracking=True)
    triage_done = fields.Boolean(string="Triagem Concluída", tracking=True)
    triage_notes = fields.Html(string="Notas de Triagem")

    incoming_email_from = fields.Char(string="Remetente Original", readonly=True, copy=False)
    incoming_email_to = fields.Char(string="Destinatário Original", readonly=True, copy=False)
    incoming_email_cc = fields.Char(string="Cópias Originais", readonly=True, copy=False)
    last_inbound_email_datetime = fields.Datetime(string="Último E-mail Recebido", readonly=True, copy=False)
    last_outbound_email_datetime = fields.Datetime(string="Último E-mail Enviado", readonly=True, copy=False)

    response_sla_days = fields.Integer(
        string="SLA de Resposta (dias)",
        compute="_compute_email_sla_rule_fields",
        store=True,
        readonly=True,
        help="Prazo efetivo de resposta aplicado pela regra de SLA do tipo de caso/prioridade.",
    )
    resolution_sla_days = fields.Integer(
        string="SLA de Resolução (dias)",
        compute="_compute_email_sla_rule_fields",
        store=True,
        readonly=True,
        help="Prazo efetivo de resolução aplicado pela regra de SLA do tipo de caso/prioridade.",
    )
    followup_sla_days = fields.Integer(
        string="Follow-up por SLA (dias)",
        compute="_compute_email_sla_rule_fields",
        store=True,
        readonly=True,
        help="Prazo efetivo para follow-up aplicado pela regra de SLA do tipo de caso/prioridade.",
    )

    effective_sla_rule_id = fields.Many2one(
        "governance.sla.rule",
        string="Regra de SLA Efetiva",
        compute="_compute_email_sla_rule_fields",
        store=True,
        readonly=True,
        copy=False,
        help="Regra de SLA aplicada automaticamente conforme empresa, tipo de caso e prioridade.",
    )


    def _get_effective_sla_rule(self):
        self.ensure_one()
        return self.env["governance.sla.rule"].get_effective_rule(
            company=self.company_id if "company_id" in self._fields else False,
            case_type=self.case_type_id,
            priority=self.priority,
        )

    @api.depends("priority", "case_type_id", "case_type_id.sla_days", "company_id")
    def _compute_email_sla_rule_fields(self):
        fallback_map = {"0": 30, "1": 15, "2": 7, "3": 3}
        config = self.env["common.config"].get_config()
        for case in self:
            rule = case._get_effective_sla_rule()
            case.effective_sla_rule_id = rule.id if rule else False
            if rule:
                case.response_sla_days = rule.response_sla_days
                case.resolution_sla_days = rule.resolution_sla_days
                case.followup_sla_days = rule.followup_days
            else:
                effective_priority = case.priority or case.case_type_id.default_priority or "1"
                case.response_sla_days = case.case_type_id.response_sla_days or config.governance_silence_days or 0
                type_priority_map = {
                    "0": case.case_type_id.sla_low_days,
                    "1": case.case_type_id.sla_medium_days,
                    "2": case.case_type_id.sla_high_days,
                    "3": case.case_type_id.sla_critical_days,
                } if case.case_type_id else {}
                case.resolution_sla_days = case.case_type_id.resolution_sla_days or case.case_type_id.sla_days or type_priority_map.get(effective_priority) or fallback_map.get(effective_priority, 15)
                case.followup_sla_days = case.case_type_id.followup_sla_days or case.case_type_id.auto_followup_days or 0

    @api.depends("priority", "case_type_id", "case_type_id.sla_days", "company_id")
    def _compute_sla_days(self):
        fallback_map = {"0": 30, "1": 15, "2": 7, "3": 3}
        for case in self:
            rule = case._get_effective_sla_rule()
            if rule:
                case.sla_days = rule.resolution_sla_days
            elif case.case_type_id and case.case_type_id.sla_days:
                case.sla_days = case.case_type_id.sla_days
            else:
                effective_priority = case.priority or case.case_type_id.default_priority or "1"
                case.sla_days = fallback_map.get(effective_priority, 15)

    @api.depends("origin_date", "priority", "case_type_id", "company_id")
    def _compute_response_deadline(self):
        config = self.env["common.config"].get_config()
        for case in self:
            if not case.origin_date:
                case.response_deadline = False
                continue
            rule = case._get_effective_sla_rule()
            days = rule.response_sla_days if rule else config.governance_silence_days
            case.response_deadline = case.origin_date + timedelta(days=days)

    @api.onchange("email_channel_id")
    def _onchange_email_channel_id_apply_defaults(self):
        for case in self:
            channel = case.email_channel_id
            if not channel:
                continue
            case.message_origin = "email"
            case.requires_triage = channel.requires_triage
            if channel.auto_assign_type and channel.case_type_id:
                case.case_type_id = channel.case_type_id
            if channel.priority and not case.priority:
                case.priority = channel.priority
            if channel.responsible_id and not case.responsible_id:
                case.responsible_id = channel.responsible_id
            if "company_id" in case._fields and channel.company_id and not case.company_id:
                case.company_id = channel.company_id
            if channel.allowed_case_type_ids:
                return {"domain": {"case_type_id": [("id", "in", channel.allowed_case_type_ids.ids)]}}

    @api.constrains("email_channel_id", "case_type_id", "company_id")
    def _check_email_channel_case_type_consistency(self):
        for case in self:
            channel = case.email_channel_id
            if not channel:
                continue
            if "company_id" in case._fields and case.company_id and channel.company_id and case.company_id != channel.company_id:
                raise ValidationError(_("A empresa do caso precisa ser a mesma do canal de e-mail."))
            if channel.allowed_case_type_ids and case.case_type_id and case.case_type_id not in channel.allowed_case_type_ids:
                raise ValidationError(_("O tipo de caso selecionado não é permitido para este canal de e-mail."))

    def _apply_case_type_defaults_to_vals(self, vals):
        case_type = self.env["governance.case.type"].browse(vals.get("case_type_id")).exists() if vals.get("case_type_id") else False
        if not case_type:
            return vals
        vals.setdefault("priority", case_type.default_priority or "1")
        if "default_responsible_id" in case_type._fields and case_type.default_responsible_id:
            vals.setdefault("responsible_id", case_type.default_responsible_id.id)
        if case_type.initial_stage_id:
            vals.setdefault("stage_id", case_type.initial_stage_id.id)
        return vals

    def _apply_email_channel_defaults_to_vals(self, vals):
        channel_id = vals.get("email_channel_id") or self.env.context.get("default_email_channel_id")
        channel = self.env["governance.email.channel"].browse(channel_id).exists() if channel_id else False
        if not channel:
            return vals
        for key, value in channel._prepare_case_defaults().items():
            vals.setdefault(key, value)
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._apply_email_channel_defaults_to_vals(vals)
            self._apply_case_type_defaults_to_vals(vals)
        records = super().create(vals_list)
        return records

    def write(self, vals):
        write_vals = dict(vals)
        if len(self) == 1:
            if "email_channel_id" in write_vals:
                self._apply_email_channel_defaults_to_vals(write_vals)
            if "case_type_id" in write_vals:
                self._apply_case_type_defaults_to_vals(write_vals)
        return super().write(write_vals)

    @api.model
    def _get_email_channel_from_message(self, msg_dict, custom_values=None):
        custom_values = custom_values or {}
        channel = self.env["governance.email.channel"].browse(custom_values.get("email_channel_id")).exists() if custom_values.get("email_channel_id") else False
        if channel:
            return channel
        return self.env["governance.email.channel"]._find_by_message_recipients(msg_dict)

    @api.model
    def _get_or_create_partner_from_email(self, email_from):
        """Mantido por compatibilidade. Internamente usa resolve_contact."""
        if not email_from:
            return self.env["res.partner"].browse()
        partner, _source, _confidence, _created = (
            self.env["res.partner"].sudo().resolve_contact(email=email_from)
        )
        return partner

    def _register_email_communication_from_message(self, msg_dict, direction="in", channel=None):
        Communication = self.env["governance.case.communication"].sudo()
        Participant = self.env["governance.case.participant"].sudo()
        for case in self:
            subject = msg_dict.get("subject") or _("E-mail sem assunto")
            body = msg_dict.get("body") or msg_dict.get("text") or ""
            email_from = msg_dict.get("email_from") or msg_dict.get("from") or ""

            partner = self.env["res.partner"].browse()
            match_source = False
            match_confidence = 0
            if direction == "in" and email_from:
                partner, match_source, match_confidence, _created = (
                    self.env["res.partner"].sudo().resolve_contact(email=email_from)
                )

            Communication.create({
                "case_id": case.id,
                "name": subject,
                "communication_type": "email",
                "direction": direction,
                "partner_id": partner.id if partner else False,
                "partner_match_source": match_source or False,
                "partner_match_confidence": match_confidence,
                "responsible_id": case.responsible_id.id or self.env.user.id,
                "note": body,
                "requires_response": bool(channel.require_response_by_default) if channel else False,
                "status": "done",
                "external_message_id": msg_dict.get("message_id") or msg_dict.get("Message-Id") or False,
                "email_from": email_from,
                "email_to": msg_dict.get("to") or msg_dict.get("email_to") or False,
                "email_cc": msg_dict.get("cc") or False,
            })
            if direction == "in" and partner and (not channel or channel.auto_add_sender_as_participant):
                exists = Participant.search([("case_id", "=", case.id), ("partner_id", "=", partner.id)], limit=1)
                if not exists:
                    Participant.create({
                        "case_id": case.id,
                        "partner_id": partner.id,
                        "role": "claimant" if not case.participant_ids else "other",
                        "is_primary": not bool(case.primary_partner_id),
                        "note": _("Adicionado automaticamente por e-mail recebido."),
                    })
            vals = {"last_inbound_email_datetime": fields.Datetime.now()}
            if email_from and not case.incoming_email_from:
                vals["incoming_email_from"] = email_from
            if msg_dict.get("to") and not case.incoming_email_to:
                vals["incoming_email_to"] = msg_dict.get("to")
            if msg_dict.get("cc") and not case.incoming_email_cc:
                vals["incoming_email_cc"] = msg_dict.get("cc")
            case.sudo().write(vals)
        return True

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        custom_values = dict(custom_values or {})
        channel = self._get_email_channel_from_message(msg_dict, custom_values=custom_values)
        if channel and not channel.create_case_from_email:
            return super().message_new(msg_dict, custom_values=custom_values)

        custom_values.setdefault("name", msg_dict.get("subject") or _("E-mail sem assunto"))
        custom_values.setdefault("description", msg_dict.get("body") or msg_dict.get("text") or "")
        custom_values.setdefault("message_origin", "email")
        custom_values.setdefault("incoming_email_from", msg_dict.get("email_from") or msg_dict.get("from") or "")
        custom_values.setdefault("incoming_email_to", msg_dict.get("to") or msg_dict.get("email_to") or "")
        custom_values.setdefault("incoming_email_cc", msg_dict.get("cc") or "")
        custom_values.setdefault("last_inbound_email_datetime", fields.Datetime.now())
        if channel:
            for key, value in channel._prepare_case_defaults().items():
                custom_values.setdefault(key, value)
        self._apply_case_type_defaults_to_vals(custom_values)

        thread = super().message_new(msg_dict, custom_values=custom_values)
        case = self.browse(thread if isinstance(thread, int) else thread.id).exists()
        if case:
            case._register_email_communication_from_message(msg_dict, direction="in", channel=channel)
        return thread

    def message_update(self, msg_dict, update_vals=None):
        channel = self._get_email_channel_from_message(msg_dict, custom_values=update_vals or {})
        result = super().message_update(msg_dict, update_vals=update_vals)
        if not channel or channel.update_existing_case:
            self._register_email_communication_from_message(msg_dict, direction="in", channel=channel)
        return result

    def action_mark_triage_done(self):
        for case in self:
            case.write({"triage_done": True, "requires_triage": False})
            case.message_post(body=_("Triagem concluída."))
        return True
