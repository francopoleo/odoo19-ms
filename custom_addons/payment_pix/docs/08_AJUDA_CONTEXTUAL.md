# Ajuda Contextual — Payment Provider: PIX (BACEN)

Este arquivo é a fonte versionada dos artigos curtos usados pelo drawer da Central de Ajuda. Execute a importação sempre que alterar este arquivo.

## Regras

- Cada bloco `HELP:ARTICLE` precisa de `code` único.
- Não liste manualmente categorias, tipos e filtros configuráveis.
- Explique o fluxo, a decisão e exemplos práticos.
- A Central de Ajuda exibirá opções dinâmicas diretamente do Odoo.

<!-- HELP:ARTICLE
code: payment_pix.payment_provider.list.overview
module: payment_pix
model: payment.provider
view_type: list
category: Pagamentos PIX
context_name: Lista de Provider
title: Como usar a lista de Provider
article_type: howto
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de Provider

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
code: payment_pix.payment_provider.form.fill
module: payment_pix
model: payment.provider
view_type: form
category: Pagamentos PIX
context_name: Formulário de Provider
title: Como preencher Provider
article_type: flow
scope: flow
audience: user
sequence: 11
show_in_context: true
-->
# Como preencher Provider

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
code: payment_pix.payment_transaction.list.overview
module: payment_pix
model: payment.transaction
view_type: list
category: Pagamentos PIX
context_name: Lista de Transaction
title: Como usar a lista de Transaction
article_type: howto
scope: context
audience: user
sequence: 20
show_in_context: true
-->
# Como usar a lista de Transaction

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
code: payment_pix.payment_transaction.form.fill
module: payment_pix
model: payment.transaction
view_type: form
category: Pagamentos PIX
context_name: Formulário de Transaction
title: Como preencher Transaction
article_type: flow
scope: flow
audience: user
sequence: 21
show_in_context: true
-->
# Como preencher Transaction

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
