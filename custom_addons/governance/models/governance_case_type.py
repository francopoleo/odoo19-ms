from odoo import api, fields, models, _


class GovernanceCaseType(models.Model):
    _name = "governance.case.type"
    _description = "Tipo de Caso de Governança"
    _order = "sequence, name"

    name = fields.Char("Nome", required=True)
    code = fields.Char("Código interno", help="Identificador curto para integrações e relatórios. Ex.: JUR, FIN ou DOC.")
    description = fields.Text("Descrição", help="Explique quando este tipo deve ser usado e qual resultado o caso precisa produzir.")
    case_family = fields.Selection([
        ("intake", "Entrada e triagem"),
        ("analysis", "Análise e conformidade"),
        ("financial", "Financeiro e valores"),
        ("operations", "Operação do imóvel"),
        ("relationship", "Relacionamento e disputas"),
    ], string="Grupo de trabalho", default="operations", required=True, index=True,
        help="Agrupa os tipos na lista por finalidade. Não altera o fluxo nem substitui o Tipo de Processo do dossiê.")
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

    case_count = fields.Integer(string="Casos", compute="_compute_case_count")

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "Já existe um Tipo de Caso com este nome. Use o tipo existente ou escolha outro nome.",
    )
    _code_unique = models.Constraint(
        "UNIQUE(code)",
        "Já existe um Tipo de Caso com este código interno.",
    )

    def _compute_pending_template_count(self):
        for record in self:
            record.pending_template_count = len(record.pending_template_ids)

    @api.depends()
    def _compute_case_count(self):
        Case = self.env["governance.case"]
        counts = {}
        if self.ids:
            data = Case.read_group(
                [("case_type_id", "in", self.ids)],
                ["case_type_id"],
                ["case_type_id"],
            )
            counts = {
                row["case_type_id"][0]: row["case_type_id_count"]
                for row in data if row.get("case_type_id")
            }
        for record in self:
            record.case_count = counts.get(record.id, 0)

    def action_view_cases(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Casos: %s") % self.name,
            "res_model": "governance.case",
            "view_mode": "list,form",
            "domain": [("case_type_id", "=", self.id)],
            "context": {"default_case_type_id": self.id},
        }
