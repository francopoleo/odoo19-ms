from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DocumentCategory(models.Model):
    _name = "document.category"
    _description = "Categoria de Documento"
    _order = "sequence, name"
    _rec_name = "name"

    name = fields.Char("Categoria", required=True, translate=True)
    code = fields.Char("Código", required=True, index=True)
    sequence = fields.Integer(default=10)
    description = fields.Text("Descrição")
    active = fields.Boolean(default=True)
    default_access_level = fields.Selection([
        ("internal", "Interno"),
        ("legal", "Jurídico"),
        ("finance", "Financeiro"),
        ("governance", "Governança"),
        ("authorized_brokers", "Corretores Autorizados"),
        ("portal", "Portal / Logado"),
        ("public", "Público"),
    ], string="Acesso Padrão", default="internal", required=True)
    allow_website_publish = fields.Boolean("Permitir Publicação no Site por Padrão")
    type_ids = fields.One2many("document.type", "category_id", string="Tipos")
    type_count = fields.Integer(compute="_compute_type_count", string="Qtd. Tipos")

    def _compute_type_count(self):
        for category in self:
            category.type_count = len(category.type_ids)

    @api.constrains("code")
    def _check_unique_code(self):
        for rec in self:
            if not rec.code:
                continue
            duplicate = self.search([("id", "!=", rec.id), ("code", "=", rec.code)], limit=1)
            if duplicate:
                raise ValidationError("Já existe uma categoria documental com este código.")
