from odoo import fields, models


class GovernanceCaseTypePendingTemplate(models.Model):
    _name = "governance.case.type.pending.template"
    _description = "Modelo de Pendência por Tipo de Caso"
    _order = "sequence, id"

    _case_type_name_unique = models.Constraint(
        "UNIQUE(case_type_id, name)",
        "Já existe uma ação com este nome neste Tipo de Caso.",
    )

    case_type_id = fields.Many2one(
        "governance.case.type",
        string="Tipo de Caso",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativo", default=True)
    name = fields.Char(
        string="Ação do checklist",
        required=True,
        help="Ação operacional verificável. Não use para representar um arquivo do dossiê ou uma obrigação formal.",
    )
    description = fields.Text(
        string="Como concluir",
        help="Explique o resultado esperado. Os arquivos continuam sendo controlados pelo dossiê.",
    )
    default_deadline_days = fields.Integer(string="Prazo Padrão (dias)", default=0)
    priority = fields.Selection([
        ("0", "Baixo"),
        ("1", "Médio"),
        ("2", "Alto"),
        ("3", "Crítico"),
    ], string="Prioridade", default="1")
    assign_to_responsible = fields.Boolean(string="Atribuir ao Responsável do Caso", default=True)
    required = fields.Boolean(string="Obrigatória", default=True)
