# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PropertyContractHistoryBulkUpload(models.TransientModel):
    _name = "property.contract.history.bulk.upload"
    _description = "Upload em Lote de Contratos"

    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Arquivos",
        help="Selecione múltiplos arquivos PDF ou imagens para processar",
    )
    asset_id = fields.Many2one(
        "property.asset",
        string="Imóvel (Opcional)",
        help="Se preenchido, todos os contratos serão vinculados a este imóvel",
    )
    contract_type = fields.Selection(
        [
            ("rental", "Aluguel/Locação"),
            ("sale", "Venda"),
            ("financing", "Financiamento/Hipoteca"),
            ("comodato", "Comodato"),
            ("other", "Outro"),
        ],
        string="Tipo (Dica)",
        help="Dica para ajudar o parser a detectar o tipo correto",
    )
    auto_extract = fields.Boolean(
        "Extrair Automaticamente",
        default=True,
        help="Executar OCR e parsing imediatamente após upload",
    )
    auto_sync = fields.Boolean(
        "Sincronizar Automaticamente",
        default=False,
        help="Sincronizar dados extraídos ao imóvel automaticamente (somente se auto_extract=True)",
    )

    def action_process(self):
        """Create contract history records and optionally auto-extract."""
        if not self.attachment_ids:
            raise UserError(_("Selecione pelo menos um arquivo para processar."))

        History = self.env["property.contract.history"]
        created_ids = []

        for attachment in self.attachment_ids:
            # Get file content
            try:
                import base64
                file_content = base64.b64decode(attachment.datas)
            except Exception:
                file_content = attachment.datas

            # Create contract history record
            vals = {
                "contract_filename": attachment.name,
                "contract_file": attachment.datas,
                "company_id": self.env.company.id,
                "asset_id": self.asset_id.id if self.asset_id else False,
                "contract_type": self.contract_type or "other",
            }

            try:
                history = History.create(vals)
                created_ids.append(history.id)

                if self.auto_extract:
                    history.action_extract()
                    if self.auto_sync and history.asset_id:
                        history.action_sync_to_asset()

            except Exception as exc:
                # Log error but continue with next file
                pass

        if created_ids:
            # Return action showing created records
            return {
                "type": "ir.actions.act_window",
                "res_model": "property.contract.history",
                "view_mode": "list,form,kanban",
                "domain": [("id", "in", created_ids)],
                "target": "current",
            }
        else:
            raise UserError(_("Nenhum contrato foi criado com sucesso."))
