from odoo import api, fields, models


class PropertyComplexDocumentExt(models.Model):
    _inherit = "property.complex"

    document_ids = fields.One2many(
        "document.document", "complex_id", string="Documentos"
    )


class PropertyAssetDocumentExt(models.Model):
    _inherit = "property.asset"

    document_ids = fields.Many2many(
        "document.document",
        relation="document_asset_rel",
        column1="asset_id",
        column2="document_id",
        string="Documentos Vinculados",
    )
    document_count = fields.Integer("Qtd. Documentos", compute="_compute_document_count")

    @api.depends("document_ids")
    def _compute_document_count(self):
        for asset in self:
            asset.document_count = len(asset.document_ids)


class PropertyContractDocumentExt(models.Model):
    _inherit = "property.contract"

    document_ids = fields.One2many(
        "document.document", "contract_id", string="Documentos"
    )
    document_count = fields.Integer("Qtd. Documentos", compute="_compute_document_count")

    @api.depends("document_ids")
    def _compute_document_count(self):
        for contract in self:
            contract.document_count = len(contract.document_ids)


class PropertyMediaDocumentExt(models.Model):
    _inherit = "property.media"

    document_id = fields.Many2one(
        "document.document", string="Documento", ondelete="cascade", tracking=True
    )
