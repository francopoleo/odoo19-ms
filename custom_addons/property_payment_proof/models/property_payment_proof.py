# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html_escape
from markupsafe import Markup
import base64
import io
import json
import re
from datetime import datetime, date
from difflib import SequenceMatcher

from ..parsers import parser_registry


def normalize_text(value):
    value = (value or "").strip().lower()
    value = re.sub(r"[\W_]+", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def normalize_doc(value):
    return re.sub(r"\D+", "", value or "")


class PropertyPaymentProof(models.Model):
    _name = "property.payment.proof"
    _description = "Comprovante de Pagamento de Aluguel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"

    name = fields.Char("Referência", readonly=True, copy=False, default="New")
    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.company, required=True)
    proof_file = fields.Binary("Arquivo do Comprovante", attachment=True)
    proof_filename = fields.Char(string="Nome do Arquivo")
    mimetype = fields.Char("MIME Type")
    raw_text = fields.Text("Texto extraído / OCR")
    extraction_log = fields.Text("Log de Extração", readonly=True)

    payment_method = fields.Selection([
        ("pix", "PIX"),
        ("transfer", "TED/DOC/Transferência"),
        ("boleto", "Boleto"),
        ("deposit", "Depósito"),
        ("other", "Outro"),
    ], string="Tipo de Pagamento")
    payment_date = fields.Date("Data da Transação")
    debit_date = fields.Date("Data de Débito", help="Data efetiva do débito bancário. Usada para comparar com o vencimento da parcela.")
    amount = fields.Monetary("Valor Identificado", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    payer_name = fields.Char("Pagador Identificado")
    payer_vat = fields.Char("CPF/CNPJ do Pagador", help="Pode estar mascarado (ex: ***.368.878-**). Partial match é aplicado no score.")
    pix_key = fields.Char("Chave PIX do Pagador", help="Telefone, e-mail, CPF ou chave aleatória identificada no comprovante.")
    normalized_payer_vat = fields.Char("CPF/CNPJ Normalizado", compute="_compute_normalized_payer_vat", store=True, index=True)
    is_pdf = fields.Boolean("É PDF", compute="_compute_is_pdf")
    receiver_name = fields.Char("Recebedor Identificado")
    transaction_id = fields.Char("ID/Autenticação/End-to-End", index=True)
    bank_name = fields.Char("Banco/Instituição")

    contract_id = fields.Many2one("property.contract", string="Contrato Sugerido", tracking=True)
    rent_id = fields.Many2one("property.rent", string="Parcela Conciliada", tracking=True)
    payment_id = fields.Many2one("property.rent.payment", string="Recebimento Gerado", readonly=True, copy=False)
    match_line_ids = fields.One2many("property.payment.proof.match", "proof_id", string="Sugestões de Conciliação")
    suggested_match_id = fields.Many2one("property.payment.proof.match", string="Melhor Sugestão", readonly=True)
    confidence_score = fields.Float("Score", readonly=True)
    matched_payload = fields.Text("JSON da Extração", readonly=True)

    is_late_payment = fields.Boolean("Pagamento em Atraso", compute="_compute_late_info", store=True)
    days_late = fields.Integer("Dias de Atraso", compute="_compute_late_info", store=True)
    late_handling = fields.Selection([
        ("none", "Não Definido"),
        ("request_fee", "Solicitar Comprovante de Juros/Mora"),
        ("defer", "Lançar Diferença no Próximo Mês"),
        ("waive", "Dispensar Juros este Mês"),
    ], string="Tratamento do Atraso", default="none", tracking=True)
    calculated_fine = fields.Monetary("Multa Calculada", currency_field="currency_id", readonly=True)
    calculated_interest = fields.Monetary("Juros Calculados", currency_field="currency_id", readonly=True)

    proof_type = fields.Selection([
        ("normal", "Comprovante de Pagamento"),
        ("manual", "Pagamento Manual"),
        ("late_fee", "Juros/Mora"),
    ], string="Tipo", default="normal", required=True, tracking=True)
    late_fee_source_id = fields.Many2one(
        "property.payment.proof",
        string="Comprovante Original",
        readonly=True,
        ondelete="set null",
    )
    late_fee_proof_ids = fields.One2many(
        "property.payment.proof",
        "late_fee_source_id",
        string="Comprovantes de Juros/Mora",
        readonly=True,
    )

    state = fields.Selection([
        ("draft", "Rascunho"),
        ("extracted", "Extraído"),
        ("matched", "Sugestão Encontrada"),
        ("review", "Revisão Manual"),
        ("approved", "Aprovado"),
        ("reconciled", "Conciliado"),
        ("rejected", "Rejeitado"),
        ("failed", "Falha no OCR"),
    ], string="Status", default="draft", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].sudo().next_by_code("property.payment.proof") or "COMP-PGTO"
        return super().create(vals_list)

    @api.depends("proof_filename")
    def _compute_is_pdf(self):
        for proof in self:
            proof.is_pdf = (proof.proof_filename or "").lower().endswith(".pdf")

    @api.depends("payer_vat")
    def _compute_normalized_payer_vat(self):
        for proof in self:
            proof.normalized_payer_vat = normalize_doc(proof.payer_vat)

    @api.depends("payment_date", "debit_date", "rent_id", "rent_id.due_date")
    def _compute_late_info(self):
        for proof in self:
            due = proof.rent_id.due_date if proof.rent_id else False
            ref = proof.debit_date or proof.payment_date
            if ref and due and ref > due:
                proof.is_late_payment = True
                proof.days_late = (ref - due).days
            else:
                proof.is_late_payment = False
                proof.days_late = 0

    def _extract_pdf_text(self, data):
        try:
            from pypdf import PdfReader
        except Exception:
            try:
                from PyPDF2 import PdfReader
            except Exception as exc:
                raise UserError(_(
                    "Não encontrei biblioteca de leitura de PDF. Instale 'pypdf' no ambiente Python ou cole o texto do comprovante no campo Texto extraído / OCR. Erro: %s"
                ) % exc)
        reader = PdfReader(io.BytesIO(data))
        chunks = []
        for page in reader.pages:
            try:
                chunks.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(chunks).strip()

    def _extract_image_text(self, data):
        try:
            from PIL import Image
            import pytesseract
        except Exception as exc:
            raise UserError(_(
                "Para OCR de imagem/scanner, instale Pillow + pytesseract + tesseract-ocr no servidor. Alternativa: cole o texto do comprovante manualmente. Erro: %s"
            ) % exc)
        image = Image.open(io.BytesIO(data))
        return pytesseract.image_to_string(image, lang="por+eng").strip()

    def _extract_text_from_file(self):
        self.ensure_one()
        if not self.proof_file:
            return self.raw_text or ""
        data = base64.b64decode(self.proof_file)
        filename = (self.proof_filename or "").lower()
        if filename.endswith(".pdf"):
            return self._extract_pdf_text(data)
        if filename.endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")):
            return self._extract_image_text(data)
        return self.raw_text or ""

    def _parse_text(self, text):
        parser = parser_registry.find(text)
        return parser.parse(text)

    def action_extract(self):
        for proof in self:
            try:
                text = proof._extract_text_from_file()
                if not text:
                    raise UserError(_("Nenhum texto foi extraído. Para PDF escaneado/imagem, instale OCR ou cole o texto manualmente."))
                parsed = proof._parse_text(text)
                proof.with_context(tracking_disable=True).write({
                    "raw_text": text,
                    "payment_method": parsed["payment_method"],
                    "payment_date": parsed["payment_date"],
                    "debit_date": parsed.get("debit_date") or False,
                    "amount": parsed["amount"],
                    "payer_name": parsed["payer_name"],
                    "payer_vat": parsed["payer_vat"],
                    "pix_key": parsed.get("pix_key") or False,
                    "receiver_name": parsed["receiver_name"],
                    "transaction_id": parsed["transaction_id"],
                    "bank_name": parsed["bank_name"],
                    "matched_payload": json.dumps(parsed, default=str, ensure_ascii=False, indent=2),
                    "state": "extracted",
                    "extraction_log": _("Extração concluída."),
                })
                currency = proof.currency_id
                amount_fmt = f"{currency.symbol} {parsed['amount']:,.2f}" if parsed.get("amount") else "-"
                debit_str = str(parsed.get("debit_date") or "")
                proof.message_post(body=Markup(
                    "<b>OCR extraído</b> <small>(parser: {parser})</small><br/>"
                    "<b>Valor:</b> {amount}<br/>"
                    "<b>Pagador:</b> {payer}<br/>"
                    "<b>Data transação:</b> {date}<br/>"
                    "<b>Data débito:</b> {debit}<br/>"
                    "<b>Tipo:</b> {method}<br/>"
                    "<b>ID/E2E:</b> {txid}"
                ).format(
                    parser=parsed.get("parser_name") or "genérico",
                    amount=amount_fmt,
                    payer=parsed.get("payer_name") or "-",
                    date=str(parsed.get("payment_date") or "-"),
                    debit=debit_str or "(não identificada — usando data da transação)",
                    method=dict(proof._fields["payment_method"].selection).get(parsed.get("payment_method"), "-"),
                    txid=parsed.get("transaction_id") or "-",
                ))
                proof.action_match(post_message=True)
            except Exception as exc:
                proof.write({"state": "failed", "extraction_log": str(exc)})
                raise

    def _rent_display_amount(self, rent):
        """Valor para exibição na lista de sugestões: amount_due total (com multa/juros)."""
        return rent.amount_due or rent.amount or 0.0

    def _rent_best_amount_diff(self, rent):
        """
        Menor diferença entre o valor do comprovante e a parcela.
        Compara contra: residual_amount (saldo restante), amount_due (total com multa) e amount (base).
        Isso garante que pagamentos do valor base batam mesmo quando a parcela tem multa ou pagamento parcial.
        """
        if not self.amount:
            return None
        candidates = [rent.amount or 0.0, rent.amount_due or 0.0]
        if "residual_amount" in rent._fields and rent.residual_amount:
            candidates.append(rent.residual_amount)
        diffs = [abs(self.amount - c) for c in candidates if c > 0]
        return min(diffs) if diffs else None

    def _score_rent(self, rent):
        """
        Score de 0–100 para a correspondência entre este comprovante e uma parcela.

        Componentes (sem acúmulo entre categorias):
          Valor      : até 40 pts
          Data       : até 20 pts  (usa debit_date quando disponível)
          Identidade : até 40 pts  (melhor entre CPF/nome locatário ou pagador autorizado)
        Penalidade: -100 pts se transaction_id já conciliado em outro comprovante.
        """
        self.ensure_one()
        score = 0.0
        reasons = []
        amount_due = self._rent_display_amount(rent)

        # ── Valor (max 40) ────────────────────────────────────────────────
        diff = self._rent_best_amount_diff(rent)
        if diff is not None:
            ref_for_pct = amount_due or 1.0
            if diff <= 0.05:
                score += 40
                reasons.append(_("Valor exato (+40)."))
            elif diff <= max(ref_for_pct * 0.02, 10.0):
                score += 25
                reasons.append(_("Valor próximo (+25)."))

        # ── Data (max 20) — usa data de débito se disponível ──────────────
        ref_date = self.debit_date or self.payment_date
        if ref_date and rent.due_date:
            delta_days = (ref_date - rent.due_date).days
            delta = abs(delta_days)
            date_label = "débito" if self.debit_date else "transação"
            if delta <= 2:
                score += 20
                reasons.append(_("Data de %s coincide com vencimento (+20).") % date_label)
            elif delta <= 7:
                score += 15
                reasons.append(_("Data de %s até 7 dias do vencimento (+15).") % date_label)
            elif delta <= 15:
                score += 10
                reasons.append(_("Data de %s até 15 dias do vencimento (+10).") % date_label)
            elif delta <= 31:
                score += 5
                reasons.append(_("Data de %s no mesmo ciclo mensal (+5).") % date_label)
            else:
                reasons.append(_("Data de %s distante do vencimento (+0).") % date_label)
            if delta_days > 0:
                reasons.append(_(
                    "⚠️ PAGAMENTO EM ATRASO: %d dia(s) após o vencimento (%s)."
                ) % (delta_days, rent.due_date.strftime("%d/%m/%Y")))

        # ── Identidade do pagador (max 40, sem acúmulo) ───────────────────
        payer = normalize_text(self.payer_name)
        partner_name = normalize_text(rent.partner_id.name)
        doc = normalize_doc(self.payer_vat)      # dígitos visíveis (masked: ex "368878", full: "12336887800")
        identity = 0
        identity_reason = ""

        # CPF/CNPJ completo do locatário (11 ou 14 dígitos)
        if doc and len(doc) >= 11 and normalize_doc(rent.partner_id.vat) == doc:
            identity = 40
            identity_reason = _("CPF/CNPJ exato bate com o locatário (+40).")

        # CPF/CNPJ completo de pagador autorizado
        if identity < 40 and doc and len(doc) >= 11:
            for pl in rent.contract_id.authorized_payer_ids.filtered(lambda p: p.active):
                if pl.normalized_vat == doc:
                    identity = 40
                    identity_reason = _("CPF/CNPJ exato consta como pagador autorizado (+40).")
                    break

        # CPF mascarado — partial match (dígitos visíveis ≥ 4 contidos no CPF do locatário/autorizado)
        if identity < 35 and doc and 4 <= len(doc) < 11:
            tenant_doc = normalize_doc(rent.partner_id.vat)
            if tenant_doc and doc in tenant_doc:
                identity = max(identity, 25)
                identity_reason = _("CPF parcialmente identificado no locatário (+25).")
            if identity < 25:
                for pl in rent.contract_id.authorized_payer_ids.filtered(lambda p: p.active):
                    if pl.normalized_vat and doc in pl.normalized_vat:
                        identity = max(identity, 25)
                        identity_reason = _("CPF parcialmente identificado em pagador autorizado (+25).")
                        break

        # Chave PIX — telefone, e-mail ou chave aleatória
        if identity < 38 and self.pix_key:
            pix_norm = re.sub(r"\D", "", self.pix_key)  # só dígitos para telefone/CPF
            pix_lower = self.pix_key.strip().lower()
            for pl in rent.contract_id.authorized_payer_ids.filtered(lambda p: p.active and p.pix_key):
                auth_pix_norm = re.sub(r"\D", "", pl.pix_key)
                auth_pix_lower = pl.pix_key.strip().lower()
                if (pix_norm and auth_pix_norm and pix_norm == auth_pix_norm) or \
                   (pix_lower and auth_pix_lower and pix_lower == auth_pix_lower):
                    identity = max(identity, 38)
                    identity_reason = _("Chave PIX consta como pagador autorizado (+38).")
                    break
            # Chave PIX bate com dados do locatário (telefone/email)
            if identity < 35:
                partner = rent.partner_id
                partner_phones = {re.sub(r"\D", "", p) for p in [partner.phone or "", partner.mobile or ""] if p}
                partner_email = (partner.email or "").strip().lower()
                if (pix_norm and pix_norm in partner_phones) or (pix_lower and pix_lower == partner_email):
                    identity = max(identity, 35)
                    identity_reason = _("Chave PIX bate com telefone/e-mail do locatário (+35).")

        # Nome de pagador autorizado
        if identity < 35 and payer:
            for pl in rent.contract_id.authorized_payer_ids.filtered(lambda p: p.active):
                auth = normalize_text(pl.name)
                if auth:
                    ratio = SequenceMatcher(None, payer, auth).ratio()
                    if ratio >= 0.88 or payer in auth or auth in payer:
                        identity = max(identity, 33)
                        identity_reason = _("Nome consta como pagador autorizado (+33).")
                        break

        # Nome do próprio locatário
        if identity < 30 and payer and partner_name:
            ratio = SequenceMatcher(None, payer, partner_name).ratio()
            if ratio >= 0.90 or payer in partner_name or partner_name in payer:
                identity = max(identity, 30)
                identity_reason = _("Nome bate com o locatário (+30).")
            elif ratio >= 0.70:
                identity = max(identity, 15)
                identity_reason = _("Nome parecido com o locatário (+15).")

        if identity_reason:
            reasons.append(identity_reason)
        score += identity

        # ── Penalidade de duplicata ───────────────────────────────────────
        if self.transaction_id:
            duplicate = self.search_count([
                ("id", "!=", self.id),
                ("transaction_id", "=", self.transaction_id),
                ("state", "in", ["approved", "reconciled"]),
            ])
            if duplicate:
                score = 0.0
                reasons.append(_("⚠️ ID de transação já conciliado em outro comprovante (score zerado)."))

        return min(max(score, 0.0), 100.0), "\n".join(reasons), amount_due

    def action_match(self, post_message=True):
        Match = self.env["property.payment.proof.match"]
        Rent = self.env["property.rent"]
        for proof in self:
            proof.match_line_ids.unlink()
            domain = [("status", "in", ["open", "late", "partial"])]
            if proof.company_id:
                domain.append(("company_id", "=", proof.company_id.id))
            # Se já há contrato definido, busca primeiro só as parcelas dele
            if proof.contract_id:
                contract_domain = domain + [("contract_id", "=", proof.contract_id.id)]
                candidates = Rent.search(contract_domain, limit=200)
                if not candidates:
                    candidates = Rent.search(domain, limit=200)
            else:
                candidates = Rent.search(domain, limit=200)
            best = False
            for rent in candidates:
                score, reasons, amount_due = proof._score_rent(rent)
                if score < 25:
                    continue
                line = Match.create({
                    "proof_id": proof.id,
                    "rent_id": rent.id,
                    "contract_id": rent.contract_id.id,
                    "partner_id": rent.partner_id.id,
                    "amount_due": proof._rent_display_amount(rent),
                    "score": score,
                    "reason": reasons,
                })
                if not best or line.score > best.score:
                    best = line
            vals = {"suggested_match_id": best.id if best else False, "confidence_score": best.score if best else 0.0}
            if best and best.score >= 80:
                vals.update({"rent_id": best.rent_id.id, "contract_id": best.contract_id.id, "state": "matched"})
            elif best:
                vals.update({"rent_id": best.rent_id.id, "contract_id": best.contract_id.id, "state": "review"})
            else:
                vals.update({"state": "review"})
            proof.with_context(tracking_disable=True).write(vals)
            # Força recompute de is_late_payment após setar rent_id
            proof._compute_late_info()
            if post_message:
                if best:
                    proof.message_post(body=Markup(
                        "<b>Conciliação automática</b><br/>"
                        "<b>Contrato:</b> {contract}<br/>"
                        "<b>Parcela:</b> {rent}<br/>"
                        "<b>Score:</b> {score:.0f}<br/>"
                        "<b>Status:</b> {state}"
                    ).format(
                        contract=best.contract_id.display_name or "-",
                        rent=best.rent_id.display_name or "-",
                        score=best.score,
                        state=dict(proof._fields["state"].selection).get(vals["state"], vals["state"]),
                    ))
                else:
                    proof.message_post(body=Markup("<b>Conciliação automática:</b> nenhuma parcela correspondente encontrada. Revisão manual necessária."))
            # Aviso automático de atraso após vincular parcela
            ref_date = proof.debit_date or proof.payment_date
            if best and ref_date and best.rent_id.due_date:
                if ref_date > best.rent_id.due_date:
                    days_late = (ref_date - best.rent_id.due_date).days
                    proof.message_post(body=Markup(
                        "<b>⚠️ Atenção: Pagamento Recebido em Atraso</b><br/>"
                        "Vencimento: <b>{due}</b> | Data de débito: <b>{pay}</b> | "
                        "Atraso: <b>{days} dia(s)</b><br/>"
                        "Use os botões no topo para definir o tratamento: "
                        "solicitar juros/mora, diferir para o próximo mês ou dispensar."
                    ).format(
                        due=best.rent_id.due_date.strftime("%d/%m/%Y"),
                        pay=ref_date.strftime("%d/%m/%Y"),
                        days=days_late,
                    ))

    def action_use_match(self):
        self.ensure_one()
        if not self.suggested_match_id:
            raise UserError(_("Não há sugestão selecionada."))
        self.write({
            "rent_id": self.suggested_match_id.rent_id.id,
            "contract_id": self.suggested_match_id.contract_id.id,
            "state": "matched",
        })

    def action_approve_and_reconcile(self):
        for proof in self:
            if not proof.rent_id:
                raise UserError(_("Selecione uma parcela para conciliar."))
            if not proof.amount or proof.amount <= 0:
                raise UserError(_("Informe o valor do comprovante."))
            if not proof.payment_date:
                raise UserError(_("Informe a data de pagamento."))
            rent = proof.rent_id
            rent.write({
                "amount_paid": proof.amount,
                "payment_date": proof.payment_date,
                "payment_method": proof.payment_method if proof.payment_method in dict(rent._fields["payment_method"].selection) else False,
                "payment_notes": _("Pagamento conciliado pelo comprovante %s. Pagador: %s. Transação: %s") % (
                    proof.name, proof.payer_name or "-", proof.transaction_id or "-"
                ),
            })
            action = rent.action_register_payment()
            payment = self.env["property.rent.payment"].search([
                ("rent_id", "=", rent.id),
                ("payment_date", "=", proof.payment_date),
                ("amount", "=", proof.amount),
            ], order="id desc", limit=1)
            proof.write({"payment_id": payment.id, "state": "reconciled"})
            proof.message_post(body=_("Comprovante conciliado com a parcela %s.") % html_escape(rent.display_name))
            if action:
                return action

    def action_print_receipt(self):
        """Reimprimir o recibo da parcela já conciliada."""
        self.ensure_one()
        if not self.rent_id:
            raise UserError(_("Nenhuma parcela conciliada."))
        return self.rent_id.action_print_receipt()

    def action_reject(self):
        self.write({"state": "rejected"})

    def _calculate_late_fees(self):
        """Returns (penalty, interest, base_amount, effective_days_late) using contract rates."""
        self.ensure_one()
        from odoo.tools.float_utils import float_round
        contract = self.contract_id or (self.rent_id.contract_id if self.rent_id else False)
        if not contract:
            raise UserError(_("Contrato não identificado para calcular encargos."))
        base_amount = self.amount or 0.0
        grace = contract.late_grace_days or 0
        days_late = max(self.days_late - grace, 0)
        if days_late <= 0:
            return 0.0, 0.0, base_amount, 0
        rounding = self.currency_id.rounding
        penalty = float_round(
            base_amount * (contract.late_fee_percent or 0.0) / 100.0,
            precision_rounding=rounding,
        )
        interest = float_round(
            base_amount * ((contract.late_interest_percent_month or 0.0) / 100.0) / 30.0 * days_late,
            precision_rounding=rounding,
        )
        return penalty, interest, base_amount, days_late

    def action_request_late_fee(self):
        """Calcula multa/juros, cria comprovante de late_fee e posta resumo no chatter."""
        for proof in self:
            if not proof.is_late_payment:
                raise UserError(_("O pagamento não está em atraso."))
            penalty, interest, base_amount, days_late_eff = proof._calculate_late_fees()
            total_fee = penalty + interest
            rent = proof.rent_id
            contract = proof.contract_id or (rent.contract_id if rent else False)
            due_str = rent.due_date.strftime("%d/%m/%Y") if rent and rent.due_date else "-"
            pay_str = proof.payment_date.strftime("%d/%m/%Y") if proof.payment_date else "-"
            proof.write({
                "late_handling": "request_fee",
                "calculated_fine": penalty,
                "calculated_interest": interest,
            })
            late_fee_proof = self.create({
                "proof_type": "late_fee",
                "late_fee_source_id": proof.id,
                "contract_id": proof.contract_id.id if proof.contract_id else False,
                "rent_id": proof.rent_id.id if proof.rent_id else False,
                "amount": total_fee,
                "state": "draft",
                "extraction_log": _(
                    "Comprovante de juros/mora gerado automaticamente.\n"
                    "Multa: R$ %.2f | Juros: R$ %.2f | Total: R$ %.2f"
                ) % (penalty, interest, total_fee),
            })
            proof.message_post(body=Markup(
                "<b>⚠️ Pagamento em Atraso — Comprovante de Juros/Mora Criado</b><br/>"
                "Pagamento em: <b>{pay_date}</b> | Vencimento: <b>{due_date}</b> | "
                "Atraso: <b>{days} dia(s)</b><br/><br/>"
                "<b>Encargos calculados:</b><br/>"
                "Base: R$ {base:.2f}<br/>"
                "Multa ({fee_pct:.2f}%): <b>R$ {penalty:.2f}</b><br/>"
                "Juros de mora ({int_pct:.4f}%/mês × {days_eff} dias): <b>R$ {interest:.2f}</b><br/>"
                "Total exigido: <b>R$ {total:.2f}</b><br/><br/>"
                "Comprovante de juros criado: <b>{lname}</b> (aguardando envio pelo locatário)."
            ).format(
                pay_date=pay_str,
                due_date=due_str,
                days=proof.days_late,
                days_eff=days_late_eff,
                base=base_amount,
                fee_pct=contract.late_fee_percent if contract else 0.0,
                penalty=penalty,
                int_pct=contract.late_interest_percent_month if contract else 0.0,
                interest=interest,
                total=total_fee,
                lname=late_fee_proof.name,
            ))
            # Atividade automática: aguardando comprovante do locatário
            responsible = (contract.user_id if contract and contract.user_id else False) or self.env.user
            late_fee_proof.activity_schedule(
                "mail.mail_activity_data_todo",
                date_deadline=fields.Date.today(),
                summary=_("Aguardando comprovante de juros/mora — %s") % proof.name,
                note=_(
                    "Encargo calculado: R$ %.2f (multa R$ %.2f + juros R$ %.2f).\n"
                    "Locatário: %s | Parcela: %s\n"
                    "Atraso de %d dia(s) — vencimento %s."
                ) % (
                    total_fee, penalty, interest,
                    rent.partner_id.name if rent else "-",
                    rent.display_name if rent else "-",
                    proof.days_late,
                    due_str,
                ),
                user_id=responsible.id,
            )

    def action_defer_to_next_month(self):
        """Calcula encargos e lança linhas de multa/juros na próxima parcela do contrato."""
        for proof in self:
            if not proof.is_late_payment:
                raise UserError(_("O pagamento não está em atraso."))
            penalty, interest, base_amount, days_late_eff = proof._calculate_late_fees()
            rent = proof.rent_id
            contract = proof.contract_id or (rent.contract_id if rent else False)
            due_str = rent.due_date.strftime("%d/%m/%Y") if rent and rent.due_date else "-"
            pay_str = proof.payment_date.strftime("%d/%m/%Y") if proof.payment_date else "-"

            # Find next open rent for this contract
            next_rent = False
            if contract and rent and rent.due_date:
                next_rent = self.env["property.rent"].search([
                    ("contract_id", "=", contract.id),
                    ("status", "in", ["open", "draft"]),
                    ("due_date", ">", rent.due_date),
                ], order="due_date asc", limit=1)

            proof.write({
                "late_handling": "defer",
                "calculated_fine": penalty,
                "calculated_interest": interest,
            })

            # Create rent lines on next rent
            lines_info = []
            if next_rent and (penalty or interest):
                next_rent._ensure_base_rent_line()
                if penalty:
                    self.env["property.rent.line"].create({
                        "rent_id": next_rent.id,
                        "sequence": 80,
                        "charge_type": "penalty",
                        "name": _(
                            "Multa diferida — atraso de %s dia(s) na parcela %s"
                        ) % (proof.days_late, rent.display_name),
                        "amount": penalty,
                        "origin": "manual",
                        "calculation_base": base_amount,
                        "days": days_late_eff,
                        "calculation_note": _(
                            "Diferido do comprovante %s. Base R$ %.2f × %.2f%%."
                        ) % (proof.name, base_amount, contract.late_fee_percent),
                    })
                    lines_info.append(_("Multa: R$ %.2f") % penalty)
                if interest:
                    self.env["property.rent.line"].create({
                        "rent_id": next_rent.id,
                        "sequence": 90,
                        "charge_type": "interest",
                        "name": _(
                            "Juros diferidos — atraso de %s dia(s) na parcela %s"
                        ) % (proof.days_late, rent.display_name),
                        "amount": interest,
                        "origin": "manual",
                        "calculation_base": base_amount,
                        "days": days_late_eff,
                        "calculation_note": _(
                            "Diferido do comprovante %s. Base R$ %.2f × %.4f%%/mês × %s dias."
                        ) % (proof.name, base_amount, contract.late_interest_percent_month, days_late_eff),
                    })
                    lines_info.append(_("Juros: R$ %.2f") % interest)

            if next_rent and lines_info:
                defer_detail = Markup(
                    "Encargos lançados na próxima parcela: <b>{next}</b><br/>{lines}"
                ).format(next=next_rent.display_name, lines=" | ".join(lines_info))
            elif not next_rent:
                defer_detail = Markup(
                    "<span style='color:#dc3545;'>"
                    "Próxima parcela aberta não encontrada — lançamento manual necessário."
                    "</span>"
                )
            else:
                defer_detail = Markup("<span>Nenhum encargo a lançar (valor zero).</span>")

            proof.message_post(body=Markup(
                "<b>📅 Atraso — Encargos Diferidos para a Próxima Parcela</b><br/>"
                "Pagamento em: <b>{pay_date}</b> | Vencimento: <b>{due_date}</b> | "
                "Atraso: <b>{days} dia(s)</b><br/><br/>"
                "<b>Cálculo:</b> Base R$ {base:.2f} | "
                "Multa ({fee_pct:.2f}%): R$ {penalty:.2f} | "
                "Juros ({int_pct:.4f}%/mês × {days_eff} dias): R$ {interest:.2f}<br/>"
                "{defer_detail}"
            ).format(
                pay_date=pay_str,
                due_date=due_str,
                days=proof.days_late,
                days_eff=days_late_eff,
                base=base_amount,
                fee_pct=contract.late_fee_percent if contract else 0.0,
                penalty=penalty,
                int_pct=contract.late_interest_percent_month if contract else 0.0,
                interest=interest,
                defer_detail=defer_detail,
            ))

    def action_waive_late_fee(self):
        """Registra dispensa de juros/mora para este mês."""
        for proof in self:
            proof.write({"late_handling": "waive"})
            proof.message_post(body=Markup(
                "<b>✅ Juros/Mora Dispensados</b><br/>"
                "Decisão registrada: juros e mora referentes ao atraso de "
                "<b>{days} dia(s)</b> foram dispensados para este ciclo."
            ).format(days=proof.days_late))


class PropertyPaymentProofMatch(models.Model):
    _name = "property.payment.proof.match"
    _description = "Sugestão de Conciliação de Comprovante"
    _order = "score desc, id desc"

    proof_id = fields.Many2one("property.payment.proof", string="Comprovante", required=True, ondelete="cascade")
    rent_id = fields.Many2one("property.rent", string="Parcela", required=True, ondelete="cascade")
    contract_id = fields.Many2one("property.contract", string="Contrato")
    partner_id = fields.Many2one("res.partner", string="Locatário")
    due_date = fields.Date("Vencimento", related="rent_id.due_date", store=True)
    due_date_display = fields.Char("Vencimento (DD/MM/AAAA)", compute="_compute_due_date_display")
    amount_due = fields.Monetary("Valor em Aberto", currency_field="currency_id")
    currency_id = fields.Many2one(related="proof_id.currency_id")
    score = fields.Float("Score")
    reason = fields.Text("Motivos")

    @api.depends("due_date")
    def _compute_due_date_display(self):
        for rec in self:
            rec.due_date_display = rec.due_date.strftime("%d/%m/%Y") if rec.due_date else ""

    def action_select_match(self):
        self.ensure_one()
        self.proof_id.write({
            "rent_id": self.rent_id.id,
            "contract_id": self.contract_id.id,
            "suggested_match_id": self.id,
            "confidence_score": self.score,
            "state": "matched",
        })
