# -*- coding: utf-8 -*-
{
    "name": "Central de Ajuda",
    "summary": "Central de ajuda contextual e biblioteca de documentação dos módulos Odoo",
    "description": """
Central de Ajuda
================

Módulo independente para importar documentação Markdown dos módulos instalados,
transformar em artigos navegáveis dentro do Odoo e oferecer base de conhecimento
para usuários, administradores e equipe técnica.
    """,
    "version": "19.0.1.20.0",
    "category": "Productivity",
    "author": "Franco Poleo / Manuela Silva",
    "website": "",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [
        "security/help_security.xml",
        "security/ir.model.access.csv",
        "data/help_category_data.xml",
        "data/help_default_content_data.xml",
        "data/help_maintenance_data.xml",
        "data/governance_help_articles.xml",
        "views/help_category_views.xml",
        "views/help_tag_views.xml",
        "views/help_article_views.xml",
        "views/help_context_views.xml",
        "views/help_context_candidate_views.xml",
        "views/help_doc_source_views.xml",
        "views/help_feedback_views.xml",
        "views/help_learning_views.xml",
        "views/help_tip_views.xml",
        "views/help_checklist_views.xml",
        "views/help_suggestion_views.xml",
        "views/help_metric_views.xml",
        "wizard/help_import_wizard_views.xml",
        "views/help_menu_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "common_help_center/static/src/components/help_systray/help_systray.js",
            "common_help_center/static/src/components/help_systray/help_systray.xml",
            "common_help_center/static/src/components/help_systray/help_systray.scss",
        ],
    },
    "application": True,
    "installable": True,
}
