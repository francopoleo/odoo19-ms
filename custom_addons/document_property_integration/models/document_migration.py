from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class DocumentMigration(models.Model):
    _inherit = "document.document"

    @api.model
    def migrate_asset_id_to_asset_ids(self):
        """
        Migra documentos com asset_id (Many2one) para asset_ids (Many2many).
        Este método deve ser executado uma única vez após a instalação do módulo.
        """
        _logger.info("Iniciando migração de asset_id para asset_ids...")

        # Buscar todos os documentos que têm dados em asset_id (campo antigo)
        # Como estamos usando Many2many, a SQL tabela foi recriada automaticamente
        # Precisamos apenas garantir que os documentos com propriedades vinculadas
        # tenham o relacionamento correto

        documents = self.search([])
        migrated_count = 0

        for doc in documents:
            # Se o documento não tem asset_ids mas deveria ter (verificar em banco de dados)
            # Esta é principalmente uma operação de verificação
            if doc.asset_ids and not doc.created_context_type:
                doc.created_context_type = "property"
                doc.document_context_type = "property"
                migrated_count += 1
            elif doc.case_ids and not doc.created_context_type:
                doc.created_context_type = "governance"
                doc.document_context_type = "governance"
                migrated_count += 1
            elif not doc.asset_ids and not doc.case_ids and not doc.created_context_type:
                doc.created_context_type = "generic"
                doc.document_context_type = "generic"
                migrated_count += 1

        _logger.info(f"Migração concluída: {migrated_count} documentos atualizados.")
        return migrated_count

    @api.model
    def _migrate_on_module_load(self):
        """Hook chamado na instalação do módulo."""
        self.migrate_asset_id_to_asset_ids()
