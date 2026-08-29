# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    """Estende o wizard de registro de pagamento para sinalizar diário PIX.

    Campos como pix_e2e_id e pix_partner_key ficam disponíveis no
    account.payment criado — editáveis diretamente na tela do pagamento.
    """
    _inherit = 'account.payment.register'

    # Campo computed não-armazenado: não cria coluna no banco de dados.
    is_pix = fields.Boolean(
        compute='_compute_is_pix',
        store=False,
        help="Verdadeiro quando o diário selecionado é um Diário PIX.",
    )

    @api.depends('journal_id.is_pix')
    def _compute_is_pix(self):
        for wizard in self:
            wizard.is_pix = bool(wizard.journal_id.is_pix)