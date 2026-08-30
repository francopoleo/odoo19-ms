# -*- coding: utf-8 -*-

from odoo import api, fields, models


class GovernanceCasePortal(models.Model):
    _inherit = "governance.case"

    portal_visibility = fields.Boolean(
        string="Visível no Portal",
        compute="_compute_portal_visibility",
        store=True,
        copy=False,
    )

    @api.depends("responsible_id", "participant_ids.partner_id")
    def _compute_portal_visibility(self):
        for case in self:
            case.portal_visibility = bool(
                case.responsible_id.partner_id or case.participant_ids
            )

    def _is_visible_to_partner(self, partner):
        """Check if partner can view this case in portal."""
        # Manager/Responsible of the case can view
        if self.responsible_id.partner_id == partner:
            return True
        # Case participants can view
        if partner in self.participant_ids.mapped("partner_id"):
            return True
        # Admin can view all
        if self.env.user.has_group("base.group_erp_manager"):
            return True
        return False

    def get_portal_cases(self, partner):
        """Get cases visible to partner in portal."""
        domain = [
            ("|"),
            ("responsible_id.partner_id", "=", partner.id),
            ("participant_ids.partner_id", "=", partner.id),
        ]
        return self.search(domain)
