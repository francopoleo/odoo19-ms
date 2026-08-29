# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_pix = fields.Boolean(
        string="Diário PIX",
        default=False,
        help=(
            "Marque para identificar este como o diário de movimentos PIX.\n"
            "• Ativa o rastreamento de Chave PIX e ID E2E nos pagamentos.\n"
            "• Adiciona automaticamente PIX como método de pagamento (Inbound e Outbound).\n"
            "• Exibe os pagamentos no menu Contabilidade → PIX."
        ),
    )

    # === CRUD METHODS === #

    @api.model_create_multi
    def create(self, vals_list):
        journals = super().create(vals_list)
        journals.filtered('is_pix')._pix_sync_payment_method_lines()
        return journals

    def write(self, vals):
        res = super().write(vals)
        if vals.get('is_pix'):
            self.filtered('is_pix')._pix_sync_payment_method_lines()
        return res

    # === PIX METHODS === #

    def _pix_sync_payment_method_lines(self):
        """Adiciona linhas de método de pagamento PIX (inbound e outbound)
        ao diário, caso ainda não existam.

        Chamado automaticamente ao criar ou salvar um diário com is_pix=True.
        """
        pix_methods = self.env['account.payment.method'].search([('code', '=', 'pix')])
        if not pix_methods:
            return

        lines_to_create = []
        for journal in self:
            existing_methods = (
                journal.inbound_payment_method_line_ids.payment_method_id
                | journal.outbound_payment_method_line_ids.payment_method_id
            )
            for method in pix_methods:
                if method not in existing_methods:
                    lines_to_create.append({
                        'name': method.name,
                        'payment_method_id': method.id,
                        'journal_id': journal.id,
                    })

        if lines_to_create:
            self.env['account.payment.method.line'].create(lines_to_create)