# Troubleshooting — Governance & Audit

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| Artigo contextual não aparece | Falta bloco `HELP:ARTICLE` ou contexto não corresponde ao model/view | Revisar `docs/08_AJUDA_CONTEXTUAL.md`, importar docs e verificar Mapa de Contextos. |
| Artigo completo aparece no drawer | Artigo importado como `Documento completo` marcado para contexto | Ajustar `show_in_context: false` ou escopo do artigo. |
| Importação duplicou artigo | `code` diferente para o mesmo conteúdo | Padronizar `code` único por módulo/model/view/fluxo. |
| Tabela Markdown não renderiza | Central antiga ou Markdown mal formatado | Atualizar Central e usar tabela com linha `|---|---|`. |
| Opções no texto estão desatualizadas | Manual listou opções configuráveis manualmente | Remover lista fixa e deixar a seção dinâmica exibir opções reais. |
| Usuário não encontra filtro citado | Filtro mudou na search view | Explicar cenário de uso; a Central mostra filtros reais. |
| Agenda aparece para usuários errados | Responsáveis/visibilidade incorretos | Revisar responsável, equipe, participantes e regras de acesso. |

## Como diagnosticar documentação contextual

1. Abra a tela com problema.
2. Clique em **Ajuda**.
3. Confira o cabeçalho `model / view`.
4. Vá em **Central de Ajuda > Ajuda Contextual > Mapa de Contextos**.
5. Filtre pelo model.
6. Corrija `08_AJUDA_CONTEXTUAL.md` ou contexto/artigo.
7. Reimporte documentação.

## Comandos úteis

```bash
./odoo-bin -d ms-teste -u governance,common_help_center --stop-after-init
```

## SQL útil em homologação

Use apenas em base de teste quando precisar limpar artigos importados do módulo:

```sql
DELETE FROM help_article WHERE module_name = 'governance';
DELETE FROM help_context WHERE module_name = 'governance';
```
