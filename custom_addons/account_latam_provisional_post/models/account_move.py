# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_latam_is_provisional_document = fields.Boolean(
        string="Documento Fiscal Provisório",
        compute="_compute_l10n_latam_is_provisional_document",
        help="Confirmado sem número fiscal real. Informe o número antes de pagar.",
    )

    @api.depends("name")
    def _compute_l10n_latam_is_provisional_document(self):
        for rec in self:
            rec.l10n_latam_is_provisional_document = bool(
                rec.name and any(p.startswith("PROV-") for p in rec.name.split())
            )

    def _post(self, soft=True):
        """Atribui nome provisório PROV-{id} para faturas manuais sem número fiscal."""
        for rec in self.filtered(
            lambda x: x.l10n_latam_use_documents
            and x.l10n_latam_manual_document_number
            and not x.l10n_latam_document_number
        ):
            doc_prefix = (rec.l10n_latam_document_type_id.doc_code_prefix or "").strip()
            prov = "PROV-%s" % rec.id
            rec.name = ("%s %s" % (doc_prefix, prov)).strip() if doc_prefix else prov
        return super()._post(soft=soft)

    @api.constrains("state", "l10n_latam_document_type_id")
    def _check_l10n_latam_documents(self):
        """Exige apenas o tipo de documento ao confirmar. Número é exigido no pagamento."""
        for move in self.filtered(
            lambda m: m.l10n_latam_use_documents and m.state == "posted"
        ):
            if not move.l10n_latam_document_type_id:
                raise ValidationError(_(
                    "O tipo de documento fiscal é obrigatório para confirmar a fatura %s.",
                    move.display_name,
                ))

    @api.onchange("name", "highest_name")
    def _onchange_name_warning(self):
        """Suprime o aviso de mudança de formato de sequência ao trocar PROV- pelo número real."""
        origin_name = self._origin.name or self.highest_name or ""
        if origin_name and any(p.startswith("PROV-") for p in origin_name.split()):
            return {}
        return super()._onchange_name_warning()

    def _check_real_fiscal_number_before_payment(self):
        """Levanta erro se alguma fatura ainda tiver número provisório."""
        for move in self:
            if not move.l10n_latam_use_documents:
                continue
            if move.name and any(p.startswith("PROV-") for p in move.name.split()):
                raise ValidationError(_(
                    "Informe o número real do documento fiscal antes de pagar a fatura %s.\n"
                    "Edite a fatura, preencha o campo 'Número do Documento' e salve.",
                    move.display_name,
                ))