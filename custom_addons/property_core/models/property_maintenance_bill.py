from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PropertyMaintenanceBill(models.Model):
    _name = "property.maintenance.bill"
    _description = "Fatura de Compra de Manutenção"
    _order = "invoice_date desc"

    # ==================== Vínculos Principais ====================
    maintenance_id = fields.Many2one(
        "property.maintenance",
        required=True,
        ondelete="cascade",
        index=True,
        string="Manutenção",
    )
    invoice_id = fields.Many2one(
        "account.move",
        required=True,
        ondelete="cascade",
        index=True,
        domain="[('move_type','=','in_invoice')]",
        string="Fatura de Compra",
    )

    # ==================== Campos Related (stored para performance) ====================
    partner_id = fields.Many2one(
        "res.partner",
        related="invoice_id.partner_id",
        store=True,
        string="Fornecedor",
    )
    invoice_date = fields.Date(
        related="invoice_id.invoice_date",
        store=True,
        string="Data da Fatura",
    )
    amount_total = fields.Monetary(
        related="invoice_id.amount_total",
        store=True,
        string="Valor Total",
    )
    amount_residual = fields.Monetary(
        related="invoice_id.amount_residual",
        store=True,
        string="Valor a Pagar",
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="invoice_id.currency_id",
        store=True,
    )
    payment_state = fields.Selection(
        related="invoice_id.payment_state",
        store=True,
        string="Pagamento",
    )
    state = fields.Selection(
        related="invoice_id.state",
        store=True,
        string="Status",
    )
    name = fields.Char(
        related="invoice_id.name",
        store=True,
        string="Nº da Fatura",
    )
    ref = fields.Char(
        related="invoice_id.ref",
        store=True,
        string="Referência do Fornecedor",
    )
    company_id = fields.Many2one(
        "res.company",
        related="maintenance_id.company_id",
        store=True,
    )
    asset_id = fields.Many2one(
        "property.asset",
        related="maintenance_id.asset_id",
        store=True,
        string="Imóvel",
    )

    # ==================== Actions ====================

    def action_view_invoice(self):
        """Abre a fatura de compra em accounting."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": self.invoice_id.id,
            "target": "new",
            "context": {"form_view_initial_mode": "edit"},
        }

    def action_post_invoice(self):
        """Posta a fatura (cria journal entries automaticamente via base_accounting_kit)."""
        self.ensure_one()
        if self.invoice_id.state != "draft":
            raise UserError(
                _("Apenas faturas em rascunho podem ser postadas.")
            )
        self.invoice_id.action_post()
        self.maintenance_id.message_post(
            body=_("Fatura %s postada. Valor: %s") %
            (self.name, self.amount_total)
        )

    def action_register_payment(self):
        """Abre o wizard padrão Odoo de registro de pagamento."""
        self.ensure_one()
        if self.invoice_id.state != "posted":
            raise UserError(
                _("Apenas faturas postadas podem ter pagamentos registrados.")
            )
        return self.invoice_id.action_register_payment()
