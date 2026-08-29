# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: PIX (BACEN)',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "Pagamentos instantâneos via PIX conforme especificação do Banco Central do Brasil.",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': [
        'payment_custom',    # provedor online PIX (portal/website)
        'account_payment',   # integração payment.provider <-> account.payment (journal_id)
    ],
    'data': [
        # QWeb templates (portal/website checkout)
        'views/payment_pix_templates.xml',
        # Formulário do provedor PIX (campos de configuração)
        'views/payment_provider_views.xml',
        # Wizard "Registrar Pagamento" com campos PIX
        'views/account_payment_register_views.xml',
        # Visões de movimentos PIX, diário e menus
        'views/account_payment_views.xml',
        # Dados: métodos de pagamento contábil (account.payment.method)
        'data/account_payment_method_data.xml',
        # Dados: payment.method (provedor online) e payment.provider
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    "author": "Franco Poleo / Manuela Silva",
    'license': 'LGPL-3',
}