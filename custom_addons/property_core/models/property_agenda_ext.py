# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PropertyInspectionAgenda(models.Model):
    _name = "property.inspection"
    _inherit = ["property.inspection", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "property_inspection_agenda_user_rel", "inspection_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "property_inspection_agenda_partner_rel", "inspection_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Vistoria: %s") % (self.name or self.reference or self.asset_id.display_name)

    def _agenda_get_description(self):
        self.ensure_one()
        parts = []
        if self.asset_id:
            parts.append("<p><strong>Imóvel:</strong> %s</p>" % self.asset_id.display_name)
        if self.contract_id:
            parts.append("<p><strong>Contrato:</strong> %s</p>" % self.contract_id.display_name)
        if self.inspection_type:
            parts.append("<p><strong>Tipo:</strong> %s</p>" % dict(self._fields["inspection_type"].selection).get(self.inspection_type))
        if self.observations:
            parts.append("<p><strong>Observações:</strong> %s</p>" % self.observations)
        if self.agenda_notes:
            parts.append(self.agenda_notes)
        return "".join(parts) or False

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.scheduled_date or self.date or fields.Date.today()

    def _agenda_get_activity_type(self):
        self.ensure_one()
        return self.env.ref("property_core.mail_activity_type_inspection", raise_if_not_found=False) or super()._agenda_get_activity_type()

    def _agenda_get_partners(self):
        self.ensure_one()
        partners = super()._agenda_get_partners()
        if self.inspector_id:
            partners |= self.inspector_id
        partners |= self.present_ids
        return partners

    def _sync_agenda_defaults(self):
        for rec in self:
            vals = {}
            if rec.scheduled_date and not rec.agenda_deadline:
                vals["agenda_deadline"] = rec.scheduled_date
            if rec.scheduled_date and not rec.agenda_start:
                vals["agenda_start"] = rec._agenda_datetime_from_date(rec.scheduled_date, hour=9)
            if rec.inspector_id and rec.inspector_id not in rec.agenda_partner_ids:
                vals["agenda_partner_ids"] = [(4, rec.inspector_id.id)]
            if vals:
                rec.with_context(skip_property_agenda_defaults=True).write(vals)

    def action_schedule(self):
        res = super().action_schedule()
        self._sync_agenda_defaults()
        for rec in self:
            rec.action_agenda_schedule_activity()
            rec.action_agenda_sync_calendar()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get("skip_property_agenda_defaults"):
            records._sync_agenda_defaults()
        return records

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_property_agenda_defaults") and any(k in vals for k in ["scheduled_date", "inspector_id"]):
            self._sync_agenda_defaults()
        return res


class PropertyMaintenanceAgenda(models.Model):
    _name = "property.maintenance"
    _inherit = ["property.maintenance", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "property_maintenance_agenda_user_rel", "maintenance_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "property_maintenance_agenda_partner_rel", "maintenance_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Manutenção: %s") % (self.name or self.reference or self.asset_id.display_name)

    def _agenda_get_description(self):
        self.ensure_one()
        parts = []
        if self.asset_id:
            parts.append("<p><strong>Imóvel:</strong> %s</p>" % self.asset_id.display_name)
        if self.vendor_id:
            parts.append("<p><strong>Fornecedor:</strong> %s</p>" % self.vendor_id.display_name)
        if self.maintenance_type:
            parts.append("<p><strong>Tipo:</strong> %s</p>" % dict(self._fields["maintenance_type"].selection).get(self.maintenance_type))
        if self.description:
            parts.append("<p><strong>Descrição:</strong> %s</p>" % self.description)
        if self.agenda_notes:
            parts.append(self.agenda_notes)
        return "".join(parts) or False

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.scheduled_date or self.request_date or fields.Date.today()

    def _agenda_get_activity_type(self):
        self.ensure_one()
        return self.env.ref("property_core.mail_activity_type_maintenance", raise_if_not_found=False) or super()._agenda_get_activity_type()

    def _agenda_get_partners(self):
        self.ensure_one()
        partners = super()._agenda_get_partners()
        if self.vendor_id:
            partners |= self.vendor_id
        return partners

    def _sync_agenda_defaults(self):
        for rec in self:
            vals = {}
            if rec.scheduled_date and not rec.agenda_deadline:
                vals["agenda_deadline"] = rec.scheduled_date
            if rec.scheduled_date and not rec.agenda_start:
                vals["agenda_start"] = rec._agenda_datetime_from_date(rec.scheduled_date, hour=9)
            if rec.vendor_id and rec.vendor_id not in rec.agenda_partner_ids:
                vals["agenda_partner_ids"] = [(4, rec.vendor_id.id)]
            if vals:
                rec.with_context(skip_property_agenda_defaults=True).write(vals)

    def action_schedule(self):
        res = super().action_schedule()
        self._sync_agenda_defaults()
        for rec in self:
            rec.action_agenda_schedule_activity()
            rec.action_agenda_sync_calendar()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get("skip_property_agenda_defaults"):
            records._sync_agenda_defaults()
        return records

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_property_agenda_defaults") and any(k in vals for k in ["scheduled_date", "vendor_id"]):
            self._sync_agenda_defaults()
        return res


class PropertyContractAgenda(models.Model):
    _name = "property.contract"
    _inherit = ["property.contract", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "property_contract_agenda_user_rel", "contract_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "property_contract_agenda_partner_rel", "contract_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Contrato: %s") % (self.name or self.display_name)

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.next_adjustment_date or self.end_date

    def _agenda_get_activity_type(self):
        self.ensure_one()
        if self.next_adjustment_date and (not self.end_date or self.next_adjustment_date <= self.end_date):
            return self.env.ref("property_core.mail_activity_type_rent_adjustment", raise_if_not_found=False) or super()._agenda_get_activity_type()
        return self.env.ref("property_core.mail_activity_type_contract_expiry", raise_if_not_found=False) or super()._agenda_get_activity_type()

    def _agenda_get_description(self):
        self.ensure_one()
        return _("Acompanhar prazo do contrato. Imóvel: %s. Início: %s. Fim: %s. Próximo reajuste: %s.") % (
            self.asset_id.display_name if self.asset_id else "-",
            self.start_date or "-",
            self.end_date or "-",
            self.next_adjustment_date or "-",
        )

    def action_schedule_contract_activity(self):
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec.next_adjustment_date or rec.end_date
        self.action_agenda_schedule_activity()
        self.action_agenda_sync_calendar()
        return True


class PropertyRentAgenda(models.Model):
    _name = "property.rent"
    _inherit = ["property.rent", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "property_rent_agenda_user_rel", "rent_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "property_rent_agenda_partner_rel", "rent_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Parcela de aluguel: %s") % (self.display_name or self.id)

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.due_date

    def _agenda_get_activity_type(self):
        self.ensure_one()
        return self.env.ref("property_core.mail_activity_type_rent_overdue", raise_if_not_found=False) or super()._agenda_get_activity_type()

    def action_schedule_rent_activity(self):
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec.due_date
        self.action_agenda_schedule_activity()
        self.action_agenda_sync_calendar()
        return True


class PropertyRentAdjustmentAgenda(models.Model):
    _name = "property.rent.adjustment"
    _inherit = ["property.rent.adjustment", "common.agenda.mixin"]

    agenda_responsible_ids = fields.Many2many(
        "res.users", "property_rent_adjustment_agenda_user_rel", "adjustment_id", "user_id",
        string="Responsáveis / Equipe",
    )
    agenda_partner_ids = fields.Many2many(
        "res.partner", "property_rent_adjustment_agenda_partner_rel", "adjustment_id", "partner_id",
        string="Participantes Externos",
    )

    def _agenda_get_title(self):
        self.ensure_one()
        return _("Reajuste: %s") % (self.display_name or self.id)

    def _agenda_get_deadline(self):
        self.ensure_one()
        return self.agenda_deadline or self.effective_date or self.adjustment_date

    def _agenda_get_activity_type(self):
        self.ensure_one()
        return self.env.ref("property_core.mail_activity_type_rent_adjustment", raise_if_not_found=False) or super()._agenda_get_activity_type()

    def action_schedule_rent_adjustment_activity(self):
        for rec in self:
            if not rec.agenda_deadline:
                rec.agenda_deadline = rec.effective_date or rec.adjustment_date
        self.action_agenda_schedule_activity()
        self.action_agenda_sync_calendar()
        return True
