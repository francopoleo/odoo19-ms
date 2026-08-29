# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class HelpCenterController(http.Controller):

    @http.route("/help_center/context", type="jsonrpc", auth="user")
    def context_help(self, model=None, view_type=None, menu_xmlid=None, action_xmlid=None, field_name=None, **kwargs):
        domain = [("active", "=", True), ("published", "=", True)]
        if model:
            domain = ["|", ("model_name", "=", model), ("model_name", "=", False)] + domain
        articles = request.env["help.article"].search(domain, limit=10)
        return [{"id": a.id, "name": a.name, "summary": a.summary or "", "type": a.article_type} for a in articles]
