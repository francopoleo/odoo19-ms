from odoo import fields, models, _
from odoo.exceptions import ValidationError


class DocumentApplyTemplateWizard(models.TransientModel):
    _name = "document.apply.template.wizard"
    _description = "Aplicar Template de Dossiê"

    dossier_id = fields.Many2one("dossier.dossier", string="Dossiê", required=True)
    template_id = fields.Many2one("document.dossier.template", string="Template", required=True, domain="[('active','=',True)]")
    create_only_missing = fields.Boolean("Criar somente itens faltantes", default=True)

    def action_apply_template(self):
        self.ensure_one()
        if not self.template_id.line_ids:
            raise ValidationError(_("O template selecionado não possui documentos necessários."))

        self.dossier_id.apply_templates(
            templates=self.template_id,
            create_only_missing=self.create_only_missing,
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "dossier.dossier",
            "res_id": self.dossier_id.id,
            "view_mode": "form",
            "target": "current",
        }
