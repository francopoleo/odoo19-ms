# -*- coding: utf-8 -*-
{
    "name": "Histórico de Contratos com OCR",
    "version": "19.0.1.0.2",
    "category": "Real Estate",
    "summary": "Upload e extração OCR de contratos históricos (aluguel, venda, financiamento) com sincronização para imóveis.",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": [
        "property_core",
        "property_payment_proof",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence.xml",
        "views/property_contract_history_views.xml",
        "views/property_asset_views.xml",
        "views/menu_views.xml",
        "wizard/bulk_upload_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
