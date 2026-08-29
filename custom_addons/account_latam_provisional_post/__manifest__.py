# -*- coding: utf-8 -*-
{
    "name": "Documento Fiscal Provisório LATAM/Brasil",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Permite confirmar faturas LATAM/Brasil com número fiscal provisório e exige número real no pagamento.",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": [
        "account",
        "l10n_latam_invoice_document",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
