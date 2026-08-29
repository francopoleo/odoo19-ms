# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DocumentDocumentAgenda(models.Model):
    _name = "document.document"
    _inherit = ["document.document", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "document_document_agenda_user_rel", "document_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "document_document_agenda_partner_rel", "document_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Documento: %s") % (self.name or self.reference)

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.next_review_date or self.expiry_date or self.review_date

    def _agenda_get_activity_type(self):
        self.ensure_one()
        if self.requires_validation and not self.is_validated:
            return self.env.ref("document_core.mail_activity_type_document_validation", raise_if_not_found=False) or super()._agenda_get_activity_type()
        if self.next_review_date:
            return self.env.ref("document_core.mail_activity_type_document_review", raise_if_not_found=False) or super()._agenda_get_activity_type()
        if self.expiry_date:
            return self.env.ref("document_core.mail_activity_type_document_expiry", raise_if_not_found=False) or super()._agenda_get_activity_type()
        return super()._agenda_get_activity_type()

    def _agenda_get_description(self):
        self.ensure_one()
        return _("Tipo: %s<br/>Vencimento: %s<br/>Próxima revisão: %s<br/>Validação exigida: %s") % (
            self.document_type_id.display_name if self.document_type_id else "-",
            self.expiry_date or "-",
            self.next_review_date or "-",
            _("Sim") if self.requires_validation else _("Não"),
        )

    def _sync_agenda_defaults(self):
        for rec in self:
            vals = {}
            if rec.responsible_id and not rec.agenda_responsible_id:
                vals["agenda_responsible_id"] = rec.responsible_id.id
            deadline = rec._agenda_get_deadline()
            if deadline and not rec.agenda_deadline:
                vals["agenda_deadline"] = deadline
            if vals:
                rec.with_context(skip_document_agenda_defaults=True).write(vals)

    def action_schedule_document_activity(self):
        # Mantém as rotinas específicas já existentes e também sincroniza a agenda comum.
        self._schedule_expiry_activity()
        self._schedule_validation_activity()
        self._schedule_review_activity()
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec._agenda_get_deadline()
        records = self.filtered(lambda d: d.agenda_deadline)
        records.action_agenda_schedule_activity()
        records.action_agenda_sync_calendar()
        return True

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get("skip_document_agenda_defaults"):
            records._sync_agenda_defaults()
        return records

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_document_agenda_defaults") and any(k in vals for k in ["responsible_id", "expiry_date", "review_date", "next_review_date", "document_type_id"]):
            self._sync_agenda_defaults()
        return res
