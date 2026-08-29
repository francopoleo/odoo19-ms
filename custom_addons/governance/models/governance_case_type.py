from odoo import fields, models


class GovernanceCaseType(models.Model):
    _name = "governance.case.type"
    _description = "Tipo de Caso de Governança"
    _order = "sequence, name"

    name = fields.Char("Nome", required=True)
    code = fields.Char("Código")
    description = fields.Text("Descrição")
    color = fields.Integer("Cor", default=0)
    sequence = fields.Integer("Sequência", default=10)
    active = fields.Boolean("Ativo", default=True)

    default_priority = fields.Selection([
        ("0", "Baixo"),
        ("1", "Médio"),
        ("2", "Alto"),
        ("3", "Crítico"),
    ], string="Prioridade Padrão", default="1")
    sla_days = fields.Integer("SLA Padrão (dias)", default=0)
    require_primary_participant = fields.Boolean("Exigir Contato Principal")
    auto_followup_days = fields.Integer("Disparar Follow-up após (dias)", default=0)
    auto_create_followup_activity = fields.Boolean("Criar Atividade de Follow-up")
    require_response_before_done = fields.Boolean("Exigir Resposta antes de Concluir")
    require_required_pendings_done = fields.Boolean("Exigir Pendências Obrigatórias Concluídas")
    require_no_open_pendings_to_close = fields.Boolean("Exigir Zero Pendências Abertas para Encerrar")

    allowed_stage_ids = fields.Many2many(
        "governance.stage",
        "governance_case_type_stage_rel",
        "case_type_id",
        "stage_id",
        string="Etapas Permitidas",
        help="Se preenchido, o caso desse tipo só poderá usar estas etapas.",
    )
    initial_stage_id = fields.Many2one("governance.stage", string="Etapa Inicial")
    waiting_stage_id = fields.Many2one("governance.stage", string="Etapa de Aguardando Resposta")
    no_response_stage_id = fields.Many2one("governance.stage", string="Etapa de Sem Resposta")
    done_stage_id = fields.Many2one("governance.stage", string="Etapa de Concluído")
    closed_stage_id = fields.Many2one("governance.stage", string="Etapa de Encerrado")

    pending_template_ids = fields.One2many(
        "governance.case.type.pending.template",
        "case_type_id",
        string="Modelos de Pendência",
    )
    pending_template_count = fields.Integer(
        string="Qtd Modelos de Pendência",
        compute="_compute_pending_template_count",
    )

    def _compute_pending_template_count(self):
        for record in self:
            record.pending_template_count = len(record.pending_template_ids)
