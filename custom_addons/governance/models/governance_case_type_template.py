from odoo import fields, models


class GovernanceCaseTypePendingTemplate(models.Model):
    _name = "governance.case.type.pending.template"
    _description = "Modelo de Pendência por Tipo de Caso"
    _order = "sequence, id"

    case_type_id = fields.Many2one(
        "governance.case.type",
        string="Tipo de Caso",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativo", default=True)
    name = fields.Char(string="Pendência", required=True)
    description = fields.Text(string="Descrição")
    default_deadline_days = fields.Integer(string="Prazo Padrão (dias)", default=0)
    priority = fields.Selection([
        ("0", "Baixo"),
        ("1", "Médio"),
        ("2", "Alto"),
        ("3", "Crítico"),
    ], string="Prioridade", default="1")
    assign_to_responsible = fields.Boolean(string="Atribuir ao Responsável do Caso", default=True)
    required = fields.Boolean(string="Obrigatória", default=True)
