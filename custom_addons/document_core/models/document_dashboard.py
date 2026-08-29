# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DocumentDashboard(models.TransientModel):
    _name = "document.dashboard"
    _description = "Painel Operacional Documental"

    name = fields.Char(default="Painel Operacional", readonly=True)

    # ── Totais ───────────────────────────────────────────────────
    total_documents = fields.Integer(readonly=True)
    complete_documents = fields.Integer(readonly=True)
    incomplete_documents = fields.Integer(readonly=True)

    # ── Ação Imediata ────────────────────────────────────────────
    expired_count = fields.Integer(readonly=True)
    expiring_count = fields.Integer(readonly=True)
    missing_file_count = fields.Integer(readonly=True)
    pending_validation_count = fields.Integer(readonly=True)

    # ── Revisões ─────────────────────────────────────────────────
    review_overdue_count = fields.Integer(readonly=True)
    review_due_soon_count = fields.Integer(readonly=True)
    review_up_to_date_count = fields.Integer(readonly=True)

    # ── Minha Operação ───────────────────────────────────────────
    my_docs_count = fields.Integer(readonly=True)
    my_expired_count = fields.Integer(readonly=True)
    my_expiring_count = fields.Integer(readonly=True)
    my_review_overdue_count = fields.Integer(readonly=True)
    my_missing_count = fields.Integer(readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        Document = self.env["document.document"]
        uid = self.env.user.id

        # Contadores básicos (campos armazenados)
        res.update({
            # Totais
            "total_documents": Document.search_count([]),
            "complete_documents": Document.search_count([
                ("document_complete", "=", True),
            ]),
            "incomplete_documents": Document.search_count([
                ("document_complete", "=", False),
            ]),
            # Ação Imediata
            "expired_count": Document.search_count([("status", "=", "expired")]),
            "expiring_count": Document.search_count([("status", "=", "expiring")]),
            "missing_file_count": Document.search_count([
                ("attachment_ids", "=", False),
            ]),
            "pending_validation_count": Document.search_count([
                ("document_type_id.requires_validation", "=", True),
                ("is_validated", "=", False),
            ]),
            # Revisões (todos armazenados)
            "review_overdue_count": Document.search_count([("review_status", "=", "overdue")]),
            "review_due_soon_count": Document.search_count([("review_status", "=", "due_soon")]),
            "review_up_to_date_count": Document.search_count([("review_status", "=", "up_to_date")]),
            # Minha Operação (todos armazenados)
            "my_docs_count": Document.search_count([("responsible_id", "=", uid)]),
            "my_expired_count": Document.search_count([
                ("responsible_id", "=", uid),
                ("status", "=", "expired"),
            ]),
            "my_expiring_count": Document.search_count([
                ("responsible_id", "=", uid),
                ("status", "=", "expiring"),
            ]),
            "my_review_overdue_count": Document.search_count([
                ("responsible_id", "=", uid),
                ("review_status", "=", "overdue"),
            ]),
            "my_missing_count": Document.search_count([
                ("responsible_id", "=", uid),
                ("document_complete", "=", False),
            ]),
        })

        return res

    def _doc_action(self, domain, name="Documentos"):
        return {
            "type": "ir.actions.act_window",
            "name": name,
            "res_model": "document.document",
            "view_mode": "list,kanban,form",
            "domain": domain,
            "context": {},
        }

    def action_refresh(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "document.dashboard",
            "view_mode": "form",
            "target": "current",
        }

    # ── Totais ───────────────────────────────────────────────────
    def action_view_all_documents(self):
        return self._doc_action([], _("Todos os Documentos"))

    def action_view_complete_documents(self):
        return self._doc_action(
            [("document_complete", "=", True)],
            _("Documentos Completos"),
        )

    def action_view_incomplete_documents(self):
        return self._doc_action(
            [("document_complete", "=", False)],
            _("Documentos Incompletos"),
        )

    # ── Ação Imediata ────────────────────────────────────────────
    def action_view_expired(self):
        return self._doc_action([("status", "=", "expired")], _("Documentos Vencidos"))

    def action_view_expiring(self):
        return self._doc_action([("status", "=", "expiring")], _("Documentos a Vencer"))

    def action_view_missing_files(self):
        return self._doc_action(
            [("attachment_ids", "=", False)],
            _("Sem Arquivo Anexado"),
        )

    def action_view_pending_validation(self):
        return self._doc_action(
            [
                ("document_type_id.requires_validation", "=", True),
                ("is_validated", "=", False),
            ],
            _("Aguardando Validação"),
        )

    # ── Revisões ─────────────────────────────────────────────────
    def action_view_review_overdue(self):
        return self._doc_action(
            [("review_status", "=", "overdue")],
            _("Revisões Atrasadas"),
        )

    def action_view_review_due_soon(self):
        return self._doc_action(
            [("review_status", "=", "due_soon")],
            _("Revisões Próximas"),
        )

    def action_view_review_up_to_date(self):
        return self._doc_action(
            [("review_status", "=", "up_to_date")],
            _("Revisões Atualizadas"),
        )

    # ── Minha Operação ───────────────────────────────────────────
    def action_view_my_docs(self):
        return self._doc_action(
            [("responsible_id", "=", self.env.user.id)],
            _("Meus Documentos"),
        )

    def action_view_my_expired(self):
        return self._doc_action(
            [("responsible_id", "=", self.env.user.id), ("status", "=", "expired")],
            _("Meus Documentos Vencidos"),
        )

    def action_view_my_expiring(self):
        return self._doc_action(
            [("responsible_id", "=", self.env.user.id), ("status", "=", "expiring")],
            _("Meus Documentos a Vencer"),
        )

    def action_view_my_review_overdue(self):
        return self._doc_action(
            [("responsible_id", "=", self.env.user.id), ("review_status", "=", "overdue")],
            _("Minhas Revisões Atrasadas"),
        )

    def action_view_my_missing(self):
        return self._doc_action(
            [("responsible_id", "=", self.env.user.id), ("document_complete", "=", False)],
            _("Meus Documentos Incompletos"),
        )

    # ── Atalhos Rápidos ──────────────────────────────────────────
    def action_shortcut_documents(self):
        return self.env["ir.actions.actions"]._for_xml_id("document_core.action_document_document")

    def action_shortcut_expiring(self):
        return self.env["ir.actions.actions"]._for_xml_id("document_core.action_document_document_expiring")

    def action_shortcut_validation(self):
        return self.env["ir.actions.actions"]._for_xml_id("document_core.action_document_document_pending_validation")
