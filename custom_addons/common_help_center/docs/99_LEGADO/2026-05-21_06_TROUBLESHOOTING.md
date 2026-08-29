# Troubleshooting - Central de Ajuda

## Artigos aparecem duplicados

### Causa provável

Códigos diferentes para o mesmo conteúdo.

### Solução

Padronize o campo `code` no frontmatter ou no bloco `HELP:ARTICLE`.

## Manual completo aparece no drawer

### Causa provável

O artigo está com `show_in_context = True` ou `scope` diferente de `full_document`.

### Solução

Para manuais completos, use:

```text
scope: full_document
show_in_context: false
```

## Contexto detecta model/view, mas não mostra artigo

### Causa provável

Não existe `help.context` ou artigo com `show_in_context=True` vinculado ao contexto.

### Solução

1. Abra **Mapa de Contextos**.
2. Filtre por **Sem contexto** ou **Contexto sem artigo**.
3. Crie/vincule artigo ou adicione bloco em `08_AJUDA_CONTEXTUAL.md`.

## Importação não atualiza artigo editado

### Causa provável

A fonte está com política `Preservar edições feitas no Odoo` e o artigo foi editado manualmente.

### Solução

Troque a política da fonte para `Sobrescrever sempre pelo Markdown` ou desmarque o controle de edição manual após revisar.

## Mapa de Contextos está muito grande

### Causa provável

Foi gerado para todos os módulos instalados.

### Solução

Use a opção **Somente módulos com docs** no importador.
