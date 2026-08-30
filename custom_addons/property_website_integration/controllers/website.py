from odoo import http, _
from odoo.http import request


class PropertyWebsite(http.Controller):

    def _get_current_broker(self):
        user = request.env.user
        if not user or user._is_public():
            return request.env["res.partner"]
        return request.env["res.partner"].sudo().search([("user_id", "=", user.id), ("category_id.name", "ilike", "Corretor")], limit=1)

    def _base_website_domain(self):
        return [("website_published", "=", True)]

    @http.route('/imoveis', auth='public', website=True, sitemap=True)
    def property_catalog(self, tipo=None, cidade=None, interesse=None, **kw):
        user = request.env.user
        broker = self._get_current_broker()
        domain = self._base_website_domain()
        if tipo:
            domain.append(("asset_type", "=", tipo))
        if cidade:
            domain.append(("city", "=", cidade))

        Asset = request.env["property.asset"].sudo()
        assets = Asset.search(domain, order="name").filtered(lambda a: a.can_user_view_on_website(user=user, broker=broker))
        all_assets = Asset.search(self._base_website_domain()).filtered(lambda a: a.can_user_view_on_website(user=user, broker=broker))
        cities = sorted(set(filter(None, all_assets.mapped("city"))))

        return request.render("property_website_integration.website_property_catalog", {
            "assets": assets,
            "cities": cities,
            "tipo": tipo,
            "cidade": cidade,
            "asset_types": [
                ("residential", "Residencial"),
                ("commercial", "Comercial"),
                ("land", "Terreno"),
                ("industrial", "Industrial"),
                ("mixed", "Uso Misto"),
            ],
        })

    @http.route('/imoveis/<int:asset_id>', auth='public', website=True, sitemap=True)
    def property_detail(self, asset_id, success=False, denied=False, **kw):
        user = request.env.user
        broker = self._get_current_broker()
        asset = request.env["property.asset"].sudo().browse(asset_id)
        if not asset.exists() or not asset.can_user_view_on_website(user=user, broker=broker):
            return request.redirect('/imoveis')

        can_submit_interest = asset.can_user_submit_interest(user=user, broker=broker)
        access_hint = False
        if not can_submit_interest:
            if asset.website_lead_policy == "disabled":
                access_hint = _("Este imóvel não está recebendo interesses pelo site no momento.")
            elif asset.website_lead_policy == "portal_only" and user._is_public():
                access_hint = _("Faça login para enviar seu interesse neste imóvel.")
            elif asset.website_lead_policy == "authorized_brokers_only":
                access_hint = _("O envio de interesse está restrito aos corretores autorizados.")

        # Fetch gallery media (only public and website_published)
        gallery = request.env["property.media"].sudo().search([
            ("asset_id", "=", asset.id),
            ("website_published", "=", True),
            ("visibility_level", "=", "public"),
            ("purpose", "=", "asset_gallery"),
            ("image_1920", "!=", False),  # Only images, not files
        ], order="is_cover DESC, sequence, id")

        cover_media = gallery.filtered(lambda m: m.is_cover)
        if not cover_media and gallery:
            cover_media = gallery[0:1]

        return request.render("property_website_integration.website_property_detail", {
            "asset": asset,
            "success": bool(kw.get("success")),
            "denied": bool(kw.get("denied")),
            "can_submit_interest": can_submit_interest,
            "access_hint": access_hint,
            "gallery": gallery,
            "cover_media": cover_media,
        })

    @http.route('/imoveis/<int:asset_id>/interesse', auth='public', website=True, methods=['POST'], csrf=True)
    def property_interest(self, asset_id, **kw):
        user = request.env.user
        broker = self._get_current_broker()
        asset = request.env["property.asset"].sudo().browse(asset_id)
        if not asset.exists() or not asset.can_user_submit_interest(user=user, broker=broker):
            return request.redirect('/imoveis/%d?denied=1' % asset_id if asset.exists() else '/imoveis')

        name = (kw.get("contact_name") or "").strip()
        email = (kw.get("contact_email") or "").strip()
        if name and email:
            source_channel = "website_public"
            access_profile = "Público"
            if user and not user._is_public():
                source_channel = "website_portal"
                access_profile = "Portal / Logado"
            if broker:
                source_channel = "website_broker"
                access_profile = "Corretor Autorizado"

            lead_broker = asset.exclusive_broker_id or broker or asset.authorized_broker_ids[:1]
            request.env["property.lead"].sudo().create({
                "name": name,
                "email": email,
                "phone": (kw.get("contact_phone") or "").strip(),
                "asset_id": asset_id,
                "interest_type": kw.get("interest_type", "rent"),
                "message": (kw.get("contact_message") or "").strip(),
                "broker_id": lead_broker.id if lead_broker else False,
                "source_channel": source_channel,
                "submitter_user_id": user.id if user and not user._is_public() else False,
                "access_profile": access_profile,
            })
            asset.message_post(body="Novo interesse recebido pelo site de %s (%s)." % (name, email))

        return request.redirect('/imoveis/%d?success=1' % asset_id)
