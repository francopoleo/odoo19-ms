# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PropertyPaymentProofManual(models.TransientModel):
    _name = "property.payment.proof.manual"
    _description = "Registrar Pagamento Manual (sem comprovante físico)"

    rent_id = fields.Many2one("property.rent", string="Parcela", required=True, readonly=True)
    contract_id = fields.Many2one("property.contract", related="rent_id.contract_id", readonly=True)
    partner_id = fields.Many2one("res.partner", related="rent_id.partner_id", readonly=True)
    due_date = fields.Date(related="rent_id.due_date", readonly=True, string="Vencimento")
    amount_due = fields.Monetary(related="rent_id.amount_due", readonly=True, string="Valor em Aberto", currency_field="currency_id")
    currency_id = fields.Many2one(related="rent_id.currency_id", readonly=True)

    amount = fields.Monetary("Valor Pago", required=True, currency_field="currency_id")
    payment_date = fields.Date("Data de Pagamento", required=True, default=fields.Date.today)
    payment_method = fields.Selection([
        ("pix", "PIX"),
        ("transfer", "Transferência Bancária"),
        ("boleto", "Boleto"),
        ("cash", "Dinheiro"),
        ("check", "Cheque"),
    ], string="Forma de Pagamento", required=True)
    notes = fields.Text(
        "Motivo / Observação",
        required=True,
        help="Obrigatório para pagamentos sem comprovante físico. Ex: depósito em espécie confirmado presencialmente, transferência identificada por extrato bancário, etc.",
    )

    @api.onchange("rent_id")
    def _onchange_rent_id(self):
        if self.rent_id:
            residual = getattr(self.rent_id, "residual_amount", 0) or self.rent_id.amount_due
            self.amount = residual

    def action_register(self):
        self.ensure_one()
        rent = self.rent_id

        if rent.status not in ("open", "late", "partial"):
            raise UserError(_("Esta parcela não está disponível para pagamento (status: %s).") % rent.status)

        # Guard: prevent double payment
        reconciled = rent.payment_proof_ids.filtered(
            lambda p: p.state == "reconciled" and p.proof_type != "late_fee"
        )
        if reconciled:
            raise UserError(_(
                "Esta parcela já possui um comprovante de pagamento conciliado (%s). "
                "Cancele o comprovante existente antes de registrar outro pagamento."
            ) % reconciled[0].name)

        # Create manual proof pre-filled, state=approved (skip OCR steps)
        proof = self.env["property.payment.proof"].create({
            "proof_type": "manual",
            "contract_id": rent.contract_id.id,
            "rent_id": rent.id,
            "amount": self.amount,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "payer_name": rent.partner_id.name,
            "extraction_log": _("Pagamento manual sem comprovante físico.\nMotivo: %s") % self.notes,
            "state": "approved",
        })

        # Write payment fields on rent and reconcile
        rent.write({
            "amount_paid": self.amount,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "payment_notes": self.notes,
        })
        result = rent.action_register_payment()

        # Link payment record
        payment = self.env["property.rent.payment"].search([
            ("rent_id", "=", rent.id),
            ("payment_date", "=", self.payment_date),
        ], order="id desc", limit=1)
        proof.write({
            "payment_id": payment.id if payment else False,
            "state": "reconciled",
        })
        proof.message_post(body=_(
            "<b>Pagamento Manual Registrado</b><br/>"
            "Valor: R$ %.2f | Data: %s | Método: %s<br/>"
            "Motivo: %s"
        ) % (self.amount, self.payment_date, dict(self._fields["payment_method"].selection).get(self.payment_method, "-"), self.notes))

        return result or {"type": "ir.actions.act_window_close"}