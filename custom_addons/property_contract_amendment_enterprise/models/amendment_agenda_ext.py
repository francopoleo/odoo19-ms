# -*- coding: utf-8 -*-
from odoo import fields, models, _


class PropertyContractAmendmentAgenda(models.Model):
    _name = "property.contract.amendment"
    _inherit = ["property.contract.amendment", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "property_amendment_agenda_user_rel", "amendment_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "property_amendment_agenda_partner_rel", "amendment_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Aditivo: %s") % (self.name or self.sequence)

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.sign_date or self.effective_date or self.instrument_date

    def _agenda_get_description(self):
        self.ensure_one()
        return _("Contrato: %s<br/>Tipo: %s<br/>Status: %s<br/>Data de efeito: %s") % (
            self.contract_id.display_name if self.contract_id else "-",
            dict(self._fields["amendment_type"].selection).get(self.amendment_type, self.amendment_type),
            dict(self._fields["status"].selection).get(self.status, self.status),
            self.effective_date or "-",
        )

    def action_schedule_amendment_activity(self):
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec._agenda_get_deadline() or fields.Date.today()
        self.action_agenda_schedule_activity()
        self.action_agenda_sync_calendar()
        return True
