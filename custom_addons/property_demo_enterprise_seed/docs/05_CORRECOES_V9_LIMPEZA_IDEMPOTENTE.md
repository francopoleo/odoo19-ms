# Correções v9 — limpeza idempotente em base limpa

Esta versão corrige o botão **Apagar massa DEMO-IMOB** para funcionar também quando nenhuma massa demo foi criada.

## Problema

A limpeza varria muitos models opcionais mesmo em bases limpas. Em ambientes com módulos parcialmente instalados, tabelas ausentes, views SQL antigas ou campos removidos, essa varredura podia causar RPC_ERROR mesmo sem haver dados `DEMO-IMOB` para apagar.

## Ajustes

- Adicionado marcador rápido em `res.partner`, `property.asset` e `property.contract` antes da varredura completa.
- Se não houver marcador central `DEMO-IMOB`, o botão retorna zero apagados sem consultar os módulos opcionais.
- `action_clear` passou a ter barreira geral com `savepoint()` e `rollback()` defensivo.
- A gravação do resumo do wizard usa `sudo()` para evitar erro secundário de regra/acesso em `TransientModel`.
- A geração com limpeza prévia também foi protegida para não misturar dados caso a limpeza falhe.
