from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class PropertyMaintenance(models.Model):
    _name = "property.maintenance"
    _description = "Manutenção de Imóvel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, request_date desc"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Título", required=True, tracking=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")
    description = fields.Text("Descrição")

    # ==================== Tipo / Prioridade ====================
    maintenance_type = fields.Selection([
        ("preventive", "Preventiva"),
        ("corrective", "Corretiva"),
        ("emergency", "Emergência"),
        ("improvement", "Benfeitoria"),
    ], string="Tipo", required=True, default="corrective", tracking=True)

    priority = fields.Selection([
        ("0", "Baixa"),
        ("1", "Normal"),
        ("2", "Alta"),
        ("3", "Crítica"),
    ], string="Prioridade", default="1", tracking=True)

    responsible_party = fields.Selection([
        ("owner", "Proprietário"),
        ("tenant", "Locatário"),
        ("condominium", "Condomínio"),
    ], string="Responsável pelo Custo", default="owner", tracking=True)

    # ==================== Vínculos ====================
    asset_id = fields.Many2one(
        "property.asset", string="Imóvel",
        required=True, ondelete="cascade", tracking=True
    )
    contract_id = fields.Many2one(
        "property.contract", string="Contrato",
        ondelete="set null", tracking=True
    )
    vendor_id = fields.Many2one(
        "res.partner", string="Fornecedor / Prestador",
        tracking=True
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        index=True,
    )

    # ==================== Datas ====================
    request_date = fields.Date(
        "Data da Solicitação", default=fields.Date.today, tracking=True
    )
    scheduled_date = fields.Date("Data Agendada", tracking=True)
    completion_date = fields.Date("Data de Conclusão", tracking=True)

    # ==================== Financeiro ====================
    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id", store=True
    )
    cost_estimate = fields.Monetary(
        "Orçamento", currency_field="currency_id", tracking=True
    )
    cost_actual = fields.Monetary(
        "Custo Real", currency_field="currency_id", tracking=True
    )

    # ==================== Arquivos ====================
    attachment_ids = fields.Many2many(
        "ir.attachment",
        relation="property_maintenance_attachment_rel",
        column1="maintenance_id",
        column2="attachment_id",
        string="Fotos / Orçamentos",
        help="Anexos rápidos da manutenção, como fotos, orçamentos, notas e relatórios.",
    )
    attachment_count = fields.Integer(
        "Arquivos", compute="_compute_attachment_count"
    )
    media_ids = fields.One2many("property.media", "maintenance_id", string="Fotos / Mídias", help="Mídias estruturadas da manutenção, como antes/depois, evidências e imagens técnicas.")
    media_count = fields.Integer("Qtd. Mídias", compute="_compute_media_count")

    # ==================== Compras Vinculadas ====================
    bill_ids = fields.One2many(
        "property.maintenance.bill",
        "maintenance_id",
        string="Compras Vinculadas",
        help="Faturas de compra/manutenção vinculadas a este maintenance.",
    )
    bill_count = fields.Integer(
        "Qtd. Compras",
        compute="_compute_bill_totals",
        store=True,
    )
    bill_amount_total = fields.Monetary(
        "Total de Compras",
        currency_field="currency_id",
        compute="_compute_bill_totals",
        store=True,
        help="Soma de todas as faturas de compra (não canceladas).",
    )
    bill_amount_due = fields.Monetary(
        "A Pagar",
        currency_field="currency_id",
        compute="_compute_bill_totals",
        store=True,
        help="Saldo a pagar nas faturas (amount_residual).",
    )

    # ==================== Status ====================
    status = fields.Selection([
        ("draft", "Solicitado"),
        ("quoted", "Orçado"),
        ("scheduled", "Agendado"),
        ("in_progress", "Em Execução"),
        ("done", "Concluído"),
        ("cancelled", "Cancelado"),
    ], default="draft", tracking=True, required=True)

    # ==================== Computed ====================

    @api.depends("attachment_ids")
    def _compute_attachment_count(self):
        for maint in self:
            maint.attachment_count = len(maint.attachment_ids)

    @api.depends("media_ids")
    def _compute_media_count(self):
        for maint in self:
            maint.media_count = len(maint.media_ids)

    @api.depends("bill_ids", "bill_ids.state", "bill_ids.amount_total", "bill_ids.amount_residual")
    def _compute_bill_totals(self):
        for maint in self:
            active = maint.bill_ids.filtered(lambda b: b.state != "cancel")
            maint.bill_count = len(active)
            maint.bill_amount_total = sum(active.mapped("amount_total"))
            maint.bill_amount_due = sum(active.mapped("amount_residual"))

    # ==================== Actions ====================

    def action_quote(self):
        self.ensure_one()
        if self.status != "draft":
            raise UserError(_("Apenas solicitações novas podem ser orçadas."))
        self.status = "quoted"
        self.message_post(body=_("Manutenção orçada: %s") % self.cost_estimate)

    def action_schedule(self):
        self.ensure_one()
        if self.status not in ("draft", "quoted"):
            raise UserError(_("Esta manutenção não pode ser agendada."))
        if not self.scheduled_date:
            raise UserError(_("Informe a data agendada."))
        self.status = "scheduled"
        self.message_post(body=_("Manutenção agendada para %s.") % self.scheduled_date)

    def action_start(self):
        self.ensure_one()
        if self.status not in ("draft", "quoted", "scheduled"):
            raise UserError(_("Esta manutenção não pode ser iniciada."))
        self.status = "in_progress"
        self.message_post(body=_("Manutenção iniciada em %s.") % date.today())

    def action_done(self):
        self.ensure_one()
        if self.status not in ("scheduled", "in_progress", "draft", "quoted"):
            raise UserError(_("Esta manutenção não pode ser concluída."))
        if not self.completion_date:
            self.completion_date = date.today()
        self.status = "done"
        self.message_post(
            body=_("Manutenção concluída em %s. Custo real: %s.") % (
                self.completion_date, self.cost_actual or self.cost_estimate
            )
        )
        # Notifica proprietário do imóvel
        owner = self.asset_id.owner_id if self.asset_id else None
        if owner:
            email_to = (
                owner.partner_id.email if owner.partner_id else owner.email
            )
            if email_to:
                template = self.env.ref(
                    "property_core.email_template_manutencao_concluida",
                    raise_if_not_found=False,
                )
                if template:
                    try:
                        template.send_mail(self.id, force_send=False)
                    except Exception:
                        pass

    def action_cancel(self):
        self.ensure_one()
        self.status = "cancelled"
        self.message_post(body=_("Manutenção cancelada."))

    def action_reset_draft(self):
        self.ensure_one()
        self.status = "draft"

    def action_create_bill(self):
        """Abre wizard para criar nova fatura de compra vinculada."""
        self.ensure_one()
        return {
            "name": _("Nova Fatura de Compra"),
            "type": "ir.actions.act_window",
            "res_model": "property.maintenance.bill.wiz",
            "view_mode": "form",
            "target": "new",
            "context": {"default_maintenance_id": self.id},
        }

    def action_view_bills(self):
        """Abre lista de faturas vinculadas."""
        self.ensure_one()
        return {
            "name": _("Compras Vinculadas"),
            "type": "ir.actions.act_window",
            "res_model": "property.maintenance.bill",
            "view_mode": "list,form",
            "domain": [("maintenance_id", "=", self.id)],
            "context": {
                "default_maintenance_id": self.id,
            },
        }

    def action_view_media(self):
        """View media related to this maintenance."""
        self.ensure_one()
        return {
            "name": _("Fotos / Mídias da Manutenção"),
            "type": "ir.actions.act_window",
            "res_model": "property.media",
            "view_mode": "kanban,list,form",
            "domain": [("maintenance_id", "=", self.id)],
            "context": {
                "default_maintenance_id": self.id,
                "default_asset_id": self.asset_id.id,
                "default_purpose": "maintenance",
                "default_context_selection": "maintenance",
                "default_upload_kind": self.env.context.get("default_upload_kind", "auto"),
            },
        }

    def action_open_bulk_media_wizard(self):
        """Open bulk media upload wizard for this maintenance."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Adicionar Múltiplas Mídias"),
            "res_model": "property.media.bulk.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_maintenance_id": self.id,
                "default_asset_id": self.asset_id.id,
                "default_context_selection": "maintenance",
                "default_purpose": "maintenance",
                "default_upload_kind": self.env.context.get("default_upload_kind", "auto"),
            },
        }

    # ==================== Constraints ====================

    @api.constrains("cost_estimate", "cost_actual")
    def _check_costs(self):
        for maint in self:
            if maint.cost_estimate < 0:
                raise ValidationError(_("O orçamento não pode ser negativo."))
            if maint.cost_actual < 0:
                raise ValidationError(_("O custo real não pode ser negativo."))

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.maintenance") or "New"
                )
        return super().create(vals_list)