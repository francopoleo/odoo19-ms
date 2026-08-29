# Ajuda Contextual - Central de Ajuda

<!-- HELP:ARTICLE
code: common_help_center.help_article.form.standard
module: common_help_center
model: help.article
view_type: form
category: Central de Ajuda
context_name: Formulário de Artigo de Ajuda
title: Como classificar um artigo de ajuda
article_type: flow
scope: flow
audience: admin
sequence: 10
-->
# Como classificar um artigo de ajuda

Use **Categoria/Área** para indicar a área funcional, como Documentos, Imóveis ou Governança.

Use **Tipo** para indicar o formato do conteúdo, como Manual do Usuário, Documentação Técnica ou Fluxo.

Use **Escopo** para indicar onde o artigo deve aparecer:

- Documento completo: Biblioteca.
- Ajuda contextual: drawer lateral.
- Fluxo prático: drawer lateral com passo a passo.
- Erro comum: troubleshooting e sugestões inteligentes.

Para evitar duplicidade, manuais completos importados de `02_MANUAL_USUARIO.md` devem ficar com **Exibir no painel contextual** desmarcado.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_context_candidate.list.audit
module: common_help_center
model: help.context.candidate
view_type: list
category: Central de Ajuda
context_name: Mapa de Contextos
title: Como usar o Mapa de Contextos
article_type: flow
scope: flow
audience: admin
sequence: 10
-->
# Como usar o Mapa de Contextos

O Mapa de Contextos mostra telas, menus e actions detectados nos módulos instalados.

Use os filtros:

- **Sem contexto**: a tela foi detectada, mas ainda não tem contexto de ajuda.
- **Contexto sem artigo**: existe contexto, mas não há artigo exibível.
- **Documentados**: a tela já possui ajuda contextual.

Para corrigir uma lacuna:

1. Clique em **Abrir/Criar Contexto**.
2. Vincule um artigo existente ou crie um bloco em `docs/08_AJUDA_CONTEXTUAL.md` no módulo de origem.
3. Rode **Importar Documentação** novamente.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_doc_source.list.import
module: common_help_center
model: help.doc.source
view_type: list
category: Central de Ajuda
context_name: Fontes Markdown
title: Como reimportar documentação sem duplicar
article_type: flow
scope: flow
audience: admin
sequence: 10
-->
# Como reimportar documentação sem duplicar

A importação é idempotente.

Cada artigo usa um código técnico (`code`). Se o código já existir, o artigo é atualizado conforme a política da fonte.

Use **Preservar edições feitas no Odoo** quando administradores fazem ajustes pelo frontend.

Use **Sobrescrever sempre pelo Markdown** quando o repositório deve ser a fonte única da documentação.
<!-- /HELP:ARTICLE -->
