# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class PropertyRent(models.Model):
    _inherit = "property.rent"

    payment_proof_ids = fields.One2many("property.payment.proof", "rent_id", string="Comprovantes")
    payment_proof_count = fields.Integer("Qtd. Comprovantes", compute="_compute_payment_proof_count")

    def _compute_payment_proof_count(self):
        for rent in self:
            rent.payment_proof_count = len(rent.payment_proof_ids)

    def action_view_payment_proofs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Comprovantes",
            "res_model": "property.payment.proof",
            "view_mode": "list,form",
            "domain": [("rent_id", "=", self.id)],
            "context": {
                "default_rent_id": self.id,
                "default_contract_id": self.contract_id.id,
                "default_amount": getattr(self, "residual_amount", False) or self.amount_due,
            },
        }

    def action_register_via_proof(self):
        """Abre formulário de novo comprovante pré-vinculado a esta parcela."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Novo Comprovante de Pagamento"),
            "res_model": "property.payment.proof",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_rent_id": self.id,
                "default_contract_id": self.contract_id.id,
                "default_amount": getattr(self, "residual_amount", False) or self.amount_due,
            },
        }

    def action_open_manual_payment_wizard(self):
        """Abre wizard de pagamento manual (sem comprovante físico)."""
        self.ensure_one()
        if self.status not in ("open", "late", "partial"):
            raise UserError(_("Esta parcela não está disponível para pagamento."))
        residual = getattr(self, "residual_amount", 0) or self.amount_due
        return {
            "type": "ir.actions.act_window",
            "name": _("Registrar Pagamento Manual"),
            "res_model": "property.payment.proof.manual",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_rent_id": self.id,
                "default_amount": residual,
            },
        }
