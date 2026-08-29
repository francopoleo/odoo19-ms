{
    "name": "Document Dossier - Aggregator",
    "version": "19.0.2.1.2",
    "category": "Document Management",
    "summary": "Aggregator and coordinator for document templates across business processes",
    "author": "Franco Poleo / Manuela Silva",
    "depends": ["document_core"],
    "license": "LGPL-3",
    "data": [
        # Security
        "security/groups.xml",
        "security/ir.model.access.csv",
        # Views
        "views/document_dossier_template_views.xml",
        "views/dossier_views.xml",
        "views/dossier_agenda_views.xml",
        "views/document_document_dossier_ext_views.xml",
        "views/document_move_to_dossier_wizard_views.xml",
        "views/document_apply_template_wizard_views.xml",
        "views/dossier_assign_wizard_views.xml",
        # Data
        "data/dossier_process_data.xml",
        # Menus (loaded last after all views/actions)
        "views/dossier_menu_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "external_dependencies": {},
}
