from odoo import api, fields, models, _
from datetime import date
from dateutil.relativedelta import relativedelta


class PropertyOwnerStatement(models.TransientModel):
    _name = "property.owner.statement"
    _description = "Extrato do Proprietário"

    # ==================== Parâmetros ====================
    owner_id = fields.Many2one(
        "res.partner", string="Proprietário",
        required=True,
        domain=[("category_id.name", "ilike", "Proprietário")],
    )
    date_from = fields.Date(
        "De", required=True,
        default=lambda self: date.today().replace(day=1)
    )
    date_to = fields.Date(
        "Até", required=True,
        default=lambda self: date.today()
    )

    # ==================== Receitas ====================
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id
    )
    rent_income = fields.Monetary(
        "Aluguéis Recebidos", currency_field="currency_id",
        compute="_compute_totals", store=False
    )
    rent_count = fields.Integer(
        "Parcelas Pagas", compute="_compute_totals", store=False
    )

    # ==================== Deduções ====================
    commission_total = fields.Monetary(
        "Comissões Pagas", currency_field="currency_id",
        compute="_compute_totals", store=False
    )
    maintenance_total = fields.Monetary(
        "Manutenções Realizadas", currency_field="currency_id",
        compute="_compute_totals", store=False
    )
    fixed_costs_total = fields.Monetary(
        "Custos Fixos (IPTU + Cond. + Foro)", currency_field="currency_id",
        compute="_compute_totals", store=False,
        help="Custo anual dos imóveis rateado pelo período"
    )

    # ==================== Resultado ====================
    gross_income = fields.Monetary(
        "Receita Bruta", currency_field="currency_id",
        compute="_compute_totals", store=False
    )
    total_deductions = fields.Monetary(
        "Total de Deduções", currency_field="currency_id",
        compute="_compute_totals", store=False
    )
    net_result = fields.Monetary(
        "Resultado Líquido", currency_field="currency_id",
        compute="_compute_totals", store=False
    )

    # ==================== Detalhes (para o relatório) ====================
    rent_ids = fields.Many2many(
        "property.rent", compute="_compute_totals", store=False
    )
    commission_ids = fields.Many2many(
        "property.commission", compute="_compute_totals", store=False,
        relation="stmt_commission_rel"
    )
    maintenance_ids = fields.Many2many(
        "property.maintenance", compute="_compute_totals", store=False,
        relation="stmt_maintenance_rel"
    )

    # ==================== Computed ====================

    @api.depends("owner_id", "date_from", "date_to")
    def _compute_totals(self):
        for stmt in self:
            if not stmt.owner_id or not stmt.date_from or not stmt.date_to:
                stmt.rent_income = 0
                stmt.rent_count = 0
                stmt.commission_total = 0
                stmt.maintenance_total = 0
                stmt.fixed_costs_total = 0
                stmt.gross_income = 0
                stmt.total_deductions = 0
                stmt.net_result = 0
                stmt.rent_ids = False
                stmt.commission_ids = False
                stmt.maintenance_ids = False
                continue

            asset_ids = self.env["property.asset"].search([("owner_id", "=", stmt.owner_id.id)]).ids

            # Aluguéis pagos no período
            rents = self.env["property.rent"].search([
                ("asset_id", "in", asset_ids),
                ("status", "=", "paid"),
                ("payment_date", ">=", stmt.date_from),
                ("payment_date", "<=", stmt.date_to),
            ])
            stmt.rent_ids = rents
            stmt.rent_income = sum(rents.mapped("amount_paid"))
            stmt.rent_count = len(rents)

            # Comissões pagas no período
            commissions = self.env["property.commission"].search([
                ("asset_id", "in", asset_ids),
                ("status", "=", "paid"),
                ("payment_date", ">=", stmt.date_from),
                ("payment_date", "<=", stmt.date_to),
            ])
            stmt.commission_ids = commissions
            stmt.commission_total = sum(commissions.mapped("commission_value"))

            # Manutenções concluídas no período
            maintenances = self.env["property.maintenance"].search([
                ("asset_id", "in", asset_ids),
                ("status", "=", "done"),
                ("completion_date", ">=", stmt.date_from),
                ("completion_date", "<=", stmt.date_to),
            ])
            stmt.maintenance_ids = maintenances
            stmt.maintenance_total = sum(maintenances.mapped("cost_actual"))

            # Custos fixos rateados pelo período
            days_in_period = (stmt.date_to - stmt.date_from).days + 1
            days_in_year = 365
            ratio = days_in_period / days_in_year
            assets = self.env["property.asset"].search([("id", "in", asset_ids)])
            annual_costs = sum(assets.mapped("total_annual_costs"))
            stmt.fixed_costs_total = annual_costs * ratio

            stmt.gross_income = stmt.rent_income
            stmt.total_deductions = (
                stmt.commission_total
                + stmt.maintenance_total
                + stmt.fixed_costs_total
            )
            stmt.net_result = stmt.gross_income - stmt.total_deductions

    # ==================== Actions ====================

    def action_print(self):
        self.ensure_one()
        return self.env.ref(
            "property_core.action_report_owner_statement"
        ).report_action(self)