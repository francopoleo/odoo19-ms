# -*- coding: utf-8 -*-
from odoo import models, fields


class PropertyContractDocument(models.Model):
    _name = "property.contract.document"
    _description = "Documento Contratual"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "contract_id, id desc"

    contract_id = fields.Many2one("property.contract", string="Contrato", required=True, ondelete="cascade")
    amendment_id = fields.Many2one("property.contract.amendment", string="Aditivo", ondelete="cascade")
    document_type_id = fields.Many2one("property.contract.document.type", string="Tipo de Documento")
    document_type = fields.Selection([
        ("original_contract", "Contrato original"),
        ("amendment", "Aditivo"),
        ("signature_certificate", "Certificado de assinatura"),
        ("registration", "Registro"),
        ("notice", "Notificação"),
        ("invoice_support", "Suporte financeiro"),
        ("approval_document", "Documento de aprovação"),
        ("termination_document", "Documento de encerramento"),
        ("other", "Outro"),
    ], string="Classificação do Documento", default="other")
    name = fields.Char(string="Nome", required=True)
    file = fields.Binary(string="Arquivo", attachment=True)
    file_name = fields.Char(string="Nome do Arquivo")
    issuer = fields.Char(
        string="Emitido por",
        help="Pessoa, empresa, cartório, plataforma ou responsável que emitiu o documento.",
    )
    signature_provider = fields.Selection([
        ("docusign", "DocuSign"),
        ("clicksign", "Clicksign"),
        ("adobesign", "Adobe Sign"),
        ("govbr", "Gov.br"),
        ("manual", "Manual"),
        ("other", "Outro"),
    ], string="Provedor de Assinatura")
    envelope_id = fields.Char(string="ID do Envelope", index=True)
    signature_status = fields.Selection([
        ("draft", "Rascunho"),
        ("sent", "Enviado"),
        ("partially_signed", "Parcialmente assinado"),
        ("completed", "Concluído"),
        ("cancelled", "Cancelado"),
    ], string="Status da Assinatura")
    sent_at = fields.Datetime(string="Enviado em")
    signed_at = fields.Datetime(string="Assinado em")
    completed_at = fields.Datetime(string="Concluído em")
    signers_json = fields.Text(string="Assinantes JSON")
    certificate_file = fields.Binary(string="Arquivo do Certificado", attachment=True)
    certificate_file_name = fields.Char(string="Nome do Arquivo do Certificado")
    certificate_html = fields.Html(string="Certificado HTML")
    checksum = fields.Char(string="Checksum")
    version = fields.Integer(string="Versão", default=1)
    is_final = fields.Boolean(string="Documento Final", default=False)
