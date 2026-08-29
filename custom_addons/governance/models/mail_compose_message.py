# -*- coding: utf-8 -*-
from odoo import fields, models, _


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _governance_get_target_cases(self):
        ctx = dict(self.env.context or {})
        if not ctx.get("mark_governance_sent"):
            return self.env["governance.case"]
        case_ids = ctx.get("default_res_ids") or ctx.get("active_ids") or []
        if ctx.get("default_model") == "governance.case" and ctx.get("default_res_id"):
            case_ids = [ctx.get("default_res_id")]
        return self.env["governance.case"].browse(case_ids).exists()

    def _governance_log_sent_email(self):
        cases = self._governance_get_target_cases()
        if not cases:
            return
        now = fields.Datetime.now()
        partner_ids = []
        for wizard in self:
            partner_ids += wizard.partner_ids.ids
        partner = self.env["res.partner"].browse(partner_ids[:1]).exists() if partner_ids else self.env["res.partner"].browse()
        for case in cases:
            self.env["governance.case.communication"].sudo().create({
                "case_id": case.id,
                "name": _("E-mail enviado pelo Odoo"),
                "communication_datetime": now,
                "communication_type": "email",
                "direction": "out",
                "partner_id": partner.id if partner else (case.primary_partner_id.id if case.primary_partner_id else False),
                "responsible_id": self.env.user.id,
                "note": _("E-mail enviado pelo assistente de composição do Odoo."),
                "requires_response": True,
                "response_deadline": case.response_deadline,
                "sent_by_odoo": True,
            })
            case.sudo().write({
                "last_outbound_email_datetime": now,
                "email_sent_date": fields.Date.today(),
            })

    def action_send_mail(self):
        result = super(MailComposeMessage, self.with_context(skip_governance_compose_log=True)).action_send_mail()
        self._governance_log_sent_email()
        return result

    def _action_send_mail(self, *args, **kwargs):
        result = super()._action_send_mail(*args, **kwargs)
        if not self.env.context.get("skip_governance_compose_log"):
            self._governance_log_sent_email()
        return result
