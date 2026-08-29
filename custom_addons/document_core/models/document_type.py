from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DocumentType(models.Model):
    _name = "document.type"
    _description = "Tipo de Documento"
    _order = "category_id, sequence, name"
    _rec_name = "name"

    name = fields.Char("Tipo de Documento", required=True, translate=True)
    code = fields.Char("Código", required=True, index=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    category_id = fields.Many2one("document.category", string="Categoria", required=True, ondelete="restrict", index=True)
    description = fields.Text("Descrição")
    scope = fields.Selection([
        ("general", "Geral"), ("asset", "Imóvel"), ("complex", "Complexo"), ("contract", "Contrato"),
        ("owner", "Proprietário"), ("broker", "Corretor"), ("lead", "Lead"),
        ("inspection", "Vistoria"), ("maintenance", "Manutenção"), ("document", "Documento"), ("media", "Mídia"),
    ], string="Aplicável a", default="asset", required=True)
    default_access_level = fields.Selection([
        ("internal", "Interno"), ("legal", "Jurídico"), ("finance", "Financeiro"),
        ("authorized_brokers", "Corretores Autorizados"), ("portal", "Portal / Logado"), ("public", "Público"),
    ], string="Acesso Padrão", default="internal", required=True)
    allow_website_publish = fields.Boolean("Pode ser Publicado no Site")
    portal_uploadable = fields.Boolean("Permitir Upload no Portal", help="Se ativado, usuários do portal podem fazer upload deste tipo de documento")
    website_default_visibility = fields.Selection([
        ("portal", "Somente Logado"), ("public", "Público"), ("authorized_brokers", "Corretores Autorizados"),
    ], string="Visibilidade Padrão no Site", default="portal")
    requires_issue_date = fields.Boolean("Exige Data de Emissão")
    requires_expiry = fields.Boolean("Exige Data de Vencimento")
    requires_review = fields.Boolean("Exige Data de Revisão")
    requires_validation = fields.Boolean("Exige Validação Formal", help="Se marcado, documento não pode ser usado sem validação por usuário autorizado")
    requires_physical_original = fields.Boolean("Exige Guarda Física")
    is_sensitive = fields.Boolean("Documento Sensível")
    review_cycle_days = fields.Integer("Ciclo de Revisão (dias)")
    allowed_file_types = fields.Char("Tipos de Arquivo Permitidos")
    document_count = fields.Integer(compute="_compute_document_count", string="Qtd. Documentos")

    def _compute_document_count(self):
        Document = self.env["document.document"].sudo()
        for rec in self:
            rec.document_count = Document.search_count([("document_type_id", "=", rec.id)])

    @api.constrains("code")
    def _check_unique_code(self):
        for rec in self:
            if not rec.code:
                continue
            duplicate = self.search([("id", "!=", rec.id), ("code", "=", rec.code)], limit=1)
            if duplicate:
                raise ValidationError("Já existe um tipo documental com este código.")

    @api.constrains("review_cycle_days")
    def _check_review_cycle_days(self):
        for rec in self:
            if rec.review_cycle_days and rec.review_cycle_days < 0:
                raise ValidationError("O ciclo de revisão não pode ser negativo.")
