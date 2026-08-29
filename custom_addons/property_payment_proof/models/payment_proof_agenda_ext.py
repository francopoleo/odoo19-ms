# -*- coding: utf-8 -*-
from odoo import fields, models, _


class PropertyPaymentProofAgenda(models.Model):
    _name = "property.payment.proof"
    _inherit = ["property.payment.proof", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "property_payment_proof_agenda_user_rel", "proof_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "property_payment_proof_agenda_partner_rel", "proof_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Comprovante: %s") % (self.name or self.proof_filename or self.id)

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.debit_date or self.payment_date or fields.Date.today()

    def _agenda_get_description(self):
        self.ensure_one()
        return _("Status: %s<br/>Contrato: %s<br/>Parcela: %s<br/>Pagador: %s<br/>Valor: %s") % (
            dict(self._fields["state"].selection).get(self.state, self.state),
            self.contract_id.display_name if self.contract_id else "-",
            self.rent_id.display_name if self.rent_id else "-",
            self.payer_name or "-",
            self.amount or 0.0,
        )

    def action_schedule_payment_proof_activity(self):
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec._agenda_get_deadline()
        self.action_agenda_schedule_activity()
        self.action_agenda_sync_calendar()
        return True
