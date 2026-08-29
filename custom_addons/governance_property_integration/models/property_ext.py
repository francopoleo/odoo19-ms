from odoo import api, fields, models


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
