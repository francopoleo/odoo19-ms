# 🚀 Setup S3 — Guia Rápido

**Um arquivo `odoo.conf` em desenvolvimento E produção. Sem duplicatas!**

---

## ⚡ 2 Minutos: Quick Start

### Desenvolvimento (seu Mac)

```bash
# 1. Instalar dependência
pip install boto3

# 2. Rodar Odoo (S3 já desabilitado)
odoo --db=odoo19_ms

# 3. Pronto! Arquivo local automático ✅
```

### Produção (seu servidor)

```bash
# 1. Instalar dependência
sudo pip install boto3

# 2. Escolha UMA opção para configurar S3:

# OPÇÃO A: Settings Odoo (mais fácil)
# https://seu-servidor.com
# → Seu nome → Settings → S3
# → Preencha credenciais → Salve

# OPÇÃO B: Variáveis de Ambiente (mais seguro)
nano ~/.bashrc
# Adicione: export ODOO_S3_*=...
source ~/.bashrc

# OPÇÃO C: odoo.conf
nano /etc/odoo/odoo.conf
# Adicione: s3_endpoint = ...

# 3. Restart Odoo
sudo systemctl restart odoo

# 4. Pronto! S3 automático ✅
```

---

## 📋 Documentação Completa

Veja [custom_addons/document_s3_storage/README.md](custom_addons/document_s3_storage/README.md) para:

- ✅ Todas as 3 formas de configuração (Settings, Env, conf)
- ✅ Migração de arquivos existentes
- ✅ Troubleshooting
- ✅ Custos e benchmarks
- ✅ Docker / CI-CD

---

## ✅ Checklist

### Dev
- [ ] `pip install boto3`
- [ ] Instalar módulo
- [ ] Criar documento + upload
- [ ] Arquivo em `/opt/odoo/var/filestore/`
- [ ] ✅ Pronto!

### Prod
- [ ] `pip install boto3`
- [ ] Configurar S3 (Settings OU Env OU conf)
- [ ] Restart Odoo
- [ ] Criar documento + upload
- [ ] Arquivo em DigitalOcean Console
- [ ] ✅ Pronto!

---

**Para mais: veja README.md**