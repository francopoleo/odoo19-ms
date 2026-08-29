from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request
from odoo.exceptions import AccessError
import logging

_logger = logging.getLogger(__name__)


class DocumentPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        """Add documents count to portal home."""
        values = super()._prepare_home_portal_values(counters)

        if "document_count" in counters:
            document_count = self._get_portal_documents_count()
            values["document_count"] = document_count

        return values

    def _get_portal_documents_count(self):
        """Count documents visible to the current partner."""
        partner = request.env.user.partner_id
        documents = request.env["document.document"].get_portal_documents(partner)
        return len(documents)

    @http.route(
        ["/my/documents", "/my/documents/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_documents(self, page=1, sortby=None, **kw):
        """Display documents accessible to current user."""
        partner = request.env.user.partner_id
        domain = [
            ("website_published", "=", True),
            ("access_level", "in", ("portal", "public")),
        ]

        searchbar_sortings = {
            "date": {"label": "Mais Recente", "order": "publication_date desc"},
            "name": {"label": "Nome", "order": "name asc"},
        }

        if sortby not in searchbar_sortings:
            sortby = "date"

        order = searchbar_sortings[sortby]["order"]

        document_count = request.env["document.document"].search_count(domain)
        pager_values = pager(
            url="/my/documents",
            total=document_count,
            page=page,
            step=10,
            url_args={"sortby": sortby},
        )
        offset = pager_values["offset"]

        documents = request.env["document.document"].search(
            domain, order=order, limit=10, offset=offset
        )

        visible_docs = []
        for doc in documents:
            if request.env["document.document"]._is_visible_to_partner(partner, doc):
                visible_docs.append(doc)

        values = {
            "documents": visible_docs,
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
            "pager": pager_values,
            "default_url": "/my/documents",
        }

        return request.render("document_portal_integration.portal_my_documents", values)

    @http.route(
        "/my/documents/<int:document_id>",
        type="http",
        auth="user",
        website=True,
    )
    def portal_document_view(self, document_id, **kw):
        """View a single document."""
        partner = request.env.user.partner_id
        document = request.env["document.document"].browse(document_id)

        if not document.exists():
            return request.not_found()

        if not request.env["document.document"]._is_visible_to_partner(partner, document):
            raise AccessError("You don't have access to this document")

        values = {
            "document": document,
        }

        return request.render("document_portal_integration.portal_document_view", values)
