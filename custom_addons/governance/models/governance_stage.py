from odoo import models, fields

class GovernanceStage(models.Model):
    _name = "governance.stage"
    _description = "Etapa de Governança"
    _order = "sequence"

    name = fields.Char(string="Nome", required=True, translate=True)
    sequence = fields.Integer(string="Ordem", default=10)
    status = fields.Selection([
        ("planned", "Planejado"),
        ("sent", "E-mail Enviado"),
        ("waiting", "Aguardando Resposta"),
        ("partial", "Resposta Parcial"),
        ("no_response", "Sem Resposta"),
        ("done", "Concluído"),
        ("closed", "Encerrado"),
    ], string="Status", required=True)
    fold = fields.Boolean(string="Recolhido no Kanban", default=False)
    color = fields.Integer(string="Cor", default=0)
