from odoo import fields, models


class CondominiumTicket(models.Model):
    _name = "property.condominium.ticket"
    _description = "Chamado do Condomínio"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, create_date desc"

    name = fields.Char(required=True, tracking=True)
    complex_id = fields.Many2one("property.complex", required=True, tracking=True, ondelete="cascade")
    unit_id = fields.Many2one("property.asset", tracking=True, ondelete="set null")
    partner_id = fields.Many2one("res.partner", tracking=True)
    category = fields.Selection(
        [("maintenance", "Manutenção"), ("service", "Serviço Comum"), ("billing", "Cobrança"), ("other", "Outros")],
        default="service",
        tracking=True,
    )
    priority = fields.Selection([("0", "Baixa"), ("1", "Normal"), ("2", "Alta"), ("3", "Crítica")], default="1", tracking=True)
    state = fields.Selection(
        [("new", "Novo"), ("in_progress", "Em Andamento"), ("waiting", "Aguardando"), ("done", "Concluído"), ("cancelled", "Cancelado")],
        default="new",
        tracking=True,
    )
    description = fields.Html()

    def action_start(self):
        self.write({"state": "in_progress"})

    def action_wait(self):
        self.write({"state": "waiting"})

    def action_done(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancelled"})
