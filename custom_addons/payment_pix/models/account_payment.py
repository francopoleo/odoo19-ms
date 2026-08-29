# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # ---------------------------------------------------------------------------
    # Campos PIX
    # ---------------------------------------------------------------------------

    is_pix = fields.Boolean(
        string="Pagamento PIX",
        compute='_compute_is_pix',
        store=True,
        help="Verdadeiro quando o pagamento é registrado no diário PIX.",
    )
    pix_e2e_id = fields.Char(
        string="ID E2E (BACEN)",
        copy=False,
        help=(
            "Identificador de transação End-to-End do BACEN. "
            "Formato: E + ISPB (8 dígitos) + aaMMddHHmm + identificador (11 caracteres). "
            "Exemplo: E12345678202501011200ABCDE123456"
        ),
    )
    pix_partner_key = fields.Char(
        string="Chave PIX do Parceiro",
        help="Chave PIX do outro lado da transação (recebedor para saídas, pagador para entradas).",
    )
    pix_partner_key_type = fields.Selection(
        string="Tipo de Chave",
        selection=[
            ('cpf',    'CPF'),
            ('cnpj',   'CNPJ'),
            ('phone',  'Telefone'),
            ('email',  'E-mail'),
            ('random', 'Chave Aleatória (EVP)'),
        ],
    )

    # ---------------------------------------------------------------------------
    # Campos computados: Conta Origem e Conta Destino
    # ---------------------------------------------------------------------------

    pix_conta_origem_id = fields.Many2one(
        comodel_name='account.account',
        string="Conta Origem",
        compute='_compute_pix_flow_accounts',
        help=(
            "Conta de onde o dinheiro saiu (débito para outbound, "
            "crédito para inbound no lançamento contábil).\n"
            "• Entrada PIX: Conta a Receber do cliente\n"
            "• Saída PIX:   Conta PIX (banco)"
        ),
    )
    pix_conta_destino_id = fields.Many2one(
        comodel_name='account.account',
        string="Conta Destino",
        compute='_compute_pix_flow_accounts',
        help=(
            "Conta para onde o dinheiro foi (crédito para outbound, "
            "débito para inbound no lançamento contábil).\n"
            "• Entrada PIX: Conta PIX (banco)\n"
            "• Saída PIX:   Conta a Pagar ao fornecedor"
        ),
    )

    # ---------------------------------------------------------------------------
    # Computes
    # ---------------------------------------------------------------------------

    @api.depends('journal_id.is_pix')
    def _compute_is_pix(self):
        for payment in self:
            payment.is_pix = payment.journal_id.is_pix

    @api.depends('payment_type', 'journal_id', 'destination_account_id')
    def _compute_pix_flow_accounts(self):
        """
        Determina as contas de origem e destino para a visão de movimentos PIX.

        Lógica contábil:
          Entrada (inbound — recebemos do cliente):
            Débito:  Conta PIX (banco)            ← destino do dinheiro
            Crédito: Conta a Receber do cliente   ← origem do dinheiro
          → pix_conta_origem = receivable   | pix_conta_destino = PIX bank

          Saída (outbound — pagamos ao fornecedor):
            Débito:  Conta a Pagar ao fornecedor  ← quitamos a dívida
            Crédito: Conta PIX (banco)            ← origem do dinheiro
          → pix_conta_origem = PIX bank    | pix_conta_destino = payable
        """
        for payment in self:
            pix_bank = payment.journal_id.default_account_id
            partner_account = payment.destination_account_id

            if payment.payment_type == 'inbound':
                # Recebemos: o dinheiro vem da conta a receber e vai para a conta PIX
                payment.pix_conta_origem_id = partner_account  # a receber (crédito)
                payment.pix_conta_destino_id = pix_bank        # PIX banco (débito)
            else:
                # Pagamos: o dinheiro sai da conta PIX e quita a conta a pagar
                payment.pix_conta_origem_id = pix_bank         # PIX banco (crédito)
                payment.pix_conta_destino_id = partner_account # a pagar (débito)