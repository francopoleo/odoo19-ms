# -*- coding: utf-8 -*-
import hashlib
import html
import re
import xml.etree.ElementTree as ET
from odoo import api, fields, models


class HelpArticle(models.Model):
    _name = "help.article"
    _description = "Artigo da Central de Ajuda"
    _order = "sequence, name"

    name = fields.Char(string="Título", required=True, translate=True)
    code = fields.Char(string="Código", required=True, index=True)
    category_id = fields.Many2one("help.category", string="Categoria", ondelete="restrict")
    tag_ids = fields.Many2many("help.tag", "help_article_tag_rel", "article_id", "tag_id", string="Tags")
    module_name = fields.Char(string="Módulo")
    model_name = fields.Char(string="Model relacionado")
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
    ], string="Tipo de View")
    menu_xmlid = fields.Char(string="XML ID do Menu")
    action_xmlid = fields.Char(string="XML ID da Ação")
    field_name = fields.Char(string="Campo relacionado")
    article_type = fields.Selection([
        ("index", "Índice"),
        ("technical", "Documentação Técnica"),
        ("user_manual", "Manual do Usuário"),
        ("configuration", "Configuração Inicial"),
        ("testing", "Guia de Testes"),
        ("implementation", "Implementação"),
        ("troubleshooting", "Troubleshooting"),
        ("changelog", "Changelog"),
        ("faq", "FAQ"),
        ("flow", "Fluxo"),
        ("field_help", "Ajuda de Campo"),
    ], string="Tipo", default="user_manual", required=True, index=True)
    content_scope = fields.Selection([
        ("full_document", "Documento completo"),
        ("context", "Ajuda contextual"),
        ("flow", "Fluxo prático"),
        ("field", "Ajuda de campo"),
        ("troubleshooting", "Erro comum"),
        ("onboarding", "Treinamento"),
    ], string="Escopo", default="context", required=True, index=True)
    show_in_context = fields.Boolean(
        string="Exibir no painel contextual",
        default=True,
        help="Desmarque para documentos completos importados, como manuais integrais. Eles continuam na biblioteca, mas não poluem o drawer contextual.",
        index=True,
    )
    audience = fields.Selection([
        ("all", "Todos"),
        ("user", "Usuário"),
        ("admin", "Administrador"),
        ("technical", "Técnico"),
    ], string="Público", default="all", required=True, index=True)
    markdown_source = fields.Text(string="Markdown")
    content_html = fields.Html(string="Conteúdo", sanitize=False)
    summary = fields.Text(string="Resumo", translate=True)
    source_id = fields.Many2one("help.doc.source", string="Fonte Markdown", ondelete="set null")
    checksum = fields.Char(string="Checksum")
    edited_in_odoo = fields.Boolean(string="Editado no Odoo", default=False, copy=False)
    published = fields.Boolean(string="Publicado", default=True)
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativo", default=True)
    related_article_ids = fields.Many2many(
        "help.article", "help_article_related_rel", "article_id", "related_id", string="Artigos relacionados"
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = self.browse()
        for vals in vals_list:
            if vals.get("markdown_source") and not vals.get("content_html"):
                vals["content_html"] = self._markdown_to_html(vals["markdown_source"])
            if vals.get("markdown_source") and not vals.get("checksum"):
                vals["checksum"] = self._checksum(vals["markdown_source"])
            code = vals.get("code")
            if code:
                existing = self.search([("code", "=", code)], limit=1)
                if existing:
                    existing.with_context(help_import=self.env.context.get("help_import")).write(vals)
                    records |= existing
                    continue
            records |= super(HelpArticle, self).create([vals])
        return records

    def write(self, vals):
        if "markdown_source" in vals and "content_html" not in vals:
            vals["content_html"] = self._markdown_to_html(vals.get("markdown_source") or "")
            vals["checksum"] = self._checksum(vals.get("markdown_source") or "")
        # Se a edição vem da tela e não de importação, marca como editado no Odoo.
        if not self.env.context.get("help_import") and any(k in vals for k in ("markdown_source", "content_html", "name", "summary")):
            vals.setdefault("edited_in_odoo", True)
        return super().write(vals)

    def action_render_markdown(self):
        for rec in self:
            rec.content_html = self._markdown_to_html(rec.markdown_source or "")
            rec.checksum = self._checksum(rec.markdown_source or "")
        return True

    def action_open(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.name,
            "res_model": "help.article",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }

    @staticmethod
    def _checksum(text):
        return hashlib.sha256((text or "").encode("utf-8")).hexdigest()

    @api.model
    def _markdown_to_html(self, markdown_text):
        """Conversor Markdown para a Central de Ajuda.

        Suporta títulos, listas, blocos de código, blockquotes, links simples,
        negrito/itálico e tabelas Markdown no padrão GitHub:

        | Coluna A | Coluna B |
        | --- | --- |
        | Valor A | Valor B |
        """
        text = markdown_text or ""
        lines = text.splitlines()
        out = []
        in_ul = False
        in_ol = False
        in_code = False
        code_lines = []
        table_rows = []

        def close_lists():
            nonlocal in_ul, in_ol
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if in_ol:
                out.append("</ol>")
                in_ol = False

        def inline_format(value):
            value = html.escape(value or "")
            value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
            value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
            value = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", value)
            value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', value)
            return value

        def is_table_sep(row):
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            return bool(cells) and all(re.match(r"^:?-{3,}:?$", c or "") for c in cells)

        def split_table_row(row):
            return [c.strip() for c in row.strip().strip("|").split("|")]

        def flush_table():
            nonlocal table_rows
            if not table_rows:
                return
            rows = table_rows
            table_rows = []
            if len(rows) < 2 or not is_table_sep(rows[1]):
                for r in rows:
                    out.append("<p>%s</p>" % inline_format(r.strip()))
                return
            headers = split_table_row(rows[0])
            body_rows = [split_table_row(r) for r in rows[2:] if r.strip()]
            out.append('<div class="table-responsive o_help_md_table_wrapper"><table class="table table-sm table-striped table-bordered o_help_md_table">')
            out.append("<thead><tr>%s</tr></thead>" % "".join("<th>%s</th>" % inline_format(h) for h in headers))
            out.append("<tbody>")
            for body in body_rows:
                if len(body) < len(headers):
                    body += [""] * (len(headers) - len(body))
                out.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline_format(c) for c in body[:len(headers)]))
            out.append("</tbody></table></div>")

        for raw in lines:
            line = raw.rstrip()
            stripped = line.strip()
            if stripped.startswith("```"):
                flush_table()
                if in_code:
                    out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(code_lines)))
                    code_lines = []
                    in_code = False
                else:
                    close_lists()
                    in_code = True
                    code_lines = []
                continue
            if in_code:
                code_lines.append(line)
                continue
            if stripped.startswith("|") and stripped.endswith("|") and "|" in stripped[1:-1]:
                close_lists()
                table_rows.append(stripped)
                continue
            else:
                flush_table()
            if not stripped:
                close_lists()
                continue
            if stripped.startswith("#"):
                close_lists()
                level = len(stripped) - len(stripped.lstrip("#"))
                level = max(1, min(level, 6))
                title = stripped[level:].strip()
                out.append(f"<h{level}>{inline_format(title)}</h{level}>")
                continue
            if stripped.startswith(">"):
                close_lists()
                out.append('<blockquote class="blockquote border-start ps-3 text-muted">%s</blockquote>' % inline_format(stripped[1:].strip()))
                continue
            if stripped.startswith(("- ", "* ")):
                if not in_ul:
                    close_lists()
                    out.append("<ul>")
                    in_ul = True
                out.append("<li>%s</li>" % inline_format(stripped[2:].strip()))
                continue
            match = re.match(r"^\d+\.\s+(.*)$", stripped)
            if match:
                if not in_ol:
                    close_lists()
                    out.append("<ol>")
                    in_ol = True
                out.append("<li>%s</li>" % inline_format(match.group(1).strip()))
                continue
            close_lists()
            out.append("<p>%s</p>" % inline_format(stripped))
        if in_code:
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(code_lines)))
        flush_table()
        close_lists()
        return "\n".join(out)

    @api.model
    def _allowed_audiences(self):
        user = self.env.user
        if user.has_group("base.group_system") or user.has_group("common_help_center.group_help_technical"):
            return ["all", "user", "admin", "technical"]
        if user.has_group("common_help_center.group_help_admin"):
            return ["all", "user", "admin"]
        return ["all", "user"]

    @api.model
    def _primary_module_for_model(self, model_name):
        """Retorna o módulo dono principal do model para evitar que integrações
        poluam o drawer contextual principal.

        Exemplo: vários módulos podem documentar `document.document`, mas o
        contexto principal do formulário/lista deve priorizar `document_core`.
        Documentos de integração continuam disponíveis na biblioteca e podem ser
        vinculados manualmente a contextos específicos por menu/action.
        """
        model_name = model_name or ""
        explicit = {
            "document.document": "document_core",
            "document.category": "document_core",
            "document.type": "document_core",
            "document.location": "document_core",
            "document.communication": "document_core",
            "property.asset": "property_core",
            "property.media": "property_core",
            "property.inspection": "property_core",
            "property.maintenance": "property_core",
            "governance.case": "governance",
            "governance.case.pending": "governance",
            "governance.case.communication": "governance",
            "common.agenda.event": "common_base",
            "help.article": "common_help_center",
            "help.context": "common_help_center",
        }
        if model_name in explicit:
            return explicit[model_name]
        if model_name.startswith("property.payment"):
            return "property_payment_proof"
        if model_name.startswith("property.contract.amendment"):
            return "property_contract_amendment_enterprise"
        if model_name.startswith("property."):
            return "property_core"
        if model_name.startswith("document."):
            return "document_core"
        if model_name.startswith("dossier."):
            return "document_dossier"
        if model_name.startswith("governance."):
            return "governance"
        if model_name.startswith("help."):
            return "common_help_center"
        return False

    @api.model
    def _is_contextual_article(self, article, model_name=False, view_type=False, primary_module=False, strict_primary=False):
        """Filtra o que pode aparecer no drawer.

        A biblioteca pode ter manuais completos, docs técnicos e integrações.
        O drawer deve mostrar apenas micro-artigos contextuais/fluxos da tela.
        """
        if not article or not article.active or not article.published:
            return False
        if article.audience not in self._allowed_audiences():
            return False
        if not article.show_in_context:
            return False
        if article.content_scope == "full_document":
            return False
        if article.article_type in ("index", "technical", "configuration", "testing", "implementation", "changelog"):
            return False
        if strict_primary and primary_module and article.module_name and article.module_name != primary_module:
            return False
        if model_name and article.model_name and article.model_name != model_name:
            return False
        if view_type and article.view_type and article.view_type != view_type:
            return False
        return True

    @api.model
    def action_normalize_contextual_display(self):
        """Saneia conteúdos que não devem poluir o drawer contextual.

        Pode ser chamada sempre no update. Não apaga nada, apenas tira do painel
        contextual artigos que são documentos completos ou genéricos globais.
        """
        articles = self.sudo().search([])
        for article in articles:
            vals = {}
            if article.content_scope == "full_document":
                vals["show_in_context"] = False
            if article.article_type in ("index", "technical", "configuration", "testing", "implementation", "changelog"):
                vals["show_in_context"] = False
            if not any([article.model_name, article.field_name, article.menu_xmlid, article.action_xmlid]) and article.module_name:
                # Artigos globais de biblioteca não entram automaticamente no drawer.
                vals["show_in_context"] = False
            if vals:
                article.with_context(help_import=True).write(vals)
        return True

    @api.model
    def action_reset_documentation_repository(self):
        """Zera a documentação importada/configurada da Central.

        Uso em homologação/desenvolvimento: limpa artigos, contextos, fontes e
        mapa de cobertura para uma importação limpa dos docs versionados.
        Mantém categorias base, grupos, menus e configurações do módulo.
        """
        sudo = self.sudo()
        for model in (
            "help.feedback",
            "help.metric",
            "help.checklist.progress",
            "help.context.candidate",
            "help.context",
            "help.doc.source",
            "help.article",
        ):
            if model in sudo.env:
                sudo.env[model].search([]).unlink()
        return True

    @api.model
    def _base_article_domain(self):
        return [
            ("active", "=", True),
            ("published", "=", True),
            ("audience", "in", self._allowed_audiences()),
        ]

    @api.model
    def _record_state_value(self, model_name=None, record_id=None):
        if not model_name or not record_id or model_name not in self.env:
            return False
        record = self.env[model_name].browse(int(record_id)).exists()
        if not record:
            return False
        for field_name in ("state", "status", "stage", "stage_id", "workflow_state"):
            if field_name in record._fields:
                try:
                    value = record[field_name]
                    if hasattr(value, "display_name"):
                        return value.display_name
                    return value or False
                except Exception:
                    return False
        return False

    @api.model
    def _serialize_article(self, article):
        return {
            "id": article.id,
            "name": article.name,
            "summary": article.summary or "",
            "type": article.article_type,
            "type_label": dict(article._fields["article_type"].selection).get(article.article_type, article.article_type),
            "scope": article.content_scope,
            "audience": article.audience,
            "module": article.module_name or "",
            "model": article.model_name or "",
            "category": article.category_id.name if article.category_id else "",
        }

    @api.model
    def get_context_bundle(self, context_info=None, query=None):
        """Retorna artigos, dicas, checklists e sugestões para o painel lateral.

        `context_info` vem do frontend e pode conter:
        - resModel
        - viewType
        - resId
        - menuXmlid
        - actionXmlid
        """
        context_info = dict(context_info or {})
        model_name = context_info.get("resModel") or context_info.get("model") or False
        view_type = context_info.get("viewType") or False
        record_id = int(context_info.get("resId") or 0)
        menu_xmlid = context_info.get("menuXmlid") or False
        action_xmlid = context_info.get("actionXmlid") or False
        action_id = context_info.get("actionId") or False
        # Se o frontend conseguir enviar apenas o ID da ação, resolve res_model/view quando possível.
        if not model_name and action_id:
            try:
                action_rec = self.env["ir.actions.act_window"].sudo().browse(int(action_id)).exists()
                if action_rec:
                    model_name = action_rec.res_model or model_name
                    if not view_type:
                        view_type = (action_rec.view_mode or "list").split(",")[0]
            except Exception:
                pass
        query = (query or "").strip()

        self.env["help.metric"].sudo().log_event({
            "event_type": "drawer_open" if not query else "search",
            "model_name": model_name or False,
            "view_type": view_type or False,
            "menu_xmlid": menu_xmlid or False,
            "action_xmlid": action_xmlid or False,
            "record_id": record_id,
            "query": query or False,
        })

        primary_module = self._primary_module_for_model(model_name)

        # Drawer enterprise: primeiro tentamos artigos vinculados ao contexto exato
        # e ao módulo dono principal do model. Isso evita misturar manual completo,
        # integrações e documentos genéricos no painel de uma tela operacional.
        scored_article_ids = {}

        def add_article(article, score, strict_primary=False):
            if not self._is_contextual_article(
                article,
                model_name=model_name,
                view_type=view_type,
                primary_module=primary_module,
                strict_primary=strict_primary,
            ):
                return
            current = scored_article_ids.get(article.id, -1)
            if score > current:
                scored_article_ids[article.id] = score

        def add_context_articles(contexts, score, strict_primary=True):
            for ctx in contexts:
                if strict_primary and primary_module and ctx.module_name and ctx.module_name != primary_module:
                    continue
                for article in ctx.article_ids.sorted(key=lambda a: (a.sequence or 0, a.name or "")):
                    add_article(article, score, strict_primary=strict_primary)

        Context = self.env["help.context"]

        # 1) Contexto por action/menu: é o mais específico quando disponível.
        if action_xmlid:
            add_context_articles(Context.search([
                ("active", "=", True),
                ("action_xmlid", "=", action_xmlid),
            ], order="priority, id", limit=4), 1200, strict_primary=False)
        if menu_xmlid:
            add_context_articles(Context.search([
                ("active", "=", True),
                ("menu_xmlid", "=", menu_xmlid),
            ], order="priority, id", limit=4), 1150, strict_primary=False)

        # 2) Contexto exato: model + view do módulo principal.
        if model_name and view_type:
            add_context_articles(Context.search([
                ("active", "=", True),
                ("model_name", "=", model_name),
                ("view_type", "=", view_type),
            ], order="priority, id", limit=8), 1000, strict_primary=True)

        # 3) Contexto do model sem view específica.
        if model_name:
            add_context_articles(Context.search([
                ("active", "=", True),
                ("model_name", "=", model_name),
                ("view_type", "=", False),
            ], order="priority, id", limit=6), 700, strict_primary=True)

        # 4) Fallback por artigos diretos somente quando não existe contexto útil
        # ou quando o usuário pesquisou explicitamente.
        if query or not scored_article_ids:
            article_domain = self._base_article_domain() + [("show_in_context", "=", True), ("content_scope", "!=", "full_document")]
            if model_name:
                article_domain.append(("model_name", "=", model_name))
            if view_type and not query:
                article_domain += ["|", ("view_type", "=", view_type), ("view_type", "=", False)]
            if primary_module and not query:
                article_domain += ["|", ("module_name", "=", primary_module), ("module_name", "=", False)]
            if query:
                article_domain += ["|", "|", ("name", "ilike", query), ("summary", "ilike", query), ("markdown_source", "ilike", query)]
            for article in self.search(article_domain, limit=20):
                score = 300 if query else 150
                if article.model_name == model_name:
                    score += 80
                if article.view_type == view_type:
                    score += 60
                if primary_module and article.module_name == primary_module:
                    score += 30
                add_article(article, score, strict_primary=not bool(query))

        article_records = self.browse(list(scored_article_ids.keys())).filtered(
            lambda a: self._is_contextual_article(
                a,
                model_name=model_name,
                view_type=view_type,
                primary_module=primary_module,
                strict_primary=False,
            )
        )
        articles = sorted(
            article_records,
            key=lambda a: (
                -scored_article_ids.get(a.id, 0),
                a.sequence or 0,
                (a.name or "").lower(),
                a.id,
            ),
        )[:6]

        tips_domain = [("active", "=", True), ("audience", "in", self._allowed_audiences())]
        if model_name:
            tips_domain.append(("model_name", "=", model_name))
        if view_type:
            tips_domain += ["|", ("view_type", "=", view_type), ("view_type", "=", False)]
        tips = self.env["help.tip"].search(tips_domain, limit=4)

        checklists_domain = [("active", "=", True), ("audience", "in", self._allowed_audiences())]
        if model_name:
            checklists_domain.append(("model_name", "=", model_name))
        if view_type:
            checklists_domain += ["|", ("view_type", "=", view_type), ("view_type", "=", False)]
        templates = self.env["help.checklist.template"].search(checklists_domain, limit=2)
        progress_map = {}
        if templates:
            progress = self.env["help.checklist.progress"].search([
                ("user_id", "=", self.env.user.id),
                ("template_id", "in", templates.ids),
                ("model_name", "=", model_name or False),
                ("record_id", "=", record_id),
            ])
            progress_map = {p.item_id.id: p.done for p in progress}

        state_value = self._record_state_value(model_name, record_id)
        suggestion_domain = [("active", "=", True)]
        if model_name:
            suggestion_domain.append(("model_name", "=", model_name))
        suggestions = []
        for rule in self.env["help.suggestion.rule"].search(suggestion_domain, limit=5):
            if rule.rule_type == "state_flow" and rule.state_value:
                if not state_value or str(rule.state_value).lower() not in str(state_value).lower():
                    continue
            suggestions.append({
                "id": rule.id,
                "name": rule.name,
                "type": rule.rule_type,
                "tip": rule.tip_text or "",
                "articles": [self._serialize_article(a) for a in rule.article_ids.filtered(lambda a: a.published and a.active)[:5]],
            })

        dynamic_reference = self._dynamic_reference_for_context(
            model_name=model_name,
            view_type=view_type,
            record_id=record_id,
            menu_xmlid=menu_xmlid,
            action_xmlid=action_xmlid,
        )

        return {
            "context": {
                "model": model_name or "",
                "viewType": view_type or "",
                "recordId": record_id,
                "state": state_value or "",
                "primaryModule": primary_module or "",
            },
            "articles": [self._serialize_article(a) for a in articles],
            "dynamic_reference": dynamic_reference,
            "tips": [{"id": t.id, "name": t.name, "content": t.content, "article_id": t.article_id.id or False} for t in tips],
            "checklists": [{
                "id": tpl.id,
                "name": tpl.name,
                "description": tpl.description or "",
                "items": [{
                    "id": item.id,
                    "name": item.name,
                    "description": item.description or "",
                    "required": item.required,
                    "done": bool(progress_map.get(item.id)),
                    "article_id": item.article_id.id or False,
                } for item in tpl.item_ids.filtered(lambda i: i.active)],
            } for tpl in templates],
            "suggestions": suggestions,
        }


    @api.model
    def _is_help_relevant_selection_field(self, field_name, field_meta):
        name = (field_name or "").lower()
        label = (field_meta.get("string") or "").lower()
        keywords = (
            "state", "status", "situação", "situacao", "priority", "prioridade",
            "type", "tipo", "kind", "categoria", "category", "access", "acesso",
            "visibility", "visibilidade", "purpose", "finalidade", "review", "revisão", "revisao",
            "document", "agenda", "workflow", "stage", "etapa",
        )
        blocked = ("activity_exception", "preview_kind")
        if any(b in name for b in blocked):
            return False
        return any(k in name or k in label for k in keywords)

    @api.model
    def _is_help_relevant_relational_field(self, field_name, field_meta):
        """Decide quais campos relacionais merecem lista de opções no drawer.

        O objetivo é mostrar opções úteis ao preencher formulários, sem despejar
        listas enormes e pouco relevantes. Campos de categoria, tipo, etapa,
        status, responsável, equipe, empresa, contato, imóvel, documento e tags
        costumam ser determinantes para o fluxo operacional.
        """
        name = (field_name or "").lower()
        label = (field_meta.get("string") or "").lower()
        relation = (field_meta.get("relation") or "").lower()
        keywords = (
            "category", "categoria", "type", "tipo", "stage", "etapa",
            "status", "state", "tag", "respons", "owner", "team", "grupo",
            "company", "empresa", "partner", "contato", "property", "imovel",
            "asset", "document", "dossier", "location", "local", "user",
        )
        return any(k in name or k in label or k in relation for k in keywords)

    @api.model
    def _format_field_type(self, field_meta):
        field_type = field_meta.get("type") or ""
        relation = field_meta.get("relation") or ""
        if relation:
            return "%s → %s" % (field_type, relation)
        return field_type

    @api.model
    def _selection_options_for_field(self, model_name, field_name, field_meta):
        selection = field_meta.get("selection") or []
        # Em Odoo, selection pode vir como lista de pares ou método; fields_get
        # normalmente resolve para lista, mas mantemos proteção.
        options = []
        if isinstance(selection, (list, tuple)):
            for item in selection:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    options.append({"value": str(item[0]), "label": str(item[1])})
        return options

    @api.model
    def _relational_options_for_field(self, field_name, field_meta, limit=12):
        relation = field_meta.get("relation")
        if not relation or relation not in self.env:
            return []
        try:
            RelModel = self.env[relation]
            domain = []
            if "active" in RelModel._fields:
                domain.append(("active", "=", True))
            records = RelModel.search(domain, limit=limit, order="display_name")
            return [{"id": rec.id, "name": rec.display_name} for rec in records]
        except Exception:
            return []

    @api.model
    def _extract_search_filters_for_model(self, model_name, limit=80):
        """Lê filtros de search views do model.

        Não usa avaliação de domínio/contexto; apenas apresenta ao usuário o nome
        do filtro, seu objetivo e quando ele agrupa resultados.
        """
        if not model_name:
            return []
        filters = []
        views = self.env["ir.ui.view"].sudo().search([
            ("model", "=", model_name),
            ("type", "=", "search"),
            ("active", "=", True),
        ], order="priority, id", limit=20)
        seen = set()
        for view in views:
            arch = view.arch_db or ""
            if not arch.strip():
                continue
            try:
                root = ET.fromstring(arch.encode("utf-8"))
            except Exception:
                continue
            for node in root.iter():
                if node.tag != "filter":
                    continue
                label = node.attrib.get("string") or node.attrib.get("name") or "Filtro"
                name = node.attrib.get("name") or label
                context = node.attrib.get("context") or ""
                domain = node.attrib.get("domain") or ""
                key = (name, label, context, domain)
                if key in seen:
                    continue
                seen.add(key)
                is_group = "group_by" in context
                filters.append({
                    "name": name,
                    "label": label,
                    "kind": "group" if is_group else "filter",
                    "kind_label": "Agrupamento" if is_group else "Filtro",
                    "domain": domain,
                    "context": context,
                    "view": view.name or "",
                })
                if len(filters) >= limit:
                    return filters
        return filters

    @api.model
    def _dynamic_reference_for_context(self, model_name=None, view_type=None, record_id=0, menu_xmlid=False, action_xmlid=False):
        """Gera referência dinâmica para o drawer.

        A documentação versionada explica o fluxo. Esta referência mostra as
        opções reais do ambiente atual: seleções, categorias/tipos/etapas,
        campos obrigatórios e filtros cadastrados nas search views.
        """
        empty = {
            "available": False,
            "model": model_name or "",
            "model_label": "",
            "view_type": view_type or "",
            "required_fields": [],
            "selection_fields": [],
            "relational_options": [],
            "search_filters": [],
            "notes": [],
            "debug": [],
        }
        if not model_name:
            empty["notes"].append("Nenhum model foi detectado para a tela atual.")
            empty["debug"].append("Contexto sem model; o frontend não enviou resModel.")
            return empty
        if model_name not in self.env:
            empty["model"] = model_name
            empty["notes"].append("O model detectado não existe no registry atual do Odoo.")
            empty["debug"].append("Model não encontrado no env: %s" % model_name)
            return empty
        try:
            Model = self.env[model_name]
            fields_meta = Model.fields_get()
        except Exception as exc:
            empty["model"] = model_name
            empty["notes"].append("Não foi possível ler os campos deste model para montar a referência dinâmica.")
            empty["debug"].append("fields_get falhou: %s" % exc)
            return empty

        model_record = self.env["ir.model"].sudo().search([("model", "=", model_name)], limit=1)
        model_label = model_record.name or model_name
        required_fields = []
        selection_fields = []
        relational_options = []

        technical_names = {
            "id", "display_name", "create_uid", "create_date", "write_uid", "write_date", "__last_update",
            "message_ids", "message_follower_ids", "message_partner_ids", "activity_ids",
            "activity_state", "activity_type_id", "activity_user_id", "activity_date_deadline",
            "activity_exception_decoration", "activity_exception_icon", "activity_summary",
            "message_needaction", "message_needaction_counter", "message_has_error", "message_has_error_counter",
            "website_message_ids", "access_token", "access_url", "access_warning",
        }
        technical_prefixes = ("message_", "activity_", "website_", "access_")

        for field_name, meta in sorted(fields_meta.items(), key=lambda item: (item[1].get("string") or item[0]).lower()):
            if field_name in technical_names or field_name.startswith(technical_prefixes):
                continue
            if meta.get("readonly") and not meta.get("required"):
                continue
            ftype = meta.get("type")
            if meta.get("required") and ftype not in ("one2many", "binary"):
                required_fields.append({
                    "name": field_name,
                    "label": meta.get("string") or field_name,
                    "type": self._format_field_type(meta),
                    "help": meta.get("help") or "",
                })
            if ftype == "selection" and self._is_help_relevant_selection_field(field_name, meta):
                options = self._selection_options_for_field(model_name, field_name, meta)
                if options:
                    selection_fields.append({
                        "name": field_name,
                        "label": meta.get("string") or field_name,
                        "required": bool(meta.get("required")),
                        "help": meta.get("help") or "",
                        "options": options,
                    })
            if ftype in ("many2one", "many2many") and self._is_help_relevant_relational_field(field_name, meta):
                options = self._relational_options_for_field(field_name, meta, limit=12)
                relational_options.append({
                    "name": field_name,
                    "label": meta.get("string") or field_name,
                    "type": self._format_field_type(meta),
                    "required": bool(meta.get("required")),
                    "help": meta.get("help") or "",
                    "options": options,
                    "truncated": len(options) >= 12,
                })

        filters = self._extract_search_filters_for_model(model_name)
        notes = []
        if relational_options:
            notes.append("As opções relacionais são lidas em tempo real dos cadastros ativos do sistema; podem variar conforme permissões, empresa e configurações.")
        if filters:
            notes.append("Os filtros e agrupamentos são lidos das search views do Odoo e refletem o que existe tecnicamente na tela.")
        debug = [
            "Campos lidos: %s" % len(fields_meta),
            "Obrigatórios: %s" % len(required_fields),
            "Seleções: %s" % len(selection_fields),
            "Relacionados relevantes: %s" % len(relational_options),
            "Filtros encontrados: %s" % len(filters),
        ]
        if not (required_fields or selection_fields or relational_options or filters):
            notes.append("Não foram encontrados campos obrigatórios, seleções, relações relevantes ou filtros para este contexto. Isso pode ocorrer em telas técnicas ou quando o frontend não detecta a view correta.")
        return {
            "available": bool(required_fields or selection_fields or relational_options or filters),
            "model": model_name,
            "model_label": model_label,
            "view_type": view_type or "",
            "required_fields": required_fields[:12],
            "selection_fields": selection_fields[:12],
            "relational_options": relational_options[:10],
            "search_filters": filters[:30],
            "notes": notes,
            "debug": debug,
        }


    @api.model
    def get_drawer_article(self, article_id=None):
        """Retorna um artigo completo para leitura dentro do drawer lateral."""
        article = self.browse(int(article_id or 0)).exists()
        if not article or not article.active or not article.published or article.audience not in self._allowed_audiences():
            return {}
        return {
            "id": article.id,
            "name": article.name,
            "summary": article.summary or "",
            "content_html": article.content_html or article._markdown_to_html(article.markdown_source or ""),
            "article_type": dict(article._fields["article_type"].selection).get(article.article_type, article.article_type),
            "scope": dict(article._fields["content_scope"].selection).get(article.content_scope, article.content_scope),
            "audience": article.audience,
            "module": article.module_name or "",
            "model": article.model_name or "",
            "category": article.category_id.name if article.category_id else "",
        }

    @api.model
    def get_error_suggestions(self, error_text=None, context_info=None):
        error_text = error_text or ""
        context_info = dict(context_info or {})
        model_name = context_info.get("resModel") or context_info.get("model") or False
        domain = [("active", "=", True), ("rule_type", "=", "error")]
        if model_name:
            domain += ["|", ("model_name", "=", model_name), ("model_name", "=", False)]
        matches = []
        for rule in self.env["help.suggestion.rule"].search(domain, limit=20):
            if rule._matches_text(error_text):
                matches.append({
                    "id": rule.id,
                    "name": rule.name,
                    "tip": rule.tip_text or "",
                    "articles": [self._serialize_article(a) for a in rule.article_ids.filtered(lambda a: a.published and a.active)[:5]],
                })
        if matches:
            self.env["help.metric"].sudo().log_event({
                "event_type": "error_suggest",
                "model_name": model_name or False,
                "error_text": error_text[:5000],
            })
        return matches

    @api.model
    def log_article_open(self, article_id=None, context_info=None):
        article = self.browse(int(article_id or 0)).exists()
        context_info = dict(context_info or {})
        if article:
            self.env["help.metric"].sudo().log_event({
                "event_type": "article_open",
                "article_id": article.id,
                "model_name": context_info.get("resModel") or False,
                "view_type": context_info.get("viewType") or False,
                "record_id": int(context_info.get("resId") or 0),
            })
        return True
