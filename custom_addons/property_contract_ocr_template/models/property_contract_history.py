# -*- coding: utf-8 -*-
import base64
import io
import json
import glob
import logging
import os
import re
import shutil
import subprocess

from markupsafe import Markup

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PropertyContractHistory(models.Model):
    _inherit = "property.contract.history"

    ocr_template_id = fields.Many2one(
        "property.contract.ocr.template",
        string="Template OCR",
        tracking=True,
        help="Template com as regras de OCR/regex usadas para procurar campos neste contrato.",
    )
    ocr_template_auto_detected = fields.Boolean("Template detectado automaticamente", readonly=True)
    ocr_force_template = fields.Boolean(
        "Forçar template selecionado",
        help="Se marcado, usa o template selecionado mesmo que a autodetecção encontre outro.",
    )

    def _is_generic_filename(self, filename):
        name = (filename or "").strip().lower()
        return name in {
            "contrato",
            "contrato.pdf",
            "contrato.jpg",
            "contrato.jpeg",
            "contrato.png",
            "arquivo_pdf_sem_nome.pdf",
            "arquivo_sem_nome",
            "anexo_sem_nome",
        }

    def _infer_filename_from_binary(self, data, fallback=False, write_safe=False):
        """Return a safe processing filename without overwriting the real upload name.

        Important: this method must not force the business filename to
        'contrato.pdf'. Generic names are acceptable only internally for MIME/type
        detection. The original filename must be preserved whenever Odoo provides it.
        """
        if fallback and not self._is_generic_filename(fallback):
            return fallback
        if not write_safe:
            return fallback or False
        if data and data[:4] == b"%PDF":
            return fallback or "arquivo_pdf_sem_nome.pdf"
        if data and data[:3] == b"\xff\xd8\xff":
            return fallback or "arquivo_imagem_sem_nome.jpg"
        if data and data[:8] == b"\x89PNG\r\n\x1a\n":
            return fallback or "arquivo_imagem_sem_nome.png"
        return fallback or "arquivo_sem_nome"

    def _find_original_attachment_filename(self):
        """Try to recover the true upload filename from ir.attachment."""
        self.ensure_one()
        attachments = self.env["ir.attachment"].search([
            ("res_model", "=", self._name),
            ("res_id", "=", self.id),
        ], order="id desc", limit=10)
        for attachment in attachments:
            if attachment.name and not self._is_generic_filename(attachment.name):
                return attachment.name
        return False

    def write(self, vals):
        """Preserve or infer the upload filename.

        Some Odoo 19 binary widgets may send the binary without the filename
        when a view extension is changed or when a legacy record is edited.
        This keeps contract_filename from being cleared and guarantees a
        readable name when the binary is a PDF/image.
        """
        if vals.get("contract_file") and not vals.get("contract_filename"):
            try:
                data = base64.b64decode(vals.get("contract_file"))
            except Exception:
                data = b""
            current_name = self[:1].contract_filename if self else False
            recovered_name = False
            if self and self[:1]:
                recovered_name = self[:1]._find_original_attachment_filename()
            filename = current_name if current_name and not self._is_generic_filename(current_name) else recovered_name
            if filename:
                vals["contract_filename"] = filename
            # Never write generic names such as contrato.pdf here.
            if data[:4] == b"%PDF" and not vals.get("mimetype"):
                vals["mimetype"] = "application/pdf"
        if "contract_filename" in vals and not vals.get("contract_filename") and "contract_file" not in vals:
            vals.pop("contract_filename")
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("contract_file") and not vals.get("contract_filename"):
                try:
                    data = base64.b64decode(vals.get("contract_file"))
                except Exception:
                    data = b""
                # Filename must come from the binary widget via filename="contract_filename".
                # Do not invent contrato.pdf, because it hides the real uploaded name.
                if data[:4] == b"%PDF" and not vals.get("mimetype"):
                    vals["mimetype"] = "application/pdf"
        return super().create(vals_list)

    # -------------------------------------------------------------------------
    # Debug/log helpers
    # -------------------------------------------------------------------------

    def _write_ocr_log(self, log, state=False, raw_text=False):
        """Always persist OCR/debug information before raising an error."""
        self.ensure_one()
        vals = {"extraction_log": "\n".join([str(item) for item in (log or []) if item is not None]) or "-"}
        if state:
            vals["state"] = state
        if raw_text is not False:
            vals["raw_text"] = raw_text or ""
        self.with_context(tracking_disable=True).write(vals)
        return vals["extraction_log"]

    def _safe_notify(self, title, message, sticky=False, notification_type="info"):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "sticky": sticky,
                "type": notification_type,
            },
        }

    def _detect_file_kind(self, data, filename="", mimetype="", log=None):
        """Detect file type by MIME, extension and binary signature.

        This is critical because the original form did not always save
        contract_filename when users uploaded files. In that case a PDF may be
        named only "contrato" and extension-based detection fails.
        """
        log = log if log is not None else []
        filename_lower = (filename or "").lower()
        mimetype_lower = (mimetype or "").lower()
        head = data[:32] if data else b""

        if mimetype_lower == "application/pdf" or filename_lower.endswith(".pdf") or head.startswith(b"%PDF"):
            if head.startswith(b"%PDF") and not filename_lower.endswith(".pdf"):
                log.append("Tipo detectado por assinatura binária: PDF (%PDF). O nome do arquivo não tinha extensão .pdf.")
            return "pdf"
        if (
            mimetype_lower in ("image/jpeg", "image/jpg")
            or filename_lower.endswith((".jpg", ".jpeg"))
            or head.startswith(b"\xff\xd8\xff")
        ):
            return "image"
        if mimetype_lower == "image/png" or filename_lower.endswith(".png") or head.startswith(b"\x89PNG"):
            return "image"
        if mimetype_lower in ("image/tiff", "image/tif") or filename_lower.endswith((".tif", ".tiff")) or head.startswith((b"II*\x00", b"MM\x00*")):
            return "image"
        if mimetype_lower == "image/webp" or filename_lower.endswith(".webp") or head.startswith(b"RIFF"):
            return "image"
        return "unknown"

    def _get_binary_file_data(self, log=None):
        self.ensure_one()
        log = log if log is not None else []

        if self.contract_file:
            try:
                data = base64.b64decode(self.contract_file)
            except Exception as exc:
                log.append(f"Falha ao decodificar campo Arquivo do Contrato: {exc}")
                data = b""
            recovered_name = self._find_original_attachment_filename()
            filename = self.contract_filename if self.contract_filename and not self._is_generic_filename(self.contract_filename) else recovered_name
            processing_filename = filename or self._infer_filename_from_binary(data, fallback=self.contract_filename, write_safe=True)
            mimetype = self.mimetype or ("application/pdf" if data[:4] == b"%PDF" else "")
            if (not self.contract_filename or self._is_generic_filename(self.contract_filename)) or not self.mimetype:
                fix_vals = {}
                if filename and (not self.contract_filename or self._is_generic_filename(self.contract_filename)):
                    fix_vals["contract_filename"] = filename
                    log.append(f"Nome original recuperado/preservado: {filename}")
                elif not filename and not self.contract_filename:
                    log.append("Nome original do arquivo não veio do widget; usando nome técnico somente para OCR, sem alterar o campo Nome do Arquivo.")
                if not self.mimetype and mimetype:
                    fix_vals["mimetype"] = mimetype
                    log.append(f"MIME estava vazio; preenchido automaticamente como: {mimetype}")
                if fix_vals:
                    self.with_context(tracking_disable=True).write(fix_vals)
            filename = processing_filename
            log.append(f"Arquivo encontrado no campo Arquivo do Contrato: {filename} ({len(data)} bytes). MIME: {mimetype or '-'}")
            return data, filename, mimetype

        attachments = self.env["ir.attachment"].search(
            [
                ("res_model", "=", self._name),
                ("res_id", "=", self.id),
                ("mimetype", "in", ["application/pdf", "image/png", "image/jpeg", "image/tiff", "image/webp"]),
            ],
            order="id desc",
        )
        log.append(f"Campo Arquivo do Contrato vazio. Anexos PDF/imagem vinculados encontrados: {len(attachments)}.")
        for attachment in attachments:
            if not attachment.datas:
                log.append(f"Anexo {attachment.id} / {attachment.name}: sem dados binários; ignorado.")
                continue
            try:
                data = base64.b64decode(attachment.datas)
            except Exception as exc:
                log.append(f"Anexo {attachment.id} / {attachment.name}: falha ao decodificar: {exc}")
                continue
            log.append(f"Usando anexo {attachment.id}: {attachment.name or '-'} ({len(data)} bytes). MIME: {attachment.mimetype or '-'}")
            return data, attachment.name or "anexo_sem_nome", attachment.mimetype or ""

        return b"", "", ""

    def _find_tessdata_dir(self):
        """Find a tessdata directory that contains por/eng traineddata.

        Homebrew/macOS sometimes exposes tesseract in /usr/local/bin but does
        not expose the same tessdata folder to pytesseract. This makes OCR run
        with the wrong/empty language set.
        """
        candidates = []
        env_value = os.environ.get("TESSDATA_PREFIX")
        if env_value:
            candidates.append(env_value)
            candidates.append(os.path.join(env_value, "tessdata"))
        candidates.extend([
            "/usr/local/share/tessdata",
            "/opt/homebrew/share/tessdata",
            "/usr/share/tesseract-ocr/5/tessdata",
            "/usr/share/tesseract-ocr/4.00/tessdata",
            "/usr/share/tessdata",
        ])
        candidates.extend(glob.glob("/usr/local/Cellar/tesseract*/**/share/tessdata", recursive=True))
        candidates.extend(glob.glob("/opt/homebrew/Cellar/tesseract*/**/share/tessdata", recursive=True))
        seen = set()
        for path in candidates:
            if not path or path in seen:
                continue
            seen.add(path)
            if not os.path.isdir(path):
                continue
            files = set(os.listdir(path))
            if "por.traineddata" in files or "eng.traineddata" in files:
                return path
        return False

    def _get_available_tesseract_languages(self):
        """Return languages reported by pytesseract/tesseract.

        Tries the default tessdata first and then a discovered tessdata folder.
        This prevents Homebrew Tesseract from reporting an incomplete/odd
        language set.
        """
        languages = []
        tessdata_dir = self._find_tessdata_dir()
        configs = [""]
        if tessdata_dir:
            configs.append(f'--tessdata-dir "{tessdata_dir}"')
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                import pytesseract
            for config in configs:
                try:
                    found = pytesseract.get_languages(config=config) or []
                    languages.extend(found)
                except Exception:
                    pass
        except Exception:
            languages = []
        if not languages:
            binary = shutil.which("tesseract")
            if binary:
                commands = [[binary, "--list-langs"]]
                if tessdata_dir:
                    commands.append([binary, "--tessdata-dir", tessdata_dir, "--list-langs"])
                for command in commands:
                    try:
                        output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=10).decode("utf-8", "ignore")
                        lines = [x.strip() for x in output.splitlines() if x.strip()]
                        languages.extend([x for x in lines if not x.lower().startswith("list of available languages")])
                    except Exception:
                        pass
        return sorted(set(languages))

    def _choose_tesseract_lang(self, log=None):
        """Choose the safest OCR language option for the current server.

        Prefer Portuguese + English, but never let a missing language make OCR
        return empty. If neither por nor eng is installed, fallback to default
        tesseract invocation and log the problem clearly.
        """
        log = log if log is not None else []
        languages = self._get_available_tesseract_languages()
        has_por = "por" in languages
        has_eng = "eng" in languages
        if has_por and has_eng:
            return "por+eng"
        if has_por:
            log.append("Idioma OCR escolhido: por. Atenção: eng não apareceu no tessdata.")
            return "por"
        if has_eng:
            log.append("Idioma OCR escolhido: eng. Atenção: por não apareceu no tessdata; instale português para melhorar contratos em PT-BR.")
            return "eng"
        log.append("ATENÇÃO: nem 'por' nem 'eng' apareceram nos idiomas do Tesseract. Tentando OCR sem parâmetro lang. Instale tessdata por/eng.")
        return False

    def _prepare_image_for_ocr(self, image, log=None, context="OCR"):
        """Improve scanned contract images before sending them to Tesseract."""
        log = log if log is not None else []
        try:
            from PIL import ImageOps, ImageFilter, ImageEnhance
            if getattr(image, "mode", "") not in ("L", "RGB"):
                image = image.convert("RGB")
            image = image.convert("L")
            image = ImageOps.autocontrast(image)
            image = ImageEnhance.Contrast(image).enhance(1.8)
            image = image.filter(ImageFilter.SHARPEN)
            width, height = image.size
            # Tesseract performs better when the rendered page has enough pixels.
            if width < 1800:
                scale = 1800.0 / max(width, 1)
                image = image.resize((int(width * scale), int(height * scale)))
                log.append(f"{context}: imagem ampliada para OCR: {image.size}.")
            return image
        except Exception as exc:
            log.append(f"{context}: pré-processamento de imagem falhou; usando imagem original: {exc}")
            return image

    def _tesseract_image_to_string(self, image, log=None, context="OCR"):
        """Run OCR with robust language/config fallback and detailed logging."""
        log = log if log is not None else []
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                import pytesseract
        except Exception as exc:
            log.append(f"{context}: pytesseract indisponível: {exc}")
            return ""

        image = self._prepare_image_for_ocr(image, log=log, context=context)
        preferred = self._choose_tesseract_lang(log)
        tessdata_dir = self._find_tessdata_dir()
        tessdata_cfg = f'--tessdata-dir "{tessdata_dir}" ' if tessdata_dir else ""
        if tessdata_dir:
            log.append(f"{context}: tessdata-dir usado: {tessdata_dir}")

        psm_configs = [
            ("psm6", "--oem 1 --psm 6"),
            ("psm4", "--oem 1 --psm 4"),
            ("psm11", "--oem 1 --psm 11"),
            ("psm3", "--oem 1 --psm 3"),
        ]
        langs = []
        if preferred:
            langs.append(preferred)
        for candidate in ("por+eng", "por", "eng"):
            if candidate not in langs:
                langs.append(candidate)
        # Default system language may work even when list-langs is odd.
        langs.append(False)

        best_text = ""
        for lang in langs:
            for cfg_label, cfg in psm_configs:
                kwargs = {"config": tessdata_cfg + cfg}
                label = lang or "padrão do sistema"
                if lang:
                    kwargs["lang"] = lang
                try:
                    text = pytesseract.image_to_string(image, **kwargs) or ""
                    clean_len = len(text.strip())
                    log.append(f"{context}: tentativa lang='{label}' {cfg_label} extraiu {clean_len} caracteres.")
                    if clean_len > len(best_text.strip()):
                        best_text = text
                    if clean_len >= 50:
                        return text
                except Exception as exc:
                    log.append(f"{context}: tentativa lang='{label}' {cfg_label} falhou: {exc}")
        return best_text

    def _get_tesseract_debug(self):
        log = []
        binary = shutil.which("tesseract")
        log.append(f"tesseract no PATH: {binary or 'NÃO ENCONTRADO'}")
        if binary:
            try:
                version = subprocess.check_output([binary, "--version"], stderr=subprocess.STDOUT, timeout=5).decode("utf-8", "ignore").splitlines()[0]
                log.append(f"tesseract --version: {version}")
            except Exception as exc:
                log.append(f"Falha ao executar tesseract --version: {exc}")

        tessdata_dir = self._find_tessdata_dir()
        log.append(f"tessdata-dir detectado: {tessdata_dir or 'NÃO ENCONTRADO'}")
        if tessdata_dir:
            log.append(f"por.traineddata: {'OK' if os.path.exists(os.path.join(tessdata_dir, 'por.traineddata')) else 'NÃO ENCONTRADO'}")
            log.append(f"eng.traineddata: {'OK' if os.path.exists(os.path.join(tessdata_dir, 'eng.traineddata')) else 'NÃO ENCONTRADO'}")
        languages = self._get_available_tesseract_languages()
        log.append(f"Total de idiomas Tesseract detectados: {len(languages)}")
        log.append(f"Idioma português 'por': {'OK' if 'por' in languages else 'NÃO ENCONTRADO'}")
        log.append(f"Idioma inglês 'eng': {'OK' if 'eng' in languages else 'NÃO ENCONTRADO'}")
        if languages:
            preview = ", ".join(languages[:80])
            if len(languages) > 80:
                preview += f", ... (+{len(languages) - 80} outros)"
            log.append("Idiomas tesseract detectados: " + preview)
        else:
            log.append("Nenhum idioma retornado por pytesseract/tesseract --list-langs.")
        if "por" not in languages or "eng" not in languages:
            log.append("AÇÃO RECOMENDADA: instalar/ajustar tessdata para incluir 'por' e 'eng'. No macOS/Homebrew: brew install tesseract-lang; se necessário, exporte TESSDATA_PREFIX para a pasta tessdata correta.")
        return log

    def _get_python_ocr_debug(self):
        log = []
        modules = [
            ("pypdf", "Leitura de PDF pesquisável"),
            ("PyPDF2", "Leitura de PDF pesquisável alternativa"),
            ("fitz", "PyMuPDF para renderizar PDF escaneado"),
            ("PIL", "Pillow para imagens"),
            ("pytesseract", "OCR Tesseract via Python"),
            ("pdf2image", "Fallback PDF para imagem via poppler"),
        ]
        for module_name, purpose in modules:
            try:
                module = __import__(module_name)
                version = getattr(module, "__version__", "ok")
                log.append(f"Python lib {module_name}: OK ({version}) - {purpose}")
            except Exception as exc:
                log.append(f"Python lib {module_name}: AUSENTE/ERRO ({exc}) - {purpose}")
        return log

    def action_debug_ocr_environment(self):
        for history in self:
            log = [
                "===== DIAGNÓSTICO DO AMBIENTE OCR =====",
                f"Banco/empresa: {history.env.cr.dbname} / {history.env.company.display_name}",
                f"Registro: {history.display_name} (ID {history.id})",
                f"Usuário: {history.env.user.display_name}",
                "",
                "--- Dependências Python ---",
            ]
            log.extend(history._get_python_ocr_debug())
            log.append("")
            log.append("--- Tesseract do sistema ---")
            log.extend(history._get_tesseract_debug())
            log.append("")
            log.append("--- Arquivo atual ---")
            data, filename, mimetype = history._get_binary_file_data(log)
            if data:
                kind = history._detect_file_kind(data, filename, mimetype, log)
                log.append(f"Tipo detectado: {kind}")
                log.append(f"Assinatura inicial bytes: {data[:12]!r}")
            else:
                log.append("Nenhum arquivo encontrado para testar.")
            history._write_ocr_log(log)
        return self._safe_notify(_("Diagnóstico OCR concluído"), _("Veja o campo Log de Extração / OCR no topo da aba Arquivo & Extração."), sticky=False)

    def action_debug_ocr_file(self):
        for history in self:
            template = history.ocr_template_id or self.env["property.contract.ocr.template"].search([("active", "=", True)], limit=1)
            text, log = history._extract_text_for_template(template=template, force_reprocess=True, debug=True)
            preview = (text or "").strip()[:1000]
            log.append("")
            log.append("===== RESULTADO DO TESTE =====")
            log.append(f"Caracteres extraídos: {len(text or '')}")
            if preview:
                log.append("Prévia dos primeiros 1000 caracteres:")
                log.append(preview)
                history._write_ocr_log(log, raw_text=text)
                return self._safe_notify(_("OCR encontrou texto"), _("Foram extraídos %s caracteres. Veja o Log de Extração / OCR.") % len(text or ""), sticky=False, notification_type="success")
            history._write_ocr_log(log, state="failed")
        return self._safe_notify(_("OCR não encontrou texto"), _("Veja o Log de Extração / OCR. Ele agora mostra arquivo, tipo detectado, bibliotecas e tentativas."), sticky=True, notification_type="warning")

    # -------------------------------------------------------------------------
    # Extraction engines
    # -------------------------------------------------------------------------

    def _extract_pdf_text_direct(self, data, log):
        text = ""
        try:
            try:
                from pypdf import PdfReader
                lib_name = "pypdf"
            except Exception:
                from PyPDF2 import PdfReader
                lib_name = "PyPDF2"
            reader = PdfReader(io.BytesIO(data))
            log.append(f"PDF texto direto: biblioteca {lib_name}; páginas detectadas: {len(reader.pages)}.")
            chunks = []
            for page_index, page in enumerate(reader.pages, start=1):
                try:
                    page_text = page.extract_text() or ""
                    chunks.append(page_text)
                    log.append(f"PDF texto direto: página {page_index}, {len(page_text)} caracteres.")
                except Exception as exc:
                    log.append(f"PDF texto direto: falha na página {page_index}: {exc}")
            text = "\n".join(chunks).strip()
        except Exception as exc:
            log.append(f"PDF texto direto indisponível: {exc}")
        return text

    def _ocr_image_bytes(self, data, log):
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                from PIL import Image
                import pytesseract
        except Exception as exc:
            log.append(f"OCR imagem indisponível. Instale pillow+pytesseract+tesseract: {exc}")
            return ""
        try:
            image = Image.open(io.BytesIO(data))
            log.append(f"OCR imagem: formato={getattr(image, 'format', '-')}, tamanho={getattr(image, 'size', '-')}, modo={getattr(image, 'mode', '-')}")
            text = self._tesseract_image_to_string(image, log, context="OCR imagem")
            log.append(f"OCR imagem: {len(text or '')} caracteres finais.")
            return (text or "").strip()
        except Exception as exc:
            log.append(f"OCR imagem falhou: {exc}")
            return ""

    def _ocr_pdf_pymupdf(self, data, page_limit, log):
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                import fitz
                from PIL import Image
                import pytesseract
        except Exception as exc:
            log.append(f"OCR PDF via PyMuPDF indisponível. Instale pymupdf+pillow+pytesseract: {exc}")
            return ""
        try:
            doc = fitz.open(stream=data, filetype="pdf")
            pages = min(len(doc), max(page_limit or 1, 1))
            log.append(f"OCR PyMuPDF: processando {pages} de {len(doc)} página(s), zoom 3x.")
            chunks = []
            for page_number in range(pages):
                page = doc.load_page(page_number)
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                page_text = self._tesseract_image_to_string(image, log, context=f"Página {page_number + 1} / PyMuPDF")
                chunks.append(page_text or "")
                log.append(f"Página {page_number + 1}: OCR PyMuPDF extraiu {len(page_text or '')} caracteres finais.")
            return "\n".join(chunks).strip()
        except Exception as exc:
            log.append(f"OCR PDF via PyMuPDF falhou: {exc}")
            return ""

    def _ocr_pdf_pdf2image(self, data, page_limit, log):
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                from pdf2image import convert_from_bytes
                import pytesseract
        except Exception as exc:
            log.append(f"OCR PDF via pdf2image indisponível. Instale pdf2image+poppler+pytesseract: {exc}")
            return ""
        try:
            last_page = max(page_limit or 1, 1)
            pages = convert_from_bytes(data, first_page=1, last_page=last_page, dpi=300)
            log.append(f"OCR pdf2image: processando {len(pages)} página(s), dpi=300.")
            chunks = []
            for idx, image in enumerate(pages, start=1):
                page_text = self._tesseract_image_to_string(image, log, context=f"Página {idx} / pdf2image")
                chunks.append(page_text or "")
                log.append(f"Página {idx}: OCR pdf2image extraiu {len(page_text or '')} caracteres finais.")
            return "\n".join(chunks).strip()
        except Exception as exc:
            log.append(f"OCR PDF via pdf2image falhou: {exc}")
            return ""

    def _extract_text_for_template(self, template=False, force_reprocess=False, debug=False):
        self.ensure_one()
        log = ["===== EXTRAÇÃO OCR/PDF ====="]
        if self.raw_text and len(self.raw_text.strip()) > 20 and not force_reprocess:
            log.append("Usando texto já existente no campo Texto extraído / OCR. Para testar o arquivo novamente, use o botão 'Testar OCR do Arquivo'.")
            return self.raw_text, log

        data, filename, mimetype = self._get_binary_file_data(log)
        if not data:
            log.append("Nenhum arquivo encontrado no campo Arquivo do Contrato nem nos anexos do registro.")
            return "", log

        kind = self._detect_file_kind(data, filename, mimetype, log)
        mode = (template.extraction_mode if template else "auto") or "auto"
        page_limit = template.page_limit if template else 8
        log.append(f"Template informado: {template.display_name if template else '-'}")
        log.append(f"Modo de extração: {mode}")
        log.append(f"Limite de páginas: {page_limit}")
        log.append(f"Tipo final usado pelo motor: {kind}")
        text = ""

        if kind == "pdf":
            if mode in ("auto", "pypdf"):
                text = self._extract_pdf_text_direct(data, log)
                log.append(f"Total após texto direto: {len(text or '')} caracteres.")
            if mode == "pypdf":
                return text, log
            if mode == "ocr" or not text or len(text.strip()) < 30:
                if text:
                    log.append("Texto direto insuficiente para template; tentando OCR de PDF escaneado.")
                text = self._ocr_pdf_pymupdf(data, page_limit, log)
                log.append(f"Total após PyMuPDF OCR: {len(text or '')} caracteres.")
                if not text or len(text.strip()) < 30:
                    text2 = self._ocr_pdf_pdf2image(data, page_limit, log)
                    log.append(f"Total após pdf2image OCR: {len(text2 or '')} caracteres.")
                    if len(text2 or "") > len(text or ""):
                        text = text2
            return text, log

        if kind == "image":
            return self._ocr_image_bytes(data, log), log

        log.append("Tipo de arquivo não suportado. Dica: se for PDF, o nome do arquivo pode estar sem extensão e a assinatura binária não foi reconhecida como %PDF.")
        return "", log

    # -------------------------------------------------------------------------
    # Main actions
    # -------------------------------------------------------------------------

    def action_detect_ocr_template(self):
        for history in self:
            text, log = history._extract_text_for_template(history.ocr_template_id)
            template = history.env["property.contract.ocr.template"]._auto_detect_from_text(text, company=history.company_id)
            vals = {"raw_text": text or history.raw_text, "extraction_log": "\n".join(log)}
            if template:
                vals.update({"ocr_template_id": template.id, "ocr_template_auto_detected": True})
            history.with_context(tracking_disable=True).write(vals)
            if not template:
                log.append("Nenhum template OCR detectado. Ajuste regex/palavras-chave do template ou selecione manualmente e marque Forçar template selecionado.")
                history._write_ocr_log(log)
                raise UserError(_("Nenhum template OCR foi detectado. Veja o Log de Extração / OCR no topo da aba Arquivo & Extração."))
        return True

    def _create_template_lines(self, line_payloads):
        self.ensure_one()
        self.line_ids.unlink()
        Line = self.env["property.contract.history.line"]
        sequence = 10
        for item in line_payloads:
            if not item.get("matched") and not item.get("required"):
                continue
            field_name = item.get("field_name")
            parsed_value = item.get("parsed_value")
            if parsed_value in (False, None):
                parsed_value = ""
            Line.create({
                "history_id": self.id,
                "field_name": field_name,
                "raw_value": item.get("raw_value") or "",
                "parsed_value": str(parsed_value),
                "field_type": self._map_template_line_type(item.get("field_type")),
                "confidence": item.get("confidence") or 0.0,
                "accepted": bool(item.get("matched") and parsed_value not in (False, None, "")),
                "notes": item.get("notes") or ("Obrigatório não encontrado" if item.get("required") and not item.get("matched") else ""),
                "sequence": sequence,
            })
            sequence += 10

    def _map_template_line_type(self, value_type):
        return {
            "date": "date",
            "float": "monetary",
            "monetary": "monetary",
            "text": "text",
            "selection": "selection",
        }.get(value_type, "char")

    def _apply_template_payload(self, template, values, lines, text, log):
        self.ensure_one()
        write_vals = {
            "raw_text": text,
            "contract_type": values.get("contract_type") or self.contract_type or "other",
            "matched_payload": json.dumps(values, default=str, ensure_ascii=False, indent=2),
            "parser_used": f"Template OCR: {template.name}",
            "state": "extracted",
            "ocr_template_id": template.id,
            "extraction_log": "\n".join(log),
        }
        target_fields = [
            "party1_name", "party1_vat", "party2_name", "party2_vat",
            "sign_date", "start_date", "end_date", "renewal_date",
            "monthly_amount", "total_value", "deposit_value",
            "address", "address_complement", "neighborhood", "city", "zip_code", "property_description",
        ]
        for field_name in target_fields:
            if field_name in values and values[field_name] not in (False, None, ""):
                write_vals[field_name] = values[field_name]
        self.with_context(tracking_disable=True).write(write_vals)
        self._create_template_lines(lines)
        missing = [l.get("field_label") or l.get("field_name") for l in lines if l.get("required") and not l.get("matched")]
        body = [
            f"<b>Extração por Template OCR</b>: {template.name}",
            f"<b>Campos encontrados:</b> {len([l for l in lines if l.get('matched')])}",
        ]
        if missing:
            body.append("<b>Obrigatórios não encontrados:</b><br/>" + "<br/>".join([f"• {m}" for m in missing]))
        self.message_post(body=Markup("<br/>".join(body)))

    def action_extract_by_template(self):
        for history in self:
            template = history.ocr_template_id
            try:
                text, log = history._extract_text_for_template(template)
                if not text or len(text.strip()) < 20:
                    log.append("RESULTADO: nenhum texto útil extraído. Use 'Diagnosticar Ambiente OCR' e confirme se tesseract + pytesseract + PyMuPDF estão instalados no mesmo ambiente do Odoo.")
                    history._write_ocr_log(log, state="failed")
                    raise UserError(_(
                        "Nenhum texto foi extraído por OCR/PDF. Veja o campo 'Log de Extração / OCR' no topo da aba 'Arquivo & Extração'."
                    ))

                if not template or not history.ocr_force_template:
                    detected = history.env["property.contract.ocr.template"]._auto_detect_from_text(text, company=history.company_id)
                    if detected:
                        template = detected
                if not template:
                    log.append("Texto foi extraído, mas nenhum template foi selecionado ou detectado.")
                    history._write_ocr_log(log, raw_text=text)
                    raise UserError(_(
                        "Texto extraído, mas nenhum template foi selecionado/detectado. Selecione um Template OCR e marque 'Forçar template selecionado', ou ajuste a autodetecção."
                    ))

                values, lines = template.extract_payload(text)
                found_count = len([l for l in lines if l.get('matched')])
                log.append(f"Template usado: {template.name}")
                log.append(f"Campos configurados no template: {len(template.line_ids)}")
                log.append(f"Campos encontrados: {found_count}")
                log.append("--- Resultado das regras do template ---")
                for item in lines:
                    label = item.get("field_label") or item.get("field_name")
                    if item.get("matched"):
                        raw = (item.get("raw_value") or "").replace("\n", " ")
                        parsed = item.get("parsed_value") or ""
                        log.append(f"OK  - {label}: bruto='{raw[:180]}' | parseado='{parsed}' | confiança={item.get('confidence')}")
                    else:
                        req = "OBRIGATÓRIO" if item.get("required") else "opcional"
                        pattern = (item.get("pattern") or "").replace("\n", " ")
                        log.append(f"NÃO - {label} ({req}). Regex não encontrou. Padrão: {pattern[:240]}")
                history._apply_template_payload(template, values, lines, text, log)
            except UserError:
                raise
            except Exception as exc:
                _logger.exception("Template OCR failed")
                extra = ["ERRO INESPERADO NO OCR/TEMPLATE:", str(exc)]
                history._write_ocr_log(extra, state="failed")
                raise UserError(_("Erro inesperado no OCR/template. Veja o Log de Extração / OCR."))
        return True

    def action_extract(self):
        """Prefer template OCR when configured/detected; fallback to original parser."""
        if self.env.context.get("skip_template_ocr"):
            return super().action_extract()
        for history in self:
            # If there is a selected template or template can be detected, use template flow.
            if history.ocr_template_id or self.env["property.contract.ocr.template"].search_count([("active", "=", True)]):
                try:
                    return history.action_extract_by_template()
                except UserError:
                    raise
                except Exception as exc:
                    _logger.exception("Template OCR failed, falling back to original parser: %s", exc)
        return super().action_extract()
