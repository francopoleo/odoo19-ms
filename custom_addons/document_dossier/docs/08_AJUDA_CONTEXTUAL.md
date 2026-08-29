# Ajuda Contextual — Document Dossier - Aggregator

Este arquivo é a fonte versionada dos artigos curtos usados pelo drawer da Central de Ajuda. Execute a importação sempre que alterar este arquivo.

## Regras

- Cada bloco `HELP:ARTICLE` precisa de `code` único.
- Não liste manualmente categorias, tipos e filtros configuráveis.
- Explique o fluxo, a decisão e exemplos práticos.
- A Central de Ajuda exibirá opções dinâmicas diretamente do Odoo.

<!-- HELP:ARTICLE
code: document_dossier.document_dossier.list.overview
module: document_dossier
model: dossier.dossier
view_type: list
category: Dossiês Documentais
context_name: Lista de Dossiês
title: Como usar a lista de Dossiês
article_type: howto
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de Dossiês

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
code: document_dossier.document_dossier.form.fill
module: document_dossier
model: dossier.dossier
view_type: form
category: Dossiês Documentais
context_name: Formulário de Dossiê
title: Como preencher Dossiê
article_type: flow
scope: flow
audience: user
sequence: 11
show_in_context: true
-->
# Como preencher Dossiê

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
code: document_dossier.document_dossier_template.list.overview
module: document_dossier
model: document.dossier.template
view_type: list
category: Dossiês Documentais
context_name: Lista de Template
title: Como usar a lista de Template
article_type: howto
scope: context
audience: user
sequence: 20
show_in_context: true
-->
# Como usar a lista de Template

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
code: document_dossier.document_dossier_template.form.fill
module: document_dossier
model: document.dossier.template
view_type: form
category: Dossiês Documentais
context_name: Formulário de Template
title: Como preencher Template
article_type: flow
scope: flow
audience: user
sequence: 21
show_in_context: true
-->
# Como preencher Template

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
code: document_dossier.dossier_dossier.kanban.overview
module: document_dossier
model: dossier.dossier
view_type: kanban
category: Dossiês Documentais
context_name: Kanban de Dossiês
title: Como acompanhar dossiês no kanban
article_type: howto
scope: context
audience: user
sequence: 9
show_in_context: true
-->
# Como acompanhar dossiês no kanban

Use o kanban para acompanhar rapidamente a situação dos dossiês, identificar pendências e priorizar o trabalho da equipe.

## Quando usar

Use o kanban quando precisar de uma visão operacional por estágio, situação ou responsável. Para análise detalhada, abra o dossiê no formulário.

## Exemplo prático

Um gestor precisa saber quais dossiês estão incompletos antes de uma reunião. Ele abre o kanban, identifica cartões com pendências e entra no dossiê para conferir documentos obrigatórios, responsáveis e prazos.

## Boas práticas

- Não crie outro dossiê para o mesmo processo; atualize o dossiê existente.
- Use atividades para cobrar uma pessoa específica.
- Use Agenda Geral apenas para marcos críticos ou compromissos operacionais.
- Confira a completude documental antes de marcar um dossiê como concluído.

> A seção dinâmica do painel mostra campos, opções e filtros reais da tela.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: document_dossier.dossier_dossier.form.documents
module: document_dossier
model: dossier.dossier
view_type: form
category: Dossiês Documentais
context_name: Formulário de Dossiê
title: Como organizar documentos dentro do dossiê
article_type: flow
scope: flow
audience: user
sequence: 12
show_in_context: true
-->
# Como organizar documentos dentro do dossiê

O dossiê reúne documentos relacionados a um processo, imóvel, caso ou fluxo operacional. Ele evita documentos soltos e ajuda a controlar completude, pendências e histórico.

## Passo a passo

1. Abra ou crie o dossiê.
2. Informe nome, processo/tipo, responsável e empresa quando aplicável.
3. Adicione documentos existentes ou crie novos documentos a partir do dossiê.
4. Use template de dossiê quando houver lista de documentos obrigatórios.
5. Verifique documentos faltantes, vencidos ou pendentes de validação.
6. Crie atividades para cobranças individuais.
7. Use Agenda Geral somente para prazo crítico ou compromisso operacional.

## Exemplo prático

Dossiê: Locação - Sala Comercial 301  
Responsável: Ana  
Documentos esperados: contrato, matrícula, IPTU e procuração.

Resultado esperado:

- documentos ficam vinculados ao dossiê;
- documentos faltantes aparecem no acompanhamento;
- atividade é criada para a pessoa responsável pela pendência;
- marco na Agenda Geral é criado apenas se houver prazo crítico.

## Erros comuns

- Anexar documentos apenas no chatter em vez de criar documentos estruturados.
- Criar dossiês duplicados para o mesmo processo.
- Marcar dossiê como completo sem revisar documentos obrigatórios.
<!-- /HELP:ARTICLE -->
