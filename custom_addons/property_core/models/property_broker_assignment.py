from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date


class PropertyBrokerAssignment(models.Model):
    _name = "property.broker.assignment"
    _description = "Mandato de Corretor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "start_date desc"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Mandato", compute="_compute_name", store=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")

    # ==================== Vínculos ====================
    asset_id = fields.Many2one(
        "property.asset", string="Imóvel",
        required=True, ondelete="restrict", tracking=True
    )
    broker_id = fields.Many2one(
        "res.partner", string="Corretor",
        required=True, ondelete="restrict", tracking=True,
        domain=[("category_id.name", "ilike", "Corretor")],
    )

    # ==================== Tipo e Exclusividade ====================
    assignment_type = fields.Selection([
        ("rental", "Locação"),
        ("sale", "Venda"),
        ("both", "Locação e Venda"),
    ], string="Tipo", required=True, default="rental", tracking=True)

    exclusive = fields.Boolean(
        "Exclusividade", default=False, tracking=True,
        help="Impede que outro corretor seja vinculado ao mesmo imóvel no mesmo período e tipo"
    )

    # ==================== Período ====================
    start_date = fields.Date(
        "Início do Mandato", required=True,
        default=fields.Date.today, tracking=True
    )
    end_date = fields.Date("Fim do Mandato", tracking=True)

    # ==================== Resultado ====================
    contract_id = fields.Many2one(
        "property.contract", string="Contrato Gerado",
        readonly=True, copy=False
    )
    commission_id = fields.Many2one(
        "property.commission", string="Comissão Gerada",
        readonly=True, copy=False
    )

    # ==================== Status ====================
    status = fields.Selection([
        ("active", "Ativo"),
        ("expired", "Expirado"),
        ("converted", "Convertido"),
        ("cancelled", "Cancelado"),
    ], string="Status", compute="_compute_status", store=True, tracking=True)

    notes = fields.Text("Observações")
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, index=True
    )

    # ==================== Computed ====================

    @api.depends("broker_id", "asset_id", "assignment_type")
    def _compute_name(self):
        type_label = {"rental": "Locação", "sale": "Venda", "both": "Locação e Venda"}
        for rec in self:
            broker = rec.broker_id.name or "Corretor"
            asset = rec.asset_id.name or "Imóvel"
            tipo = type_label.get(rec.assignment_type, "")
            rec.name = "Mandato %s — %s (%s)" % (broker, asset, tipo)

    @api.depends("start_date", "end_date", "contract_id")
    def _compute_status(self):
        today = date.today()
        for rec in self:
            if rec.contract_id:
                rec.status = "converted"
            elif rec.end_date and rec.end_date < today:
                rec.status = "expired"
            else:
                rec.status = "active"

    # ==================== Constraints ====================

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(_("A data de fim deve ser posterior ao início do mandato."))

    @api.constrains("asset_id", "broker_id", "start_date", "end_date", "exclusive", "assignment_type")
    def _check_exclusivity(self):
        for rec in self:
            if not rec.exclusive:
                continue
            # Tipos conflitantes
            conflict_types = {
                "rental": ["rental", "both"],
                "sale": ["sale", "both"],
                "both": ["rental", "sale", "both"],
            }
            domain = [
                ("asset_id", "=", rec.asset_id.id),
                ("exclusive", "=", True),
                ("id", "!=", rec.id),
                ("assignment_type", "in", conflict_types.get(rec.assignment_type, [])),
                ("status", "=", "active"),
            ]
            for other in self.search(domain):
                # Verifica sobreposição de datas
                other_end = other.end_date or date(9999, 12, 31)
                rec_end = rec.end_date or date(9999, 12, 31)
                rec_start = rec.start_date or date.today()
                if rec_start <= other_end and other.start_date <= rec_end:
                    raise ValidationError(_(
                        "Conflito de exclusividade: o corretor %(broker)s já possui mandato "
                        "exclusivo para o imóvel %(asset)s no período informado."
                    ) % {
                        "broker": other.broker_id.name,
                        "asset": rec.asset_id.name,
                    })

    # ==================== Actions ====================

    def action_cancel(self):
        self.ensure_one()
        self.status = "cancelled"
        self.message_post(body=_("Mandato cancelado em %s.") % date.today())

    def action_open_dispute(self):
        """Abre caso de governança para disputa de comissão."""
        self.ensure_one()
        gov_model = self.env["governance.case"]
        values = {
            "name": _("Disputa de Mandato: %s") % self.name,
            "description": _(
                "<p>Disputa originada do mandato <strong>%s</strong>.</p>"
                "<p>Corretor: %s | Imóvel: %s | Tipo: %s</p>"
            ) % (
                self.reference,
                self.broker_id.name,
                self.asset_id.name,
                dict(self._fields["assignment_type"].selection).get(self.assignment_type, ""),
            ),
        }
        if "assignment_ids" in gov_model._fields:
            values["assignment_ids"] = [(4, self.id)]
        if "asset_ids" in gov_model._fields and self.asset_id:
            values["asset_ids"] = [(4, self.asset_id.id)]
        case = gov_model.create(values)
        self.message_post(
            body=_("Caso de governança %s aberto para este mandato.") % case.reference
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Caso de Governança",
            "res_model": "governance.case",
            "res_id": case.id,
            "view_mode": "form",
        }

    def action_view_governance_cases(self):
        self.ensure_one()
        gov_model = self.env["governance.case"]
        has_assignment_link = "assignment_ids" in gov_model._fields
        return {
            "type": "ir.actions.act_window",
            "name": "Casos de Governança",
            "res_model": "governance.case",
            "view_mode": "list,form",
            "domain": [("assignment_ids", "in", self.id)] if has_assignment_link else [("id", "=", 0)],
            "context": {"default_assignment_ids": [(4, self.id)]} if has_assignment_link else {},
        }

    # ==================== Cron ====================

    @api.model
    def action_cron_check_expiry(self):
        """Daily cron: notify about assignments expiring in 7 days and log expired ones."""
        today = date.today()
        from datetime import timedelta
        in_7 = today + timedelta(days=7)

        expiring_soon = self.search([
            ("status", "=", "active"),
            ("end_date", "<=", in_7),
            ("end_date", ">=", today),
        ])
        for rec in expiring_soon:
            already = rec.activity_ids.filtered(
                lambda a: "mandato" in (a.summary or "").lower()
            )
            if not already:
                days_left = (rec.end_date - today).days
                rec.activity_schedule(
                    "property_core.mail_activity_type_broker_assignment",
                    date_deadline=rec.end_date,
                    summary=_("Mandato vence em %s dias — %s") % (days_left, rec.broker_id.name),
                    note=_("O mandato do corretor '%s' para o imóvel '%s' vence em %s. Providencie renovação ou encerramento.") % (
                        rec.broker_id.name, rec.asset_id.name, rec.end_date
                    ),
                    user_id=rec.create_uid.id,
                )

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.broker.assignment") or "New"
                )
        return super().create(vals_list)