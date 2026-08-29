# -*- coding: utf-8 -*-
from odoo import models, fields


class PropertyContractObligation(models.Model):
    _name = "property.contract.obligation"
    _description = "Obrigação Contratual"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "due_date, id"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade")
    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo", ondelete="set null")
    obligation_type = fields.Selection([
        ("insurance_renewal", "Renovação de seguro"),
        ("guarantee_renewal", "Renovação de garantia"),
        ("license_delivery", "Entrega de licença"),
        ("project_approval", "Aprovação de projeto"),
        ("fit_out_delivery", "Entrega de adaptação/implantação"),
        ("maintenance", "Manutenção"),
        ("iptu_payment", "Pagamento de IPTU"),
        ("condominium_payment", "Pagamento de condomínio"),
        ("notice_requirement", "Notificação"),
        ("registration", "Registro"),
        ("inspection", "Vistoria"),
        ("restitution", "Restituição/devolução"),
        ("confidentiality", "Confidencialidade"),
        ("conformidade", "Conformidade"),
        ("other", "Outra"),
    ], string="Tipo de Obrigação", default="other")
    responsible_party = fields.Selection([
        ("landlord", "Locador"),
        ("tenant", "Locatário"),
        ("both", "Ambos"),
        ("third_party", "Terceiro"),
    ], string="Parte Responsável", default="tenant")
    name = fields.Char(string="Nome", required=True)
    description = fields.Text(string="Descrição")
    due_date = fields.Date(string="Data de Vencimento")
    recurrence = fields.Selection([
        ("none", "Sem recorrência"),
        ("monthly", "Mensal"),
        ("quarterly", "Trimestral"),
        ("semiannual", "Semestral"),
        ("annual", "Anual"),
    ], string="Recorrência", default="none")
    status = fields.Selection([
        ("pending", "Pendente"),
        ("done", "Concluída"),
        ("late", "Atrasada"),
        ("cancelled", "Cancelada"),
    ], string="Status", default="pending", tracking=True)
    penalty = fields.Char(string="Penalidade")
    source_clause = fields.Char(string="Cláusula de Origem")
