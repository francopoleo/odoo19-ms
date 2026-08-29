# Ajuda Contextual — Property Document Portal

Este arquivo é a fonte versionada dos artigos curtos usados pelo drawer da Central de Ajuda. Execute a importação sempre que alterar este arquivo.

## Regras

- Cada bloco `HELP:ARTICLE` precisa de `code` único.
- Não liste manualmente categorias, tipos e filtros configuráveis.
- Explique o fluxo, a decisão e exemplos práticos.
- A Central de Ajuda exibirá opções dinâmicas diretamente do Odoo.

<!-- HELP:ARTICLE
code: property_document_portal.property_document_portal.list.overview
module: property_document_portal
model: document.document
view_type: list
category: Portal de Documentos Imobiliários
context_name: Lista de Portal
title: Como usar a lista de Portal
article_type: howto
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de Portal

Use a lista para localizar registros, aplicar filtros, acompanhar responsáveis e identificar pendências. Priorize filtros de acompanhamento em vez de criar registros duplicados.

## Exemplo

Um usuário precisa encontrar registros pendentes. Ele abre a lista, aplica o filtro adequado e usa os agrupamentos para organizar por responsável, situação ou tipo, conforme a tela disponibilizar.

## Boas práticas

- Use filtros antes de criar novos registros.
- Agrupe por responsável ou situação quando precisar acompanhar volume.
- Abra o registro principal para decisões; não resolva fluxo complexo apenas pela lista.

> Consulte também a seção **Campos, opções e filtros desta tela**. Ela mostra automaticamente campos obrigatórios, opções reais, categorias/tipos relacionados e filtros disponíveis no Odoo.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: property_document_portal.property_document_portal.form.fill
module: property_document_portal
model: document.document
view_type: form
category: Portal de Documentos Imobiliários
context_name: Formulário de Portal
title: Como preencher Portal
article_type: flow
scope: flow
audience: user
sequence: 11
show_in_context: true
-->
# Como preencher Portal

Use o formulário para preencher dados principais, responsáveis, vínculos e informações operacionais do registro.

## Exemplo

Ao preencher um registro, informe o responsável principal, revise campos obrigatórios, escolha categorias/tipos conforme a finalidade e salve antes de criar atividades ou marcos da Agenda Geral.

## Regras importantes

- Atividades são usadas para tarefas individuais.
- Agenda Geral é usada para marcos críticos ou compromissos operacionais.
- Anexos devem ser inseridos no campo próprio do fluxo quando existir.
- Se uma opção não aparecer, revise a configuração funcional do módulo.

> Consulte também a seção **Campos, opções e filtros desta tela**. Ela mostra automaticamente campos obrigatórios, opções reais, categorias/tipos relacionados e filtros disponíveis no Odoo.
<!-- /HELP:ARTICLE -->
