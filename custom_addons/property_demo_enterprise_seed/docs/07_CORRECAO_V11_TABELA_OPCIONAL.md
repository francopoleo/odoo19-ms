# Correção v11 — models opcionais com `_auto=False` e tabela ausente

## Problema

Em alguns bancos, o model opcional `common.communication.base` permanecia no registry, mas a tabela física `common_communication_base` não existia no PostgreSQL.

A versão anterior ignorava a checagem de tabela quando o model tinha `_auto=False`, permitindo que o `create()` chegasse ao banco e gerasse:

```text
ERROR: relation "common_communication_base" does not exist
```

## Correção

A função `_model_table_ready()` agora verifica `to_regclass()` sempre que o model possui `_table`, independentemente de `_auto=True` ou `_auto=False`.

Também foi reforçado o tratamento de erro em `_safe_create_optional()`: se o PostgreSQL sinalizar relação/tabela inexistente, o model é marcado como ignorado pelo restante da execução para não repetir o mesmo erro no log.

## Efeito esperado

Se `common.communication.base` ou qualquer outro model opcional existir no registry mas não tiver tabela/view física, o seed pula silenciosamente aquele bloco e continua gerando os demais dados.
