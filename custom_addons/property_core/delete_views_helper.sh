#!/bin/bash
# Helper script to delete cached views from PostgreSQL database
# Run this if the pre_init_hook doesn't work

# Usage: ./delete_views_helper.sh <db_name>
# Example: ./delete_views_helper.sh ms

if [ -z "$1" ]; then
    echo "Usage: $0 <database_name>"
    echo "Example: $0 ms"
    exit 1
fi

DB_NAME="$1"

echo "[property_core] Connecting to database: $DB_NAME"

# Delete child views first
psql -d "$DB_NAME" -c "
    DELETE FROM ir_ui_view
    WHERE inherit_id IN (
        SELECT id FROM ir_ui_view
        WHERE module = 'property_core'
        AND name IN ('view_property_contract_form', 'view_property_complex_form', 'view_property_asset_form')
    );
"

echo "[property_core] Deleted inherited views"

# Delete parent views
psql -d "$DB_NAME" -c "
    DELETE FROM ir_ui_view
    WHERE module = 'property_core'
    AND name IN ('view_property_contract_form', 'view_property_complex_form', 'view_property_asset_form');
"

echo "[property_core] Deleted parent views"

# Clean up ir_model_data
psql -d "$DB_NAME" -c "
    DELETE FROM ir_model_data
    WHERE module = 'property_core'
    AND name IN ('view_property_contract_form', 'view_property_complex_form', 'view_property_asset_form')
    AND model = 'ir.ui.view';
"

echo "[property_core] Cleaned up ir_model_data"
echo "[property_core] Done! You can now restart Odoo."