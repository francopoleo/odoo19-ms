{
    "name": "Document Core",
    "version": "19.0.1.16.0",
    "category": "Real Estate/Documents",
    "summary": "Gestão documental com pré-visualização, validação, ciclos de revisão e completude",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": ["mail", "common_base"],
    "data": [
        "security/document_security.xml",
        "security/ir.model.access.csv",
        "data/document_sequence_data.xml",
        "data/document_seed_data.xml",
        "data/document_core_data.xml",
        "views/document_views.xml",
        "views/document_type_views.xml",
        "views/property_document_type_views.xml",
        "views/document_dashboard_views.xml",
        "views/document_agenda_views.xml",
        "views/document_communication_views.xml",
        "views/document_reject_wizard_views.xml",
        "views/document_menu_views.xml",
        "views/document_agenda_menu_views.xml",
        "views/document_workflow_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "document_core/static/src/css/document.css"
        ]
    },
    "installable": True,
    "application": True,
}
