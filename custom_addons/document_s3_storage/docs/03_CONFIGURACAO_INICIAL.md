# Configuração Inicial — Document S3 Storage

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Pré-requisitos

- Módulo instalado e atualizado sem erro.
- Usuários internos com grupos corretos.
- Dados mestres mínimos cadastrados.
- Central de Ajuda instalada para exibir artigos contextuais.

## 2. Configurações do módulo

Configure os cadastros de apoio antes de iniciar operação. Exemplos variam por módulo:

| Tipo de configuração | Exemplos | Impacto na ajuda dinâmica |
|---|---|---|
| Categorias | categorias documentais, categorias de mídia, categorias de caso | Aparecem no drawer como opções reais. |
| Tipos | tipos de documento, tipos de caso, tipos de contrato | Aparecem como opções relacionadas quando o campo existir na tela. |
| Responsáveis/equipe | usuários internos, responsáveis principais, equipes | Afetam atividades, visibilidade e Agenda Geral. |
| Status/etapas | estados do processo, etapas de manutenção, revisão ou validação | Campos `selection` são exibidos automaticamente pela Central. |
| Filtros/search views | filtros de vencidos, pendentes, publicados, arquivados | São lidos da view de busca quando possível. |

## 3. Configuração da Central de Ajuda

1. Garanta que o módulo tenha `docs/08_AJUDA_CONTEXTUAL.md`.
2. Vá em **Central de Ajuda > Configuração > Importar Documentação**.
3. Marque **Varrer módulos instalados**, **Importar fontes ativas** e **Gerar mapa de contextos**.
4. Após importar, revise **Mapa de Contextos**.
5. Corrija telas como **Sem contexto** ou **Contexto sem artigo**.

## 4. Checklist inicial

- [ ] Usuários e grupos revisados.
- [ ] Cadastros de apoio criados.
- [ ] Sequências e parâmetros conferidos.
- [ ] Menus principais acessíveis.
- [ ] Central de Ajuda importada.
- [ ] Mapa de Contextos sem telas críticas pendentes.
- [ ] Fluxos principais testados com dados reais de exemplo.
