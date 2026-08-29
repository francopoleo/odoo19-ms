# Ajuda Contextual — Central de Ajuda

Este arquivo é a fonte versionada dos artigos curtos usados pelo drawer da Central de Ajuda. Ele pode ser importado sempre sem duplicar artigos, pois cada bloco usa `code` único.


<!-- HELP:ARTICLE
code: common_help_center.help_article.list.using
module: common_help_center
model: help.article
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.article
title: Como usar a lista de help.article
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.article

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.article`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_article.form.create
module: common_help_center
model: help.article
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.article
title: Como preencher help.article
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.article

Esta tela registra ou atualiza um item do modelo `help.article`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_article.field.name
module: common_help_center
model: help.article
view_type: form
field: name
category: Central de Ajuda
context_name: help.article / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.article`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Título |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_article.field.code
module: common_help_center
model: help.article
view_type: form
field: code
category: Central de Ajuda
context_name: help.article / Campo code
title: Como preencher o campo code
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `code`

Este campo é importante para o fluxo do modelo `help.article`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Código |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_article.field.article_type
module: common_help_center
model: help.article
view_type: form
field: article_type
category: Central de Ajuda
context_name: help.article / Campo article_type
title: Como preencher o campo article_type
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `article_type`

Este campo é importante para o fluxo do modelo `help.article`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Selection |
| Obrigatório | Sim |
| Rótulo | Tipo |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_category.list.using
module: common_help_center
model: help.category
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.category
title: Como usar a lista de help.category
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.category

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.category`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_category.form.create
module: common_help_center
model: help.category
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.category
title: Como preencher help.category
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.category

Esta tela registra ou atualiza um item do modelo `help.category`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_category.field.name
module: common_help_center
model: help.category
view_type: form
field: name
category: Central de Ajuda
context_name: help.category / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.category`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Nome |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_category.field.code
module: common_help_center
model: help.category
view_type: form
field: code
category: Central de Ajuda
context_name: help.category / Campo code
title: Como preencher o campo code
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `code`

Este campo é importante para o fluxo do modelo `help.category`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Código |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_template.list.using
module: common_help_center
model: help.checklist.template
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.checklist.template
title: Como usar a lista de help.checklist.template
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.checklist.template

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.checklist.template`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_template.form.create
module: common_help_center
model: help.checklist.template
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.checklist.template
title: Como preencher help.checklist.template
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.checklist.template

Esta tela registra ou atualiza um item do modelo `help.checklist.template`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_template.field.name
module: common_help_center
model: help.checklist.template
view_type: form
field: name
category: Central de Ajuda
context_name: help.checklist.template / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.checklist.template`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Nome |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_template.field.audience
module: common_help_center
model: help.checklist.template
view_type: form
field: audience
category: Central de Ajuda
context_name: help.checklist.template / Campo audience
title: Como preencher o campo audience
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `audience`

Este campo é importante para o fluxo do modelo `help.checklist.template`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Selection |
| Obrigatório | Sim |
| Rótulo | Público |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_item.list.using
module: common_help_center
model: help.checklist.item
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.checklist.item
title: Como usar a lista de help.checklist.item
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.checklist.item

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.checklist.item`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_item.form.create
module: common_help_center
model: help.checklist.item
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.checklist.item
title: Como preencher help.checklist.item
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.checklist.item

Esta tela registra ou atualiza um item do modelo `help.checklist.item`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_item.field.template_id
module: common_help_center
model: help.checklist.item
view_type: form
field: template_id
category: Central de Ajuda
context_name: help.checklist.item / Campo template_id
title: Como preencher o campo template_id
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `template_id`

Este campo é importante para o fluxo do modelo `help.checklist.item`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Many2one |
| Obrigatório | Sim |
| Rótulo | Checklist |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_item.field.name
module: common_help_center
model: help.checklist.item
view_type: form
field: name
category: Central de Ajuda
context_name: help.checklist.item / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.checklist.item`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Item |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_progress.list.using
module: common_help_center
model: help.checklist.progress
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.checklist.progress
title: Como usar a lista de help.checklist.progress
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.checklist.progress

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.checklist.progress`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_progress.form.create
module: common_help_center
model: help.checklist.progress
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.checklist.progress
title: Como preencher help.checklist.progress
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.checklist.progress

Esta tela registra ou atualiza um item do modelo `help.checklist.progress`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_progress.field.user_id
module: common_help_center
model: help.checklist.progress
view_type: form
field: user_id
category: Central de Ajuda
context_name: help.checklist.progress / Campo user_id
title: Como preencher o campo user_id
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `user_id`

Este campo é importante para o fluxo do modelo `help.checklist.progress`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Many2one |
| Obrigatório | Sim |
| Rótulo | Usuário |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_progress.field.template_id
module: common_help_center
model: help.checklist.progress
view_type: form
field: template_id
category: Central de Ajuda
context_name: help.checklist.progress / Campo template_id
title: Como preencher o campo template_id
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `template_id`

Este campo é importante para o fluxo do modelo `help.checklist.progress`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Many2one |
| Obrigatório | Sim |
| Rótulo | Checklist |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_checklist_progress.field.item_id
module: common_help_center
model: help.checklist.progress
view_type: form
field: item_id
category: Central de Ajuda
context_name: help.checklist.progress / Campo item_id
title: Como preencher o campo item_id
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `item_id`

Este campo é importante para o fluxo do modelo `help.checklist.progress`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Many2one |
| Obrigatório | Sim |
| Rótulo | Item |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_context.list.using
module: common_help_center
model: help.context
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.context
title: Como usar a lista de help.context
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.context

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.context`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_context.form.create
module: common_help_center
model: help.context
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.context
title: Como preencher help.context
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.context

Esta tela registra ou atualiza um item do modelo `help.context`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_context.field.name
module: common_help_center
model: help.context
view_type: form
field: name
category: Central de Ajuda
context_name: help.context / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.context`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Nome |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_context.field.context_kind
module: common_help_center
model: help.context
view_type: form
field: context_kind
category: Central de Ajuda
context_name: help.context / Campo context_kind
title: Como preencher o campo context_kind
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `context_kind`

Este campo é importante para o fluxo do modelo `help.context`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Selection |
| Obrigatório | Sim |
| Rótulo | Tipo de Contexto |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_context_candidate.list.using
module: common_help_center
model: help.context.candidate
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.context.candidate
title: Como usar a lista de help.context.candidate
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.context.candidate

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.context.candidate`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_context_candidate.form.create
module: common_help_center
model: help.context.candidate
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.context.candidate
title: Como preencher help.context.candidate
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.context.candidate

Esta tela registra ou atualiza um item do modelo `help.context.candidate`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_doc_source.list.using
module: common_help_center
model: help.doc.source
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.doc.source
title: Como usar a lista de help.doc.source
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.doc.source

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.doc.source`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_doc_source.form.create
module: common_help_center
model: help.doc.source
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.doc.source
title: Como preencher help.doc.source
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.doc.source

Esta tela registra ou atualiza um item do modelo `help.doc.source`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_doc_source.field.name
module: common_help_center
model: help.doc.source
view_type: form
field: name
category: Central de Ajuda
context_name: help.doc.source / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.doc.source`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Nome |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_doc_source.field.module_name
module: common_help_center
model: help.doc.source
view_type: form
field: module_name
category: Central de Ajuda
context_name: help.doc.source / Campo module_name
title: Como preencher o campo module_name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `module_name`

Este campo é importante para o fluxo do modelo `help.doc.source`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Módulo |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_doc_source.field.file_path
module: common_help_center
model: help.doc.source
view_type: form
field: file_path
category: Central de Ajuda
context_name: help.doc.source / Campo file_path
title: Como preencher o campo file_path
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `file_path`

Este campo é importante para o fluxo do modelo `help.doc.source`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Caminho do Arquivo |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_feedback.list.using
module: common_help_center
model: help.feedback
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.feedback
title: Como usar a lista de help.feedback
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.feedback

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.feedback`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_feedback.form.create
module: common_help_center
model: help.feedback
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.feedback
title: Como preencher help.feedback
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.feedback

Esta tela registra ou atualiza um item do modelo `help.feedback`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_feedback.field.article_id
module: common_help_center
model: help.feedback
view_type: form
field: article_id
category: Central de Ajuda
context_name: help.feedback / Campo article_id
title: Como preencher o campo article_id
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `article_id`

Este campo é importante para o fluxo do modelo `help.feedback`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Many2one |
| Obrigatório | Sim |
| Rótulo | Artigo |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_feedback.field.user_id
module: common_help_center
model: help.feedback
view_type: form
field: user_id
category: Central de Ajuda
context_name: help.feedback / Campo user_id
title: Como preencher o campo user_id
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `user_id`

Este campo é importante para o fluxo do modelo `help.feedback`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Many2one |
| Obrigatório | Sim |
| Rótulo | Usuário |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_feedback.field.rating
module: common_help_center
model: help.feedback
view_type: form
field: rating
category: Central de Ajuda
context_name: help.feedback / Campo rating
title: Como preencher o campo rating
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `rating`

Este campo é importante para o fluxo do modelo `help.feedback`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Selection |
| Obrigatório | Sim |
| Rótulo | Avaliação |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_learning_path.list.using
module: common_help_center
model: help.learning.path
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.learning.path
title: Como usar a lista de help.learning.path
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.learning.path

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.learning.path`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_learning_path.form.create
module: common_help_center
model: help.learning.path
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.learning.path
title: Como preencher help.learning.path
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.learning.path

Esta tela registra ou atualiza um item do modelo `help.learning.path`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_learning_path.field.name
module: common_help_center
model: help.learning.path
view_type: form
field: name
category: Central de Ajuda
context_name: help.learning.path / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.learning.path`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Nome |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_learning_path.field.audience
module: common_help_center
model: help.learning.path
view_type: form
field: audience
category: Central de Ajuda
context_name: help.learning.path / Campo audience
title: Como preencher o campo audience
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `audience`

Este campo é importante para o fluxo do modelo `help.learning.path`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Selection |
| Obrigatório | Sim |
| Rótulo | Público |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_learning_step.list.using
module: common_help_center
model: help.learning.step
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.learning.step
title: Como usar a lista de help.learning.step
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.learning.step

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.learning.step`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_learning_step.form.create
module: common_help_center
model: help.learning.step
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.learning.step
title: Como preencher help.learning.step
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.learning.step

Esta tela registra ou atualiza um item do modelo `help.learning.step`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_learning_step.field.learning_path_id
module: common_help_center
model: help.learning.step
view_type: form
field: learning_path_id
category: Central de Ajuda
context_name: help.learning.step / Campo learning_path_id
title: Como preencher o campo learning_path_id
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `learning_path_id`

Este campo é importante para o fluxo do modelo `help.learning.step`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Many2one |
| Obrigatório | Sim |
| Rótulo | Trilha |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_learning_step.field.name
module: common_help_center
model: help.learning.step
view_type: form
field: name
category: Central de Ajuda
context_name: help.learning.step / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.learning.step`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Nome |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_metric.list.using
module: common_help_center
model: help.metric
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.metric
title: Como usar a lista de help.metric
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.metric

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.metric`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_metric.form.create
module: common_help_center
model: help.metric
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.metric
title: Como preencher help.metric
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.metric

Esta tela registra ou atualiza um item do modelo `help.metric`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_metric.field.event_type
module: common_help_center
model: help.metric
view_type: form
field: event_type
category: Central de Ajuda
context_name: help.metric / Campo event_type
title: Como preencher o campo event_type
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `event_type`

Este campo é importante para o fluxo do modelo `help.metric`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Selection |
| Obrigatório | Sim |
| Rótulo | Tipo de Evento |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_metric.field.user_id
module: common_help_center
model: help.metric
view_type: form
field: user_id
category: Central de Ajuda
context_name: help.metric / Campo user_id
title: Como preencher o campo user_id
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `user_id`

Este campo é importante para o fluxo do modelo `help.metric`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Many2one |
| Obrigatório | Sim |
| Rótulo | Usuário |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_suggestion_rule.list.using
module: common_help_center
model: help.suggestion.rule
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.suggestion.rule
title: Como usar a lista de help.suggestion.rule
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.suggestion.rule

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.suggestion.rule`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_suggestion_rule.form.create
module: common_help_center
model: help.suggestion.rule
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.suggestion.rule
title: Como preencher help.suggestion.rule
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.suggestion.rule

Esta tela registra ou atualiza um item do modelo `help.suggestion.rule`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_suggestion_rule.field.name
module: common_help_center
model: help.suggestion.rule
view_type: form
field: name
category: Central de Ajuda
context_name: help.suggestion.rule / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.suggestion.rule`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Nome |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_suggestion_rule.field.rule_type
module: common_help_center
model: help.suggestion.rule
view_type: form
field: rule_type
category: Central de Ajuda
context_name: help.suggestion.rule / Campo rule_type
title: Como preencher o campo rule_type
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `rule_type`

Este campo é importante para o fluxo do modelo `help.suggestion.rule`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Selection |
| Obrigatório | Sim |
| Rótulo | Tipo de Regra |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_tag.list.using
module: common_help_center
model: help.tag
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.tag
title: Como usar a lista de help.tag
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.tag

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.tag`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_tag.form.create
module: common_help_center
model: help.tag
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.tag
title: Como preencher help.tag
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.tag

Esta tela registra ou atualiza um item do modelo `help.tag`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_tag.field.name
module: common_help_center
model: help.tag
view_type: form
field: name
category: Central de Ajuda
context_name: help.tag / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.tag`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Nome |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_tip.list.using
module: common_help_center
model: help.tip
view_type: list
field: 
category: Central de Ajuda
context_name: Lista de help.tip
title: Como usar a lista de help.tip
article_type: context
scope: context
audience: user
sequence: 10
show_in_context: true
-->
# Como usar a lista de help.tip

Use a lista para localizar, filtrar, agrupar e acompanhar registros do modelo `help.tip`.

## Exemplo prático

| Situação | Ação recomendada |
| --- | --- |
| Procurar registro específico | Use a busca superior por nome, responsável ou status. |
| Acompanhar pendências | Use filtros de situação, responsável e datas. |
| Analisar volume | Agrupe por responsável, categoria ou situação quando disponível. |

## Resultado esperado

- O usuário encontra rapidamente o registro certo.
- Os filtros reduzem ruído operacional.
- A lista serve como painel de acompanhamento, não como local de configuração indevida.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_tip.form.create
module: common_help_center
model: help.tip
view_type: form
field: 
category: Central de Ajuda
context_name: Formulário de help.tip
title: Como preencher help.tip
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como preencher help.tip

Esta tela registra ou atualiza um item do modelo `help.tip`.

## Passo a passo

1. Preencha os campos obrigatórios destacados pelo Odoo.
2. Informe responsável, empresa e situação quando existirem.
3. Anexe arquivos, documentos ou mídias nos campos próprios do fluxo.
4. Use **Agendar atividade** para tarefas individuais.
5. Use **Agenda Geral** apenas para marcos operacionais relevantes.
6. Salve e confira se o histórico foi atualizado.

## Exemplo

| Campo | Exemplo |
| --- | --- |
| Responsável | João |
| Prazo | 22/05 |
| Observação | Acompanhar até regularização. |

## Resultado esperado

- Registro salvo sem erro.
- Atividade criada apenas quando houver cobrança individual.
- Agenda Geral criada apenas quando for marco formal ou compromisso operacional.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_tip.field.name
module: common_help_center
model: help.tip
view_type: form
field: name
category: Central de Ajuda
context_name: help.tip / Campo name
title: Como preencher o campo name
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `name`

Este campo é importante para o fluxo do modelo `help.tip`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Char |
| Obrigatório | Sim |
| Rótulo | Título |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_tip.field.content
module: common_help_center
model: help.tip
view_type: form
field: content
category: Central de Ajuda
context_name: help.tip / Campo content
title: Como preencher o campo content
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `content`

Este campo é importante para o fluxo do modelo `help.tip`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Text |
| Obrigatório | Sim |
| Rótulo | Dica |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_tip.field.audience
module: common_help_center
model: help.tip
view_type: form
field: audience
category: Central de Ajuda
context_name: help.tip / Campo audience
title: Como preencher o campo audience
article_type: field_help
scope: field
audience: user
sequence: 30
show_in_context: true
-->
# Campo `audience`

Este campo é importante para o fluxo do modelo `help.tip`.

| Informação | Valor |
| --- | --- |
| Tipo técnico | Selection |
| Obrigatório | Sim |
| Rótulo | Público |

## Recomendação

Preencha este campo antes de salvar para evitar validações incompletas e para permitir filtros, responsáveis, relatórios e ajuda contextual correta.
<!-- /HELP:ARTICLE -->

<!-- HELP:ARTICLE
code: common_help_center.help_article.form.markdown_tables
module: common_help_center
model: help.article
view_type: form
field: 
category: Central de Ajuda
context_name: Artigo da Central de Ajuda
title: Como escrever Markdown com tabelas
article_type: flow
scope: flow
audience: user
sequence: 1
show_in_context: true
-->
# Como escrever Markdown com tabelas

A Central de Ajuda renderiza tabelas Markdown no formato padrão.

## Exemplo

| Campo | Descrição |
| --- | --- |
| `code` | Código único do artigo. |
| `model` | Model relacionado ao contexto. |
| `view_type` | Tipo de tela: list, form, kanban etc. |

## Regras

- Use uma linha de cabeçalho.
- Use uma linha separadora com `---`.
- Não deixe linhas vazias no meio da tabela.
- Reimporte ou clique em **Renderizar Markdown** após alterar o conteúdo.
<!-- /HELP:ARTICLE -->


## Referência dinâmica de campos, opções e filtros

A Central de Ajuda agora exibe, no drawer contextual, uma seção gerada em tempo real chamada **Campos, opções e filtros desta tela**.

Essa seção não substitui os artigos documentados em `docs/08_AJUDA_CONTEXTUAL.md`; ela complementa o fluxo com as opções realmente existentes no ambiente atual.

Ela pode listar:

| Item | Origem | Uso |
| --- | --- | --- |
| Campos obrigatórios | `fields_get()` do model atual | Ajuda o usuário a saber o mínimo para salvar o formulário |
| Opções fixas | Campos `selection` | Mostra todos os valores possíveis, como situação, prioridade, finalidade, tipo de conteúdo |
| Categorias, tipos e cadastros relacionados | Campos `many2one`/`many2many` relevantes | Mostra categorias, tipos, etapas, responsáveis, empresas, tags e outros cadastros ativos |
| Filtros e agrupamentos | Search views (`ir.ui.view` type `search`) | Mostra filtros de lista e opções de agrupamento disponíveis na tela |

### Como usar na documentação dos módulos

Nos artigos contextuais, documente o **fluxo de negócio** e deixe a Central complementar com opções dinâmicas. Exemplo:

```markdown
<!-- HELP:ARTICLE
code: document_core.document_document.form.create
module: document_core
model: document.document
view_type: form
category: Gestão Documental
context_name: Formulário de Documento
title: Como criar um novo documento
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como criar um novo documento

1. Preencha o nome do documento.
2. Escolha a categoria e o tipo documental.
3. Anexe o arquivo principal.
4. Informe responsável, validade ou revisão quando necessário.
5. Salve e acompanhe o documento nos menus de monitoramento.

Abaixo do artigo, a Central exibirá automaticamente as categorias, tipos, campos obrigatórios e filtros disponíveis no ambiente atual.
<!-- /HELP:ARTICLE -->
```

### Regra enterprise

- O artigo contextual deve explicar **quando e por que preencher**.
- A referência dinâmica deve mostrar **quais opções existem agora**.
- Categorias e tipos não devem ser escritos manualmente no artigo se forem cadastros configuráveis, porque podem mudar por empresa/cliente.
- Quando uma nova funcionalidade criar campo, seleção, categoria, filtro ou agrupamento, atualize o fluxo no `08_AJUDA_CONTEXTUAL.md` e rode a importação da Central de Ajuda.
