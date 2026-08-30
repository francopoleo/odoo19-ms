{
    "name": "Property Portal Integration",
    "version": "19.0.1.0.0",
    "category": "Real Estate/Properties",
    "summary": "Portal integration bridge for Property Core module",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": ["portal", "property_core"],
    "data": [
        "security/ir.model.access.csv",
        "security/property_portal_security.xml",
        "views/portal_templates.xml",
    ],
    "installable": True,
    "auto_install": False,
}
