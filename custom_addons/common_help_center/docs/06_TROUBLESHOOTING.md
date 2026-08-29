# Troubleshooting — Central de Ajuda

## Problemas comuns

| Problema | Causa provável | Solução |
| --- | --- | --- |
| Menu não aparece | Grupo/permissão ou módulo não instalado | Atualizar módulo, revisar grupos e ACLs. |
| Erro de view XML | XPath ou campo inexistente | Conferir traceback e ajustar view herdada. |
| Atividade aparece em módulo errado | Tipo de atividade não restringido por model | Revisar tipos de atividade e contexto. |
| Agenda não aparece | Falta responsável/data ou sincronização | Preencher responsável/prazo e sincronizar Agenda Geral. |
| Artigo não aparece no drawer | Falta `HELP:ARTICLE` ou contexto | Atualizar `docs/08_AJUDA_CONTEXTUAL.md` e importar docs. |
| Tabela Markdown não formata | Renderizador antigo ou artigo não re-renderizado | Atualizar `common_help_center`, clicar Renderizar Markdown ou reimportar documentação. |

## Comandos úteis

```bash
./odoo-bin -d ms -u common_help_center --stop-after-init
```

```sql
DELETE FROM ir_attachment WHERE url LIKE '/web/assets/%';
```

## Erro: Missing required value for the field Código (code) ao importar documentação

### Causa

Um arquivo `docs/08_AJUDA_CONTEXTUAL.md` estava sem blocos `HELP:ARTICLE` e sem metadados com `code`. Em versões anteriores, o importador tentava criar um artigo contextual único sem código.

### Solução

A partir da v16, arquivos `08_AJUDA_CONTEXTUAL.md` sem blocos contextuais são ignorados. Para criar ajuda contextual, use blocos no padrão:

```markdown
<!-- HELP:ARTICLE
code: modulo.model.view.nome_unico
module: nome_modulo
model: nome.model
view_type: form
title: Título do artigo
-->
# Conteúdo
<!-- /HELP:ARTICLE -->
```
