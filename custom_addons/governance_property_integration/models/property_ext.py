from odoo import api, fields, models, _


class PropertyAssetGovernanceExt(models.Model):
    _inherit = "property.asset"

    governance_case_count = fields.Integer(
        "Qtd. Casos", compute="_compute_governance_case_count"
    )

    @api.depends()
    def _compute_governance_case_count(self):
        gov_model = self.env["governance.case"]
        has_asset_link = "asset_ids" in gov_model._fields
        for asset in self:
            if has_asset_link:
                asset.governance_case_count = gov_model.search_count(
                    [("asset_ids", "in", asset.id)]
                )
            else:
                asset.governance_case_count = 0

    def action_view_governance_cases(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Casos de Governança — %s") % self.display_name,
            "res_model": "governance.case",
            "view_mode": "list,kanban,form",
            "domain": [("asset_ids", "in", self.id)],
            "context": {"default_primary_asset_id": self.id},
        }

    def action_create_governance_case(self):
        self.ensure_one()
        owner = self.owner_id
        return {
            "type": "ir.actions.act_window",
            "name": _("Novo caso de governança — %s") % self.display_name,
            "res_model": "governance.case",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_name": _("Acompanhamento do imóvel — %s") % self.display_name,
                "default_description": _(
                    "Caso aberto a partir do imóvel %s para registrar comunicações, "
                    "respostas, pendências, obrigações, riscos e decisões."
                ) % self.display_name,
                "default_company_id": self.company_id.id,
                "default_case_scope": "single_property",
                "default_primary_asset_id": self.id,
                "default_asset_ids": [(6, 0, [self.id])],
                "default_partner_ids": [(6, 0, [owner.id])] if owner else False,
            },
        }


class PropertyContractGovernanceExt(models.Model):
    _inherit = "property.contract"

    governance_case_count = fields.Integer(
        "Qtd. Casos", compute="_compute_governance_case_count"
    )

    @api.depends()
    def _compute_governance_case_count(self):
        gov_model = self.env["governance.case"]
        has_contract_link = "contract_ids" in gov_model._fields
        for contract in self:
            if has_contract_link:
                contract.governance_case_count = gov_model.search_count(
                    [("contract_ids", "in", contract.id)]
                )
            else:
                contract.governance_case_count = 0


class PropertyBrokerAssignmentGovernanceExt(models.Model):
    _inherit = "property.broker.assignment"

    governance_case_count = fields.Integer(
        "Qtd. Casos", compute="_compute_governance_case_count"
    )

    @api.depends()
    def _compute_governance_case_count(self):
        gov_model = self.env["governance.case"]
        has_assignment_link = "assignment_ids" in gov_model._fields
        for assignment in self:
            if has_assignment_link:
                assignment.governance_case_count = gov_model.search_count(
                    [("assignment_ids", "in", assignment.id)]
                )
            else:
                assignment.governance_case_count = 0
