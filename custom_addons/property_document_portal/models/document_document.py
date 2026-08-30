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

        # A regra de portal restringe a leitura direta de property.asset ao
        # proprietário. Para decidir se um documento pode ser exibido, a
        # relação precisa ser inspecionada com sudo; isso não concede acesso
        # ao imóvel nem altera o conjunto final de documentos autorizados.
        asset = document.asset_id.sudo()
        if not asset:
            return False

        if asset.owner_id == partner:
            return True

        active_contracts = self.env["property.contract"].sudo().search(
            [
                ("asset_id", "=", asset.id),
                ("partner_id", "=", partner.id),
                ("status", "in", ("draft", "active", "expired", "renewing")),
            ]
        )
        if active_contracts:
            return True

        broker_assignments = self.env["property.broker.assignment"].sudo().search(
            [
                ("asset_id", "=", asset.id),
                # broker_id já aponta diretamente para res.partner; não existe
                # um campo partner_id intermediário nesse modelo.
                ("broker_id", "=", partner.id),
                ("status", "in", ("active", "converted")),
            ]
        )
        if broker_assignments:
            return True

        return False
