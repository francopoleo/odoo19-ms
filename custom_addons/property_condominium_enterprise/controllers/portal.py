from odoo import http
from odoo import fields
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class CondominiumPortal(CustomerPortal):
    def _condo_context(self, rel):
        if not rel:
            return {"complex_name": False, "unit_name": False}
        complex_name = rel.complex_id.sudo().display_name if rel.complex_id else False
        unit_name = rel.asset_id.sudo().display_name if rel.asset_id else False
        return {"complex_name": complex_name, "unit_name": unit_name}

    def _get_partner_domain(self, partner):
        return [("partner_id", "=", partner.id)]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        domain = self._get_partner_domain(partner)
        if "condo_charge_count" in counters:
            values["condo_charge_count"] = request.env["property.condominium.charge"].search_count(domain)
        if "condo_ticket_count" in counters:
            values["condo_ticket_count"] = request.env["property.condominium.ticket"].search_count(domain)
        return values

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        rel = request.env["property.condominium.relationship"].sudo().search([
            ("partner_id", "=", partner.id),
            ("active", "=", True),
        ], limit=1)
        has_condo_access = bool(rel)
        values["show_condo_links"] = has_condo_access
        values["has_condo_access"] = has_condo_access
        values.update(self._condo_context(rel))
        return values

    @http.route(["/my/condominium", "/my/condominium/page/<int:page>"], auth="user", website=True)
    def portal_my_condominium(self, page=1, **kw):
        partner = request.env.user.partner_id
        domain = self._get_partner_domain(partner)
        rel = request.env["property.condominium.relationship"].sudo().search([
            ("partner_id", "=", partner.id),
            ("active", "=", True),
        ], limit=1)
        Charge = request.env["property.condominium.charge"]
        total = Charge.search_count(domain)
        pager = portal_pager(url="/my/condominium", total=total, page=page, step=10)
        charges = Charge.search(domain, limit=10, offset=pager["offset"], order="due_date desc")
        today = fields.Date.context_today(request.env.user)
        open_charges = Charge.search(domain + [("state", "in", ["open", "overdue"])])
        overdue_total = sum(c.amount_total or 0.0 for c in open_charges if c.due_date and c.due_date < today)
        open_total = sum(c.amount_total or 0.0 for c in open_charges)
        aging = {
            "current": {"label": "Vencendo", "count": 0, "amount": 0.0},
            "bucket_0_30": {"label": "0 a 30 dias", "count": 0, "amount": 0.0},
            "bucket_31_60": {"label": "31 a 60 dias", "count": 0, "amount": 0.0},
            "bucket_61_90": {"label": "61 a 90 dias", "count": 0, "amount": 0.0},
            "bucket_90_plus": {"label": "Acima de 90 dias", "count": 0, "amount": 0.0},
        }
        for charge in open_charges:
            overdue_days = max((today - charge.due_date).days, 0) if charge.due_date else 0
            if overdue_days <= 0:
                bucket = "current"
            elif overdue_days <= 30:
                bucket = "bucket_0_30"
            elif overdue_days <= 60:
                bucket = "bucket_31_60"
            elif overdue_days <= 90:
                bucket = "bucket_61_90"
            else:
                bucket = "bucket_90_plus"
            aging[bucket]["count"] += 1
            aging[bucket]["amount"] += charge.amount_total or 0.0
        return request.render("property_condominium_enterprise.portal_my_condominium", {
            "charges": charges,
            "pager": pager,
            "open_total": open_total,
            "overdue_total": overdue_total,
            "aging": aging,
            **self._condo_context(rel),
            "has_condo_access": bool(request.env["property.condominium.relationship"].search_count([
                ("partner_id", "=", partner.id),
                ("active", "=", True),
            ])),
        })

    @http.route(["/my/condominium/boletos"], auth="user", website=True)
    def portal_my_condominium_boletos(self, **kw):
        return request.redirect("/my/condominium")

    @http.route(["/my/condominium/charge/<int:charge_id>/boleto"], auth="user", website=True)
    def portal_my_condominium_charge_boleto(self, charge_id, **kw):
        partner = request.env.user.partner_id
        charge = request.env["property.condominium.charge"].sudo().browse(charge_id)
        if not charge.exists() or charge.partner_id.id != partner.id:
            raise AccessError("Você não tem permissão para acessar esta cobrança.")
        if not charge.invoice_id:
            return request.redirect("/my/condominium")
        return request.redirect(f"/web#id={charge.invoice_id.id}&model=account.move&view_type=form")

    @http.route(["/my/condominium/charge/<int:charge_id>/boleto/pdf"], auth="user", website=True)
    def portal_my_condominium_charge_boleto_pdf(self, charge_id, **kw):
        partner = request.env.user.partner_id
        charge = request.env["property.condominium.charge"].sudo().browse(charge_id)
        if not charge.exists() or charge.partner_id.id != partner.id:
            raise AccessError("Você não tem permissão para acessar esta cobrança.")
        invoice = charge.invoice_id.sudo() if charge.invoice_id else False
        if not invoice:
            return request.redirect("/my/condominium")
        return request.redirect(f"/account/download_invoice_documents/{invoice.id}/pdf?allow_fallback=1")

    @http.route(["/my/condominium/tickets", "/my/condominium/tickets/page/<int:page>"], auth="user", website=True)
    def portal_my_condominium_tickets(self, page=1, **kw):
        partner = request.env.user.partner_id
        domain = self._get_partner_domain(partner)
        Ticket = request.env["property.condominium.ticket"]
        rel = request.env["property.condominium.relationship"].sudo().search([
            ("partner_id", "=", partner.id),
            ("active", "=", True),
        ], limit=1)
        total = Ticket.search_count(domain)
        pager = portal_pager(url="/my/condominium/tickets", total=total, page=page, step=10)
        tickets = Ticket.search(domain, limit=10, offset=pager["offset"], order="create_date desc")
        return request.render("property_condominium_enterprise.portal_my_condominium_tickets", {
            "tickets": tickets,
            "pager": pager,
            **self._condo_context(rel),
            "has_condo_access": bool(request.env["property.condominium.relationship"].search_count([
                ("partner_id", "=", partner.id),
                ("active", "=", True),
            ])),
        })

    @http.route(["/my/condominium/tickets/new"], auth="user", website=True, methods=["GET", "POST"], csrf=False)
    def portal_my_condominium_ticket_new(self, **post):
        partner = request.env.user.partner_id
        Relationship = request.env["property.condominium.relationship"]
        rel = Relationship.search([("partner_id", "=", partner.id), ("active", "=", True)], limit=1)
        if request.httprequest.method == "POST":
            if not rel and not post.get("complex_id"):
                return request.render("property_condominium_enterprise.portal_my_condominium_ticket_new", {
                    "error": "Você precisa ter um vínculo ativo com um condomínio para abrir chamado.",
                    "has_condo_access": False,
                    "complex_id": False,
                })
            values = {
                "name": post.get("name") or "Novo chamado",
                "complex_id": int(post.get("complex_id") or (rel.complex_id.id if rel and rel.complex_id else 0)),
                "unit_id": int(post.get("unit_id") or 0) or False,
                "partner_id": partner.id,
                "category": post.get("category") or "service",
                "priority": post.get("priority") or "1",
                "description": post.get("description") or "",
            }
            ticket = request.env["property.condominium.ticket"].sudo().create(values)
            return request.redirect(f"/my/condominium/tickets?created={ticket.id}")
        return request.render("property_condominium_enterprise.portal_my_condominium_ticket_new", {
            "has_condo_access": bool(rel),
            "complex_id": rel.complex_id.id if rel and rel.complex_id else False,
            "unit_id": False,
            **self._condo_context(rel),
        })

    @http.route(["/my/condominium/meus-chamados"], auth="user", website=True)
    def portal_my_condominium_meus_chamados(self, **kw):
        return request.redirect("/my/condominium/tickets")
