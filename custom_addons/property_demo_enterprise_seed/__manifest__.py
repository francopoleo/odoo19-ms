# -*- coding: utf-8 -*-
{
    "name": "Real Estate Enterprise Demo Seed",
    "summary": "Gera massa enterprise completa para imóveis, contratos, documentos, governança, corretores, mandatos, comissões, repasses e OCR.",
    "version": "19.0.1.0.12",
    "category": "Real Estate",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    # Mantido propositalmente enxuto.
    # Os módulos de dossiê, governança, comprovantes, aditivos e valuation são usados de forma condicional pelo Python.
    # Assim o seed não derruba a instalação quando algum módulo opcional ainda não está instalado ou está temporariamente not installable.
    "depends": [
        "property_core",
        "document_core",
        "governance",
        "document_property_integration",
        "governance_property_integration",
        "document_governance_integration",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/01_document_types.xml",
        "data/03_documents.xml",
        "data/04_governance_types.xml",
        "data/06_governance_cases.xml",
        "data/07_property_assets.xml",
        "data/09_integrations.xml",
        "views/demo_generator_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "application": False,
    "installable": True,  # Desabilitar demo
}
