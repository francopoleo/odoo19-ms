# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HelpContextCandidate(models.Model):
    _name = "help.context.candidate"
    _description = "Mapa de Contextos de Ajuda"
    _order = "module_name, model_name, view_type, name"

    name = fields.Char(string="Contexto", compute="_compute_name", store=True)
    module_name = fields.Char(string="Módulo", index=True)
    model_name = fields.Char(string="Model", index=True)
    view_type = fields.Selection([
        ("form", "Formulário"),
        ("list", "Lista"),
        ("kanban", "Kanban"),
        ("calendar", "Calendário"),
        ("search", "Pesquisa"),
        ("pivot", "Tabela Dinâmica"),
        ("graph", "Gráfico"),
        ("activity", "Atividades"),
        ("gantt", "Gantt"),
        ("cohort", "Coorte"),
        ("map", "Mapa"),
        ("dashboard", "Dashboard"),
        ("other", "Outro"),
    ], string="Tipo de View", index=True)
    view_id = fields.Many2one("ir.ui.view", string="View Técnica", ondelete="set null")
    view_xmlid = fields.Char(string="XML ID da View", index=True)
    action_id = fields.Many2one("ir.actions.act_window", string="Ação", ondelete="set null")
    action_xmlid = fields.Char(string="XML ID da Ação", index=True)
    menu_id = fields.Many2one("ir.ui.menu", string="Menu", ondelete="set null")
    menu_xmlid = fields.Char(string="XML ID do Menu", index=True)
    context_id = fields.Many2one("help.context", string="Contexto de Ajuda", ondelete="set null")
    article_count = fields.Integer(string="Artigos", default=0, readonly=True)
    has_context = fields.Boolean(string="Tem contexto", default=False, readonly=True)
    status = fields.Selection([
        ("missing", "Sem contexto"),
        ("empty", "Contexto sem artigo"),
        ("documented", "Documentado"),
    ], string="Situação", default="missing", index=True, readonly=True)
    last_scan_date = fields.Datetime(string="Última varredura", readonly=True)
    note = fields.Text(string="Observações")
    active = fields.Boolean(string="Ativo", default=True)

    @api.depends("module_name", "model_name", "view_type", "view_xmlid", "action_xmlid", "menu_xmlid")
    def _compute_name(self):
        for rec in self:
            parts = []
            if rec.model_name:
                parts.append(rec.model_name)
            if rec.view_type:
                parts.append(rec.view_type)
            if rec.menu_xmlid:
                parts.append(rec.menu_xmlid)
            elif rec.action_xmlid:
                parts.append(rec.action_xmlid)
            elif rec.view_xmlid:
                parts.append(rec.view_xmlid)
            rec.name = " / ".join(parts) or "Contexto sem identificação"

    def action_refresh_coverage(self):
        for rec in self:
            rec._refresh_coverage_values()
        return True

    def _refresh_coverage_values(self):
        Article = self.env["help.article"].sudo()
        Context = self.env["help.context"].sudo()
        for rec in self:
            context = rec.context_id
            if not context and (rec.model_name or rec.view_type or rec.action_xmlid or rec.menu_xmlid):
                domain = [("active", "=", True)]
                if rec.model_name:
                    domain.append(("model_name", "=", rec.model_name))
                if rec.view_type:
                    domain.append(("view_type", "=", rec.view_type))
                if rec.action_xmlid:
                    domain.append(("action_xmlid", "=", rec.action_xmlid))
                if rec.menu_xmlid:
                    domain.append(("menu_xmlid", "=", rec.menu_xmlid))
                context = Context.search(domain, limit=1)
            count = 0
            if context:
                count += len(context.article_ids.filtered(lambda a: a.active and a.published and a.show_in_context))
            article_domain = [("active", "=", True), ("published", "=", True), ("show_in_context", "=", True)]
            if rec.model_name:
                article_domain.append(("model_name", "=", rec.model_name))
            if rec.view_type:
                article_domain.append(("view_type", "=", rec.view_type))
            count += Article.search_count(article_domain)
            vals = {
                "has_context": bool(context),
                "article_count": count,
                "status": "documented" if context and count else ("empty" if context else "missing"),
            }
            if context and not rec.context_id:
                vals["context_id"] = context.id
            rec.write(vals)

    def action_open_or_create_context(self):
        self.ensure_one()
        context = self.context_id
        if not context:
            domain = [("active", "=", True)]
            if self.model_name:
                domain.append(("model_name", "=", self.model_name))
            if self.view_type:
                domain.append(("view_type", "=", self.view_type))
            if self.action_xmlid:
                domain.append(("action_xmlid", "=", self.action_xmlid))
            if self.menu_xmlid:
                domain.append(("menu_xmlid", "=", self.menu_xmlid))
            context = self.env["help.context"].search(domain, limit=1)
        if not context:
            category = self.env["help.category"].search([("code", "=", "module.%s" % (self.module_name or ""))], limit=1)
            context = self.env["help.context"].create({
                "name": self.name,
                "module_name": self.module_name,
                "model_name": self.model_name,
                "view_type": self.view_type,
                "menu_xmlid": self.menu_xmlid,
                "action_xmlid": self.action_xmlid,
                "category_id": category.id if category else False,
                "description": "Contexto gerado automaticamente pelo Mapa de Contextos. Vincule artigos curtos ou crie um arquivo docs/08_AJUDA_CONTEXTUAL.md no módulo.",
            })
        self.context_id = context.id
        self.action_refresh_coverage()
        return {
            "type": "ir.actions.act_window",
            "name": "Contexto de Ajuda",
            "res_model": "help.context",
            "res_id": context.id,
            "view_mode": "form",
            "target": "current",
        }

    @api.model
    def _normalize_view_type(self, view_type):
        """Normaliza nomes técnicos do Odoo para os nomes usados na Central.

        Odoo 19 pode expor lista como ``list`` ou ``tree`` dependendo da origem
        do XML/action. Para cobertura de ajuda, ambos representam a mesma tela.
        """
        view_type = (view_type or "").strip()
        mapping = {
            "tree": "list",
            "list": "list",
            "form": "form",
            "kanban": "kanban",
            "calendar": "calendar",
            "search": "search",
            "pivot": "pivot",
            "graph": "graph",
            "activity": "activity",
            "gantt": "gantt",
            "cohort": "cohort",
            "map": "map",
            "dashboard": "dashboard",
        }
        return mapping.get(view_type, "other" if view_type else False)

    @api.model
    def _split_view_modes(self, view_mode):
        modes = []
        for raw in (view_mode or "").split(","):
            mode = self._normalize_view_type(raw)
            if mode and mode not in modes:
                modes.append(mode)
        return modes or [False]

    @api.model
    def _xmlid_for_record(self, record):
        if not record:
            return False
        return record.get_external_id().get(record.id)

    @api.model
    def _upsert_candidate(self, key_domain, vals):
        vals = dict(vals)
        vals["view_type"] = self._normalize_view_type(vals.get("view_type")) or vals.get("view_type")
        rec = self.search(key_domain, limit=1)
        if rec:
            rec.write(vals)
            return False
        self.create(vals)
        return True

    @api.model
    def action_generate_candidates(self, modules=None, only_modules_with_docs=True):
        """Gera mapa amplo de contexto para views, actions e menus.

        A versão anterior olhava principalmente XML IDs e apenas o primeiro
        ``view_mode`` de cada action. Isso fazia telas como Dossiê em lista,
        kanban ou formulário ficarem sem cobertura quando a action principal
        abria primeiro em kanban. Agora cada action/menu gera um candidato por
        modo de visualização e o tipo ``tree`` é normalizado para ``list``.
        """
        Source = self.env["help.doc.source"].sudo()
        IrData = self.env["ir.model.data"].sudo()
        View = self.env["ir.ui.view"].sudo()
        Action = self.env["ir.actions.act_window"].sudo()
        Menu = self.env["ir.ui.menu"].sudo()
        Module = self.env["ir.module.module"].sudo()
        modules_set = set(modules or [])
        if only_modules_with_docs:
            if not modules_set:
                Source.action_discover_installed_module_docs()
                modules_set = set(Source.search([]).mapped("module_name"))
        if not modules_set:
            modules_set = set(Module.search([("state", "=", "installed")]).mapped("name"))

        count = 0
        now = fields.Datetime.now()
        module_list = list(modules_set)

        # 1) Views com XML ID do módulo, incluindo form/list/kanban/search/calendar/pivot/graph/activity etc.
        view_data = IrData.search([("model", "=", "ir.ui.view"), ("module", "in", module_list)])
        for data in view_data:
            view = View.browse(data.res_id).exists()
            if not view or not view.model:
                continue
            normalized_type = self._normalize_view_type(view.type)
            if not normalized_type:
                continue
            xmlid = "%s.%s" % (data.module, data.name)
            vals = {
                "module_name": data.module,
                "model_name": view.model,
                "view_type": normalized_type,
                "view_id": view.id,
                "view_xmlid": xmlid,
                "last_scan_date": now,
                "note": "View técnica detectada automaticamente.",
            }
            if self._upsert_candidate([("view_xmlid", "=", xmlid)], vals):
                count += 1

        # 2) Actions: cria um candidato para cada modo de view declarado na action.
        action_data = IrData.search([("model", "=", "ir.actions.act_window"), ("module", "in", module_list)])
        for data in action_data:
            action = Action.browse(data.res_id).exists()
            if not action or not action.res_model:
                continue
            xmlid = "%s.%s" % (data.module, data.name)
            for mode in self._split_view_modes(action.view_mode):
                suffix = mode or "default"
                vals = {
                    "module_name": data.module,
                    "model_name": action.res_model,
                    "view_type": mode,
                    "action_id": action.id,
                    "action_xmlid": xmlid,
                    "last_scan_date": now,
                    "note": "Action detectada automaticamente para o modo de visualização %s." % (mode or "padrão"),
                }
                domain = [("action_xmlid", "=", xmlid), ("view_type", "=", mode or False), ("menu_xmlid", "=", False)]
                if self._upsert_candidate(domain, vals):
                    count += 1

        # 3) Menus com action de janela: candidato por modo de visualização do menu/action.
        menu_data = IrData.search([("model", "=", "ir.ui.menu"), ("module", "in", module_list)])
        for data in menu_data:
            menu = Menu.browse(data.res_id).exists()
            if not menu or not menu.action or menu.action._name != "ir.actions.act_window":
                continue
            action = menu.action
            xmlid = "%s.%s" % (data.module, data.name)
            action_xmlid = self._xmlid_for_record(action)
            for mode in self._split_view_modes(action.view_mode):
                vals = {
                    "module_name": data.module,
                    "model_name": action.res_model,
                    "view_type": mode,
                    "menu_id": menu.id,
                    "menu_xmlid": xmlid,
                    "action_id": action.id,
                    "action_xmlid": action_xmlid,
                    "last_scan_date": now,
                    "note": "Menu detectado automaticamente para o modo de visualização %s." % (mode or "padrão"),
                }
                domain = [("menu_xmlid", "=", xmlid), ("view_type", "=", mode or False)]
                if self._upsert_candidate(domain, vals):
                    count += 1

        # 4) Cobertura extra por model principal de cada módulo: quando há model mas não há action/menu direto,
        # gera candidatos básicos form/list/kanban para auditoria. Isso ajuda a perceber módulos que precisam docs.
        model_data = IrData.search([("model", "=", "ir.model"), ("module", "in", module_list)])
        for data in model_data:
            model_rec = self.env["ir.model"].sudo().browse(data.res_id).exists()
            if not model_rec or not model_rec.model:
                continue
            for mode in ("list", "form"):
                domain = [
                    ("module_name", "=", data.module),
                    ("model_name", "=", model_rec.model),
                    ("view_type", "=", mode),
                    ("view_xmlid", "=", False),
                    ("action_xmlid", "=", False),
                    ("menu_xmlid", "=", False),
                ]
                vals = {
                    "module_name": data.module,
                    "model_name": model_rec.model,
                    "view_type": mode,
                    "last_scan_date": now,
                    "note": "Candidato gerado por model técnico para auditoria de cobertura.",
                }
                if self._upsert_candidate(domain, vals):
                    count += 1

        self.search([]).action_refresh_coverage()
        return count

    @api.model
    def action_recompute_existing_coverage(self):
        self.search([]).action_refresh_coverage()
        return True
