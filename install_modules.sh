#!/bin/bash

# Script de instalação automática de módulos Odoo 19 MS
# Segue a ordem correta conforme INSTALLATION_ORDER.md

set -e

DB_NAME="ms"
PYTHON_BIN="./.venv/bin/python"
ODOO_BIN="odoo-bin"
CONFIG="odoo.conf"

echo "================================================"
echo "🚀 Instalando módulos Odoo 19 MS"
echo "================================================"
echo ""

# Fase 1: Base modules
echo "📦 FASE 1: Módulos Base..."
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i common_base --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i common_help_center --stop-after-init

# Fase 2: Módulos Principais
echo "📦 FASE 2: Módulos Principais..."
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_core --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i document_core --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i governance --stop-after-init

# Fase 3: Integrações e Extensões
echo "📦 FASE 3: Integrações e Extensões..."
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_valuation_engine --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i governance_property_integration --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i document_governance_integration --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i document_property_integration --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_condominium_enterprise --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_contract_amendment_enterprise --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_contract_history --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_payment_proof --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_portal_integration --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_website_integration --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i property_demo_enterprise_seed --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i document_portal_integration --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i governance_portal_integration --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i partner_overview --stop-after-init

# Fase 4: Localização Brasileira
echo "📦 FASE 4: Localização Brasileira..."
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i l10n_br_base --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i l10n_br_coa --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i l10n_br_crm --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i l10n_br_hr --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i l10n_br_resource --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i l10n_br_zip --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i l10n_br_currency_rate_update --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i l10n_br_account_due_list --stop-after-init

# Fase 5: Utilitários
echo "📦 FASE 5: Utilitários..."
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i auto_database_backup --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i code_backend_theme --stop-after-init
$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i dynamic_accounts_report --stop-after-init

echo ""
echo "================================================"
echo "✅ Instalação concluída com sucesso!"
echo "================================================"
echo ""
echo "🚀 Inicie o Odoo com:"
echo "   ./.venv/bin/python odoo-bin --conf=odoo.conf"
echo ""
