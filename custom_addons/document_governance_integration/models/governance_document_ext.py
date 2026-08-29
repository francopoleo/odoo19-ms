# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class GovernanceCaseDocumentExt(models.Model):
    _inherit = "governance.case"

    document_ids = fields.One2many("document.document", "case_id", string="Documentos")
    document_count = fields.Integer("Qtd. Documentos", compute="_compute_document_count")

    @api.depends("document_ids")
    def _compute_document_count(self):
        for case in self:
            case.document_count = len(case.document_ids)

    def action_view_documents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Documentos — %s") % self.display_name,
            "res_model": "document.document",
            "view_mode": "list,form",
            "domain": [("case_id", "=", self.id)],
            "context": {
                "default_case_id": self.id,
                "default_company_id": self.company_id.id,
                "default_access_level": "governance",
            },
        }

    def action_new_document(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Novo Documento do Caso"),
            "res_model": "document.document",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_case_id": self.id,
                "default_company_id": self.company_id.id,
                "default_access_level": "governance",
                "default_responsible_id": self.responsible_id.id,
            },
        }


class DocumentGovernanceExt(models.Model):
    _inherit = "document.document"

    case_id = fields.Many2one(
        "governance.case",
        string="Caso de Governança",
        ondelete="set null",
        tracking=True,
        index=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    governance_reference = fields.Char(
        "Referência de Governança",
        related="case_id.reference",
        store=True,
        readonly=True,
    )

    @api.onchange("case_id")
    def _onchange_case_id_company(self):
        for doc in self:
            if doc.case_id:
                doc.company_id = doc.case_id.company_id
                doc.access_level = "governance"
                if not doc.responsible_id:
                    doc.responsible_id = doc.case_id.responsible_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            case_id = vals.get("case_id")
            if case_id:
                case = self.env["governance.case"].browse(case_id).exists()
                if case:
                    vals.setdefault("company_id", case.company_id.id)
                    vals.setdefault("access_level", "governance")
                    vals.setdefault("responsible_id", case.responsible_id.id)
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        if "case_id" in vals:
            for doc in self.filtered("case_id"):
                updates = {}
                if doc.case_id.company_id and doc.company_id != doc.case_id.company_id:
                    updates["company_id"] = doc.case_id.company_id.id
                if doc.access_level != "governance":
                    updates["access_level"] = "governance"
                if updates:
                    super(DocumentGovernanceExt, doc).write(updates)
        return res
