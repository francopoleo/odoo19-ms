{
    "name": "Property Document Portal",
    "version": "19.0.1.0.0",
    "category": "Real Estate/Documents",
    "summary": "Portal integration for property documents via contracts and broker assignments",
    "description": """
        Extends document_portal_integration with property-specific visibility rules.

        Features:
        - Document visibility via active property contracts
        - Document visibility via broker assignments
        - Group documents by property in portal
        - Integration with property.contract and property.broker_assignment

        Requires:
        - document_portal_integration (provides portal base)
        - document_property_integration (provides document-property link)
    """,
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": [
        "property_core",
        "document_property_integration",
        "document_portal_integration",
    ],
    "data": [
        "security/property_document_portal_security.xml",
        "security/ir.model.access.csv",
        "models/document_document_views.xml",
        "views/portal_templates_property.xml",
    ],
    "installable": True,
    "auto_install": False,
}
