{
    "name": "Property Website Integration",
    "version": "19.0.1.0.0",
    "category": "Real Estate/Properties",
    "summary": "Website integration bridge for Property Core module",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": ["website", "property_core"],
    "data": [
        "security/property_website_security.xml",
        "views/property_asset_ext_views.xml",
        "views/property_complex_ext_views.xml",
        "views/website_templates.xml",
    ],
    "installable": True,
    "auto_install": False,
}
