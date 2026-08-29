# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _


class GovernanceCaseAgenda(models.Model):
    _name = "governance.case"
    _inherit = ["governance.case", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "governance_case_agenda_user_rel", "case_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "governance_case_agenda_partner_rel", "case_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Governança: %s") % (self.name or self.reference)

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.next_action_date or self.response_deadline or self.resolution_deadline

    def _agenda_get_activity_type(self):
        self.ensure_one()
        if self.response_state == "overdue":
            return self.env.ref("governance.activity_type_response_overdue", raise_if_not_found=False) or super()._agenda_get_activity_type()
        if self.open_required_pending_count:
            return self.env.ref("governance.activity_type_required_pending", raise_if_not_found=False) or super()._agenda_get_activity_type()
        return self.env.ref("governance.activity_type_followup", raise_if_not_found=False) or super()._agenda_get_activity_type()

    def _agenda_get_description(self):
        self.ensure_one()
        return _("Caso: %s<br/>Tipo: %s<br/>Prazo de resposta: %s<br/>Prazo de resolução: %s<br/>Próxima pendência: %s") % (
            self.name or "-",
            self.case_type_id.display_name if self.case_type_id else "-",
            self.response_deadline or "-",
            self.resolution_deadline or "-",
            self.next_pending_due_date or "-",
        )

    def _sync_agenda_defaults(self):
        """Keep the generic agenda fields aligned with the case owner.

        The case itself can have many agenda milestones. These defaults are only
        used by manual activity creation and as fallback for generated milestones.
        """
        for rec in self:
            vals = {}
            if rec.responsible_id and not rec.agenda_responsible_id:
                vals["agenda_responsible_id"] = rec.responsible_id.id
            if rec.partner_ids:
                missing = rec.partner_ids - rec.agenda_partner_ids
                if missing:
                    vals.setdefault("agenda_partner_ids", [])
                    vals["agenda_partner_ids"] += [(4, p.id) for p in missing]
            if not rec.agenda_deadline and rec._agenda_get_deadline():
                vals["agenda_deadline"] = rec._agenda_get_deadline()
            if vals:
                rec.with_context(skip_governance_agenda_marker_sync=True).write(vals)

    def _governance_case_is_closed(self):
        self.ensure_one()
        return self.status in ("done", "closed")

    def _governance_case_marker_domain(self, agenda_type=False):
        self.ensure_one()
        domain = [
            ("source_model", "=", self._name),
            ("source_res_id", "=", self.id),
            ("agenda_module", "=", "governance"),
        ]
        if agenda_type:
            domain.append(("agenda_type", "=", agenda_type))
        return domain

    def _governance_prepare_marker_vals(self, agenda_type, date_value, title, description, hour=9, duration_hours=1.0):
        self.ensure_one()
        start = self._agenda_datetime_from_date(date_value, hour=hour)
        stop = start + timedelta(hours=duration_hours or 1.0)
        responsible_users = self._agenda_get_responsible_users()
        visible_users = self._agenda_get_visible_users()
        partners = self._agenda_get_partners()
        responsible = responsible_users[:1]
        return {
            "name": title,
            "start": start,
            "stop": stop,
            "user_id": responsible.id or self.env.user.id,
            "responsible_user_ids": [(6, 0, responsible_users.ids)],
            "partner_ids": [(6, 0, partners.ids)],
            "location": self._agenda_get_location(),
            "description": description,
            "visibility": self._agenda_get_visibility(),
            "visible_user_ids": [(6, 0, visible_users.ids)],
            "agenda_module": "governance",
            "agenda_type": agenda_type,
            "source_model": self._name,
            "source_res_id": self.id,
            "source_key": agenda_type,
            "source_name": self.display_name,
            "company_id": self.env.company.id,
            "state": "scheduled",
            "active": True,
        }

    def _governance_sync_marker(self, agenda_type, date_value, title, description, hour=9, duration_hours=1.0, done=False):
        self.ensure_one()
        Event = self.env["common.agenda.event"].with_context(active_test=False)
        event = Event.search(self._governance_case_marker_domain(agenda_type), limit=1)
        if done:
            if event:
                event.write({"state": "done"})
            return event
        if not date_value:
            if event:
                event.action_archive()
            return event
        vals = self._governance_prepare_marker_vals(agenda_type, date_value, title, description, hour=hour, duration_hours=duration_hours)
        if event:
            event.write(vals)
        else:
            event = Event.create(vals)
        return event

    def _governance_close_case_markers(self, archive=False):
        Event = self.env["common.agenda.event"].with_context(active_test=False)
        for rec in self:
            domains = [rec._governance_case_marker_domain()]
            if rec.pending_ids:
                domains.append([
                    ("source_model", "=", "governance.case.pending"),
                    ("source_res_id", "in", rec.pending_ids.ids),
                    ("agenda_module", "=", "governance"),
                ])
            if rec.communication_ids:
                domains.append([
                    ("source_model", "=", "governance.case.communication"),
                    ("source_res_id", "in", rec.communication_ids.ids),
                    ("agenda_module", "=", "governance"),
                ])
            events = Event.browse()
            for domain in domains:
                events |= Event.search(domain)
            if events:
                events.write({"state": "done", "active": not archive})
        return True

    def action_sync_governance_agenda_markers(self):
        """Synchronize only high-value governance milestones with Agenda Geral.

        This avoids turning every chatter activity into a calendar item. The case
        creates/updates only: response deadline, resolution deadline, and next
        follow-up/action. Formal pendências and meetings have their own records.
        """
        for rec in self:
            rec._sync_agenda_defaults()
            if rec._governance_case_is_closed():
                rec._governance_close_case_markers(archive=(rec.status == "closed"))
                continue

            base_desc = rec._agenda_get_description()

            # 1) Response deadline: if response has been received, mark the marker as done.
            rec._governance_sync_marker(
                "governance_response_deadline",
                rec.response_deadline,
                _("Prazo de Resposta - %s") % (rec.name or rec.reference),
                base_desc,
                hour=9,
                done=bool(rec.response_date),
            )

            # 2) Resolution deadline: remains active while the case is open.
            rec._governance_sync_marker(
                "governance_resolution_deadline",
                rec.resolution_deadline,
                _("Prazo de Resolução - %s") % (rec.name or rec.reference),
                base_desc,
                hour=10,
            )

            # 3) Follow-up / next action: only if the operational queue computed one.
            rec._governance_sync_marker(
                "governance_followup",
                rec.next_action_date,
                _("Follow-up de Governança - %s") % (rec.name or rec.reference),
                base_desc,
                hour=11,
            )
        return True

    def action_schedule_case_activity(self):
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec._agenda_get_deadline()
        return self.action_agenda_schedule_activity()

    def action_governance_sync_agenda_complete(self):
        """Case-level enterprise sync: one operational activity + agenda milestones."""
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec._agenda_get_deadline()
        self.action_agenda_schedule_activity()
        self.action_sync_governance_agenda_markers()
        return True

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get("skip_governance_agenda_marker_sync"):
            records.with_context(skip_governance_agenda_marker_sync=True)._sync_agenda_defaults()
            records.action_sync_governance_agenda_markers()
        return records

    def write(self, vals):
        res = super().write(vals)
        watched = {
            "responsible_id", "partner_ids", "origin_date", "response_date", "stage_id",
            "case_type_id", "priority", "agenda_visibility", "agenda_viewer_user_ids",
            "agenda_responsible_id", "agenda_responsible_ids", "agenda_partner_ids",
        }
        if not self.env.context.get("skip_governance_agenda_marker_sync") and (watched.intersection(vals) or not vals):
            self.action_sync_governance_agenda_markers()
        return res


class GovernancePendingAgenda(models.Model):
    _name = "governance.case.pending"
    _inherit = ["governance.case.pending", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "governance_pending_agenda_user_rel", "pending_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "governance_pending_agenda_partner_rel", "pending_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Pendência de Governança: %s") % self.name

    def _agenda_get_type(self):
        self.ensure_one()
        return "governance_pending"

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.due_date

    def _agenda_get_activity_type(self):
        self.ensure_one()
        return self.env.ref("governance.activity_type_required_pending", raise_if_not_found=False) or super()._agenda_get_activity_type()

    def _agenda_get_description(self):
        self.ensure_one()
        return _("Pendência do caso %s.<br/>Obrigatória: %s<br/>Prioridade: %s") % (
            self.case_id.display_name if self.case_id else "-",
            _("Sim") if self.required else _("Não"),
            dict(self._fields["priority"].selection).get(self.priority, self.priority),
        )

    def _sync_agenda_defaults(self):
        for rec in self:
            vals = {}
            if rec.due_date and not rec.agenda_deadline:
                vals["agenda_deadline"] = rec.due_date
            if rec.due_date and not rec.agenda_start:
                vals["agenda_start"] = rec._agenda_datetime_from_date(rec.due_date, hour=9)
            if rec.responsible_id and not rec.agenda_responsible_id:
                vals["agenda_responsible_id"] = rec.responsible_id.id
            if rec.case_id and rec.case_id.partner_ids:
                missing = rec.case_id.partner_ids - rec.agenda_partner_ids
                if missing:
                    vals.setdefault("agenda_partner_ids", [])
                    vals["agenda_partner_ids"] += [(4, p.id) for p in missing]
            if vals:
                rec.with_context(skip_governance_agenda_defaults=True).write(vals)

    def _sync_pending_agenda_state(self):
        for rec in self:
            rec._sync_agenda_defaults()
            if rec.state == "open" and rec.due_date and rec.responsible_id:
                rec.action_agenda_schedule_activity()
                rec.action_agenda_sync_calendar()
            elif rec.agenda_calendar_event_id:
                if rec.state == "done":
                    rec.agenda_calendar_event_id.write({"state": "done"})
                elif rec.state == "cancel":
                    rec.agenda_calendar_event_id.write({"state": "cancelled", "active": False})
        return True

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get("skip_governance_agenda_defaults"):
            records._sync_pending_agenda_state()
        return records

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_governance_agenda_defaults") and any(k in vals for k in ["due_date", "responsible_id", "state", "case_id", "agenda_visibility", "agenda_viewer_user_ids"]):
            self._sync_pending_agenda_state()
        return res


class GovernanceCommunicationAgenda(models.Model):
    _name = "governance.case.communication"
    _inherit = ["governance.case.communication", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "governance_communication_agenda_user_rel", "communication_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "governance_communication_agenda_partner_rel", "communication_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Compromisso de Governança: %s") % self.name

    def _agenda_get_type(self):
        self.ensure_one()
        return "governance_meeting"

    def _agenda_get_description(self):
        self.ensure_one()
        return _("Caso: %s<br/>Tipo de comunicação: %s<br/>Direção: %s<br/>%s") % (
            self.case_id.display_name if self.case_id else "-",
            dict(self._fields["communication_type"].selection).get(self.communication_type, self.communication_type),
            dict(self._fields["direction"].selection).get(self.direction, self.direction),
            self.note or "",
        )

    def _sync_agenda_defaults(self):
        for rec in self.filtered(lambda c: c.communication_type == "meeting"):
            vals = {}
            if rec.communication_datetime and not rec.agenda_start:
                vals["agenda_start"] = rec.communication_datetime
            if rec.partner_id and rec.partner_id not in rec.agenda_partner_ids:
                vals["agenda_partner_ids"] = [(4, rec.partner_id.id)]
            if rec.responsible_id and not rec.agenda_responsible_id:
                vals["agenda_responsible_id"] = rec.responsible_id.id
            if rec.case_id and rec.case_id.partner_ids:
                missing = rec.case_id.partner_ids - rec.agenda_partner_ids
                if missing:
                    vals.setdefault("agenda_partner_ids", [])
                    vals["agenda_partner_ids"] += [(4, p.id) for p in missing]
            if vals:
                rec.with_context(skip_governance_agenda_defaults=True).write(vals)

    def _sync_communication_agenda_state(self):
        for rec in self:
            if rec.communication_type == "meeting":
                rec._sync_agenda_defaults()
                if rec.agenda_start:
                    rec.action_agenda_sync_calendar()
            elif rec.agenda_calendar_event_id:
                rec.agenda_calendar_event_id.write({"state": "cancelled", "active": False})
        return True

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get("skip_governance_agenda_defaults"):
            records._sync_communication_agenda_state()
        return records

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_governance_agenda_defaults") and any(k in vals for k in ["communication_type", "communication_datetime", "partner_id", "responsible_id", "case_id", "agenda_visibility", "agenda_viewer_user_ids"]):
            self._sync_communication_agenda_state()
        return res
