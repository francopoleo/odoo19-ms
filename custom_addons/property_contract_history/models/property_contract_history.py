# -*- coding: utf-8 -*-
import json
import logging
import re
import urllib.error
import urllib.request
import base64
import io
from datetime import datetime, date
from difflib import SequenceMatcher

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html_escape
from markupsafe import Markup

from ..parsers import parser_registry

_logger = logging.getLogger(__name__)


def normalize_text(value):
    """Normalize text for comparison."""
    value = (value or "").strip().lower()
    value = re.sub(r"[\W_]+", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def normalize_doc(value):
    """Normalize document to digits only."""
    return re.sub(r"\D+", "", value or "")


class PropertyContractHistory(models.Model):
    _name = "property.contract.history"
    _description = "Histórico de Contratos com OCR"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"

    # ─────────────────────────────────────────────────────────────────────────
    # IDENTIFICATION & STATE
    # ─────────────────────────────────────────────────────────────────────────

    name = fields.Char("Referência", readonly=True, copy=False, default="New")
    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        default=lambda self: self.env.company,
        required=True,
    )
    contract_type = fields.Selection(
        [
            ("rental", "Aluguel/Locação"),
            ("sale", "Venda"),
            ("financing", "Financiamento/Hipoteca"),
            ("comodato", "Comodato"),
            ("other", "Outro"),
        ],
        string="Tipo de Contrato",
        help="Tipo detectado automaticamente pelo parser",
    )

    state = fields.Selection(
        [
            ("draft", "Rascunho"),
            ("extracted", "Extraído"),
            ("reviewed", "Revisado"),
            ("approved", "Aprovado"),
            ("synced", "Sincronizado"),
            ("rejected", "Rejeitado"),
            ("failed", "Falha no OCR"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    # ─────────────────────────────────────────────────────────────────────────
    # FILE & EXTRACTION
    # ─────────────────────────────────────────────────────────────────────────

    contract_file = fields.Binary("Arquivo do Contrato", attachment=True)
    contract_filename = fields.Char("Nome do Arquivo")
    mimetype = fields.Char("MIME Type")
    raw_text = fields.Text("Texto extraído / OCR")
    extraction_log = fields.Text("Log de Extração", readonly=True)
    matched_payload = fields.Text("JSON da Extração", readonly=True)
    parser_used = fields.Char("Parser Utilizado", readonly=True)

    # ─────────────────────────────────────────────────────────────────────────
    # LINKED RECORDS
    # ─────────────────────────────────────────────────────────────────────────

    asset_id = fields.Many2one(
        "property.asset",
        string="Imóvel",
        help="Imóvel vinculado a este contrato",
    )
    contract_id = fields.Many2one(
        "property.contract",
        string="Contrato Associado",
        help="Contrato existente no Odoo (opcional)",
    )
    sync_to_asset = fields.Boolean(
        "Sincronizar com Imóvel",
        default=True,
        help="Permitir sincronização de dados para o imóvel?",
    )

    # ─────────────────────────────────────────────────────────────────────────
    # PARTIES INVOLVED
    # ─────────────────────────────────────────────────────────────────────────

    party1_name = fields.Char("Parte 1 - Nome")
    party1_vat = fields.Char("Parte 1 - CPF/CNPJ")
    party2_name = fields.Char("Parte 2 - Nome")
    party2_vat = fields.Char("Parte 2 - CPF/CNPJ")

    # ─────────────────────────────────────────────────────────────────────────
    # CRITICAL DATES
    # ─────────────────────────────────────────────────────────────────────────

    sign_date = fields.Date("Data da Assinatura")
    start_date = fields.Date("Data de Início")
    end_date = fields.Date("Data de Término")
    renewal_date = fields.Date(
        "Data de Renovação",
        help="Próxima data de revisão/renovação do contrato",
    )

    # ─────────────────────────────────────────────────────────────────────────
    # FINANCIAL DATA
    # ─────────────────────────────────────────────────────────────────────────

    monthly_amount = fields.Monetary(
        "Valor Mensal",
        currency_field="currency_id",
        help="Aluguel, prestação ou valor mensal",
    )
    total_value = fields.Monetary(
        "Valor Total",
        currency_field="currency_id",
        help="Valor total (venda, financiamento, etc.)",
    )
    deposit_value = fields.Monetary(
        "Valor de Caução/Depósito",
        currency_field="currency_id",
        help="Caução ou depósito (contratos de aluguel)",
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
    )

    # ─────────────────────────────────────────────────────────────────────────
    # PROPERTY DETAILS (EXTRACTED)
    # ─────────────────────────────────────────────────────────────────────────

    address = fields.Char("Endereço do Imóvel")
    address_complement = fields.Char("Complemento")
    neighborhood = fields.Char("Bairro")
    city = fields.Char("Cidade")
    zip_code = fields.Char("CEP")
    property_description = fields.Text("Descrição do Imóvel")

    # ─────────────────────────────────────────────────────────────────────────
    # SYNC TRACKING
    # ─────────────────────────────────────────────────────────────────────────

    synced_to_asset_id = fields.Many2one(
        "property.asset",
        string="Sincronizado com Imóvel",
        readonly=True,
        help="Qual imóvel foi sincronizado com este contrato",
    )
    sync_timestamp = fields.Datetime("Data da Sincronização", readonly=True)
    sync_log = fields.Text("Log de Sincronização", readonly=True)
    superseded_by_id = fields.Many2one(
        "property.contract.history",
        string="Substituído por",
        readonly=True,
        help="Contrato mais recente que substituiu este",
    )

    # ─────────────────────────────────────────────────────────────────────────
    # RELATIONSHIPS
    # ─────────────────────────────────────────────────────────────────────────

    line_ids = fields.One2many(
        "property.contract.history.line",
        "history_id",
        string="Campos Extraídos",
        help="Cada linha é um campo extraído com score de confiança",
    )
    history_ids = fields.One2many(
        "property.contract.history",
        "superseded_by_id",
        string="Versões Anteriores",
        readonly=True,
    )

    # ─────────────────────────────────────────────────────────────────────────
    # LIFECYCLE
    # ─────────────────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].sudo().next_by_code("property.contract.history")
                    or "CTRT-HIST"
                )
        return super().create(vals_list)

    # ─────────────────────────────────────────────────────────────────────────
    # PDF TEXT EXTRACTION (Reuse payment_proof pattern)
    # ─────────────────────────────────────────────────────────────────────────

    def _ocr_image_to_text(self, image):
        """Executa OCR em uma imagem com fallback de idioma."""
        try:
            import pytesseract
        except Exception as exc:
            raise UserError(_(
                "OCR de imagem não disponível. Instale pytesseract e tesseract-ocr no servidor, "
                "ou cole o texto manualmente no campo 'Texto extraído / OCR'. Erro: %s"
            ) % exc)

        try:
            text = pytesseract.image_to_string(image, lang="por+eng")
        except Exception:
            text = pytesseract.image_to_string(image, lang="eng")
        return (text or "").strip()

    def _extract_pdf_text(self, data):
        """Extrai texto pesquisável de PDF com pypdf/PyPDF2."""
        try:
            from pypdf import PdfReader
        except Exception:
            try:
                from PyPDF2 import PdfReader
            except Exception as exc:
                raise UserError(_(
                    "Biblioteca de leitura de PDF não encontrada. Instale 'pypdf' ou cole o texto do contrato "
                    "no campo 'Texto extraído / OCR'. Erro: %s"
                ) % exc)

        reader = PdfReader(io.BytesIO(data))
        chunks = []
        for page in reader.pages:
            try:
                chunks.append(page.extract_text() or "")
            except Exception as exc:
                _logger.warning("Could not extract text from PDF page: %s", exc)
                continue
        return "\n".join(chunks).strip()

    def _extract_pdf_with_pymupdf_ocr(self, data, max_pages=6):
        """Renderiza páginas do PDF com PyMuPDF e aplica OCR. Não depende de poppler."""
        try:
            import fitz  # PyMuPDF
            from PIL import Image
        except Exception as exc:
            _logger.info("PyMuPDF/Pillow OCR fallback unavailable: %s", exc)
            return ""

        chunks = []
        try:
            doc = fitz.open(stream=data, filetype="pdf")
            for page_index in range(min(len(doc), max_pages)):
                page = doc.load_page(page_index)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                text = self._ocr_image_to_text(image)
                if text:
                    chunks.append(text)
        except Exception as exc:
            _logger.warning("PyMuPDF PDF OCR fallback failed: %s", exc)
            return ""
        return "\n".join(chunks).strip()

    def _extract_pdf_with_pdf2image_ocr(self, data, max_pages=6):
        """Converte PDF com pdf2image/poppler e aplica OCR."""
        try:
            from pdf2image import convert_from_bytes
        except Exception as exc:
            _logger.info("pdf2image OCR fallback unavailable: %s", exc)
            return ""

        chunks = []
        try:
            images = convert_from_bytes(data, first_page=1, last_page=max_pages, dpi=220)
            for image in images:
                text = self._ocr_image_to_text(image)
                if text:
                    chunks.append(text)
        except Exception as exc:
            _logger.warning("pdf2image PDF OCR fallback failed: %s", exc)
            return ""
        return "\n".join(chunks).strip()

    def _extract_pdf_as_image(self, data):
        """Fallback OCR para PDF escaneado: tenta PyMuPDF e depois pdf2image."""
        text = self._extract_pdf_with_pymupdf_ocr(data)
        if text and len(text.strip()) >= 10:
            return text
        text = self._extract_pdf_with_pdf2image_ocr(data)
        return (text or "").strip()

    def _extract_image_text(self, data):
        """Extrai texto de imagem via OCR."""
        try:
            from PIL import Image
        except Exception as exc:
            raise UserError(_(
                "Para OCR de imagem/scanner, instale Pillow + pytesseract + tesseract-ocr. "
                "Alternativa: cole o texto manualmente. Erro: %s"
            ) % exc)
        try:
            image = Image.open(io.BytesIO(data))
            return self._ocr_image_to_text(image)
        except Exception as exc:
            _logger.warning("Image OCR failed: %s", exc)
            return ""

    def _extract_text_from_file(self):
        """Extrai texto do arquivo enviado.

        Contratos frequentemente chegam como PDF escaneado. Por isso o fluxo é:
        1) texto pesquisável do PDF; 2) OCR com PyMuPDF; 3) OCR com pdf2image/poppler.
        """
        self.ensure_one()
        if not self.contract_file:
            return self.raw_text or ""

        data = base64.b64decode(self.contract_file)
        filename = (self.contract_filename or "").lower()
        logs = []

        if filename.endswith(".pdf"):
            text = self._extract_pdf_text(data)
            if text and len(text.strip()) >= 10:
                logs.append(_("PDF com texto pesquisável: extração direta concluída."))
                self.with_context(tracking_disable=True).write({"extraction_log": "\n".join(logs)})
                return text

            logs.append(_("PDF sem texto pesquisável suficiente; tentando OCR de PDF escaneado."))
            text = self._extract_pdf_as_image(data)
            if text and len(text.strip()) >= 10:
                logs.append(_("OCR de PDF escaneado concluído."))
                self.with_context(tracking_disable=True).write({"extraction_log": "\n".join(logs)})
                return text

            logs.append(_(
                "Nenhum texto foi extraído do PDF. Possíveis causas: PDF escaneado sem OCR instalado, "
                "PyMuPDF/pdf2image/poppler ausente, tesseract ausente ou PDF protegido."
            ))
            self.with_context(tracking_disable=True).write({"extraction_log": "\n".join(logs)})
            return ""

        if filename.endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")):
            text = self._extract_image_text(data)
            if text:
                self.with_context(tracking_disable=True).write({"extraction_log": _("OCR de imagem concluído.")})
            return text

        return self.raw_text or ""

    # ─────────────────────────────────────────────────────────────────────────
    # PARSING & EXTRACTION
    # ─────────────────────────────────────────────────────────────────────────

    def _parse_text(self, text):
        """Parse text using parser registry."""
        parser = parser_registry.find(text)
        return parser.parse(text)

    def action_extract(self):
        """Extract text from file and parse into structured fields."""
        for history in self:
            try:
                # Step 1: Extract text - prioriza raw_text manual, depois arquivo
                text = history.raw_text or history._extract_text_from_file()
                if not text:
                    message = _(
                        "Nenhum texto foi extraído. Se o arquivo for PDF escaneado/imagem, instale OCR no servidor "
                        "(tesseract-ocr + pytesseract e, para PDF escaneado, PyMuPDF ou pdf2image/poppler). "
                        "Alternativa: cole o texto no campo 'Texto extraído / OCR'.\n\nLog técnico:\n%s"
                    ) % (history.extraction_log or "-")
                    history.with_context(tracking_disable=True).write({
                        "state": "failed",
                        "extraction_log": message,
                    })
                    raise UserError(message)

                # Step 2: Parse text
                parsed = history._parse_text(text)

                # Step 3: Store raw text and parsed data
                history.with_context(tracking_disable=True).write(
                    {
                        "raw_text": text,
                        "contract_type": parsed.get("contract_type") or "other",
                        "party1_name": parsed.get("party1_name") or False,
                        "party1_vat": parsed.get("party1_vat") or False,
                        "party2_name": parsed.get("party2_name") or False,
                        "party2_vat": parsed.get("party2_vat") or False,
                        "sign_date": parsed.get("sign_date") or False,
                        "start_date": parsed.get("start_date") or False,
                        "end_date": parsed.get("end_date") or False,
                        "monthly_amount": parsed.get("monthly_amount") or 0.0,
                        "total_value": parsed.get("total_value") or 0.0,
                        "deposit_value": parsed.get("deposit_value") or 0.0,
                        "address": parsed.get("address") or False,
                        "neighborhood": parsed.get("neighborhood") or False,
                        "city": parsed.get("city") or False,
                        "zip_code": parsed.get("zip_code") or False,
                        "property_description": parsed.get("property_description") or False,
                        "matched_payload": json.dumps(parsed, default=str, ensure_ascii=False, indent=2),
                        "parser_used": parsed.get("parser_name") or "generic",
                        "state": "extracted",
                        "extraction_log": _("Extração concluída com sucesso."),
                    }
                )

                # Step 4: Create detail lines for each field
                Line = self.env["property.contract.history.line"]
                fields_extracted = [
                    ("party1_name", "Parte 1 - Nome", parsed.get("party1_name"), "char", 95),
                    ("party1_vat", "Parte 1 - CPF/CNPJ", parsed.get("party1_vat"), "char", 85),
                    ("party2_name", "Parte 2 - Nome", parsed.get("party2_name"), "char", 95),
                    ("party2_vat", "Parte 2 - CPF/CNPJ", parsed.get("party2_vat"), "char", 85),
                    ("sign_date", "Data da Assinatura", parsed.get("sign_date"), "date", 90),
                    ("start_date", "Data de Início", parsed.get("start_date"), "date", 90),
                    ("end_date", "Data de Término", parsed.get("end_date"), "date", 85),
                    ("monthly_amount", "Valor Mensal", parsed.get("monthly_amount"), "monetary", 85),
                    ("total_value", "Valor Total", parsed.get("total_value"), "monetary", 85),
                    ("deposit_value", "Caução/Depósito", parsed.get("deposit_value"), "monetary", 80),
                    ("address", "Endereço", parsed.get("address"), "char", 80),
                    ("neighborhood", "Bairro", parsed.get("neighborhood"), "char", 75),
                    ("city", "Cidade", parsed.get("city"), "char", 80),
                    ("zip_code", "CEP", parsed.get("zip_code"), "char", 90),
                    ("property_description", "Descrição Imóvel", parsed.get("property_description"), "text", 70),
                ]

                for field_name, label, value, field_type, confidence in fields_extracted:
                    if value:
                        Line.create(
                            {
                                "history_id": history.id,
                                "field_name": field_name,
                                "raw_value": str(value),
                                "parsed_value": str(value),
                                "field_type": field_type,
                                "confidence": confidence,
                                "accepted": True,  # Auto-accept extracted values
                            }
                        )

                # Step 5: Post extraction summary
                history.message_post(
                    body=Markup(
                        "<b>OCR Extraído</b> <small>(parser: {parser})</small><br/>"
                        "<b>Tipo:</b> {contract_type}<br/>"
                        "<b>Parte 1:</b> {party1}<br/>"
                        "<b>Parte 2:</b> {party2}<br/>"
                        "<b>Período:</b> {start_date} até {end_date}<br/>"
                        "<b>Valor Mensal:</b> {monthly}<br/>"
                        "<b>Imóvel:</b> {address}<br/>"
                        "<b>Campos extraídos:</b> {line_count}"
                    ).format(
                        parser=parsed.get("parser_name") or "genérico",
                        contract_type=dict(history._fields["contract_type"].selection).get(
                            parsed.get("contract_type"), parsed.get("contract_type")
                        )
                        or "-",
                        party1=parsed.get("party1_name") or "-",
                        party2=parsed.get("party2_name") or "-",
                        start_date=str(parsed.get("start_date") or "-"),
                        end_date=str(parsed.get("end_date") or "-"),
                        monthly=f"R$ {parsed.get('monthly_amount'):,.2f}"
                        if parsed.get("monthly_amount")
                        else "-",
                        address=parsed.get("address") or "-",
                        line_count=len(history.line_ids),
                    )
                )

            except Exception as exc:
                history.write({"state": "failed", "extraction_log": str(exc)})
                raise

    def action_manual_review(self):
        """Transition to reviewed state after user validates extracted fields."""
        for history in self:
            if history.state != "extracted":
                raise UserError(
                    _("Contrato deve estar em estado 'Extraído' para revisão.")
                )
            # Validate that critical fields are accepted
            if not history.line_ids.filtered(lambda l: l.accepted):
                raise UserError(
                    _(
                        "Nenhum campo foi marcado como aceito. Revise os campos extraídos antes de prosseguir."
                    )
                )
            history.state = "reviewed"
            history.message_post(body=_("Contrato revisado manualmente pelo usuário."))

    def action_approve(self):
        """Approve and lock the record for sync."""
        for history in self:
            if history.state != "reviewed":
                raise UserError(
                    _("Contrato deve estar em estado 'Revisado' antes de aprovação.")
                )
            history.state = "approved"
            history.message_post(body=_("Contrato aprovado. Pronto para sincronização."))

    # ─────────────────────────────────────────────────────────────────────────
    # ASSET MATCHING & SYNC
    # ─────────────────────────────────────────────────────────────────────────

    def _safe_field_value(self, record, field_name):
        """Return a field value only when it exists on the target model.

        This module is used with different versions/customizations of
        property.asset. Some databases use address/neighborhood, others use
        street/street2/state_id. Accessing a missing field directly breaks the
        Buscar Imóvel button with AttributeError.
        """
        if not record or field_name not in record._fields:
            return ""
        value = record[field_name]
        if hasattr(value, "display_name"):
            return value.display_name or ""
        return value or ""

    def _set_update_if_field_exists(self, record, updates, field_name, value):
        """Safely stage a write only for fields available on the target model."""
        if value not in (False, None, "") and field_name in record._fields:
            updates[field_name] = value
            return True
        return False

    def _score_property_match(self, asset):
        """Score similarity between extracted property data and property.asset."""
        if not asset:
            return 0.0

        extracted_text = normalize_text(
            " ".join([
                self.address or "",
                self.address_complement or "",
                self.neighborhood or "",
                self.city or "",
                self.zip_code or "",
                self.property_description or "",
            ])
        )
        if not extracted_text:
            return 0.0

        asset_text = normalize_text(
            " ".join([
                self._safe_field_value(asset, "name"),
                self._safe_field_value(asset, "display_name"),
                self._safe_field_value(asset, "address"),
                self._safe_field_value(asset, "street"),
                self._safe_field_value(asset, "street2"),
                self._safe_field_value(asset, "address_complement"),
                self._safe_field_value(asset, "neighborhood"),
                self._safe_field_value(asset, "district"),
                self._safe_field_value(asset, "city"),
                self._safe_field_value(asset, "state_id"),
                self._safe_field_value(asset, "zip"),
                self._safe_field_value(asset, "zip_code"),
                self._safe_field_value(asset, "registration_number"),
                self._safe_field_value(asset, "municipal_registration"),
                self._safe_field_value(asset, "property_code"),
                self._safe_field_value(asset, "code"),
            ])
        )
        if not asset_text:
            return 0.0

        ratio = SequenceMatcher(None, extracted_text, asset_text).ratio()

        # Bonus for exact tokens that usually identify the unit, such as sala/loja number.
        bonus = 0.0
        extracted_tokens = set(re.findall(r"\b(?:sala|loja|conjunto|apto|ap)\s*\d+[a-z]?|\b\d{2,5}[a-z]?\b", extracted_text))
        asset_tokens = set(re.findall(r"\b(?:sala|loja|conjunto|apto|ap)\s*\d+[a-z]?|\b\d{2,5}[a-z]?\b", asset_text))
        if extracted_tokens and asset_tokens and extracted_tokens.intersection(asset_tokens):
            bonus = 20.0

        return min(100.0, (ratio * 100.0) + bonus)

    def action_find_asset(self):
        """Auto-suggest matching property.asset based on address similarity."""
        self.ensure_one()
        if not any([self.address, self.property_description, self.city, self.neighborhood, self.zip_code]):
            raise UserError(_("Nenhum dado do imóvel foi extraído para buscar imóvel."))

        Asset = self.env["property.asset"]
        domain = []
        if "company_id" in Asset._fields and self.company_id:
            domain.append(("company_id", "=", self.company_id.id))
        candidates = Asset.search(domain)

        matches = []
        for asset in candidates:
            score = self._score_property_match(asset)
            if score > 40:  # Threshold
                matches.append((score, asset))

        if matches:
            matches.sort(reverse=True, key=lambda x: x[0])
            best_score, best_asset = matches[0]
            self.write({"asset_id": best_asset.id})
            self.message_post(
                body=Markup(_("Imóvel sugerido: <b>%s</b> (score: %.0f%%)"))
                % (best_asset.display_name, best_score)
            )
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Imóvel encontrado"),
                    "message": _("Imóvel sugerido: %s") % best_asset.display_name,
                    "type": "success",
                    "sticky": False,
                },
            }

        # Não deve bloquear o usuário com Invalid Operation.
        # Quando não houver match automático, deixe o campo asset_id editável
        # para seleção manual no formulário.
        self.message_post(
            body=_("Nenhum imóvel correspondente foi encontrado automaticamente. Selecione o imóvel manualmente no campo Imóvel.")
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Busca automática sem resultado"),
                "message": _("Nenhum imóvel correspondente foi encontrado automaticamente. O campo Imóvel está liberado para seleção manual."),
                "type": "warning",
                "sticky": False,
            },
        }


    def _partner_from_extracted_party(self, name, vat=False):
        """Find or create a partner from OCR data, when enough information exists."""
        name = (name or "").strip()
        vat = normalize_doc(vat)
        Partner = self.env["res.partner"].sudo()
        partner = False

        if vat:
            partner = Partner.search([("vat", "=", vat)], limit=1)
        if not partner and name:
            partner = Partner.search([("name", "=ilike", name)], limit=1)
        if not partner and name:
            vals = {"name": name}
            if vat:
                vals["vat"] = vat
            if "company_id" in Partner._fields and self.company_id:
                vals["company_id"] = self.company_id.id
            partner = Partner.create(vals)
        return partner

    def _is_valid_contract_value(self, Contract, field_name, value):
        """Validate values for flexible target fields before create()."""
        if value in (False, None, "") or field_name not in Contract._fields:
            return False
        field = Contract._fields[field_name]
        if getattr(field, "type", False) == "selection":
            selection = field.selection
            if callable(selection):
                selection = selection(Contract)
            keys = [item[0] for item in (selection or [])]
            return value in keys
        return True

    def _put_if_contract_field_exists(self, Contract, vals, field_name, value):
        """Safely add a value only if the destination field exists and value is usable."""
        if self._is_valid_contract_value(Contract, field_name, value):
            vals[field_name] = value
            return True
        return False

    def _put_first_existing_contract_field(self, Contract, vals, field_names, value):
        """Put a value in the first available compatible field from a list of aliases."""
        for field_name in field_names:
            if self._put_if_contract_field_exists(Contract, vals, field_name, value):
                return True
        return False

    def _put_all_existing_contract_fields(self, Contract, vals, field_names, value):
        """Put the same semantic value in all compatible aliases that exist.

        Some deployments keep both legacy and new fields on property.contract.
        Example: date_start may exist for an old UI, while start_date is the
        database-required field. If we only fill the first alias, create() can
        still fail with a NOT NULL error.
        """
        written = False
        for field_name in field_names:
            if self._put_if_contract_field_exists(Contract, vals, field_name, value):
                written = True
        return written

    def _history_start_date_for_contract(self):
        """Best available start date for creating property.contract."""
        self.ensure_one()
        return self.start_date or self.sign_date or fields.Date.context_today(self)

    def _history_end_date_for_contract(self):
        """Best available end date for creating property.contract."""
        self.ensure_one()
        return self.end_date or self.renewal_date or self.start_date


    def _find_or_create_record_from_partner(self, model_name, partner, role_label=False):
        """Return a record in model_name that represents partner.

        This is needed because some real-estate modules use business models
        such as property.tenant/property.owner on property.contract instead of
        pointing directly to res.partner.
        """
        self.ensure_one()
        if not partner or model_name not in self.env.registry.models:
            return False

        Model = self.env[model_name].sudo()

        # 1) Try exact links to res.partner first.
        for link_field in ("partner_id", "contact_id", "res_partner_id", "commercial_partner_id"):
            if link_field in Model._fields:
                rec = Model.search([(link_field, "=", partner.id)], limit=1)
                if rec:
                    return rec

        # 2) Try fiscal document and name.
        for vat_field in ("vat", "cnpj_cpf", "document_number", "tax_id"):
            if vat_field in Model._fields and partner.vat:
                rec = Model.search([(vat_field, "=", partner.vat)], limit=1)
                if rec:
                    return rec

        if "name" in Model._fields and partner.name:
            rec = Model.search([("name", "=", partner.name)], limit=1)
            if rec:
                return rec

        # 3) Create a minimal compatible record.
        vals = {}
        for link_field in ("partner_id", "contact_id", "res_partner_id"):
            if link_field in Model._fields:
                vals[link_field] = partner.id
                break

        if "name" in Model._fields:
            vals["name"] = partner.name or role_label or _("Parte do contrato")
        if "display_name" in Model._fields and "name" not in vals:
            vals["display_name"] = partner.display_name
        if "vat" in Model._fields and partner.vat:
            vals["vat"] = partner.vat
        if "email" in Model._fields and partner.email:
            vals["email"] = partner.email
        if "phone" in Model._fields and partner.phone:
            vals["phone"] = partner.phone
        if "mobile" in Model._fields and partner.mobile:
            vals["mobile"] = partner.mobile
        if "company_id" in Model._fields and self.company_id:
            vals["company_id"] = self.company_id.id

        try:
            return Model.create(vals)
        except Exception as exc:
            _logger.exception("Could not create %s from partner %s", model_name, partner.id)
            raise UserError(_(
                "Não foi possível criar o cadastro auxiliar %(model)s para %(partner)s.\n\n"
                "Esse model possui campos obrigatórios adicionais. Complete/crie manualmente o cadastro e tente novamente.\n\n"
                "Erro técnico: %(error)s"
            ) % {
                "model": model_name,
                "partner": partner.display_name,
                "error": exc,
            })

    def _contract_relation_value_from_partner(self, field, partner, role_label=False):
        """Convert a res.partner into the correct comodel expected by property.contract."""
        if not partner or field.type != "many2one":
            return False
        comodel = field.comodel_name
        if comodel == "res.partner":
            return partner.id
        if comodel in self.env.registry.models:
            rec = self._find_or_create_record_from_partner(comodel, partner, role_label=role_label)
            return rec.id if rec else False
        return False

    def _put_first_existing_contract_party_field(self, Contract, vals, field_names, partner, role_label=False):
        """Put party value respecting the actual Many2one comodel.

        Example: tenant_id may point to property.tenant, while party2_id may
        point directly to res.partner. This avoids FK errors like putting a
        res.partner id into property_contract.tenant_id.
        """
        if not partner:
            return False
        for field_name in field_names:
            if field_name not in Contract._fields:
                continue
            field = Contract._fields[field_name]
            value = self._contract_relation_value_from_partner(field, partner, role_label=role_label)
            if value:
                vals[field_name] = value
                return True
        return False

    def _prepare_contract_values_from_history(self):
        """Prepare property.contract values using only fields that exist in the target model.

        The property.contract model varies between installations. This method is intentionally
        defensive so the OCR history module can create a contract in different databases without
        crashing on missing custom fields.
        """
        self.ensure_one()
        Contract = self.env["property.contract"]
        vals = {}

        contract_name = self.contract_filename or self.name or _("Contrato OCR")
        self._put_first_existing_contract_field(Contract, vals, ["name", "reference"], contract_name)
        self._put_first_existing_contract_field(Contract, vals, ["company_id"], self.company_id.id if self.company_id else False)
        self._put_first_existing_contract_field(Contract, vals, ["asset_id", "property_id", "real_estate_asset_id"], self.asset_id.id if self.asset_id else False)
        self._put_first_existing_contract_field(Contract, vals, ["contract_type", "type", "rent_type"], self.contract_type or "rental")

        # Common dates/value aliases used in custom real-estate modules.
        # IMPORTANT: fill all aliases, not only the first one. In your current
        # database property.contract has start_date as NOT NULL, while date_start
        # also exists. Filling only date_start caused the SQL error reported by Odoo.
        contract_start = self._history_start_date_for_contract()
        contract_end = self._history_end_date_for_contract()
        self._put_all_existing_contract_fields(Contract, vals, ["start_date", "date_start", "initial_date", "contract_start_date"], contract_start)
        self._put_all_existing_contract_fields(Contract, vals, ["end_date", "date_end", "final_date", "contract_end_date"], contract_end)
        self._put_all_existing_contract_fields(Contract, vals, ["sign_date", "signature_date", "date_signature"], self.sign_date or contract_start)
        self._put_all_existing_contract_fields(Contract, vals, ["monthly_amount", "rent_value", "monthly_rent", "amount", "rental_value"], self.monthly_amount)
        self._put_all_existing_contract_fields(Contract, vals, ["total_value", "sale_price", "contract_value"], self.total_value)
        self._put_all_existing_contract_fields(Contract, vals, ["deposit_value", "security_deposit", "guarantee_amount"], self.deposit_value)
        self._put_all_existing_contract_fields(Contract, vals, ["currency_id"], self.currency_id.id if self.currency_id else False)

        # Parties: create/fetch partners, then map to common custom field aliases if present.
        party1 = self._partner_from_extracted_party(self.party1_name, self.party1_vat)
        party2 = self._partner_from_extracted_party(self.party2_name, self.party2_vat)
        if party1:
            self._put_first_existing_contract_party_field(
                Contract, vals,
                ["landlord_id", "lessor_id", "owner_id", "party1_id", "partner_id"],
                party1,
                role_label=_("Locadora"),
            )
        if party2:
            self._put_first_existing_contract_party_field(
                Contract, vals,
                ["tenant_id", "lessee_id", "renter_id", "party2_id"],
                party2,
                role_label=_("Locatária"),
            )

        # Keep extracted text and address in note/description fields when available.
        summary_parts = [
            _("Criado a partir do histórico OCR: %s") % (self.name or "-"),
            _("Arquivo: %s") % (self.contract_filename or "-"),
            _("Locadora/Parte 1: %s - %s") % (self.party1_name or "-", self.party1_vat or "-"),
            _("Locatária/Parte 2: %s - %s") % (self.party2_name or "-", self.party2_vat or "-"),
            _("Imóvel extraído: %s") % (self.property_description or self.address or "-"),
        ]
        summary = "\n".join(summary_parts)
        self._put_first_existing_contract_field(Contract, vals, ["notes", "note", "description", "internal_notes", "observations"], summary)
        self._put_first_existing_contract_field(Contract, vals, ["ocr_history_id", "contract_history_id", "source_history_id"], self.id)
        self._put_first_existing_contract_field(Contract, vals, ["original_filename"], self.contract_filename)

        return vals

    def action_create_contract_from_history(self):
        """Create a property.contract from validated OCR data. Separate from asset matching."""
        for history in self:
            if history.contract_id:
                raise UserError(_("Este histórico já possui um contrato associado: %s") % history.contract_id.display_name)
            if history.state not in ("extracted", "reviewed", "approved", "synced"):
                raise UserError(_("Extraia e revise os dados antes de criar o contrato."))
            if not history.asset_id:
                raise UserError(_("Associe um imóvel antes de criar o contrato."))
            if "property.contract" not in history.env.registry.models:
                raise UserError(_("O model property.contract não está instalado nesta base."))

            Contract = history.env["property.contract"].sudo()
            vals = history._prepare_contract_values_from_history()

            # Final safety for required fields that are known to exist in your
            # property.contract deployment. These assignments are harmless if the
            # fields do not exist because vals is checked against _fields.
            if "start_date" in Contract._fields and not vals.get("start_date"):
                vals["start_date"] = history._history_start_date_for_contract()
            if "end_date" in Contract._fields and not vals.get("end_date"):
                vals["end_date"] = history._history_end_date_for_contract()

            missing_required = []
            for field_name, field in Contract._fields.items():
                if field.required and not vals.get(field_name) and field_name not in ("id", "display_name", "create_uid", "create_date", "write_uid", "write_date"):
                    # Odoo/default_get may fill many required fields automatically;
                    # report only the common business fields that block SQL/create.
                    if field_name in ("start_date", "end_date", "asset_id", "property_id", "tenant_id", "partner_id", "company_id"):
                        missing_required.append(field.string or field_name)
            if missing_required:
                raise UserError(_("Não foi possível criar o contrato. Campos obrigatórios sem valor: %s") % ", ".join(missing_required))

            try:
                contract = Contract.create(vals)
            except Exception as exc:
                _logger.exception("Could not create property.contract from OCR history %s", history.id)
                raise UserError(_(
                    "Não foi possível criar o contrato automaticamente.\n\n"
                    "Provável causa: o model property.contract possui campos obrigatórios específicos "
                    "que não existem no histórico OCR.\n\nErro técnico: %s"
                ) % exc)

            history.write({"contract_id": contract.id})
            history.message_post(
                body=Markup(_(
                    "<b>Contrato criado a partir do OCR</b><br/>Contrato: <b>%s</b><br/>Imóvel: <b>%s</b>"
                )) % (contract.display_name, history.asset_id.display_name)
            )

            return {
                "type": "ir.actions.act_window",
                "name": _("Contrato Criado"),
                "res_model": "property.contract",
                "res_id": contract.id,
                "view_mode": "form",
                "target": "current",
            }
        return False

    def action_confirm_asset_association(self):
        """Confirm the manually selected asset without creating/syncing a contract."""
        for history in self:
            if not history.asset_id:
                raise UserError(_("Selecione um imóvel antes de confirmar a associação."))
            history.message_post(body=_("Imóvel associado manualmente ao histórico: %s") % history.asset_id.display_name)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Imóvel associado"),
                "message": _("O imóvel foi associado ao histórico. A criação do contrato é opcional."),
                "type": "success",
                "sticky": False,
            },
        }

    def action_sync_to_asset(self):
        """Sync extracted data to property.asset."""
        for history in self:
            if not history.sync_to_asset:
                raise UserError(
                    _("Sincronização desabilitada para este contrato. Habilite a opção antes de sincronizar.")
                )

            if not history.asset_id:
                # Try to find asset automatically
                try:
                    history.action_find_asset()
                except Exception:
                    raise UserError(
                        _(
                            "Nenhum imóvel especificado. Selecione ou deixe encontrar automaticamente."
                        )
                    )

            asset = history.asset_id
            if not asset:
                raise UserError(_("Imóvel não disponível para sincronização."))

            # Build updates from accepted lines
            updates = {}
            sync_details = []

            for line in history.line_ids.filtered(lambda l: l.accepted):
                field = line.field_name
                value = line.parsed_value

                if field == "address" and value:
                    if self._set_update_if_field_exists(asset, updates, "address", value) or self._set_update_if_field_exists(asset, updates, "street", value):
                        sync_details.append(f"• Endereço: {value}")
                elif field == "neighborhood" and value:
                    if (
                        self._set_update_if_field_exists(asset, updates, "neighborhood", value)
                        or self._set_update_if_field_exists(asset, updates, "district", value)
                        or self._set_update_if_field_exists(asset, updates, "street2", value)
                    ):
                        sync_details.append(f"• Bairro: {value}")
                elif field == "city" and value:
                    if self._set_update_if_field_exists(asset, updates, "city", value):
                        sync_details.append(f"• Cidade: {value}")
                elif field == "zip_code" and value:
                    if self._set_update_if_field_exists(asset, updates, "zip_code", value) or self._set_update_if_field_exists(asset, updates, "zip", value):
                        sync_details.append(f"• CEP: {value}")
                elif field == "monthly_amount":
                    try:
                        monthly_val = float(value or 0)
                        if monthly_val > 0 and self._set_update_if_field_exists(asset, updates, "monthly_rent", monthly_val):
                            sync_details.append(f"• Aluguel Mensal: R$ {monthly_val:,.2f}")
                    except Exception:
                        pass
                elif field == "total_value":
                    try:
                        total_val = float(value or 0)
                        if total_val > 0 and self._set_update_if_field_exists(asset, updates, "sale_price", total_val):
                            sync_details.append(f"• Preço: R$ {total_val:,.2f}")
                    except Exception:
                        pass

            if updates:
                asset.write(updates)

                # Mark sync tracking
                history.write(
                    {
                        "synced_to_asset_id": asset.id,
                        "sync_timestamp": fields.Datetime.now(),
                        "sync_log": "\n".join(sync_details) if sync_details else "Sincronização realizada.",
                        "state": "synced",
                    }
                )

                # Mark older contracts as superseded
                older_domain = [
                    ("asset_id", "=", asset.id),
                    ("state", "in", ["synced"]),
                    ("id", "!=", history.id),
                ]
                if history.sign_date:
                    older_domain.append(("sign_date", "<", history.sign_date))
                older = self.search(older_domain)
                for old in older:
                    old.write({"superseded_by_id": history.id})

                history.message_post(
                    body=Markup(
                        "<b>✓ Sincronização Concluída</b><br/>"
                        "Imóvel: <b>%s</b><br/>"
                        "%s"
                    )
                    % (asset.display_name, "<br/>".join(sync_details))
                )

            else:
                raise UserError(
                    _(
                        "Nenhum campo aceito para sincronizar. Revise os campos extraídos."
                    )
                )

    def action_reject(self):
        """Reject and reset to draft."""
        self.write({"state": "rejected"})
        for history in self:
            history.message_post(
                body=_("Contrato rejeitado. Retornado para rascunho.")
            )


    def action_view_contract(self):
        """Open the associated property.contract."""
        self.ensure_one()
        if not self.contract_id:
            raise UserError(_("Nenhum contrato associado a este histórico."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Contrato Associado"),
            "res_model": "property.contract",
            "res_id": self.contract_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_view_lines(self):
        """Open view with extracted field lines."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Campos Extraídos",
            "res_model": "property.contract.history.line",
            "view_mode": "list,form",
            "domain": [("history_id", "=", self.id)],
            "context": {"default_history_id": self.id},
            "target": "current",
        }

    def action_view_history(self):
        """Open view with superseded contracts."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Versões Anteriores",
            "res_model": "property.contract.history",
            "view_mode": "list,form",
            "domain": [("superseded_by_id", "=", self.id)],
            "target": "current",
        }
