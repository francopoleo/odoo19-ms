from odoo import api, fields, models
from odoo.addons.common_base.models.partner_resolution import MATCH_SOURCES  # noqa: F401 — re-export


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_stakeholder_profile_ids = fields.One2many(
        "property.stakeholder.profile",
        "partner_id",
        string="Perfis Imobiliários",
        help="Perfis imobiliários vinculados a este contato mestre. Use esta seção para atribuir papéis como proprietário, locatário, corretor ou investidor sem criar um novo contato.",
    )
    has_property_stakeholder_profile = fields.Boolean(
        string="Possui Perfil Imobiliário",
        compute="_compute_has_property_stakeholder_profile",
        compute_sudo=True,
        store=True,
    )
    property_stakeholder_profile_count = fields.Integer(
        compute="_compute_property_stakeholder_profile_count",
        compute_sudo=True,
        store=True,
    )

    @api.depends("property_stakeholder_profile_ids")
    def _compute_has_property_stakeholder_profile(self):
        for rec in self:
            rec.has_property_stakeholder_profile = bool(rec.property_stakeholder_profile_ids)

    @api.depends("property_stakeholder_profile_ids")
    def _compute_property_stakeholder_profile_count(self):
        for rec in self:
            rec.property_stakeholder_profile_count = len(rec.property_stakeholder_profile_ids)

    def action_view_property_stakeholder_profiles(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Perfis Imobiliários",
            "res_model": "property.stakeholder.profile",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }

    def action_new_property_stakeholder_profile(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Novo Perfil Imobiliário",
            "res_model": "property.stakeholder.profile",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_partner_id": self.id,
                "default_company_id": self.env.company.id,
            },
        }

    @api.model
    def _resolve_contact_extended(self, email=None, phone=None):
        """Resolução imobiliária via property.stakeholder.profile."""
        if email:
            profile = self.env["property.stakeholder.profile"].sudo().search(
                [("partner_id.email", "=ilike", email)], limit=1
            )
            if profile and profile.partner_id:
                return (profile.partner_id, "stakeholder_email", 90)

            lead = self.env["property.lead"].sudo().search(
                [("email", "=ilike", email), ("partner_id", "!=", False)], limit=1
            )
            if lead and lead.partner_id:
                return (lead.partner_id, "lead_email", 85)

        return super()._resolve_contact_extended(email=email, phone=phone)
