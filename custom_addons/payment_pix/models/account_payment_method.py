# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.fields import Domain


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        """Override: registra PIX como método de pagamento contábil.

        mode='multi' → pode ser adicionado a múltiplos diários.
        type=('bank',) → disponível apenas para diários do tipo Banco.
        A restrição a diários is_pix=True é feita em _get_payment_method_domain.
        """
        res = super()._get_payment_method_information()
        res['pix'] = {'mode': 'multi', 'type': ('bank',)}
        return res

    @api.model
    def _get_payment_method_domain(self, code, **kwargs):
        """Override: restringe PIX aos diários marcados como Diário PIX."""
        domain = super()._get_payment_method_domain(code, **kwargs)
        if code == 'pix':
            domain &= Domain('is_pix', '=', True)
        return domain