# -*- coding: utf-8 -*-
from odoo import models, fields


class PropertyContractOption(models.Model):
    _name = "property.contract.option"
    _description = "Opção Contratual"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "exercise_deadline, id"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade")
    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo", ondelete="set null")
    option_type = fields.Selection([
        ("renewal", "Renovação"),
        ("purchase_preference", "Preferência de compra"),
        ("expansion", "Expansão"),
        ("termination", "Rescisão"),
        ("right_of_first_refusal", "Direito de preferência"),
        ("exclusive_use", "Uso exclusivo"),
        ("extension", "Extensão"),
        ("break_option", "Opção de saída"),
    ], string="Tipo de Opção", required=True)
    name = fields.Char(string="Nome", required=True)
    notice_start_date = fields.Date(string="Início da Janela de Notificação")
    notice_deadline = fields.Date(string="Prazo de Notificação")
    exercise_deadline = fields.Date(string="Prazo de Exercício")
    status = fields.Selection([
        ("available", "Disponível"),
        ("notice_sent", "Notificação enviada"),
        ("exercised", "Exercida"),
        ("expired", "Expirada"),
        ("waived", "Renunciada"),
        ("cancelled", "Cancelada"),
    ], string="Status", default="available", tracking=True)
    exercised_at = fields.Datetime(string="Exercida em")
    exercise_document_id = fields.Many2one("property.contract.document", string="Documento de Exercício")
    notes = fields.Text(string="Observações")
