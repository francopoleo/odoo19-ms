# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager


class GovernancePortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        if 'governance_case_count' in counters:
            values['governance_case_count'] = request.env["governance.case"].sudo().search_count(
                [
                    ("|"),
                    ("responsible_id.partner_id", "=", partner.id),
                    ("participant_ids.partner_id", "=", partner.id),
                ]
            )
        return values

    @http.route(["/my/governance", "/my/governance/page/<int:page>"], auth="user", website=True)
    def portal_my_governance_cases(self, page=1, sortby=None, **kw):
        """Portal list of governance cases for user."""
        partner = request.env.user.partner_id
        Case = request.env["governance.case"].sudo()

        domain = [
            ("|"),
            ("responsible_id.partner_id", "=", partner.id),
            ("participant_ids.partner_id", "=", partner.id),
        ]

        searchbar_sortings = {
            "date": {"label": "Data (nova)", "order": "create_date desc"},
            "name": {"label": "Assunto", "order": "name"},
            "stage": {"label": "Etapa", "order": "stage_id"},
            "priority": {"label": "Prioridade", "order": "priority desc"},
        }

        if not sortby:
            sortby = "date"
        sort_order = searchbar_sortings[sortby]["order"]

        case_count = Case.search_count(domain)
        pager_obj = pager(
            url="/my/governance",
            url_args={"sortby": sortby},
            total=case_count,
            page=page,
            step=10,
        )
        cases = Case.search(domain, order=sort_order, limit=10, offset=pager_obj["offset"])

        return request.render(
            "governance_portal_integration.portal_my_governance_cases",
            {
                "cases": cases,
                "page_name": "my_governance_cases",
                "pager": pager_obj,
                "sortby": sortby,
                "searchbar_sortings": searchbar_sortings,
            },
        )

    @http.route("/my/governance/<int:case_id>", auth="user", website=True, sitemap=False)
    def portal_governance_case_detail(self, case_id, **kw):
        """Portal detail view of a governance case."""
        partner = request.env.user.partner_id
        case = request.env["governance.case"].sudo().browse(case_id)

        if not case.exists():
            return request.not_found()

        # Check access
        if not case._is_visible_to_partner(partner):
            return request.not_found()

        # Get related documents
        documents = case.document_ids if hasattr(case, "document_ids") else []

        # Get communications/messages
        communications = case.case_communication_ids if hasattr(case, "case_communication_ids") else []

        # Get pending items
        pending_items = case.pending_ids if hasattr(case, "pending_ids") else []

        return request.render(
            "governance_portal_integration.portal_governance_case_detail",
            {
                "case": case,
                "page_name": "governance_case",
                "documents": documents,
                "communications": communications,
                "pending_items": pending_items,
            },
        )
