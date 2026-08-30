# -*- coding: utf-8 -*-
{
    "name": "Real Estate Enterprise Demo Seed",
    "summary": "Gera massa enterprise completa para imóveis, contratos, documentos, governança, corretores, mandatos, comissões, repasses e OCR.",
    "version": "19.0.1.0.13",
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
        "document_dossier_governance",
        "enterprise_configuration_seed",
    ],
    # Os XML abaixo são carregados somente pelo wizard/backend, em uma
    # execução explícita. A instalação do módulo não deve criar massa demo.
    "data": [
        "security/ir.model.access.csv",
        "views/demo_generator_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "application": False,
    "installable": True,
}
