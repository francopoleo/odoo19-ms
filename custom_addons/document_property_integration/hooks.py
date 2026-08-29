import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Run document migration after installation.

    Migrates documents to use asset_ids (Many2many) instead of asset_id (Many2one).
    """
    try:
        _logger.info("[document_property_integration] Starting post_init_hook...")
        _logger.info("[document_property_integration] Running document migration (asset_id -> asset_ids)...")

        DocumentModel = env["document.document"]
        DocumentModel._migrate_on_module_load()

        _logger.info("[document_property_integration] post_init_hook completed successfully")
    except Exception as e:
        _logger.warning("[document_property_integration] Document migration skipped (non-critical): %s" % str(e))
        try:
            env.cr.rollback()
        except:
            pass
        # Never raise - allow Odoo to continue installation
