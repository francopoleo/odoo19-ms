#!/bin/bash

# ============================================================
# SETUP DigitalOcean Spaces para Odoo
# ============================================================
# Este script ajuda a configurar o DigitalOcean Spaces
# e gerar as chaves de acesso

set -e

echo "============================================================"
echo "DigitalOcean Spaces Setup para Odoo 19"
echo "============================================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================================
# PASSO 1: Verificar Pré-requisitos
# ============================================================
echo -e "${YELLOW}[1/5] Verificando pré-requisitos...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 não encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 encontrado${NC}"

if ! python3 -c "import boto3" 2>/dev/null; then
    echo -e "${YELLOW}ℹ Installing boto3...${NC}"
    pip3 install boto3 --quiet
    echo -e "${GREEN}✓ boto3 instalado${NC}"
else
    echo -e "${GREEN}✓ boto3 já instalado${NC}"
fi

echo ""

# ============================================================
# PASSO 2: Coletar Informações
# ============================================================
echo -e "${YELLOW}[2/5] Coletando informações...${NC}"
echo ""

read -p "Nome do seu Space (ex: odoo-documents): " SPACE_NAME
read -p "Região (nyc3, sfo3, sgp1, ams3, fra1, lon1, blr1, syd1, tor1): " REGION

# Validar região
VALID_REGIONS=("nyc3" "sfo3" "sgp1" "ams3" "fra1" "lon1" "blr1" "syd1" "tor1")
if [[ ! " ${VALID_REGIONS[@]} " =~ " ${REGION} " ]]; then
    echo -e "${RED}✗ Região inválida!${NC}"
    exit 1
fi

# Endpoint mapping
case $REGION in
    nyc3) ENDPOINT="https://nyc3.digitaloceanspaces.com" ;;
    sfo3) ENDPOINT="https://sfo3.digitaloceanspaces.com" ;;
    sgp1) ENDPOINT="https://sgp1.digitaloceanspaces.com" ;;
    ams3) ENDPOINT="https://ams3.digitaloceanspaces.com" ;;
    fra1) ENDPOINT="https://fra1.digitaloceanspaces.com" ;;
    lon1) ENDPOINT="https://lon1.digitaloceanspaces.com" ;;
    blr1) ENDPOINT="https://blr1.digitaloceanspaces.com" ;;
    syd1) ENDPOINT="https://syd1.digitaloceanspaces.com" ;;
    tor1) ENDPOINT="https://tor1.digitaloceanspaces.com" ;;
esac

read -p "Access Key (DigitalOcean Spaces): " ACCESS_KEY
read -s -p "Secret Key (DigitalOcean Spaces): " SECRET_KEY
echo ""

echo ""

# ============================================================
# PASSO 3: Testar Conexão
# ============================================================
echo -e "${YELLOW}[3/5] Testando conexão com DigitalOcean...${NC}"

python3 << EOF
import boto3
import sys

try:
    s3 = boto3.client(
        's3',
        endpoint_url='$ENDPOINT',
        aws_access_key_id='$ACCESS_KEY',
        aws_secret_access_key='$SECRET_KEY',
        region_name='$REGION',
    )

    # Test: listar buckets
    response = s3.list_buckets()
    print(f"✓ Conexão bem-sucedida!")
    print(f"  Buckets existentes: {len(response.get('Buckets', []))}")

except Exception as e:
    print(f"✗ Erro na conexão: {str(e)}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Credenciais validadas${NC}"
else
    echo -e "${RED}✗ Falha na validação${NC}"
    exit 1
fi

echo ""

# ============================================================
# PASSO 4: Verificar se Space existe
# ============================================================
echo -e "${YELLOW}[4/5] Verificando Space...${NC}"

SPACE_EXISTS=$(python3 << EOF
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='$ENDPOINT',
    aws_access_key_id='$ACCESS_KEY',
    aws_secret_access_key='$SECRET_KEY',
    region_name='$REGION',
)

try:
    s3.head_bucket(Bucket='$SPACE_NAME')
    print("true")
except:
    print("false")
EOF
)

if [ "$SPACE_EXISTS" = "true" ]; then
    echo -e "${GREEN}✓ Space '$SPACE_NAME' já existe${NC}"
else
    echo -e "${YELLOW}ℹ Space não existe, criando...${NC}"

    python3 << EOF
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='$ENDPOINT',
    aws_access_key_id='$ACCESS_KEY',
    aws_secret_access_key='$SECRET_KEY',
    region_name='$REGION',
)

try:
    s3.create_bucket(Bucket='$SPACE_NAME')
    print(f"✓ Space '$SPACE_NAME' criado com sucesso!")
except Exception as e:
    print(f"✗ Erro ao criar Space: {str(e)}")
EOF
fi

echo ""

# ============================================================
# PASSO 5: Gerar arquivo de configuração
# ============================================================
echo -e "${YELLOW}[5/5] Gerando configuração...${NC}"

cat > /tmp/s3_config.txt << EOF
# ========== Configuração para odoo.conf ==========
s3_endpoint = $ENDPOINT
s3_access_key = $ACCESS_KEY
s3_secret_key = $SECRET_KEY
s3_bucket = $SPACE_NAME
s3_region = $REGION
# ================================================
EOF

echo -e "${GREEN}✓ Configuração gerada!${NC}"
echo ""
echo "Adicione as seguintes linhas ao seu odoo.conf (em produção):"
echo ""
cat /tmp/s3_config.txt
echo ""

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}Setup concluído com sucesso!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "Próximos passos:"
echo "1. Copie a configuração acima para seu odoo.prod.conf"
echo "2. Instale o módulo: document_s3_storage"
echo "3. Reinicie o Odoo"
echo ""