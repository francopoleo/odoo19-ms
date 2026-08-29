from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class PropertyPortal(CustomerPortal):

    # ==================== Home portal counters ====================

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        if 'contract_count' in counters:
            values['contract_count'] = request.env['property.contract'].search_count([
                ('partner_id', '=', partner.id),
                ('status', 'not in', ['draft']),
            ])
        if 'rent_count' in counters:
            values['rent_count'] = request.env['property.rent'].search_count([
                ('partner_id', '=', partner.id),
                ('status', 'not in', ['draft', 'cancelled']),
            ])
        if 'owner_asset_count' in counters:
            owner = request.env['property.owner'].search([
                ('partner_id', '=', partner.id)
            ], limit=1)
            values['owner_asset_count'] = len(owner.asset_ids) if owner else 0
        return values

    # ==================== Contratos ====================

    @http.route(['/my/contracts', '/my/contracts/page/<int:page>'],
                auth='user', website=True)
    def portal_my_contracts(self, page=1, **kw):
        partner = request.env.user.partner_id
        Contract = request.env['property.contract']

        domain = [('partner_id', '=', partner.id), ('status', 'not in', ['draft'])]
        total = Contract.search_count(domain)
        pager = portal_pager(url='/my/contracts', total=total, page=page, step=10)
        contracts = Contract.search(
            domain, limit=10, offset=pager['offset'], order='start_date desc'
        )
        return request.render('property_portal_integration.portal_my_contracts', {
            'contracts': contracts,
            'pager': pager,
            'page_name': 'contracts',
        })

    @http.route('/my/contracts/<int:contract_id>', auth='user', website=True)
    def portal_contract_detail(self, contract_id, **kw):
        partner = request.env.user.partner_id
        contract = request.env['property.contract'].browse(contract_id)

        if not contract.exists() or contract.partner_id != partner:
            return request.redirect('/my')

        rents = contract.rent_ids.filtered(
            lambda r: r.status not in ('draft', 'cancelled')
        ).sorted('due_date')
        documents = request.env['document.document'].search([
            ('contract_id', '=', contract.id)
        ])

        # Get cover image for property (first published media or asset image)
        cover_media = False
        if contract.asset_id:
            cover_media = request.env["property.media"].search([
                ("asset_id", "=", contract.asset_id.id),
                ("is_cover", "=", True),
                ("website_published", "=", True),
                ("visibility_level", "in", ("portal", "public")),
                ("image_1920", "!=", False),
            ], limit=1)

        return request.render('property_portal_integration.portal_contract_detail', {
            'contract': contract,
            'rents': rents,
            'documents': documents,
            'cover_media': cover_media,
            'page_name': 'contracts',
        })

    # ==================== Parcelas ====================

    # ==================== Portal Proprietário ====================

    @http.route(['/my/properties', '/my/properties/page/<int:page>'],
                auth='user', website=True)
    def portal_my_properties(self, page=1, **kw):
        partner = request.env.user.partner_id
        owner = request.env['property.owner'].search(
            [('partner_id', '=', partner.id)], limit=1
        )
        if not owner:
            return request.redirect('/my')

        assets = owner.asset_ids
        return request.render('property_portal_integration.portal_my_properties', {
            'owner': owner,
            'assets': assets,
            'page_name': 'properties',
        })

    @http.route('/my/properties/<int:asset_id>', auth='user', website=True)
    def portal_property_detail(self, asset_id, **kw):
        partner = request.env.user.partner_id
        owner = request.env['property.owner'].search(
            [('partner_id', '=', partner.id)], limit=1
        )
        asset = request.env['property.asset'].browse(asset_id)
        if not owner or asset.owner_id != owner:
            return request.redirect('/my')

        active_contracts = asset.contract_ids.filtered(
            lambda c: c.status in ('active', 'expiring', 'renewing')
        )

        # Fetch gallery media for portal (only published to portal or public)
        gallery = request.env["property.media"].search([
            ("asset_id", "=", asset.id),
            ("website_published", "=", True),
            ("visibility_level", "in", ("portal", "public")),
            ("image_1920", "!=", False),
        ], order="is_cover DESC, sequence, id")

        # Group gallery by finality/category for portal presentation.
        gallery_by_role = {
            "Galeria": gallery.filtered(lambda m: m.purpose == "asset_gallery"),
        }
        gallery_by_role = {k: v for k, v in gallery_by_role.items() if v}

        return request.render('property_portal_integration.portal_property_detail', {
            'owner': owner,
            'asset': asset,
            'active_contracts': active_contracts,
            'gallery': gallery,
            'gallery_by_role': gallery_by_role,
            'page_name': 'properties',
        })

    @http.route(['/my/rents', '/my/rents/page/<int:page>'],
                auth='user', website=True)
    def portal_my_rents(self, page=1, **kw):
        partner = request.env.user.partner_id
        Rent = request.env['property.rent']

        domain = [
            ('partner_id', '=', partner.id),
            ('status', 'not in', ['draft', 'cancelled']),
        ]
        total = Rent.search_count(domain)
        pager = portal_pager(url='/my/rents', total=total, page=page, step=15)
        rents = Rent.search(domain, limit=15, offset=pager['offset'], order='due_date desc')
        return request.render('property_portal_integration.portal_my_rents', {
            'rents': rents,
            'pager': pager,
            'page_name': 'rents',
        })
