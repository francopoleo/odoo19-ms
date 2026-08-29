# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


def _ensure_res_partner_schema(env):
    """Create missing columns in res_partner table for property_core extensions."""
    cr = env.cr

    # List of columns to create: (column_name, column_type)
    columns_to_create = [
        ('mobile', 'varchar'),
        ('creci', 'varchar'),
        ('commission_rate', 'numeric'),
        ('bank_name', 'varchar'),
        ('bank_agency', 'varchar'),
        ('bank_account', 'varchar'),
        ('budget_min', 'numeric'),
        ('budget_max', 'numeric'),
        ('currency_id', 'integer'),
        ('investment_profile', 'varchar'),
    ]

    # Check which columns exist
    cr.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'res_partner'
        AND column_name IN %s
    """, (tuple([col[0] for col in columns_to_create]),))

    existing_columns = {row[0] for row in cr.fetchall()}

    # Create missing columns
    for col_name, col_type in columns_to_create:
        if col_name not in existing_columns:
            try:
                if col_type == 'integer':
                    sql = f'ALTER TABLE res_partner ADD COLUMN {col_name} {col_type} DEFAULT NULL'
                elif col_type == 'numeric':
                    sql = f'ALTER TABLE res_partner ADD COLUMN {col_name} {col_type}(16,2) DEFAULT NULL'
                else:  # varchar
                    sql = f'ALTER TABLE res_partner ADD COLUMN {col_name} {col_type} DEFAULT NULL'

                cr.execute(sql)
                _logger.info(f"[property_core] Created column res_partner.{col_name}")
            except Exception as e:
                _logger.warning(f"[property_core] Could not create column {col_name}: {str(e)}")

    cr.commit()


def _disable_binary_tracking(env):
    """Disable mail tracking for binary fields left by old development versions."""
    env.cr.execute("""
        UPDATE ir_model_fields
           SET tracking = 0
         WHERE model IN ('property.asset', 'property.media', 'property.complex')
           AND ttype = 'binary'
           AND COALESCE(tracking, 0) <> 0
    """)



def pre_init_hook(env):
    """Remove cached views BEFORE loading XML to avoid validation errors.

    Note: In Odoo 19, pre_init_hook receives only env, not cr and registry.
    """
    try:
        _logger.info("[property_core] Starting pre_init_hook: ensuring schema...")
        _ensure_res_partner_schema(env)

        _logger.info("[property_core] Clearing old views...")

        cr = env.cr

        # Step 1: Find parent view IDs via ir_model_data
        sql_find_parents = """
            SELECT res_id FROM ir_model_data
            WHERE module = 'property_core'
            AND name IN (
                'view_property_contract_form',
                'view_property_complex_form',
                'view_property_asset_form',
                'view_property_owner_form',
                'view_property_tenant_form',
                'view_property_broker_form'
            )
            AND model = 'ir.ui.view'
        """
        cr.execute(sql_find_parents)
        parent_view_ids = [row[0] for row in cr.fetchall()]
        _logger.info(f"[property_core] Found parent view IDs: {parent_view_ids}")

        # Step 2: Find and delete child views (inherited views)
        if parent_view_ids:
            placeholders = ','.join(['%s'] * len(parent_view_ids))
            sql_delete_children = f"""
                DELETE FROM ir_ui_view
                WHERE inherit_id IN ({placeholders})
            """
            cr.execute(sql_delete_children, parent_view_ids)
            affected = cr.rowcount
            _logger.info(f"[property_core] Deleted {affected} inherited views")

        # Step 3: Delete parent views
        if parent_view_ids:
            placeholders = ','.join(['%s'] * len(parent_view_ids))
            sql_delete_parent = f"""
                DELETE FROM ir_ui_view
                WHERE id IN ({placeholders})
            """
            cr.execute(sql_delete_parent, parent_view_ids)
            affected = cr.rowcount
            _logger.info(f"[property_core] Deleted {affected} parent views")

        # Step 4: Clean up ir_model_data entries
        sql_delete_data = """
            DELETE FROM ir_model_data
            WHERE module = 'property_core'
            AND name IN (
                'view_property_contract_form',
                'view_property_complex_form',
                'view_property_asset_form',
                'view_property_owner_form',
                'view_property_tenant_form',
                'view_property_broker_form'
            )
            AND model = 'ir.ui.view'
        """
        cr.execute(sql_delete_data)
        _logger.info(f"[property_core] Cleaned up ir_model_data entries")

        cr.commit()
        _logger.info("[property_core] pre_init_hook completed successfully")

    except Exception as e:
        _logger.exception("[property_core] Error in pre_init_hook: %s" % str(e))
        env.cr.rollback()
        # Don't raise, allow Odoo to continue


def post_init_hook(env):
    """Cleanup hook after initialization.

    Note: In Odoo 19, post_init_hook also receives only env.
    This hook is designed to be fault-tolerant during module installation.
    """
    try:
        _logger.info("[property_core] Starting post_init_hook...")
        _logger.info("[property_core] Running media cleanup...")

        try:
            _disable_binary_tracking(env)
        except Exception as tracking_error:
            _logger.warning("[property_core] Binary tracking disable failed (non-critical): %s" % str(tracking_error))

        # Clean up mídias with both image_1920 and file_data populated
        # This is optional and should not block module installation
        try:
            env.cr.execute("""
                SELECT EXISTS(
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'property_media'
                )
            """)
            table_exists = env.cr.fetchone()[0]
            if table_exists:
                try:
                    PropertyMedia = env['property.media']
                    PropertyMedia.action_cleanup_binary_conflicts()
                except Exception as cleanup_error:
                    _logger.warning("[property_core] Media cleanup skipped (non-critical): %s" % str(cleanup_error))
        except Exception as check_error:
            _logger.warning("[property_core] Could not check property_media table: %s" % str(check_error))

        _logger.info("[property_core] post_init_hook completed")

    except Exception as e:
        _logger.exception("[property_core] Unexpected error in post_init_hook: %s" % str(e))
        try:
            env.cr.rollback()
        except:
            pass
        # Never raise - allow Odoo to continue installation