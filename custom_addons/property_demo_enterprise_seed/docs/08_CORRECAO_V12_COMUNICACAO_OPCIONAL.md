# Correção v12 — comunicação opcional com tabela ausente

## Problema

Em algumas bases, o model `common.communication.base` aparece no registry, mas a tabela física `common_communication_base` não existe no PostgreSQL.

Isso gerava logs do tipo:

```text
ERROR: relation "common_communication_base" does not exist
```

## Correção

- Adicionado helper `_table_exists()` com `to_regclass()`.
- `_model_table_ready()` agora usa esse helper para qualquer model com `_table`.
- A criação de `common.agenda.event` e `common.communication.base` agora faz pré-checagem explícita antes do loop.
- Quando a relação física está ausente, o model é marcado como ignorado pelo restante da execução, sem repetir erro para cada registro.
- Adicionado log de versão no início de `action_generate()` e `action_clear()`.

## Resultado esperado

Se `common.communication.base` não tiver tabela, a massa continua normalmente e apenas pula comunicações comuns.
