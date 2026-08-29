# -*- coding: utf-8 -*-

from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_post(self):
        for payment in self:
            invoices = payment.reconciled_invoice_ids | payment.reconciled_bill_ids
            invoices._check_real_fiscal_number_before_payment()

        return super().action_post()
