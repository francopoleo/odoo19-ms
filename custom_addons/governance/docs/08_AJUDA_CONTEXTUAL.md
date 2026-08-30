# Ajuda Contextual — Governance & Audit

Este arquivo é a fonte versionada dos artigos curtos usados pelo drawer da Central de Ajuda. Execute a importação sempre que alterar este arquivo.

## Regras

- Cada bloco `HELP:ARTICLE` precisa de `code` único.
- Não liste manualmente categorias, tipos e filtros configuráveis.
- Explique o fluxo, a decisão e exemplos práticos.
- A Central de Ajuda exibirá opções dinâmicas diretamente do Odoo.

<!-- HELP:ARTICLE
code: governance.governance_case.list.overview
module: governance
model: governance.case
view_type: list
category: Governança e Auditoria
context_name: Lista de Case
title: Como usar a lista de Case
article_type: howto
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de Case

Use a lista para localizar registros, aplicar filtros, acompanhar responsáveis e identificar pendências. Priorize filtros de acompanhamento em vez de criar registros duplicados.

## Exemplo

Um usuário precisa encontrar registros pendentes. Ele abre a lista, aplica o filtro adequado e usa os agrupamentos para organizar por responsável, situação ou tipo, conforme a tela disponibilizar.

## Boas práticas

- Use filtros antes de criar novos registros.
- Agrupe por responsável ou situação quando precisar acompanhar volume.
- Abra o registro principal para decisões; não resolva fluxo complexo apenas pela lista.

> Consulte também a seção **Campos, opções e filtros desta tela**. Ela mostra automaticamente campos obrigatórios, opções reais, categorias/tipos relacionados e filtros disponíveis no Odoo.
<!-- /HELP:ARTICLE -->

## Processo profissional de governança

Um **caso** é o processo completo. Dentro dele, registre cada obrigação, comunicação, resposta formal, decisão, risco e controle separadamente.

- **Obrigação:** o que deve ser entregue ou executado, por quem e até quando.
- **Comunicação:** o histórico do contato, como e-mail, carta, reunião ou telefone.
- **Resposta formal:** a análise do conteúdo recebido; não é apenas o e-mail.
- **Decisão:** aprovação, rejeição ou aceitação de exceção, sempre com fundamentação.
- **Risco:** evento que pode afetar o resultado, com probabilidade, impacto e tratamento.
- **Controle:** verificação repetível que reduz um risco e possui responsável e frequência.

O caso só deve ser concluído quando não houver obrigações abertas nem riscos críticos sem tratamento. O encerramento é uma decisão do processo, não apenas uma mudança visual de etapa.

<!-- HELP:ARTICLE
code: governance.governance_case.form.fill
module: governance
model: governance.case
view_type: form
category: Governança e Auditoria
context_name: Formulário de Case
title: Como preencher Case
article_type: flow
scope: flow
audience: user
sequence: 11
show_in_context: true
-->
# Como preencher Case

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
code: governance.governance_case_pending.list.overview
module: governance
model: governance.case.pending
view_type: list
category: Governança e Auditoria
context_name: Lista de Pending
title: Como usar a lista de Pending
article_type: howto
scope: context
audience: user
sequence: 20
show_in_context: true
-->
# Como usar a lista de Pending

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
code: governance.governance_case_pending.form.fill
module: governance
model: governance.case.pending
view_type: form
category: Governança e Auditoria
context_name: Formulário de Pending
title: Como preencher Pending
article_type: flow
scope: flow
audience: user
sequence: 21
show_in_context: true
-->
# Como preencher Pending

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
code: governance.governance_case_communication.list.overview
module: governance
model: governance.case.communication
view_type: list
category: Governança e Auditoria
context_name: Lista de Communication
title: Como usar a lista de Communication
article_type: howto
scope: context
audience: user
sequence: 30
show_in_context: true
-->
# Como usar a lista de Communication

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
code: governance.governance_case_communication.form.fill
module: governance
model: governance.case.communication
view_type: form
category: Governança e Auditoria
context_name: Formulário de Communication
title: Como preencher Communication
article_type: flow
scope: flow
audience: user
sequence: 31
show_in_context: true
-->
# Como preencher Communication

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
code: governance.case.form.milestones
module: governance
model: governance.case
view_type: form
category: Governança
context_name: Formulário de Caso
title: Como usar prazos, pendências e Agenda Geral no caso de governança
article_type: flow
scope: flow
audience: user
sequence: 30
show_in_context: true
-->
# Como usar prazos, pendências e Agenda Geral no caso de governança

O caso pode ter muitas atividades, mas a Agenda Geral deve receber apenas marcos críticos.

## Exemplo

Caso: Reclamação de infiltração  
Prazo de resposta: 22/05  
Prazo de resolução: 04/06  
Responsável: João

Resultado esperado na Agenda Geral:
- Prazo de Resposta - Reclamação de infiltração
- Prazo de Resolução - Reclamação de infiltração

Atividades simples como ligar, enviar e-mail ou conferir documento ficam no chatter do caso.

> Consulte também a seção **Campos, opções e filtros desta tela**. Ela mostra automaticamente campos obrigatórios, opções reais, categorias/tipos relacionados e filtros disponíveis no Odoo.
<!-- /HELP:ARTICLE -->
