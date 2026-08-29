from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date


class PropertyMaintenanceBillWizard(models.TransientModel):
    _name = "property.maintenance.bill.wiz"
    _description = "Criar Fatura de Compra de Manutenção"

    maintenance_id = fields.Many2one(
        "property.maintenance",
        required=True,
        readonly=True,
        string="Manutenção",
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
        string="Fornecedor",
        domain="[('is_company','=',True),('supplier_rank','>',0)]",
    )
    invoice_date = fields.Date(
        default=fields.Date.today,
        required=True,
        string="Data da Fatura",
    )
    ref = fields.Char(
        string="Referência / Nº NF",
        help="Número da nota fiscal ou referência do documento do fornecedor.",
    )
    line_ids = fields.One2many(
        "property.maintenance.bill.wiz.line",
        "wizard_id",
        string="Itens",
        required=True,
    )
    company_id = fields.Many2one(
        "res.company",
        related="maintenance_id.company_id",
        store=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        store=True,
    )

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """Ao mudar fornecedor, limpa linhas para o usuário refazer."""
        if self.line_ids:
            self.line_ids = [(5, 0, 0)]

    def action_create_bill(self):
        """Cria account.move e property.maintenance.bill."""
        self.ensure_one()

        if not self.line_ids:
            raise UserError(_("Adicione pelo menos um item à fatura."))

        # 1. Cria account.move em DRAFT
        invoice_lines = []
        total_subtotal = 0.0

        for line in self.line_ids:
            amount = line.quantity * line.price_unit
            total_subtotal += amount

            invoice_lines.append(
                (
                    0,
                    0,
                    {
                        "name": line.name,
                        "quantity": line.quantity,
                        "price_unit": line.price_unit,
                        "account_id": line.account_id.id,
                    },
                )
            )

        invoice = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": self.partner_id.id,
                "invoice_date": self.invoice_date,
                "ref": self.ref,
                "company_id": self.company_id.id,
                "currency_id": self.currency_id.id,
                "maintenance_id": self.maintenance_id.id,
                "invoice_line_ids": invoice_lines,
            }
        )

        # 2. Cria property.maintenance.bill vinculando invoice
        bill = self.env["property.maintenance.bill"].create(
            {
                "maintenance_id": self.maintenance_id.id,
                "invoice_id": invoice.id,
            }
        )

        # 3. Posta mensagem no chatter
        self.maintenance_id.message_post(
            body=_(
                "Nova fatura de compra criada: %s\n"
                "Fornecedor: %s\n"
                "Valor: %s\n"
                "Status: Rascunho (aguardando revisão)"
            )
            % (invoice.name, self.partner_id.name, invoice.amount_total)
        )

        # 4. Retorna action para abrir a fatura criada
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoice.id,
            "target": "current",
            "context": {"form_view_initial_mode": "edit"},
        }


class PropertyMaintenanceBillWizardLine(models.TransientModel):
    _name = "property.maintenance.bill.wiz.line"
    _description = "Linha de Item da Fatura de Compra"

    wizard_id = fields.Many2one(
        "property.maintenance.bill.wiz",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(
        required=True,
        string="Descrição do Item",
    )
    quantity = fields.Float(
        default=1.0,
        required=True,
        string="Quantidade",
    )
    price_unit = fields.Monetary(
        required=True,
        currency_field="currency_id",
        string="Valor Unitário",
    )
    account_id = fields.Many2one(
        "account.account",
        required=True,
        domain="[('account_type','in',['expense','expense_depreciation'])]",
        string="Conta Contábil",
    )
    subtotal = fields.Monetary(
        compute="_compute_subtotal",
        store=True,
        currency_field="currency_id",
        string="Subtotal",
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="wizard_id.currency_id",
        store=True,
    )

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
