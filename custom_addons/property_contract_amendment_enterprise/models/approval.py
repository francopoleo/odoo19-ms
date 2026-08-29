# -*- coding: utf-8 -*-
from odoo import models, fields


class PropertyContractApproval(models.Model):
    _name = "property.contract.approval"
    _description = "Aprovação Contratual"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "amendment_id, sequence, id"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade")
    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo", ondelete="cascade")
    approval_type = fields.Selection([
        ("legal", "Jurídico"),
        ("commercial", "Comercial"),
        ("financial", "Financeiro"),
        ("risk", "Risco"),
        ("accounting", "Contabilidade"),
        ("asset_manager", "Gestor do Ativo"),
        ("board", "Diretoria"),
        ("conformidade", "Conformidade"),
        ("registration", "Cadastro/Registro"),
    ], string="Tipo de Aprovação", required=True)
    required_group_id = fields.Many2one("res.groups", string="Grupo Responsável")
    approver_id = fields.Many2one("res.users", string="Aprovador")
    status = fields.Selection([
        ("pending", "Pendente"),
        ("approved", "Aprovado"),
        ("rejected", "Rejeitado"),
        ("skipped", "Ignorado"),
        ("cancelled", "Cancelado"),
    ], string="Status", default="pending", tracking=True)
    requested_at = fields.Datetime(string="Solicitado em", default=fields.Datetime.now)
    approved_at = fields.Datetime(string="Aprovado em")
    rejected_at = fields.Datetime(string="Rejeitado em")
    comments = fields.Text(string="Comentários")
    sequence = fields.Integer(string="Sequência", default=10)

    def action_approve(self):
        self.write({"status": "approved", "approved_at": fields.Datetime.now(), "approver_id": self.env.user.id})

    def action_reject(self):
        self.write({"status": "rejected", "rejected_at": fields.Datetime.now(), "approver_id": self.env.user.id})
