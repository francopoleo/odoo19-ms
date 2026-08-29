{
    "name": "Document Portal Integration",
    "version": "19.0.1.0.0",
    "category": "Documents",
    "summary": "Portal integration bridge for document_core module",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": ["portal", "document_core"],
    "data": [
        "views/document_ext_views.xml",
        "views/portal_templates.xml",
    ],
    "installable": True,
    "auto_install": False,
}
