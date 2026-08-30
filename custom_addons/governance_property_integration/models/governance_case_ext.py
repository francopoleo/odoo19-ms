from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GovernanceCasePropertyExt(models.Model):
    _inherit = "governance.case"

    case_scope = fields.Selection(
        [
            ("single_property", "Um imóvel"),
            ("portfolio", "Carteira de imóveis"),
            ("corporate", "Corporativo / sem imóvel específico"),
        ],
        string="Escopo do Caso",
        default="corporate",
        tracking=True,
        help="Define se o caso trata uma unidade, uma carteira ou um assunto corporativo.",
    )
    primary_asset_id = fields.Many2one(
        "property.asset",
        string="Imóvel Principal",
        domain="[('company_id', '=', company_id)]",
        check_company=True,
        tracking=True,
        help="Imóvel de referência do caso. Os demais imóveis continuam em Imóveis Relacionados.",
    )

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

    @api.constrains("case_scope", "asset_ids", "primary_asset_id", "contract_ids")
    def _check_property_case_scope(self):
        for case in self:
            if case.case_scope == "single_property" and len(case.asset_ids) > 1:
                raise ValidationError(_(
                    "Um caso com escopo 'Um imóvel' não pode conter vários imóveis. "
                    "Use o escopo 'Carteira de imóveis'."
                ))
            if case.primary_asset_id and case.primary_asset_id not in case.asset_ids:
                raise ValidationError(_(
                    "O imóvel principal precisa estar entre os imóveis relacionados."
                ))
            if case.asset_ids and case.contract_ids:
                invalid_contracts = case.contract_ids.filtered(
                    lambda contract: contract.asset_id and contract.asset_id not in case.asset_ids
                )
                if invalid_contracts:
                    raise ValidationError(_(
                        "Todos os contratos relacionados precisam pertencer a um dos imóveis "
                        "selecionados no caso. Contratos incompatíveis: %s"
                    ) % ", ".join(invalid_contracts.mapped("display_name")))
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
