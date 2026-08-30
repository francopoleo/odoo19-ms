# -*- coding: utf-8 -*-
{
    "name": "Enterprise Configuration Seed",
    "summary": "Catálogos operacionais padrão do ERP imobiliário enterprise.",
    "version": "19.0.1.0.0",
    "category": "Real Estate/Configuration",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": [
        "common_base",
        "document_core",
        "document_dossier",
        "governance",
        "property_core",
        "property_contract_amendment_enterprise",
    ],
    "data": [],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
