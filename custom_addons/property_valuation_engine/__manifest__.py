# -*- coding: utf-8 -*-
{
    "name": "Property Valuation Engine",
    "summary": "Motor enterprise de estimativa de valor imobiliário integrado ao property_core",
    "description": """
Property Valuation Engine
=========================

Módulo complementar ao property_core para estimativa gerencial de valor de venda e locação.
Inclui referência de preço por m², imóveis comparáveis, fontes, fatores de ajuste,
histórico auditável de cálculo e aprovação gerencial.

Este módulo não substitui laudo técnico de avaliação. O objetivo é apoiar decisão,
precificação, negociação, gestão patrimonial e memória institucional.
    """,
    "version": "19.0.1.0.5",
    "category": "Real Estate",
    "author": "Franco Poleo / Manuela Silva",
    "website": "https://generative.com.br",
    "license": "LGPL-3",
    "depends": [
        "base",
        "property_core",
    ],
    "data": [
        "security/valuation_security.xml",
        "security/ir.model.access.csv",
        "security/valuation_record_rules.xml",
        "data/valuation_sequence_data.xml",
        "data/valuation_algorithm_data.xml",
        "data/valuation_factor_data.xml",
        "views/valuation_source_views.xml",
        "views/valuation_factor_views.xml",
        "views/price_m2_reference_views.xml",
        "views/market_comparable_views.xml",
        "views/valuation_algorithm_views.xml",
        "views/valuation_run_views.xml",
        "views/property_asset_valuation_views.xml",
        "views/valuation_menus.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
