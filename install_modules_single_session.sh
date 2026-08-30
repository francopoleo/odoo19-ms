#!/bin/bash

# Script de instalação em sessão única para evitar erro de concorrência
# Apenas módulos que realmente existem no projeto

set -e

DB_NAME="ms"
PYTHON_BIN="./.venv/bin/python"
ODOO_BIN="odoo-bin"
CONFIG="odoo.conf"

# Lista de módulos a instalar na ordem correta (APENAS módulos que existem)
MODULES=(
  # Fase 1: Base
  "common_base"
  "common_help_center"

  # Fase 2: Principais
  "property_core"
  "document_core"
  "governance"

  # Fase 3: Integrações - Property
  "property_valuation_engine"
  "property_condominium_enterprise"
  "property_contract_amendment_enterprise"
  "property_contract_history"
  "property_payment_proof"
  "property_portal_integration"
  "property_document_portal"
  "property_website_integration"

  # Fase 4: Integrações - Document
  "document_governance_integration"
  "document_property_integration"
  "document_portal_integration"
  "document_dossier"
  "document_dossier_property"
  "document_dossier_governance"
  "document_s3_storage"

  # Fase 5: Integrações - Governance
  "governance_property_integration"
  "governance_portal_integration"

  # Fase 6: Localização Brasileira
  "l10n_br_partner_cep_identity"

  # Fase 7: Pagamentos e Documentos Fiscais
  "payment_pix"
  "account_latam_provisional_post"

  # Fase 8: Seed/Demo
  "property_contract_ocr_template"
  "enterprise_configuration_seed"

  # Fase 9: Utilitários (utils_addons)
  "auto_database_backup"
#  "code_backend_theme"
#  "dynamic_accounts_report"
)

echo "================================================"
echo "🚀 Instalando módulos Odoo 19 MS (sessão única)"
echo "================================================"
echo ""

# Apaga banco de dados se existir
echo "🗑️  Verificando banco de dados anterior..."
if psql -U franco -h localhost -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
  echo "⚠️  Banco '$DB_NAME' encontrado. Terminando conexões..."
  psql -U franco -h localhost postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$DB_NAME' AND pid != pg_backend_pid();" 2>/dev/null || true
  sleep 1
  echo "⚠️  Apagando banco..."
  dropdb -U franco -h localhost $DB_NAME
  echo "✅ Banco anterior apagado"
else
  echo "✅ Banco não existe (novo)"
fi
echo ""

# Cria novo banco de dados
echo "📁 Criando novo banco de dados '$DB_NAME'..."
createdb -U franco -h localhost $DB_NAME
echo "✅ Banco de dados criado"
echo ""

# Cria string com os módulos separados por vírgula
MODULES_STR=$(IFS=, ; echo "${MODULES[*]}")

echo "📦 Instalando ${#MODULES[@]} módulos..."
echo "Módulos: $MODULES_STR"
echo ""

$PYTHON_BIN $ODOO_BIN --conf=$CONFIG -d $DB_NAME -i "$MODULES_STR" --stop-after-init

echo ""
echo "================================================"
echo "✅ Instalação concluída com sucesso!"
echo "================================================"
echo ""
echo "Total de módulos instalados: ${#MODULES[@]}"
echo ""
echo "🚀 Inicie o Odoo com:"
echo "   ./.venv/bin/python odoo-bin --conf=odoo.conf"
echo ""
