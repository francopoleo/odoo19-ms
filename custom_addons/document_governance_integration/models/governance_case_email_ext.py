# -*- coding: utf-8 -*-
import base64
import logging

from odoo import api, models, _

_logger = logging.getLogger(__name__)


class GovernanceCaseEmailExtDocuments(models.Model):
    _inherit = "governance.case"

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        """Auto-importa anexos do e-mail como document.document quando configurado no canal."""
        case = super().message_new(msg_dict, custom_values)
        # Obter canal via email_channel_id (pode ter sido populado pelo super)
        channel = case.email_channel_id
        if channel and channel.auto_import_attachments:
            attachments = msg_dict.get("attachments") or []
            if attachments:
                case._auto_import_email_attachments(attachments)
        return case

    def _auto_import_email_attachments(self, attachments):
        """Cria document.document para cada anexo de e-mail recebido."""
        self.ensure_one()
        Document = self.env["document.document"]
        Attachment = self.env["ir.attachment"].sudo()
        for att in attachments:
            fname = att.fname if hasattr(att, "fname") else att[0]
            content = att.content if hasattr(att, "content") else att[1]
            info = att.info if hasattr(att, "info") else (att[2] if len(att) > 2 else {})
            # Ignorar imagens inline (CID attachments)
            if isinstance(info, dict) and info.get("cid"):
                continue
            if isinstance(content, str):
                encoding = info.get("encoding", "utf-8") if isinstance(info, dict) else "utf-8"
                try:
                    content = content.encode(encoding)
                except (UnicodeEncodeError, LookupError):
                    content = content.encode("utf-8", errors="replace")
            try:
                doc = Document.with_context(document_core_system_defaults=True).create({
                    "name": fname,
                    "company_id": self.company_id.id,
                    "access_level": "governance",
                    "responsible_id": self.responsible_id.id if self.responsible_id else False,
                    "case_id": self.id,
                    "source": "external",
                })
                ir_att = Attachment.create({
                    "name": fname,
                    "datas": base64.b64encode(content),
                    "type": "binary",
                    "res_model": "document.document",
                    "res_id": doc.id,
                })
                doc.with_context(document_core_system_defaults=True).write({
                    "attachment_ids": [(4, ir_att.id)]
                })
                _logger.info(
                    "Governance: anexo '%s' importado como document.document %s no caso %s",
                    fname, doc.id, self.reference,
                )
            except Exception as e:
                _logger.warning(
                    "Governance: falha ao importar anexo '%s' no caso %s: %s",
                    fname, self.id, e,
                )
