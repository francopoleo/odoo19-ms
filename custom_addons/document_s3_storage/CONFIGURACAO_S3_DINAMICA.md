# ⚡ Configuração Dinâmica S3 — 3 Opções

**O módulo `document_s3_storage` configura S3 automaticamente, sem precisar de múltiplos odoo.conf!**

---

## 🎯 Comparação das 3 Opções

| Opção | Onde Usar | Facilidade | Segurança |
|-------|-----------|-----------|-----------|
| **1. Settings Odoo** | Dev + Prod | ⭐⭐⭐⭐⭐ Muito fácil | ⭐⭐⭐⭐ (criptografado no BD) |
| **2. Variáveis Ambiente** | Dev + Prod + Docker | ⭐⭐⭐⭐ Fácil | ⭐⭐⭐⭐⭐ (não em arquivo) |
| **3. odoo.conf** | Fallback | ⭐⭐⭐ Médio | ⭐⭐⭐ (arquivo) |

---

## ✅ OPÇÃO 1: Via Settings do Odoo (Recomendado)

### Desenvolvimento (seu Mac)

```
1. Abra: http://localhost:8069
2. Login como admin
3. Clique seu nome (top-right) → Settings
4. Busque: "S3"
5. Marque: ☑️ "Habilitar S3/DigitalOcean Spaces"
6. Deixe em branco (desabilitado)
7. Salve
```

✅ Pronto! Desenvolvimento funcionando com storage local.

### Produção (seu servidor)

```
1. SSH no servidor
2. Abra Odoo: https://seu-servidor.com
3. Login como admin
4. Clique seu nome (top-right) → Settings
5. Busque: "S3"
6. Marque: ☑️ "Habilitar S3/DigitalOcean Spaces"
7. Preencha:
   Endpoint:    https://nyc3.digitaloceanspaces.com
   Access Key:  DO00XXXXXXXXXXXX
   Secret Key:  XXXXXXXXXXXXXXXX
   Bucket:      seu-bucket-odoo
   Region:      nyc3
8. Clique: "Testar Conexão"
9. Se OK, salve
```

✅ Pronto! Produção usando S3 automaticamente.

**Vantagens:**
- ✅ Sem editar arquivos
- ✅ Interface visual
- ✅ Teste de conexão incorporado
- ✅ Um único odoo.conf em dev e prod
- ✅ Configuração salva no BD (persistente)

---

## ✅ OPÇÃO 2: Variáveis de Ambiente

**Para Docker, CI/CD, ou ambiente seguro:**

### Desenvolvimento (seu Mac)

```bash
# Adicione ao ~/.bashrc (Mac) ou ~/.zshrc
export ODOO_S3_ENDPOINT=""
export ODOO_S3_ACCESS_KEY=""
export ODOO_S3_SECRET_KEY=""
export ODOO_S3_BUCKET=""
export ODOO_S3_REGION="nyc3"

# Recarregue:
source ~/.zshrc

# Inicie Odoo:
odoo --db=odoo19_ms
```

✅ Pronto! S3 desabilitado (variáveis vazias).

### Produção (seu servidor)

```bash
# SSH no servidor
ssh usuario@seu-servidor

# Edite ~/.bashrc ou /etc/environment
nano ~/.bashrc

# Adicione:
export ODOO_S3_ENDPOINT="https://nyc3.digitaloceanspaces.com"
export ODOO_S3_ACCESS_KEY="DO00XXXXXXXXXXXX"
export ODOO_S3_SECRET_KEY="XXXXXXXXXXXXXXXX"
export ODOO_S3_BUCKET="seu-bucket-odoo"
export ODOO_S3_REGION="nyc3"

# Salve e teste:
source ~/.bashrc
echo $ODOO_S3_BUCKET  # Deve mostrar seu bucket

# Inicie Odoo:
sudo systemctl restart odoo
```

✅ Pronto! S3 habilitado automaticamente via environment.

**Vantagens:**
- ✅ Credenciais não em arquivo
- ✅ Ideal para Docker: `ENV ODOO_S3_*=...`
- ✅ CI/CD compatível
- ✅ Um único odoo.conf em dev e prod
- ✅ Máximo segurança

---

## ✅ OPÇÃO 3: odoo.conf (Fallback)

**Se nenhuma das anteriores estiver configurada:**

```ini
# ~/.odoorc (Dev) ou /etc/odoo/odoo.conf (Prod)
[options]
addons_path = /opt/odoo/addons
db_host = localhost
db_user = odoo

# OPCIONAL - S3
s3_endpoint = https://nyc3.digitaloceanspaces.com
s3_access_key = DO00XXXXXXXXXXXX
s3_secret_key = XXXXXXXXXXXXXXXX
s3_bucket = seu-bucket-odoo
s3_region = nyc3
```

**Vantagens:**
- ✅ Simples
- ✅ Tradicional

**Desvantagens:**
- ❌ Credenciais em arquivo
- ❌ Difícil de manter sincronizado dev/prod

---

## 🚀 Minha Recomendação

### Para Desenvolvimento
```
Use OPÇÃO 1 (Settings)
├─ Deixe S3 desabilitado em Settings
├─ Arquivos locais automaticamente
└─ Sem configuração necessária
```

### Para Produção
```
Use OPÇÃO 2 (Variáveis de Ambiente)
├─ Defina ODOO_S3_* no servidor
├─ Criptografe com PM2/systemd
└─ Máxima segurança
```

---

## 🔄 Fluxo Automático (Invisível)

```
Dev Local
  ↓
Usuário faz upload
  ↓
Módulo verifica:
  1. Settings do Odoo habilitado? Não ✅
  2. Variáveis de ambiente? Não ✅
  3. odoo.conf S3? Não ✅
  ↓
S3 DESABILITADO
  ↓
Arquivo salva em: /opt/odoo/var/filestore/...
  ↓
✅ Funciona!


Produção
  ↓
Usuário faz upload
  ↓
Módulo verifica:
  1. Settings do Odoo habilitado? Sim! ✅
  2. Credenciais válidas? Sim! ✅
  ↓
S3 HABILITADO
  ↓
Arquivo sobe para DigitalOcean automaticamente
  ↓
✅ Funciona!
```

---

## ✔️ Checklist: Seu Setup

### Desenvolvimento (seu Mac)

```
☐ 1. Instalar: pip install boto3
☐ 2. Rodar Odoo normalmente
☐ 3. Verificar: Settings → S3 (desabilitado)
☐ 4. Criar documento + upload
☐ 5. Verificar arquivo em: /opt/odoo/var/filestore/...
☐ 6. ✅ Pronto!
```

### Produção (seu servidor)

```
☐ 1. Instalar: pip install boto3
☐ 2. Definir ODOO_S3_* em ~/.bashrc
☐ 3. Restart Odoo: sudo systemctl restart odoo
☐ 4. Verificar logs: tail /var/log/odoo/odoo.log
☐ 5. Criar documento + upload
☐ 6. Verificar em DigitalOcean Console
☐ 7. ✅ Pronto!
```

---

## 🔒 Segurança

### Variáveis de Ambiente (mais seguro)

```bash
# Usar systemd overlay:
sudo mkdir -p /etc/systemd/system/odoo.service.d
sudo nano /etc/systemd/system/odoo.service.d/environment.conf
```

Adicione:
```ini
[Service]
Environment="ODOO_S3_ENDPOINT=https://nyc3.digitaloceanspaces.com"
Environment="ODOO_S3_ACCESS_KEY=DO00..."
Environment="ODOO_S3_SECRET_KEY=..."
Environment="ODOO_S3_BUCKET=seu-bucket"
```

Salve, depois:
```bash
sudo systemctl daemon-reload
sudo systemctl restart odoo
```

**Credenciais não ficam em arquivo!** ✅

---

## 🆘 Troubleshooting

### Dev: Arquivo não subindo para S3

```
Esperado! S3 está desabilitado em dev.
Arquivo vai para: /opt/odoo/var/filestore/...
```

### Prod: Arquivo não subindo para S3

```bash
# 1. Verificar variáveis:
printenv | grep ODOO_S3

# 2. Se vazio, adicionar e restart:
export ODOO_S3_*=...
sudo systemctl restart odoo

# 3. Verificar logs:
tail -100 /var/log/odoo/odoo.log | grep -i s3
```

### Erro: "No module named boto3"

```bash
pip install boto3
# ou
sudo pip install boto3
```

---

## 📊 Resumo: Um arquivo odoo.conf em Todo Lugar

```ini
# /etc/odoo/odoo.conf (IDÊNTICO em dev e prod!)
[options]
addons_path = /opt/odoo/addons
db_host = localhost
db_user = odoo
workers = 4
# Sem S3 aqui! Usa Settings ou Env vars
```

Depois:
- **Dev:** Settings → S3 desabilitado → arquivo local
- **Prod:** Env vars ODOO_S3_* → S3 automático

🎉 **Transparente e seguro!**