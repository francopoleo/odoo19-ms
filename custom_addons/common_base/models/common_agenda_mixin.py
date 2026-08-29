# -*- coding: utf-8 -*-
from datetime import datetime, time, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CommonAgendaMixin(models.AbstractModel):
    """Reusable scheduling layer for operational records.

    Separates two concepts:
    - mail.activity: internal responsibility / deadline / follow-up;
    - common.agenda.event: compromisso operacional exibido na Agenda Geral, separado das Reuniões do Odoo.
    """

    _name = "common.agenda.mixin"
    _description = "Agenda e Atividades Operacionais"

    agenda_responsible_id = fields.Many2one(
        "res.users",
        string="Responsável Principal",
        tracking=True,
        help="Usuário interno responsável pelo acompanhamento do registro.",
    )
    agenda_deadline = fields.Date(
        "Prazo da Atividade",
        tracking=True,
        help="Prazo usado para criar atividade interna no Odoo.",
    )
    agenda_start = fields.Datetime(
        "Início Agendado",
        tracking=True,
        help="Data/hora real do compromisso para aparecer no calendário.",
    )
    agenda_stop = fields.Datetime(
        "Fim Agendado",
        tracking=True,
        help="Data/hora final do compromisso no calendário.",
    )
    agenda_duration_hours = fields.Float(
        "Duração Prevista (h)",
        default=1.0,
        help="Usada para calcular o fim do evento quando o campo Fim Agendado não estiver preenchido.",
    )
    agenda_location = fields.Char(
        "Local do Compromisso",
        help="Local exibido no evento de calendário.",
    )
    agenda_notes = fields.Html(
        "Notas de Agenda",
        help="Resumo operacional enviado para atividade/calendário.",
    )
    agenda_visibility = fields.Selection(
        [
            ("restricted", "Somente responsáveis/participantes"),
            ("custom", "Responsáveis + usuários adicionais"),
            ("internal", "Todos os usuários internos"),
        ],
        string="Quem pode visualizar",
        default="restricted",
        required=True,
        tracking=True,
        help=(
            "Controla a visualização da agenda e das atividades geradas. "
            "Administradores da Agenda Geral sempre podem auditar todos os eventos."
        ),
    )
    agenda_viewer_user_ids = fields.Many2many(
        "res.users",
        string="Usuários adicionais com acesso",
        help="Usuários internos que também poderão visualizar o evento e as atividades desta agenda.",
    )
    agenda_calendar_event_id = fields.Many2one(
        "common.agenda.event",
        string="Evento da Agenda Geral",
        copy=False,
        readonly=True,
        ondelete="set null",
    )
    agenda_calendar_synced = fields.Boolean(
        "Agenda Geral Sincronizada",
        compute="_compute_agenda_calendar_synced",
    )

    @api.depends("agenda_calendar_event_id")
    def _compute_agenda_calendar_synced(self):
        for rec in self:
            rec.agenda_calendar_synced = bool(rec.agenda_calendar_event_id)

    @api.onchange("agenda_start", "agenda_duration_hours")
    def _onchange_agenda_start_duration(self):
        for rec in self:
            if rec.agenda_start and not rec.agenda_stop:
                rec.agenda_stop = rec.agenda_start + timedelta(hours=rec.agenda_duration_hours or 1.0)

    def _agenda_get_title(self):
        self.ensure_one()
        return self.display_name or self.name_get()[0][1]

    def _agenda_get_description(self):
        self.ensure_one()
        parts = []
        if self.agenda_notes:
            parts.append(self.agenda_notes)
        if hasattr(self, "description") and self.description:
            parts.append(self.description)
        if hasattr(self, "observations") and self.observations:
            parts.append("<p><strong>Observações:</strong> %s</p>" % self.observations)
        return "".join(parts) or False

    def _agenda_get_location(self):
        self.ensure_one()
        if self.agenda_location:
            return self.agenda_location
        asset = getattr(self, "asset_id", False)
        if asset:
            parts = []
            for fname in ("address", "street", "neighborhood", "city", "state_id"):
                if fname in asset._fields:
                    value = asset[fname]
                    if getattr(value, "display_name", False):
                        value = value.display_name
                    if value:
                        parts.append(str(value))
            return ", ".join(parts) if parts else asset.display_name
        return False

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or False

    def _agenda_get_type(self):
        """Classifica itens gerados na Agenda Geral."""
        self.ensure_one()
        return {
            "property.inspection": "inspection",
            "property.maintenance": "maintenance",
            "governance.case": "governance_case",
            "governance.case.pending": "governance_pending",
            "governance.case.communication": "governance_meeting",
            "document.document": "document",
            "dossier.dossier": "dossier",
            "property.contract": "contract",
            "property.rent": "rent",
            "property.rent.adjustment": "rent_adjustment",
            "property.contract.amendment": "contract_amendment",
            "property.payment.proof": "payment_proof",
        }.get(self._name, "operational")

    def _agenda_get_module(self):
        self.ensure_one()
        if self._name.startswith("property.payment"):
            return "financial"
        if self._name.startswith("property."):
            return "property"
        if self._name.startswith("governance."):
            return "governance"
        if self._name.startswith("document.") or self._name.startswith("dossier."):
            return "document"
        return "other"

    def _agenda_get_activity_type(self):
        self.ensure_one()
        return self.env.ref("common_base.mail_activity_type_operational_deadline", raise_if_not_found=False) or self.env.ref("mail.mail_activity_data_todo", raise_if_not_found=False)

    def _agenda_get_responsible_users(self):
        self.ensure_one()
        users = self.env["res.users"]
        if self.agenda_responsible_id:
            users |= self.agenda_responsible_id
        if "agenda_responsible_ids" in self._fields:
            users |= self.agenda_responsible_ids
        for fname in ("responsible_id", "user_id"):
            if fname in self._fields and self[fname]:
                users |= self[fname]
        if not users:
            users = self.env.user
        return users

    def _agenda_get_visible_users(self):
        """Users that may see generated enterprise agenda records.

        Esta lista é copiada para common.agenda.event para que menus
        e regras de visibilidade funcionem sem expor a agenda a todos.
        """
        self.ensure_one()
        users = self.env["res.users"]
        users |= self._agenda_get_responsible_users()
        if "agenda_viewer_user_ids" in self._fields:
            users |= self.agenda_viewer_user_ids
        if self.create_uid:
            users |= self.create_uid
        if self.env.user:
            users |= self.env.user
        # If an internal user is a participant through its partner, include it.
        for partner in self._agenda_get_partners():
            if "user_ids" in partner._fields:
                users |= partner.user_ids
        return users

    def _agenda_get_visibility(self):
        self.ensure_one()
        return self.agenda_visibility or "restricted"

    def _agenda_get_partners(self):
        self.ensure_one()
        partners = self.env["res.partner"]
        if "agenda_partner_ids" in self._fields:
            partners |= self.agenda_partner_ids
        for user in self._agenda_get_responsible_users():
            if user.partner_id:
                partners |= user.partner_id
        for fname in ("partner_id", "primary_partner_id", "vendor_id", "inspector_id"):
            if fname in self._fields and self[fname]:
                partners |= self[fname]
        if "partner_ids" in self._fields:
            partners |= self.partner_ids
        if "present_ids" in self._fields:
            partners |= self.present_ids
        if self.env.user.partner_id:
            partners |= self.env.user.partner_id
        return partners

    def _agenda_get_start_stop(self):
        self.ensure_one()
        start = self.agenda_start
        stop = self.agenda_stop
        if not start:
            deadline = self._agenda_get_deadline()
            if deadline:
                start = self._agenda_datetime_from_date(deadline, hour=9)
        if start and not stop:
            stop = start + timedelta(hours=self.agenda_duration_hours or 1.0)
        return start, stop

    def _agenda_prepare_event_vals(self):
        self.ensure_one()
        start, stop = self._agenda_get_start_stop()
        if not start:
            raise UserError(_("Informe o Início Agendado ou um Prazo da Atividade para criar o item na Agenda Geral."))
        if not stop:
            stop = start + timedelta(hours=self.agenda_duration_hours or 1.0)
        partners = self._agenda_get_partners()
        responsible_users = self._agenda_get_responsible_users()
        visible_users = self._agenda_get_visible_users()
        responsible = responsible_users[:1]
        return {
            "name": self._agenda_get_title(),
            "start": start,
            "stop": stop,
            "user_id": responsible.id or self.env.user.id,
            "responsible_user_ids": [(6, 0, responsible_users.ids)],
            "partner_ids": [(6, 0, partners.ids)],
            "location": self._agenda_get_location(),
            "description": self._agenda_get_description(),
            "visibility": self._agenda_get_visibility(),
            "visible_user_ids": [(6, 0, visible_users.ids)],
            "agenda_module": self._agenda_get_module(),
            "agenda_type": self._agenda_get_type(),
            "source_model": self._name,
            "source_res_id": self.id,
            "source_key": False,
            "source_name": self.display_name,
            "company_id": self.env.company.id,
        }

    def _agenda_write_calendar_defaults(self):
        """Persist fallback start/stop when the user only informed a deadline/date.

        This fixes the case where an activity is created but the record has no agenda_start,
        portanto a Agenda Geral não consegue exibir depois.
        """
        for rec in self:
            start, stop = rec._agenda_get_start_stop()
            vals = {}
            if start and not rec.agenda_start:
                vals["agenda_start"] = start
            if stop and not rec.agenda_stop:
                vals["agenda_stop"] = stop
            if vals:
                rec.write(vals)

    def _agenda_prepare_activity_meta_vals(self):
        """Return extra values for mail.activity.

        We intentionally do not add stored custom fields to mail.activity in
        Odoo 18/19. The mail/discuss webclient fetches activities very early and
        custom stored columns can cause UndefinedColumn errors if code and DB are
        temporarily out of sync during deployment.

        Visibility of activities is controlled by the assigned responsible user
        and by access to the original record. Calendar events keep the richer
        Agenda Geral visibility metadata.
        """
        self.ensure_one()
        return {}

    def action_agenda_schedule_activity(self):
        Activity = self.env["mail.activity"]
        for rec in self:
            deadline = rec._agenda_get_deadline()
            if not deadline:
                raise UserError(_("Informe o Prazo da Atividade para criar atividades."))
            activity_type = rec._agenda_get_activity_type()
            if not activity_type:
                raise UserError(_("Tipo de atividade padrão não encontrado."))
            summary = rec._agenda_get_title()
            note = rec._agenda_get_description() or _("Acompanhar prazo operacional deste registro.")
            for user in rec._agenda_get_responsible_users():
                existing = Activity.search([
                    ("res_model", "=", rec._name),
                    ("res_id", "=", rec.id),
                    ("activity_type_id", "=", activity_type.id),
                    ("user_id", "=", user.id),
                ], limit=1)
                vals = {
                    "date_deadline": deadline,
                    "summary": summary,
                    "note": note,
                }
                meta_vals = rec._agenda_prepare_activity_meta_vals()
                if existing:
                    existing.write(dict(vals, **meta_vals))
                else:
                    rec.activity_schedule(
                        activity_type_id=activity_type.id,
                        user_id=user.id,
                        date_deadline=deadline,
                        summary=summary,
                        note=note,
                    )
                    created = Activity.search([
                        ("res_model", "=", rec._name),
                        ("res_id", "=", rec.id),
                        ("activity_type_id", "=", activity_type.id),
                        ("user_id", "=", user.id),
                    ], order="id desc", limit=1)
                    if created and meta_vals:
                        created.write(meta_vals)
            rec.message_post(body=_("Atividade(s) sincronizada(s) para o prazo %s.") % deadline)
        return True

    def action_agenda_sync_calendar(self):
        """Create/update the operational Agenda Geral event.

        This intentionally does NOT create calendar.event. Odoo treats
        calendar.event as a meeting, which is why operational appointments were
        appearing as "Reuniões". Agenda Geral has its own model and calendar view.
        """
        Event = self.env["common.agenda.event"]
        for rec in self:
            rec._agenda_write_calendar_defaults()
            vals = rec._agenda_prepare_event_vals()
            if rec.agenda_calendar_event_id:
                rec.agenda_calendar_event_id.write(vals)
                event = rec.agenda_calendar_event_id
            else:
                event = Event.create(vals)
                rec.write({"agenda_calendar_event_id": event.id})
            rec.message_post(body=_("Item da Agenda Geral sincronizado: %s") % event.display_name)
        return True

    def action_agenda_sync_activity_and_calendar(self):
        """Sincronização enterprise: atividade interna + item da Agenda Geral."""
        self.action_agenda_schedule_activity()
        self.action_agenda_sync_calendar()
        return True

    def action_agenda_open_calendar_event(self):
        self.ensure_one()
        if not self.agenda_calendar_event_id:
            raise UserError(_("Este registro ainda não possui item na Agenda Geral."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Item da Agenda Geral"),
            "res_model": "common.agenda.event",
            "res_id": self.agenda_calendar_event_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_agenda_remove_calendar_event(self):
        """Detach the operational agenda item from this record.

        In the enterprise agenda we avoid hard-deleting operational history for
        normal users. Removing an agenda item from the source record cancels and
        archives the Agenda Geral entry, then clears the relation. Administrators
        may still hard-delete from the Agenda Geral list/form when required.
        """
        for rec in self:
            if rec.agenda_calendar_event_id:
                event = rec.agenda_calendar_event_id
                event.sudo().write({"state": "cancelled", "active": False})
                rec.write({"agenda_calendar_event_id": False})
        return True

    @api.model
    def _agenda_datetime_from_date(self, value, hour=9):
        if not value:
            return False
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            # fields.Date handles date strings; fields.Datetime handles datetime strings.
            try:
                if len(value) > 10:
                    return fields.Datetime.from_string(value)
                value = fields.Date.from_string(value)
            except Exception:
                value = fields.Date.from_string(value[:10])
        return datetime.combine(value, time(hour=hour, minute=0, second=0))
