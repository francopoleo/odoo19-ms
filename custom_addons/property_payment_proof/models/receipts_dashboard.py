# -*- coding: utf-8 -*-
"""
Dashboard Operacional de Recebimentos.

Painel de trabalho diário para conciliação de comprovantes de aluguel:
- Fila por estado (prioridade → confirmar → revisão → falha → rascunho)
- Qualidade da conciliação automática (score / taxa de auto-match)
- Atrasos pendentes de tratamento
- Trend semanal e breakdown por método/banco
"""
import calendar
from datetime import date, timedelta

from odoo import api, fields, models


class PropertyReceiptsDashboard(models.TransientModel):
    _name = "property.receipts.dashboard"
    _description = "Dashboard Operacional de Recebimentos"

    name = fields.Char(default="Recebimentos")
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
    )

    # ── Hero ───────────────────────────────────────────────────────────────
    proof_ready_count = fields.Integer("Prontos p/ Confirmar", compute="_compute_all")
    proof_ready_amount = fields.Monetary("Valor a Confirmar", compute="_compute_all", currency_field="currency_id")
    proof_reconciled_month_count = fields.Integer("Conciliados no Mês", compute="_compute_all")
    proof_reconciled_month_amount = fields.Monetary("Conciliado no Mês", compute="_compute_all", currency_field="currency_id")
    proof_attention_count = fields.Integer("Requer Atenção", compute="_compute_all")
    proof_total_pending = fields.Integer("Total em Aberto", compute="_compute_all")

    # ── Fila por estado ────────────────────────────────────────────────────
    proof_draft_count = fields.Integer("Rascunho", compute="_compute_all")
    proof_extracted_count = fields.Integer("Extraído", compute="_compute_all")
    proof_matched_count = fields.Integer("Sugestão Automática", compute="_compute_all")
    proof_review_count = fields.Integer("Revisão Manual", compute="_compute_all")
    proof_failed_count = fields.Integer("Falha OCR", compute="_compute_all")
    proof_rejected_count = fields.Integer("Rejeitados", compute="_compute_all")

    proof_draft_amount = fields.Monetary("Valor Rascunho", compute="_compute_all", currency_field="currency_id")
    proof_extracted_amount = fields.Monetary("Valor Extraído", compute="_compute_all", currency_field="currency_id")
    proof_matched_amount = fields.Monetary("Valor Sugestão", compute="_compute_all", currency_field="currency_id")
    proof_review_amount = fields.Monetary("Valor Revisão", compute="_compute_all", currency_field="currency_id")

    # ── Qualidade da conciliação ───────────────────────────────────────────
    auto_match_rate = fields.Float("Taxa Auto-Conciliação (%)", digits=(5, 1), compute="_compute_all")
    avg_score = fields.Float("Score Médio", digits=(5, 1), compute="_compute_all")
    high_score_count = fields.Integer("Score ≥ 80 (automático)", compute="_compute_all")
    mid_score_count = fields.Integer("Score 50–79 (revisão)", compute="_compute_all")
    low_score_count = fields.Integer("Score < 50 (manual)", compute="_compute_all")

    # ── Atrasos ────────────────────────────────────────────────────────────
    proof_late_count = fields.Integer("Comprovantes com Atraso", compute="_compute_all")
    proof_late_no_handling = fields.Integer("Atraso sem Tratamento", compute="_compute_all")
    proof_late_fee_count = fields.Integer("Solicitando Juros/Mora", compute="_compute_all")
    proof_late_defer_count = fields.Integer("Diferido Próx. Mês", compute="_compute_all")
    proof_late_waive_count = fields.Integer("Juros Dispensados", compute="_compute_all")
    proof_late_amount = fields.Monetary("Valor dos Atrasos", compute="_compute_all", currency_field="currency_id")
    proof_late_fee_pending_count = fields.Integer("Comp. de Juros Aguardando Envio", compute="_compute_all")

    # ── Charts ─────────────────────────────────────────────────────────────
    chart_weekly_html = fields.Html("Trend Semanal", compute="_compute_charts", sanitize=False)
    chart_funnel_html = fields.Html("Funil de Conciliação", compute="_compute_charts", sanitize=False)
    chart_method_html = fields.Html("Por Método de Pagamento", compute="_compute_charts", sanitize=False)
    chart_score_html = fields.Html("Distribuição de Score", compute="_compute_charts", sanitize=False)

    # ── Computed ───────────────────────────────────────────────────────────

    def _compute_all(self):
        today = date.today()
        month_start = today.replace(day=1)
        Proof = self.env["property.payment.proof"]

        for dash in self:
            # Prontos para confirmar (matched ou review com score ≥ 50)
            ready = Proof.search([("state", "in", ["matched", "review"]), ("confidence_score", ">=", 50)])
            dash.proof_ready_count = len(ready)
            dash.proof_ready_amount = sum(ready.mapped("amount"))

            # Conciliados no mês
            reconciled_month = Proof.search([
                ("state", "=", "reconciled"),
                ("write_date", ">=", str(month_start)),
            ])
            dash.proof_reconciled_month_count = len(reconciled_month)
            dash.proof_reconciled_month_amount = sum(reconciled_month.mapped("amount"))

            # Por estado
            def _search(domain):
                return Proof.search(domain)

            drafts = _search([("state", "=", "draft")])
            extracted = _search([("state", "=", "extracted")])
            matched = _search([("state", "=", "matched")])
            review = _search([("state", "=", "review")])
            failed = _search([("state", "=", "failed")])
            rejected = _search([("state", "=", "rejected")])

            dash.proof_draft_count = len(drafts)
            dash.proof_extracted_count = len(extracted)
            dash.proof_matched_count = len(matched)
            dash.proof_review_count = len(review)
            dash.proof_failed_count = len(failed)
            dash.proof_rejected_count = len(rejected)

            dash.proof_draft_amount = sum(drafts.mapped("amount"))
            dash.proof_extracted_amount = sum(extracted.mapped("amount"))
            dash.proof_matched_amount = sum(matched.mapped("amount"))
            dash.proof_review_amount = sum(review.mapped("amount"))

            dash.proof_attention_count = len(drafts) + len(extracted) + len(failed)
            dash.proof_total_pending = (
                len(drafts) + len(extracted) + len(matched) + len(review) + len(failed)
            )

            # Atrasos
            late_all = Proof.search([("is_late_payment", "=", True), ("state", "not in", ["rejected"])])
            dash.proof_late_count = len(late_all)
            dash.proof_late_amount = sum(late_all.mapped("amount"))
            dash.proof_late_no_handling = Proof.search_count([
                ("is_late_payment", "=", True),
                ("late_handling", "in", [False, "none"]),
                ("state", "not in", ["reconciled", "rejected"]),
            ])
            dash.proof_late_fee_count = Proof.search_count([("late_handling", "=", "request_fee")])
            dash.proof_late_defer_count = Proof.search_count([("late_handling", "=", "defer")])
            dash.proof_late_waive_count = Proof.search_count([("late_handling", "=", "waive")])
            dash.proof_late_fee_pending_count = Proof.search_count([
                ("proof_type", "=", "late_fee"),
                ("state", "in", ["draft", "extracted", "review"]),
            ])

            # Qualidade
            scored = Proof.search([
                ("state", "not in", ["draft", "failed", "rejected"]),
                ("confidence_score", ">", 0),
            ])
            scores = scored.mapped("confidence_score")
            dash.avg_score = sum(scores) / len(scores) if scores else 0.0
            dash.high_score_count = sum(1 for s in scores if s >= 80)
            dash.mid_score_count = sum(1 for s in scores if 50 <= s < 80)
            dash.low_score_count = sum(1 for s in scores if s < 50)
            total_scored = len(scores)
            dash.auto_match_rate = (dash.high_score_count / total_scored * 100) if total_scored else 0.0

    def _compute_charts(self):
        today = date.today()
        Proof = self.env["property.payment.proof"]
        cur = self.env.company.currency_id.symbol or "R$"

        for dash in self:
            # ── Trend semanal: últimas 8 semanas (recebidos vs conciliados) ──
            weeks_data = []
            for w in range(7, -1, -1):
                w_end = today - timedelta(days=today.weekday()) + timedelta(weeks=-w + 1) - timedelta(days=1)
                w_start = w_end - timedelta(days=6)
                received = Proof.search_count([
                    ("create_date", ">=", str(w_start)),
                    ("create_date", "<=", str(w_end) + " 23:59:59"),
                ])
                reconciled = Proof.search_count([
                    ("state", "=", "reconciled"),
                    ("write_date", ">=", str(w_start)),
                    ("write_date", "<=", str(w_end) + " 23:59:59"),
                ])
                label = w_start.strftime("%d/%m")
                weeks_data.append((label, received, reconciled))

            max_w = max((max(r, c) for _, r, c in weeks_data), default=1) or 1
            ch, bw, gap = 80, 28, 8
            vb_w = 8 * (bw * 2 + gap + 4) + gap
            bars = ""
            for i, (label, rec, con) in enumerate(weeks_data):
                x = i * (bw * 2 + gap + 4)
                rh = max(int(rec / max_w * ch), 2 if rec else 0)
                ch2 = max(int(con / max_w * ch), 2 if con else 0)
                bars += (
                    f'<rect x="{x}" y="{ch - rh}" width="{bw}" height="{rh}" fill="#aac8fd" rx="2"/>'
                    f'<rect x="{x + bw + 2}" y="{ch - ch2}" width="{bw}" height="{ch2}" fill="#198754" rx="2"/>'
                    f'<text x="{x + bw}" y="{ch + 14}" text-anchor="middle" font-size="8" fill="#6c757d">{label}</text>'
                )
                if rec:
                    bars += f'<text x="{x + bw // 2}" y="{ch - rh - 3}" text-anchor="middle" font-size="7.5" fill="#0d6efd">{rec}</text>'
                if con:
                    bars += f'<text x="{x + bw + 2 + bw // 2}" y="{ch - ch2 - 3}" text-anchor="middle" font-size="7.5" fill="#198754">{con}</text>'

            dash.chart_weekly_html = (
                f'<div style="padding:4px 0;">'
                f'<div style="display:flex;gap:16px;margin-bottom:8px;flex-wrap:wrap;">'
                f'<span style="font-size:11px;"><span style="display:inline-block;width:12px;height:12px;background:#aac8fd;border-radius:2px;vertical-align:middle;margin-right:4px;"></span>Recebidos</span>'
                f'<span style="font-size:11px;"><span style="display:inline-block;width:12px;height:12px;background:#198754;border-radius:2px;vertical-align:middle;margin-right:4px;"></span>Conciliados</span>'
                f'</div>'
                f'<svg viewBox="0 0 {vb_w} {ch + 22}" style="width:100%;display:block;">{bars}</svg>'
                f'</div>'
            )

            # ── Funil de conciliação ──
            stages = [
                ("Upload", dash.proof_draft_count, "#6c757d"),
                ("Extraído", dash.proof_extracted_count, "#0dcaf0"),
                ("Com Sugestão", dash.proof_matched_count + dash.proof_review_count, "#ffc107"),
                ("Conciliado/mês", dash.proof_reconciled_month_count, "#198754"),
            ]
            max_s = max(s for _, s, _ in stages) or 1
            funnel_bars = ""
            for i, (label, count, color) in enumerate(stages):
                pct = round(count / max_s * 100)
                funnel_bars += (
                    f'<div style="margin-bottom:8px;">'
                    f'<div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">'
                    f'<span style="color:{color};font-weight:600;">{label}</span>'
                    f'<span style="color:#495057;font-weight:700;">{count}</span>'
                    f'</div>'
                    f'<div style="background:#f0f0f0;border-radius:4px;height:14px;">'
                    f'<div style="width:{pct}%;background:{color};border-radius:4px;height:14px;min-width:{2 if count else 0}px;"></div>'
                    f'</div>'
                    f'</div>'
                )
            if dash.proof_failed_count:
                funnel_bars += (
                    f'<div style="margin-top:4px;font-size:11px;color:#dc3545;">'
                    f'&#9888; {dash.proof_failed_count} comprovante(s) com falha no OCR aguardando correção'
                    f'</div>'
                )
            dash.chart_funnel_html = funnel_bars

            # ── Por método de pagamento ──
            methods = [
                ("pix", "PIX", "#6f42c1"),
                ("transfer", "TED/DOC", "#0d6efd"),
                ("boleto", "Boleto", "#fd7e14"),
                ("deposit", "Depósito", "#20c997"),
                ("other", "Outro", "#6c757d"),
            ]
            method_bars = ""
            total_proofs = Proof.search_count([("state", "!=", "rejected")])
            for key, label, color in methods:
                cnt = Proof.search_count([("payment_method", "=", key), ("state", "!=", "rejected")])
                if not cnt:
                    continue
                pct = round(cnt / total_proofs * 100) if total_proofs else 0
                method_bars += (
                    f'<div style="margin-bottom:8px;">'
                    f'<div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">'
                    f'<span style="color:{color};font-weight:600;">{label}</span>'
                    f'<span style="color:#495057;">{cnt} ({pct}%)</span>'
                    f'</div>'
                    f'<div style="background:#f0f0f0;border-radius:4px;height:10px;">'
                    f'<div style="width:{pct}%;background:{color};border-radius:4px;height:10px;min-width:{2 if cnt else 0}px;"></div>'
                    f'</div>'
                    f'</div>'
                )
            dash.chart_method_html = method_bars or '<span style="color:#6c757d;font-size:12px;">Sem dados ainda.</span>'

            # ── Distribuição de score ──
            buckets = [
                ("≥ 90 (Excelente)", "#198754", lambda s: s >= 90),
                ("80–89 (Auto)", "#20c997", lambda s: 80 <= s < 90),
                ("50–79 (Revisão)", "#ffc107", lambda s: 50 <= s < 80),
                ("< 50 (Manual)", "#dc3545", lambda s: s < 50),
            ]
            all_scored = Proof.search([("confidence_score", ">", 0), ("state", "not in", ["draft", "rejected", "failed"])])
            all_scores_list = all_scored.mapped("confidence_score")
            total_s = len(all_scores_list) or 1
            score_bars = ""
            for label, color, fn in buckets:
                cnt = sum(1 for s in all_scores_list if fn(s))
                pct = round(cnt / total_s * 100)
                score_bars += (
                    f'<div style="margin-bottom:8px;">'
                    f'<div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">'
                    f'<span style="color:{color};font-weight:600;">{label}</span>'
                    f'<span style="color:#495057;">{cnt} ({pct}%)</span>'
                    f'</div>'
                    f'<div style="background:#f0f0f0;border-radius:4px;height:10px;">'
                    f'<div style="width:{pct}%;background:{color};border-radius:4px;height:10px;min-width:{2 if cnt else 0}px;"></div>'
                    f'</div>'
                    f'</div>'
                )
            dash.chart_score_html = score_bars or '<span style="color:#6c757d;font-size:12px;">Sem dados ainda.</span>'

    # ── Actions ────────────────────────────────────────────────────────────

    def _proof_action(self, name, domain, order="confidence_score desc, create_date desc"):
        return {
            "type": "ir.actions.act_window",
            "name": name,
            "res_model": "property.payment.proof",
            "view_mode": "list,form",
            "domain": domain,
            "context": {"search_default_pending": 0},
        }

    def action_view_ready(self):
        return self._proof_action(
            "Prontos para Confirmar",
            [("state", "in", ["matched", "review"]), ("confidence_score", ">=", 50)],
        )

    def action_view_draft(self):
        return self._proof_action("Upload Pendente", [("state", "=", "draft")])

    def action_view_extracted(self):
        return self._proof_action("Extraídos sem Sugestão", [("state", "=", "extracted")])

    def action_view_matched(self):
        return self._proof_action("Sugestão Automática (≥ 80)", [("state", "=", "matched")])

    def action_view_review(self):
        return self._proof_action("Em Revisão Manual", [("state", "=", "review")])

    def action_view_failed(self):
        return self._proof_action("Falha no OCR", [("state", "=", "failed")])

    def action_view_rejected(self):
        return self._proof_action("Rejeitados", [("state", "=", "rejected")])

    def action_view_late_fee_pending(self):
        return self._proof_action(
            "Comprovantes de Juros Aguardando Envio",
            [("proof_type", "=", "late_fee"), ("state", "in", ["draft", "extracted", "review"])],
        )

    def action_view_late_no_handling(self):
        return self._proof_action(
            "Atrasos sem Tratamento",
            [("is_late_payment", "=", True), ("late_handling", "in", [False, "none"]),
             ("state", "not in", ["reconciled", "rejected"])],
        )

    def action_view_reconciled_month(self):
        from datetime import date
        month_start = str(date.today().replace(day=1))
        return self._proof_action(
            "Conciliados no Mês",
            [("state", "=", "reconciled"), ("write_date", ">=", month_start)],
        )

    def action_bulk_confirm_high_score(self):
        """Confirma automaticamente todos os comprovantes com score >= 80 e estado 'matched'."""
        proofs = self.env["property.payment.proof"].search([
            ("state", "=", "matched"),
            ("confidence_score", ">=", 80),
        ])
        confirmed = 0
        errors = []
        for proof in proofs:
            try:
                proof.action_approve_and_reconcile()
                confirmed += 1
            except Exception as exc:
                errors.append(f"{proof.name}: {exc}")

        msg = _("%d comprovante(s) confirmados automaticamente.") % confirmed
        if errors:
            msg += "\n" + _("%d com erro: %s") % (len(errors), " | ".join(errors[:3]))
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Confirmação em Lote"),
                "message": msg,
                "type": "success" if not errors else "warning",
                "sticky": True,
            },
        }

    def action_bulk_upload(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Upload em Lote",
            "res_model": "property.payment.proof.bulk.upload",
            "view_mode": "form",
            "target": "new",
        }