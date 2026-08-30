from odoo import api, fields, models


class DocumentDocumentPortalExt(models.Model):
    _inherit = "document.document"

    shared_partner_ids = fields.Many2many(
        "res.partner",
        "document_document_shared_partner_rel",
        "document_id",
        "partner_id",
        string="Shared with Partners",
        help="Partners with direct access to this document",
    )

    @api.model
    def _is_visible_to_partner(self, partner, document):
        """Check if document is visible to partner via portal."""
        if not document.website_published:
            return False

        if document.access_level not in ("portal", "public"):
            return False

        if document.access_level == "public":
            return True

        if partner in document.shared_partner_ids:
            return True

        # Módulos especializados podem acrescentar vínculos de negócio
        # (imóvel, contrato, condomínio etc.) sem duplicar esta política base.
        return self._extend_portal_visibility(partner, document, False)

    def _extend_portal_visibility(self, partner, document, is_visible):
        """Ponto de extensão para regras de visibilidade específicas."""
        return is_visible

    def get_portal_documents(self, partner=None):
        """Get documents visible to partner in portal."""
        from odoo import http
        if not partner:
            partner = http.request.env.user.partner_id

        domain = [
            ("website_published", "=", True),
            ("access_level", "in", ("portal", "public")),
        ]

        documents = self.search(domain)

        visible_docs = []
        for doc in documents:
            if self._is_visible_to_partner(partner, doc):
                visible_docs.append(doc)

        return visible_docs
