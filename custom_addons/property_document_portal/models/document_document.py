from odoo import api, fields, models


class DocumentDocumentPropertyExt(models.Model):
    _inherit = "document.document"

    asset_id = fields.Many2one(
        "property.asset",
        string="Propriedade",
        ondelete="set null",
        index=True,
        help="Imóvel associado a este documento",
    )

    property_contract_id = fields.Many2one(
        "property.contract",
        string="Contrato de Propriedade",
        ondelete="set null",
        index=True,
        help="Contrato de propriedade associado a este documento",
    )

    @api.model
    def _extend_portal_visibility(self, partner, document, is_visible):
        """
        Extend base portal visibility with property-specific rules.

        Called by document_portal_integration to add property-specific visibility.
        Returns True if partner should have access via property contract/assignment.
        """
        if is_visible:
            return True

        if not document.website_published or document.access_level not in ("portal", "public"):
            return False

        if document.access_level == "public":
            return True

        if not document.asset_id:
            return False

        active_contracts = self.env["property.contract"].search(
            [
                ("asset_id", "=", document.asset_id.id),
                ("partner_id", "=", partner.id),
                ("status", "in", ("draft", "active", "expired", "renewing")),
            ]
        )
        if active_contracts:
            return True

        broker_assignments = self.env["property.broker_assignment"].search(
            [
                ("asset_id", "=", document.asset_id.id),
                ("broker_id.partner_id", "=", partner.id),
                ("status", "in", ("active", "pending")),
            ]
        )
        if broker_assignments:
            return True

        return False
