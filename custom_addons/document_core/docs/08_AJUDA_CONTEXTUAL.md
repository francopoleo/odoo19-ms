# Ajuda Contextual — Document Core

Este arquivo é a fonte versionada dos artigos curtos usados pelo drawer da Central de Ajuda. Execute a importação sempre que alterar este arquivo.

## Regras

- Cada bloco `HELP:ARTICLE` precisa de `code` único.
- Não liste manualmente categorias, tipos e filtros configuráveis.
- Explique o fluxo, a decisão e exemplos práticos.
- A Central de Ajuda exibirá opções dinâmicas diretamente do Odoo.

<!-- HELP:ARTICLE
code: document_core.document_document.list.overview
module: document_core
model: document.document
view_type: list
category: Gestão Documental
context_name: Lista de Document
title: Como usar a lista de Document
article_type: howto
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de Document

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
code: document_core.document_document.form.fill
module: document_core
model: document.document
view_type: form
category: Gestão Documental
context_name: Formulário de Document
title: Como preencher Document
article_type: flow
scope: flow
audience: user
sequence: 11
show_in_context: true
-->
# Como preencher Document

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

<!-- HELP:ARTICLE
code: document_core.document_category.list.overview
module: document_core
model: document.category
view_type: list
category: Gestão Documental
context_name: Lista de Category
title: Como usar a lista de Category
article_type: howto
scope: context
audience: user
sequence: 20
show_in_context: true
-->
# Como usar a lista de Category

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
code: document_core.document_category.form.fill
module: document_core
model: document.category
view_type: form
category: Gestão Documental
context_name: Formulário de Category
title: Como preencher Category
article_type: flow
scope: flow
audience: user
sequence: 21
show_in_context: true
-->
# Como preencher Category

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

<!-- HELP:ARTICLE
code: document_core.document_type.list.overview
module: document_core
model: document.type
view_type: list
category: Gestão Documental
context_name: Lista de Type
title: Como usar a lista de Type
article_type: howto
scope: context
audience: user
sequence: 30
show_in_context: true
-->
# Como usar a lista de Type

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
code: document_core.document_type.form.fill
module: document_core
model: document.type
view_type: form
category: Gestão Documental
context_name: Formulário de Type
title: Como preencher Type
article_type: flow
scope: flow
audience: user
sequence: 31
show_in_context: true
-->
# Como preencher Type

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

<!-- HELP:ARTICLE
code: document_core.document_location.list.overview
module: document_core
model: document.location
view_type: list
category: Gestão Documental
context_name: Lista de Location
title: Como usar a lista de Location
article_type: howto
scope: context
audience: user
sequence: 40
show_in_context: true
-->
# Como usar a lista de Location

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
code: document_core.document_location.form.fill
module: document_core
model: document.location
view_type: form
category: Gestão Documental
context_name: Formulário de Location
title: Como preencher Location
article_type: flow
scope: flow
audience: user
sequence: 41
show_in_context: true
-->
# Como preencher Location

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

<!-- HELP:ARTICLE
code: document_core.document_document.form.expiry
module: document_core
model: document.document
view_type: form
category: Gestão Documental
context_name: Formulário de Documento
title: Como tratar vencimento, revisão e validação de documentos
article_type: flow
scope: flow
audience: user
sequence: 30
show_in_context: true
-->
# Como tratar vencimento, revisão e validação de documentos

Use vencimento, revisão e validação para controlar risco documental. Um documento vencido pode bloquear processo, contrato, dossiê ou governança.

## Exemplo

Documento: Certidão Negativa  
Vencimento: 30/06  
Responsável: Juliana

Resultado esperado:
- atividade de revisão para Juliana;
- marco na Agenda Geral apenas se for prazo crítico;
- documento aparece nos menus de acompanhamento quando estiver a vencer ou vencido.

## Decisão

- Use atividade para lembrar a pessoa de revisar.
- Use Agenda Geral quando o vencimento impactar operação, contrato, auditoria ou obrigação externa.

> Consulte também a seção **Campos, opções e filtros desta tela**. Ela mostra automaticamente campos obrigatórios, opções reais, categorias/tipos relacionados e filtros disponíveis no Odoo.
<!-- /HELP:ARTICLE -->
