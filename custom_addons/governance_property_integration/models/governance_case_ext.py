from odoo import api, fields, models, _


class GovernanceCasePropertyExt(models.Model):
    _inherit = "governance.case"

    asset_ids = fields.Many2many(
        "property.asset",
        relation="governance_case_property_asset_rel",
        column1="case_id",
        column2="asset_id",
        string="Imóveis Relacionados",
        domain="[('company_id', '=', company_id)]",
        check_company=True,
    )
    contract_ids = fields.Many2many(
        "property.contract",
        relation="governance_case_property_contract_rel",
        column1="case_id",
        column2="contract_id",
        string="Contratos Relacionados",
        domain="[('company_id', '=', company_id)]",
        check_company=True,
    )
    assignment_ids = fields.Many2many(
        "property.broker.assignment",
        relation="governance_case_broker_assignment_rel",
        column1="case_id",
        column2="assignment_id",
        string="Mandatos em Disputa",
        domain="[('company_id', '=', company_id)]",
        check_company=True,
    )
    asset_count = fields.Integer("Qtd Imóveis", compute="_compute_property_counts")
    contract_count = fields.Integer("Qtd Contratos", compute="_compute_property_counts")
    assignment_count = fields.Integer("Mandatos", compute="_compute_property_counts")
    @api.depends("asset_ids", "contract_ids", "assignment_ids")
    def _compute_property_counts(self):
        for case in self:
            case.asset_count = len(case.asset_ids)
            case.contract_count = len(case.contract_ids)
            case.assignment_count = len(case.assignment_ids)

    def action_view_assets(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Imóveis — %s") % self.name,
            "res_model": "property.asset",
            "view_mode": "list,form",
            "domain": [("id", "in", self.asset_ids.ids)],
        }

    def action_view_contracts(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Contratos — %s") % self.name,
            "res_model": "property.contract",
            "view_mode": "list,form",
            "domain": [("id", "in", self.contract_ids.ids)],
        }

    def action_view_assignments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Mandatos — %s") % self.name,
            "res_model": "property.broker.assignment",
            "view_mode": "list,form",
            "domain": [("id", "in", self.assignment_ids.ids)],
        }
