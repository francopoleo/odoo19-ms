# -*- coding: utf-8 -*-
from odoo import models, fields


class PropertyContractAmendmentReason(models.Model):
    _name = "property.contract.amendment.reason"
    _description = "Motivo de Aditivo Contratual"
    _order = "category, name"

    name = fields.Char(string="Nome", required=True, translate=True)
    code = fields.Char(string="Código", required=True, index=True)
    category = fields.Selection([
        ("general", "Geral"),
        ("party", "Partes"),
        ("term", "Prazo"),
        ("financial", "Financeiro"),
        ("asset", "Imóvel/Área"),
        ("operation", "Uso e Operação"),
        ("guarantee", "Garantias"),
        ("works", "Obras e Benfeitorias"),
        ("expenses", "Encargos e Despesas"),
        ("legal", "Jurídico/Conformidade"),
        ("termination", "Encerramento"),
    ], string="Categoria", required=True, default="general")
    description = fields.Text(string="Descrição")
    active = fields.Boolean(string="Ativo", default=True)

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'O código do motivo de aditivo deve ser único.',
    )


class PropertyContractFinancialReason(models.Model):
    _name = "property.contract.financial.reason"
    _description = "Motivo Financeiro Contratual"
    _order = "impact_type, name"

    name = fields.Char(string="Nome", required=True, translate=True)
    code = fields.Char(string="Código", required=True, index=True)
    impact_type = fields.Selection([
        ("plus", "A mais / Débito / Acréscimo"),
        ("minus", "A menos / Crédito / Desconto"),
        ("neutral", "Neutro"),
    ], string="Tipo de Impacto", required=True, default="neutral")
    description = fields.Text(string="Descrição")
    active = fields.Boolean(string="Ativo", default=True)

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'O código do motivo financeiro deve ser único.',
    )


class PropertyContractDocumentType(models.Model):
    _name = "property.contract.document.type"
    _description = "Tipo de Documento Contratual"
    _order = "sequence, name"

    name = fields.Char(string="Nome", required=True, translate=True)
    code = fields.Char(string="Código", required=True, index=True)
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativo", default=True)

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'O código do tipo de documento deve ser único.',
    )
