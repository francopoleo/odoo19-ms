# -*- coding: utf-8 -*-
import hashlib
import os
import re
from pathlib import Path
from odoo import api, fields, models, tools, _


DOC_TYPE_BY_FILENAME = {
    "00_INDICE.md": "index",
    "01_DOCUMENTACAO_TECNICA.md": "technical",
    "02_MANUAL_USUARIO.md": "user_manual",
    "03_CONFIGURACAO_INICIAL.md": "configuration",
    "04_GUIA_TESTES.md": "testing",
    "05_GUIA_IMPLEMENTACAO.md": "implementation",
    "06_TROUBLESHOOTING.md": "troubleshooting",
    "07_CHANGELOG_FUNCIONAL.md": "changelog",
    "08_AJUDA_CONTEXTUAL.md": "contextual_help",
}

TITLE_BY_TYPE = {
    "index": "Índice",
    "technical": "Documentação Técnica",
    "user_manual": "Manual do Usuário",
    "configuration": "Configuração Inicial",
    "testing": "Guia de Testes",
    "implementation": "Guia de Implementação",
    "troubleshooting": "Troubleshooting",
    "changelog": "Changelog Funcional",
    "contextual_help": "Ajuda Contextual",
}

TRUE_VALUES = {"1", "true", "sim", "yes", "y"}
FALSE_VALUES = {"0", "false", "nao", "não", "no", "n"}


class HelpDocSource(models.Model):
    _name = "help.doc.source"
    _description = "Fonte Markdown da Central de Ajuda"
    _order = "module_name, file_path"

    name = fields.Char(string="Nome", required=True)
    module_name = fields.Char(string="Módulo", required=True, index=True)
    file_path = fields.Char(string="Caminho do Arquivo", required=True)
    doc_type = fields.Selection([
        ("index", "Índice"),
        ("technical", "Documentação Técnica"),
        ("user_manual", "Manual do Usuário"),
        ("configuration", "Configuração Inicial"),
        ("testing", "Guia de Testes"),
        ("implementation", "Implementação"),
        ("troubleshooting", "Troubleshooting"),
        ("changelog", "Changelog"),
        ("contextual_help", "Ajuda Contextual"),
        ("faq", "FAQ"),
    ], string="Tipo", default="user_manual", required=True)
    overwrite_policy = fields.Selection([
        ("preserve_odoo", "Preservar edições feitas no Odoo"),
        ("overwrite", "Sobrescrever sempre pelo Markdown"),
    ], string="Política de Reimportação", default="preserve_odoo", required=True)
    article_id = fields.Many2one("help.article", string="Artigo", ondelete="set null")
    last_import_date = fields.Datetime(string="Última Importação", readonly=True)
    checksum = fields.Char(string="Checksum", readonly=True)
    active = fields.Boolean(string="Ativo", default=True)

    def action_import(self):
        for source in self:
            source._import_file()
        return True

    def _import_file(self):
        self.ensure_one()
        path = Path(self.file_path)
        if not path.exists() or not path.is_file():
            return False
        markdown = path.read_text(encoding="utf-8", errors="ignore")
        checksum = hashlib.sha256(markdown.encode("utf-8")).hexdigest()

        # Arquivo especial: cada bloco HELP:ARTICLE vira um artigo contextual curto.
        if self.doc_type == "contextual_help":
            imported = self._import_contextual_blocks(markdown, checksum)
            self.write({"last_import_date": fields.Datetime.now(), "checksum": checksum})
            return imported

        meta, body = self._split_front_matter(markdown)
        title = meta.get("title") or self._extract_title(body) or "%s - %s" % (TITLE_BY_TYPE.get(self.doc_type, "Documento"), self.module_name)
        code = meta.get("code") or self._make_article_code(self.module_name, self.doc_type, path.name)
        category = self._category_from_meta(meta) or self._category_for_module(meta.get("module") or self.module_name) or self._category_for_type(self.doc_type)
        article_type = meta.get("article_type") or meta.get("type") or self.doc_type
        content_scope = meta.get("scope") or meta.get("content_scope") or "full_document"
        show_in_context = self._bool_from_meta(meta.get("show_in_context"), default=(content_scope != "full_document"))
        values = {
            "name": title,
            "code": code,
            "module_name": meta.get("module") or self.module_name,
            "model_name": meta.get("model") or meta.get("model_name") or False,
            "view_type": meta.get("view_type") or False,
            "field_name": meta.get("field") or meta.get("field_name") or False,
            "menu_xmlid": meta.get("menu_xmlid") or False,
            "action_xmlid": meta.get("action_xmlid") or False,
            "article_type": self._normalize_article_type(article_type),
            "audience": self._normalize_audience(meta.get("audience") or self._audience_for_type(self.doc_type)),
            "markdown_source": body,
            "category_id": category.id if category else False,
            "source_id": self.id,
            "checksum": checksum,
            "published": True,
            "content_scope": self._normalize_scope(content_scope),
            "show_in_context": show_in_context,
            "summary": meta.get("summary") or False,
            "sequence": int(meta.get("sequence") or 10),
        }
        article = self._upsert_article(values)
        self._link_article_to_context_from_meta(article, meta)
        self.write({"article_id": article.id, "last_import_date": fields.Datetime.now(), "checksum": checksum})
        return True

    def _upsert_article(self, values):
        Article = self.env["help.article"]
        code = values.get("code")
        article = code and Article.search([("code", "=", code)], limit=1) or False
        if article:
            if self.overwrite_policy == "overwrite" or not article.edited_in_odoo:
                article.with_context(help_import=True).write(values)
            return article
        return Article.with_context(help_import=True).create(values)

    def _import_contextual_blocks(self, markdown, checksum):
        """Importa blocos no padrão:

        <!-- HELP:ARTICLE
        code: document.document.form.create
        title: Como criar um novo documento
        module: document_core
        model: document.document
        view_type: form
        context_name: Formulário de Documento
        -->
        # Conteúdo
        <!-- /HELP:ARTICLE -->
        """
        block_re = re.compile(r"<!--\s*HELP:ARTICLE\s*(.*?)\s*-->\s*(.*?)\s*<!--\s*/HELP:ARTICLE\s*-->", re.S | re.I)
        blocks = list(block_re.finditer(markdown or ""))
        if not blocks:
            # Arquivos 08_AJUDA_CONTEXTUAL.md são fonte de blocos HELP:ARTICLE.
            # Se o arquivo tiver apenas texto introdutório/placeholder, não cria artigo
            # global sem código/modelo, pois isso polui o drawer e, em Odoo 19, pode
            # quebrar por campo obrigatório code.
            meta, body = self._split_front_matter(markdown)
            meta.setdefault("module", self.module_name)
            has_context_metadata = any([
                meta.get("code"),
                meta.get("model"),
                meta.get("model_name"),
                meta.get("menu_xmlid"),
                meta.get("action_xmlid"),
                meta.get("field"),
                meta.get("field_name"),
            ])
            if not has_context_metadata:
                return 0
            meta.setdefault("code", self._make_article_code(self.module_name, "contextual_help", Path(self.file_path).name))
            meta.setdefault("scope", "context")
            meta.setdefault("show_in_context", "true")
            meta.setdefault("article_type", "flow")
            return bool(self._import_contextual_article(meta, body, checksum))
        imported = 0
        for idx, match in enumerate(blocks, start=1):
            meta = self._parse_metadata(match.group(1))
            body = (match.group(2) or "").strip()
            meta.setdefault("module", self.module_name)
            meta.setdefault("scope", "context")
            meta.setdefault("show_in_context", "true")
            meta.setdefault("article_type", "flow")
            if not meta.get("code"):
                meta["code"] = self._make_context_article_code(meta, idx)
            article = self._import_contextual_article(meta, body, checksum)
            if article:
                imported += 1
        return imported

    def _import_contextual_article(self, meta, body, checksum):
        title = meta.get("title") or self._extract_title(body) or "Ajuda Contextual - %s" % (meta.get("model") or meta.get("module") or self.module_name)
        category = self._category_from_meta(meta) or self._category_for_module(meta.get("module") or self.module_name)
        values = {
            "name": title,
            "code": meta.get("code"),
            "module_name": meta.get("module") or self.module_name,
            "model_name": meta.get("model") or meta.get("model_name") or False,
            "view_type": meta.get("view_type") or False,
            "field_name": meta.get("field") or meta.get("field_name") or False,
            "menu_xmlid": meta.get("menu_xmlid") or False,
            "action_xmlid": meta.get("action_xmlid") or False,
            "article_type": self._normalize_article_type(meta.get("article_type") or meta.get("type") or "flow"),
            "content_scope": self._normalize_scope(meta.get("scope") or "context"),
            "show_in_context": self._bool_from_meta(meta.get("show_in_context"), default=True),
            "audience": self._normalize_audience(meta.get("audience") or "all"),
            "summary": meta.get("summary") or False,
            "markdown_source": body,
            "category_id": category.id if category else False,
            "source_id": self.id,
            "checksum": checksum,
            "published": True,
            "sequence": int(meta.get("sequence") or 10),
        }
        article = self._upsert_article(values)
        self._link_article_to_context_from_meta(article, meta)
        return article

    def _link_article_to_context_from_meta(self, article, meta):
        module_name = meta.get("module") or self.module_name or article.module_name
        model_name = meta.get("model") or meta.get("model_name") or article.model_name
        view_type = meta.get("view_type") or article.view_type
        menu_xmlid = meta.get("menu_xmlid") or article.menu_xmlid
        action_xmlid = meta.get("action_xmlid") or article.action_xmlid
        field_name = meta.get("field") or meta.get("field_name") or article.field_name
        if not any([model_name, view_type, menu_xmlid, action_xmlid, field_name]):
            return False
        Context = self.env["help.context"]
        domain = [("active", "=", True)]
        if module_name:
            domain.append(("module_name", "=", module_name))
        if model_name:
            domain.append(("model_name", "=", model_name))
        if view_type:
            domain.append(("view_type", "=", view_type))
        if field_name:
            domain.append(("field_name", "=", field_name))
        if action_xmlid:
            domain.append(("action_xmlid", "=", action_xmlid))
        if menu_xmlid:
            domain.append(("menu_xmlid", "=", menu_xmlid))
        context = Context.search(domain, limit=1)
        if not context:
            category = self._category_from_meta(meta) or article.category_id
            context = Context.create({
                "name": meta.get("context_name") or self._default_context_name(model_name, view_type, field_name),
                "category_id": category.id if category else False,
                "context_kind": meta.get("context_kind") or ("field" if field_name else "screen"),
                "module_name": module_name,
                "model_name": model_name,
                "view_type": view_type,
                "field_name": field_name,
                "menu_xmlid": menu_xmlid,
                "action_xmlid": action_xmlid,
                "description": meta.get("context_description") or False,
            })
        if article and article not in context.article_ids:
            context.write({"article_ids": [(4, article.id)]})
        return context

    @api.model
    def action_discover_installed_module_docs(self):
        """Descobre docs/*.md dos módulos instalados e cria fontes Markdown.

        A descoberta é idempotente: pode ser rodada sempre, como o fluxo de traduções do Odoo.
        Se o arquivo já existe como fonte, ele é reutilizado.
        """
        installed = self.env["ir.module.module"].sudo().search([("state", "=", "installed")])
        module_names = set(installed.mapped("name"))
        count = 0
        for module_name in sorted(module_names):
            module_path = self._find_module_path(module_name)
            if not module_path:
                continue
            docs_dir = module_path / "docs"
            if not docs_dir.exists():
                continue
            for doc_file in sorted(docs_dir.glob("*.md")):
                doc_type = DOC_TYPE_BY_FILENAME.get(doc_file.name, "user_manual")
                source = self.search([("module_name", "=", module_name), ("file_path", "=", str(doc_file))], limit=1)
                if not source:
                    self.create({
                        "name": "%s / %s" % (module_name, doc_file.name),
                        "module_name": module_name,
                        "file_path": str(doc_file),
                        "doc_type": doc_type,
                    })
                    count += 1
                else:
                    # Atualiza tipo caso o padrão tenha evoluído.
                    source.doc_type = doc_type
        return count

    @api.model
    def action_import_active_sources(self):
        sources = self.search([("active", "=", True)])
        sources.action_import()
        return len(sources)

    @api.model
    def _find_module_path(self, module_name):
        addons_paths = tools.config.get("addons_path") or ""
        if isinstance(addons_paths, str):
            paths = [p for p in addons_paths.split(os.pathsep) if p]
        else:
            paths = list(addons_paths)
        for addons_path in paths:
            candidate = Path(addons_path).expanduser() / module_name
            if (candidate / "__manifest__.py").exists() or (candidate / "__openerp__.py").exists():
                return candidate
        return False

    @api.model
    def _extract_title(self, markdown):
        for line in (markdown or "").splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        return False

    @api.model
    def _split_front_matter(self, markdown):
        text = markdown or ""
        if text.startswith("---\n"):
            end = text.find("\n---", 4)
            if end > 0:
                meta_text = text[4:end]
                body = text[end + len("\n---"):].lstrip("\n")
                return self._parse_metadata(meta_text), body
        return {}, text

    @api.model
    def _parse_metadata(self, meta_text):
        meta = {}
        for raw in (meta_text or "").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().lower().replace("-", "_")
            value = value.strip().strip('"').strip("'")
            meta[key] = value
        return meta

    @api.model
    def _make_article_code(self, module_name, doc_type, filename):
        safe = (filename or "doc").lower().replace(".md", "").replace(" ", "_").replace("-", "_")
        return "%s.%s.%s" % (module_name, doc_type, safe)

    @api.model
    def _make_context_article_code(self, meta, index):
        parts = [meta.get("module") or self.module_name or "module"]
        if meta.get("model") or meta.get("model_name"):
            parts.append((meta.get("model") or meta.get("model_name")).replace(".", "_"))
        if meta.get("view_type"):
            parts.append(meta.get("view_type"))
        if meta.get("field") or meta.get("field_name"):
            parts.append((meta.get("field") or meta.get("field_name")).replace(".", "_"))
        title = (meta.get("title") or "artigo_%s" % index).lower()
        title = re.sub(r"[^a-z0-9_]+", "_", title, flags=re.I).strip("_")[:60]
        parts.append(title or str(index))
        return ".".join(parts)

    @api.model
    def _default_context_name(self, model_name, view_type, field_name=False):
        if field_name:
            return "%s / Campo %s" % (model_name or "Contexto", field_name)
        if model_name and view_type:
            labels = dict(self.env["help.context"]._fields["view_type"].selection)
            return "%s / %s" % (model_name, labels.get(view_type, view_type))
        return model_name or "Contexto de Ajuda"

    @api.model
    def _bool_from_meta(self, value, default=False):
        if value is None or value == "":
            return default
        value = str(value).strip().lower()
        if value in TRUE_VALUES:
            return True
        if value in FALSE_VALUES:
            return False
        return default

    @api.model
    def _normalize_article_type(self, value):
        value = (value or "user_manual").strip()
        allowed = dict(self.env["help.article"]._fields["article_type"].selection)
        return value if value in allowed else "user_manual"

    @api.model
    def _normalize_scope(self, value):
        value = (value or "context").strip()
        allowed = dict(self.env["help.article"]._fields["content_scope"].selection)
        return value if value in allowed else "context"

    @api.model
    def _normalize_audience(self, value):
        value = (value or "all").strip()
        allowed = dict(self.env["help.article"]._fields["audience"].selection)
        return value if value in allowed else "all"

    @api.model
    def _category_from_meta(self, meta):
        code = meta.get("category_code")
        name = meta.get("category") or meta.get("area")
        if code:
            category = self.env["help.category"].search([("code", "=", code)], limit=1)
            if category:
                return category
        if name:
            code = code or "custom.%s" % re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_")
            category = self.env["help.category"].search(["|", ("code", "=", code), ("name", "=", name)], limit=1)
            if category:
                return category
            return self.env["help.category"].create({"name": name, "code": code, "sequence": 50})
        return False

    @api.model
    def _category_for_module(self, module_name):
        """Categoria funcional por módulo."""
        labels = {
            "document_core": "Documentos",
            "property_core": "Imóveis",
            "governance": "Governança",
            "common_base": "Agenda Geral",
            "document_dossier": "Dossiês",
            "common_help_center": "Central de Ajuda",
        }
        if not module_name:
            return False
        code = "module.%s" % module_name
        category = self.env["help.category"].search([("code", "=", code)], limit=1)
        if category:
            return category
        return self.env["help.category"].create({
            "name": labels.get(module_name, module_name.replace("_", " ").title()),
            "code": code,
            "sequence": 50,
        })

    @api.model
    def _category_for_type(self, doc_type):
        code = {
            "technical": "technical",
            "user_manual": "user_manual",
            "configuration": "configuration",
            "testing": "testing",
            "implementation": "implementation",
            "troubleshooting": "troubleshooting",
            "changelog": "changelog",
        }.get(doc_type, "overview")
        return self.env["help.category"].search([("code", "=", code)], limit=1)

    @api.model
    def _audience_for_type(self, doc_type):
        if doc_type == "technical":
            return "technical"
        if doc_type in ("configuration", "implementation", "testing"):
            return "admin"
        return "all"
