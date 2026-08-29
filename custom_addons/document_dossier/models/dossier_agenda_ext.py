# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DossierDossierAgenda(models.Model):
    _name = "dossier.dossier"
    _inherit = ["dossier.dossier", "mail.thread", "mail.activity.mixin", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "dossier_dossier_agenda_user_rel", "dossier_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "dossier_dossier_agenda_partner_rel", "dossier_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Dossiê: %s") % self.name

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.target_date

    def _agenda_get_description(self):
        self.ensure_one()
        return _("Processo: %s<br/>Origem: %s<br/>Conclusão alvo: %s<br/>Progresso: %s%%") % (
            self.process_id.display_name if self.process_id else "-",
            self.target_display or "-",
            self.target_date or "-",
            round(self.completion_percent or 0, 2),
        )

    def _sync_agenda_defaults(self):
        for rec in self:
            vals = {}
            if rec.responsible_id and not rec.agenda_responsible_id:
                vals["agenda_responsible_id"] = rec.responsible_id.id
            if rec.target_date and not rec.agenda_deadline:
                vals["agenda_deadline"] = rec.target_date
            if vals:
                rec.with_context(skip_dossier_agenda_defaults=True).write(vals)

    def action_schedule_dossier_activity(self):
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec.target_date
        records = self.filtered(lambda d: d.agenda_deadline)
        records.action_agenda_schedule_activity()
        records.action_agenda_sync_calendar()
        return True

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get("skip_dossier_agenda_defaults"):
            records._sync_agenda_defaults()
        return records

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_dossier_agenda_defaults") and any(k in vals for k in ["responsible_id", "target_date"]):
            self._sync_agenda_defaults()
        return res
