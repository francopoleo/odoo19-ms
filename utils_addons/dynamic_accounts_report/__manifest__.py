# -*- coding: utf-8 -*-
"""
Odoo19 Dynamic Accounting Reports
==================================

Módulo de relatórios contábeis dinâmicos para Odoo 19.

Features:
---------
• Relatórios dinâmicos de contabilidade
• Extrato de diário geral
• Balancete de verificação
• Balanço patrimonial
• Demonstração de resultado
• Livro de caixa
• Razão de parceiros
• Contas a pagar vencidas
• Contas a receber vencidas
• Livro de banco
• Relatório de impostos
• Dashboards visuais interativos

Author: Cybrosys Techno Solutions
Modified by: Franco Poleo / Manuela Silva
License: LGPL-3
"""

{
    "name": "Odoo19 Dynamic Accounting Reports",
    "version": "19.0.1.0.0",
    "category": "Real Estate/Accounting",
    "summary": "Relatórios contábeis dinâmicos para Odoo 19",
    "description": """
        Módulo de relatórios contábeis dinâmicos que cria extrato de diário geral,
        balancete de verificação, balanço patrimonial, demonstração de resultado,
        livro de caixa, razão de parceiros e outros relatórios contábeis.
    """,
    "author": "Cybrosys Techno Solutions",
    "website": "https://www.cybrosys.com",
    "license": "LGPL-3",
    "depends": ["base_accounting_kit"],
    "data": [
        # Security
        "security/ir.model.access.csv",
        # Views
        "views/accounting_report_views.xml",
        # Reports
        "report/trial_balance.xml",
        "report/general_ledger_templates.xml",
        "report/financial_report_template.xml",
        "report/partner_ledger_templates.xml",
        "report/financial_reports_views.xml",
        "report/balance_sheet_report_templates.xml",
        "report/bank_book_templates.xml",
        "report/aged_payable_templates.xml",
        "report/aged_receivable_templates.xml",
        "report/tax_report_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "dynamic_accounts_report/static/src/xml/general_ledger_view.xml",
            "dynamic_accounts_report/static/src/xml/trial_balance_view.xml",
            "dynamic_accounts_report/static/src/xml/cash_flow_templates.xml",
            "dynamic_accounts_report/static/src/xml/bank_flow_templates.xml",
            "dynamic_accounts_report/static/src/xml/profit_and_loss_templates.xml",
            "dynamic_accounts_report/static/src/xml/balance_sheet_template.xml",
            "dynamic_accounts_report/static/src/xml/partner_ledger_view.xml",
            "dynamic_accounts_report/static/src/xml/aged_payable_report_views.xml",
            "dynamic_accounts_report/static/src/xml/aged_receivable_report_views.xml",
            "dynamic_accounts_report/static/src/xml/tax_report_views.xml",
            "dynamic_accounts_report/static/src/css/accounts_report.css",
            "dynamic_accounts_report/static/src/js/general_ledger.js",
            "dynamic_accounts_report/static/src/js/trial_balance.js",
            "dynamic_accounts_report/static/src/js/cash_flow.js",
            "dynamic_accounts_report/static/src/js/bank_flow.js",
            "dynamic_accounts_report/static/src/js/profit_and_loss.js",
            "dynamic_accounts_report/static/src/js/balance_sheet.js",
            "dynamic_accounts_report/static/src/js/partner_ledger.js",
            "dynamic_accounts_report/static/src/js/aged_payable_report.js",
            "dynamic_accounts_report/static/src/js/aged_receivable_report.js",
            "dynamic_accounts_report/static/src/js/tax_report.js",
        ]
    },
    "images": ["static/description/banner.gif"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
