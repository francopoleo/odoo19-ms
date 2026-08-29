import base64
from urllib.parse import quote

from odoo import http
from odoo.http import request


class DocumentCorePreviewController(http.Controller):
    @http.route(
        "/document_core/document/<int:document_id>/attachment/<int:attachment_id>",
        type="http",
        auth="user",
        methods=["GET"],
    )
    def document_attachment(self, document_id, attachment_id, download="0", **kwargs):
        """Entrega anexo vinculado ao documento por rota estável."""
        document = request.env["document.document"].search([("id", "=", document_id)], limit=1)
        if not document:
            return request.not_found()

        attachment = request.env["ir.attachment"].sudo().browse(attachment_id).exists()
        if not attachment:
            return request.not_found()

        if attachment.id not in document.sudo().attachment_ids.ids:
            return request.not_found()

        raw = attachment.datas
        if not raw:
            return request.not_found()

        try:
            content = base64.b64decode(raw)
        except Exception:
            return request.not_found()

        filename = attachment.name or "documento"
        safe_filename = filename.replace('"', "'")
        quoted_filename = quote(filename.encode("utf-8"))
        as_download = str(download).lower() in ("1", "true", "yes")
        disposition = "attachment" if as_download else "inline"

        headers = [
            ("Content-Type", attachment.mimetype or "application/octet-stream"),
            ("Content-Length", str(len(content))),
            ("X-Content-Type-Options", "nosniff"),
            (
                "Content-Disposition",
                "%s; filename=\"%s\"; filename*=UTF-8''%s" % (disposition, safe_filename, quoted_filename),
            ),
        ]
        return request.make_response(content, headers=headers)
