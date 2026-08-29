# -*- coding: utf-8 -*-
{
    "name": "Property Contract OCR Templates",
    "version": "19.0.1.1.0",
    "category": "Real Estate/Documents",
    "summary": "Templates de OCR/regex para extrair dados de contratos imobiliários",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": ["property_contract_history"],
    "post_init_hook": "post_init_hook",
    "data": [
        "security/ir.model.access.csv",
        "views/property_contract_ocr_template_views.xml",
        "views/property_contract_history_views.xml",
        "data/lease_template_data.xml",
        "data/default_templates.xml",
    ],
    "installable": True,
    "application": False,
}
