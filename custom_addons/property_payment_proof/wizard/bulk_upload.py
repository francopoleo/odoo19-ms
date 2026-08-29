# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PropertyPaymentProofBulkUpload(models.TransientModel):
    _name = "property.payment.proof.bulk.upload"
    _description = "Upload em Lote de Comprovantes de Pagamento"

    attachment_ids = fields.Many2many(
        "ir.attachment",
        "proof_bulk_upload_att_rel",
        "wizard_id",
        "attachment_id",
        string="Arquivos (PDF/imagem)",
    )
    contract_id = fields.Many2one(
        "property.contract",
        string="Contrato (opcional)",
        help="Se informado, a busca de parcelas é limitada a este contrato.",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        required=True,
        default=lambda self: self.env.company,
    )

    def action_process(self):
        self.ensure_one()
        if not self.attachment_ids:
            raise UserError(_("Selecione ao menos um arquivo para processar."))

        Proof = self.env["property.payment.proof"]
        created = Proof
        errors = []

        for att in self.attachment_ids:
            proof = Proof.create({
                "proof_file": att.datas,
                "proof_filename": att.name,
                "contract_id": self.contract_id.id if self.contract_id else False,
                "company_id": self.company_id.id,
            })
            try:
                proof.action_extract()
                created |= proof
            except Exception as exc:
                errors.append(f"{att.name}: {exc}")
                created |= proof  # mantém na lista mesmo com falha, para revisão

        if errors:
            # Loga os erros mas não aborta — os registros com falha ficam em state=failed
            self.env["bus.bus"]._sendone(
                self.env.user.partner_id,
                "simple_notification",
                {
                    "title": _("Upload em lote — atenção"),
                    "message": _("%d arquivo(s) com erro:\n%s") % (len(errors), "\n".join(errors)),
                    "warning": True,
                },
            )

        return {
            "type": "ir.actions.act_window",
            "name": _("Comprovantes Processados"),
            "res_model": "property.payment.proof",
            "view_mode": "list,form",
            "domain": [("id", "in", created.ids)],
            "target": "current",
        }