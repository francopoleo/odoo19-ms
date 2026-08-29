# Guia de Deploy e Atualização

## Ordem recomendada

1. Fazer backup do banco.
2. Substituir módulos no `custom_addons`.
3. Atualizar módulos base/integradores antes dos módulos finais.
4. Rodar testes funcionais.
5. Reimportar documentação na Central de Ajuda.
6. Validar Mapa de Contextos.

## Comando padrão

```bash
./odoo-bin -d ms -u common_base,common_help_center,document_core,document_dossier,governance,property_core --stop-after-init
```

## Limpeza de assets quando necessário

```sql
DELETE FROM ir_attachment WHERE url LIKE '/web/assets/%';
```
