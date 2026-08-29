# Correções v7 - Models opcionais com tabela ausente

Esta versão torna o gerador mais tolerante quando o model ainda aparece no registry do Odoo, mas a tabela física não existe no PostgreSQL.

## Caso corrigido

Exemplo observado em `common.communication.base`:

```text
ERROR: relation "common_communication_base" does not exist
```

O gerador agora verifica `to_regclass(<tabela>)` antes de fazer `search`, `create` ou limpeza nos models opcionais. Quando a tabela não existe, o model é ignorado uma única vez na execução.

## Recursão em property.lead

Se `property.lead` ainda estiver com o bug de recursão no projeto principal, o seed deixa de tentar criar novos leads depois do primeiro `RecursionError`, evitando centenas de logs repetidos.

O correto continua sendo aplicar o patch no `property_core/models/property_lead.py` para corrigir a sincronização com `res.partner`.
