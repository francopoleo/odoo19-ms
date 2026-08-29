# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DossierDossier(models.Model):
    _name = "dossier.dossier"
    _description = "Document Dossier - Aggregator for Document Collections"
    _order = "create_date desc"

    # ── Basic Info ────────────────────────────────────────────────────
    name = fields.Char(string="Nome do Dossiê", required=True, translate=True)
    description = fields.Text(string="Descrição", translate=True)

    # ── Process & Organization ────────────────────────────────────────
    process_id = fields.Many2one(
        comodel_name="dossier.process",
        string="Tipo de Processo",
        required=True,
        ondelete="restrict",
    )

    domain = fields.Selection(
        selection=[
            ("governance", "Governança"),
            ("property", "Imóvel"),
            ("hr", "Recursos Humanos"),
            ("generic", "Genérico/Outro"),
        ],
        string="Domínio",
        compute="_compute_domain",
        store=True,
    )

    # ── Registro de Origem ────────────────────────────────────────────
    target_model = fields.Char(
        string="Modelo de Origem",
        readonly=True,
        copy=False,
        index=True,
        help="Modelo técnico do registro que originou o dossiê, como property.asset, property.contract ou governance.case.",
    )
    target_res_id = fields.Integer(
        string="ID de Origem",
        readonly=True,
        copy=False,
        index=True,
        help="ID técnico do registro que originou o dossiê.",
    )
    target_name = fields.Char(
        string="Registro de Origem",
        readonly=True,
        copy=False,
        help="Nome amigável do registro que originou o dossiê.",
    )
    target_display = fields.Char(
        string="Origem",
        compute="_compute_target_display",
    )

    # ── Documents ─────────────────────────────────────────────────────
    document_ids = fields.Many2many(
        comodel_name="document.document",
        relation="dossier_dossier_document_rel",
        column1="dossier_id",
        column2="document_id",
        string="Documents",
    )

    # ── Status & Ownership ────────────────────────────────────────────
    state = fields.Selection(
        selection=[
            ("draft", "Rascunho"),
            ("active", "Ativo"),
            ("closed", "Fechado"),
        ],
        string="State",
        default="draft",
        required=True,
    )

    responsible_id = fields.Many2one(
        comodel_name="res.users",
        string="Usuário Responsável",
        ondelete="set null",
    )

    # ── Dates ─────────────────────────────────────────────────────────
    created_date = fields.Date(string="Created Date", default=fields.Date.today)
    target_date = fields.Date(string="Data Alvo de Conclusão")
    closed_date = fields.Date(string="Data de Fechamento", readonly=True)

    # ── Document Statistics (Computed) ────────────────────────────────
    document_count = fields.Integer(
        string="Total Documents",
        compute="_compute_document_stats",
        store=True,
    )

    complete_documents = fields.Integer(
        string="Complete Documents",
        compute="_compute_document_stats",
        store=True,
    )

    incomplete_documents = fields.Integer(
        string="Incomplete Documents",
        compute="_compute_document_stats",
        store=True,
    )

    missing_requirements = fields.Integer(
        string="Missing Requirements Total",
        compute="_compute_document_stats",
        store=True,
    )

    # Completion percentage
    completion_percent = fields.Float(
        string="Completion %",
        compute="_compute_completion_percent",
    )

    # Overall dossiér completeness
    dossier_complete = fields.Boolean(
        string="Dossiér Complete",
        compute="_compute_dossier_complete",
    )

    # ── Constraints ───────────────────────────────────────────────────
    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'Dossier name must be unique',
    )

    # ── Computed Fields ───────────────────────────────────────────────
    @api.depends("process_id")
    def _compute_domain(self):
        for record in self:
            record.domain = record.process_id.domain if record.process_id else "generic"

    @api.depends("target_model", "target_res_id", "target_name")
    def _compute_target_display(self):
        labels = {
            "property.asset": _("Imóvel"),
            "property.contract": _("Contrato"),
            "governance.case": _("Governança"),
        }
        for record in self:
            if record.target_model and record.target_res_id:
                label = labels.get(record.target_model, record.target_model)
                name = record.target_name or str(record.target_res_id)
                record.target_display = "%s: %s" % (label, name)
            else:
                record.target_display = False

    def _get_target_record(self):
        self.ensure_one()
        if not self.target_model or not self.target_res_id:
            return self.env[self._name].browse()
        try:
            Model = self.env[self.target_model]
        except KeyError:
            return self.env[self._name].browse()
        record = Model.browse(self.target_res_id)
        return record.exists()

    def _prepare_document_vals_from_target(self):
        """Retorna valores padrão para documentos criados a partir do dossiê."""
        self.ensure_one()
        Document = self.env["document.document"]
        target = self._get_target_record()
        vals = {}

        if self.responsible_id and "responsible_id" in Document._fields:
            vals["responsible_id"] = self.responsible_id.id

        if target and hasattr(target, "company_id") and target.company_id and "company_id" in Document._fields:
            vals["company_id"] = target.company_id.id

        if self.target_model == "property.asset" and target:
            if "asset_id" in Document._fields:
                vals["asset_id"] = target.id
        elif self.target_model == "property.contract" and target:
            if "contract_id" in Document._fields:
                vals["contract_id"] = target.id
            if "asset_id" in Document._fields and getattr(target, "asset_id", False):
                vals["asset_id"] = target.asset_id.id
        elif self.target_model == "governance.case" and target:
            if "case_id" in Document._fields:
                vals["case_id"] = target.id

        return vals

    def _document_domain_from_target(self, include_related=False):
        """Domínio de documentos que pertencem ao mesmo contexto do dossiê."""
        self.ensure_one()
        target = self._get_target_record()
        if not target:
            return [("id", "=", 0)]

        Document = self.env["document.document"]

        if self.target_model == "property.asset":
            if "asset_id" not in Document._fields:
                return [("id", "=", 0)]
            domain = [("asset_id", "=", target.id)]
            if include_related and "contract_id" in Document._fields:
                contract_ids = target.contract_ids.ids if "contract_ids" in target._fields else []
                if contract_ids:
                    domain = ["|", ("asset_id", "=", target.id), ("contract_id", "in", contract_ids)]
            return domain

        if self.target_model == "property.contract":
            if "contract_id" not in Document._fields:
                return [("id", "=", 0)]
            domain = [("contract_id", "=", target.id)]
            if include_related and "asset_id" in Document._fields and getattr(target, "asset_id", False):
                domain = ["|", ("contract_id", "=", target.id), ("asset_id", "=", target.asset_id.id)]
            return domain

        if self.target_model == "governance.case":
            if "case_id" not in Document._fields:
                return [("id", "=", 0)]
            domain = [("case_id", "=", target.id)]
            if include_related:
                parts = [[("case_id", "=", target.id)]]
                if "asset_id" in Document._fields and "asset_ids" in target._fields and target.asset_ids:
                    parts.append([("asset_id", "in", target.asset_ids.ids)])
                if "contract_id" in Document._fields and "contract_ids" in target._fields and target.contract_ids:
                    parts.append([("contract_id", "in", target.contract_ids.ids)])
                domain = parts[0]
                for extra in parts[1:]:
                    domain = ["|"] + domain + extra
                return domain
            return domain

        return [("id", "=", 0)]

    def _link_existing_documents_from_target(self, include_related=False):
        Document = self.env["document.document"]
        for dossier in self:
            docs = Document.search(dossier._document_domain_from_target(include_related=include_related))
            if docs:
                dossier.write({"document_ids": [(4, doc_id) for doc_id in docs.ids]})

    def _find_template_line_document(self, line):
        self.ensure_one()
        normalized_name = (line.name or "").strip().lower()
        return self.document_ids.filtered(
            lambda doc: (
                (line.document_type_id and doc.document_type_id == line.document_type_id)
                or ((doc.name or "").strip().lower() == normalized_name)
            )
        )

    def _prepare_document_vals_from_template_line(self, line):
        self.ensure_one()
        vals = self._prepare_document_vals_from_target()
        vals.update({
            "name": line.name or (line.document_type_id.name if line.document_type_id else _("Documento esperado")),
            "description": line.description,
            "notes": line.notes,
            "document_type_id": line.document_type_id.id if line.document_type_id else False,
            "document_state": "draft",
        })
        return vals

    def _apply_template(self, template, create_only_missing=True):
        self.ensure_one()
        if not template or not template.line_ids:
            return self.env["document.document"]

        Document = self.env["document.document"].with_context(document_core_system_defaults=True)
        created_docs = self.env["document.document"]
        for line in template.line_ids:
            existing = self._find_template_line_document(line)
            if existing and create_only_missing:
                continue
            doc = Document.create(self._prepare_document_vals_from_template_line(line))
            created_docs |= doc

        if created_docs:
            self.write({"document_ids": [(4, doc_id) for doc_id in created_docs.ids]})
        return created_docs

    def apply_templates(self, templates=None, create_only_missing=True):
        for dossier in self:
            template_records = templates or dossier.process_id.template_ids
            for template in template_records:
                dossier._apply_template(template, create_only_missing=create_only_missing)
        return True

    @api.depends("document_ids")
    def _compute_document_stats(self):
        for record in self:
            docs = record.document_ids
            record.document_count = len(docs)
            record.complete_documents = len([d for d in docs if d.document_complete])
            record.incomplete_documents = len([d for d in docs if not d.document_complete])
            record.missing_requirements = sum(d.missing_requirements_count for d in docs)

    @api.depends("complete_documents", "document_count")
    def _compute_completion_percent(self):
        for record in self:
            if record.document_count == 0:
                record.completion_percent = 0.0
            else:
                record.completion_percent = (record.complete_documents / record.document_count) * 100

    @api.depends("incomplete_documents", "document_count")
    def _compute_dossier_complete(self):
        for record in self:
            if record.document_count == 0:
                record.dossier_complete = False
            else:
                # Dossiér is complete if all documents are complete
                record.dossier_complete = record.incomplete_documents == 0

    # ── Workflow Methods ──────────────────────────────────────────────
    def action_activate(self):
        """Activate dossiér - all documents must be complete"""
        for record in self:
            if not record.dossier_complete:
                raise UserError(
                    _("Cannot activate dossiér with incomplete documents. "
                      "Please complete all required documents first.")
                )
            record.state = "active"

    def action_close(self):
        """Close dossiér and archive it"""
        for record in self:
            record.state = "closed"
            record.closed_date = fields.Date.today()

    def action_reopen(self):
        """Reopen a closed dossiér"""
        for record in self:
            record.state = "draft"
            record.closed_date = None

    # ── Apply Template ────────────────────────────────────────────────
    def action_apply_template(self):
        """Abrir wizard para aplicar template ao dossiê."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Aplicar Template de Dossiê"),
            "res_model": "document.apply.template.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_dossier_id": self.id,
                "default_template_id": self.process_id.template_ids[:1].id,
            },
        }

    # ── View Actions ──────────────────────────────────────────────────
    def action_view_documents(self):
        """Open related documents"""
        return {
            "type": "ir.actions.act_window",
            "name": _("Documents in Dossiér"),
            "res_model": "document.document",
            "view_mode": "list,form,kanban",
            "domain": [("id", "in", self.document_ids.ids)],
            "context": {"create": False},
        }

    def action_view_incomplete(self):
        """Open incomplete documents"""
        incomplete = self.document_ids.filtered(lambda d: not d.document_complete)
        return {
            "type": "ir.actions.act_window",
            "name": _("Incomplete Documents"),
            "res_model": "document.document",
            "view_mode": "list,form,kanban",
            "domain": [("id", "in", incomplete.ids)],
            "context": {"create": False},
        }
