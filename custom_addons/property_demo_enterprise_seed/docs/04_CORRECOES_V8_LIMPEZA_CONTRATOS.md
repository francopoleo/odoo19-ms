# Correções v8 — limpeza completa de contratos DEMO-IMOB

A limpeza agora identifica contratos DEMO-IMOB mesmo quando o campo `name` foi alterado por sequência/ativação do contrato.

Critérios usados para localizar contratos de teste:

- `property.contract.name` contendo `DEMO-IMOB`;
- `property.contract.additional_clauses` contendo `DEMO-IMOB`;
- locatário/parceiro vinculado com nome `DEMO-IMOB`;
- parcelas, recebimentos e pagadores autorizados vinculados ao contrato;
- referências indiretas em comprovantes e notas.

Também foi melhorado o `unlink`: se o lote falhar por um único registro preso por FK/regra, o gerador tenta apagar item a item e registra no log somente o que ficou bloqueado.
