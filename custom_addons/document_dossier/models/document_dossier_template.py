from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DocumentDossierTemplate(models.Model):
    _name = "document.dossier.template"
    _description = "Template de Dossiê Documental"
    _order = "sequence, name"

    active = fields.Boolean(default=True)
    sequence = fields.Integer("Sequência", default=10)
    name = fields.Char("Nome", required=True)
    code = fields.Char("Código")
    description = fields.Text("Descrição")
    line_ids = fields.One2many("document.dossier.template.line", "template_id", string="Documentos Necessários", copy=True)
    required_line_count = fields.Integer("Obrigatórios", compute="_compute_line_counts")
    total_line_count = fields.Integer("Total de Itens", compute="_compute_line_counts")

    @api.depends("line_ids", "line_ids.required")
    def _compute_line_counts(self):
        for template in self:
            template.total_line_count = len(template.line_ids)
            template.required_line_count = len(template.line_ids.filtered(lambda line: line.required))


class DocumentDossierTemplateLine(models.Model):
    _name = "document.dossier.template.line"
    _description = "Item do Template de Dossiê"
    _order = "template_id, sequence, id"

    template_id = fields.Many2one("document.dossier.template", string="Template", required=True, ondelete="cascade")
    sequence = fields.Integer("Sequência", default=10)
    name = fields.Char("Nome do Documento Esperado", required=True)
    document_type_id = fields.Many2one("document.type", string="Tipo Documental", ondelete="restrict")
    category_id = fields.Many2one("document.category", string="Categoria", related="document_type_id.category_id", readonly=True)
    required = fields.Boolean("Obrigatório", default=True)
    requires_file = fields.Boolean("Arquivo Obrigatório", default=True)
    description = fields.Char("Descrição / Orientação")
    notes = fields.Text("Instruções")

    @api.onchange("document_type_id")
    def _onchange_document_type_id(self):
        for line in self:
            if line.document_type_id and not line.name:
                line.name = line.document_type_id.name

    @api.constrains("name", "template_id")
    def _check_name(self):
        for line in self:
            if not (line.name or "").strip():
                raise ValidationError(_("Informe o nome do documento esperado."))
