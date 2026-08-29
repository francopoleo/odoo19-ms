# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def action_create_payments(self):
        """Bloqueia o wizard de pagamento se alguma fatura for provisória."""
        provisional = self.line_ids.move_id.filtered(
            lambda m: m.name and any(p.startswith("PROV-") for p in m.name.split())
        )
        if provisional:
            names = "\n".join(provisional.mapped("display_name"))
            raise UserError(_(
                "As seguintes faturas estão com número fiscal provisório.\n"
                "Informe o número real do documento fiscal e salve antes de pagar:\n\n%s",
                names,
            ))
        return super().action_create_payments()
