# Documentação Técnica - Central de Ajuda

## 1. Objetivo técnico

O módulo `common_help_center` importa documentação Markdown dos módulos instalados e a transforma em artigos pesquisáveis e contextuais dentro do Odoo.

A arquitetura separa:

| Camada | Model | Uso |
|---|---|---|
| Biblioteca | `help.article` | Artigos completos e artigos contextuais |
| Classificação | `help.category`, `help.tag` | Área funcional e tags |
| Contexto | `help.context` | Liga telas, models, menus, actions e campos a artigos |
| Fonte | `help.doc.source` | Arquivos Markdown dos módulos |
| Mapa de contexto | `help.context.candidate` | Lista telas/models detectados e status de documentação |
| Feedback | `help.feedback` | Avaliação dos usuários |
| Aprendizado | `help.learning.path`, `help.learning.step` | Trilhas de aprendizado |
| Checklists | `help.checklist.template`, `help.checklist.item`, `help.checklist.progress` | Checklists por tela/registro |
| Dicas | `help.tip` | Dicas rápidas por contexto |
| Inteligência | `help.suggestion.rule`, `help.metric` | Sugestões e métricas |

## 2. Estrutura de documentação dos módulos

Cada módulo deve manter no mínimo:

```text
modulo/
├── README.md
└── docs/
    ├── 00_INDICE.md
    ├── 01_DOCUMENTACAO_TECNICA.md
    ├── 02_MANUAL_USUARIO.md
    ├── 03_CONFIGURACAO_INICIAL.md
    ├── 04_GUIA_TESTES.md
    ├── 05_GUIA_IMPLEMENTACAO.md
    ├── 06_TROUBLESHOOTING.md
    ├── 07_CHANGELOG_FUNCIONAL.md
    └── 08_AJUDA_CONTEXTUAL.md
```

Os arquivos `00` a `07` entram como documentos completos na Biblioteca. O arquivo `08_AJUDA_CONTEXTUAL.md` alimenta o drawer de ajuda contextual.

## 3. Importação idempotente

A importação pode ser rodada sempre. O identificador principal é o campo `code` do artigo.

Regras:

- Se o artigo não existe, cria.
- Se o artigo existe e não foi editado no Odoo, atualiza pelo Markdown.
- Se o artigo foi editado no Odoo e a política é `preserve_odoo`, preserva a edição.
- Se a política é `overwrite`, sobrescreve pelo Markdown.
- Fontes Markdown são identificadas por `module_name + file_path`.

## 4. Arquivo `08_AJUDA_CONTEXTUAL.md`

Esse arquivo usa blocos especiais:

```markdown
<!-- HELP:ARTICLE
code: document_core.document_document.form.create
module: document_core
model: document.document
view_type: form
category: Documentos
context_name: Formulário de Documento
title: Como criar um novo documento
article_type: flow
scope: flow
audience: user
sequence: 10
-->
# Como criar um novo documento

Conteúdo curto, prático e contextual.
<!-- /HELP:ARTICLE -->
```

Cada bloco cria ou atualiza um `help.article` e vincula o artigo ao `help.context` correspondente.

## 5. Mapa de Contextos

O model `help.context.candidate` funciona como uma lista de lacunas de documentação.

Ele é gerado a partir de:

- `ir.ui.view`
- `ir.actions.act_window`
- `ir.ui.menu`

O objetivo é listar telas e menus técnicos, como:

```text
document.document / list
document.document / form
property.asset / form
governance.case / form
```

Situações:

| Situação | Significado |
|---|---|
| Sem contexto | A tela foi detectada, mas não há `help.context` |
| Contexto sem artigo | Existe contexto, mas sem artigos contextuais |
| Documentado | Existe contexto e ao menos um artigo exibível |

## 6. Models principais

### `help.article`

Representa qualquer conteúdo de ajuda.

Campos importantes:

| Campo | Uso |
|---|---|
| `code` | Identificador idempotente do artigo |
| `article_type` | Manual, técnico, configuração, fluxo, troubleshooting etc. |
| `content_scope` | Documento completo, ajuda contextual, fluxo, campo, erro comum |
| `show_in_context` | Define se aparece no drawer |
| `module_name` | Módulo relacionado |
| `model_name` | Model relacionado |
| `view_type` | Form, list, kanban, calendar |
| `field_name` | Campo específico |
| `source_id` | Fonte Markdown importada |
| `edited_in_odoo` | Indica edição manual no Odoo |

### `help.context`

Liga artigos à tela atual.

Campos importantes:

| Campo | Uso |
|---|---|
| `model_name` | Model detectado pelo frontend |
| `view_type` | Tipo de view detectado |
| `menu_xmlid` | Menu de origem |
| `action_xmlid` | Action de origem |
| `field_name` | Ajuda de campo |
| `article_ids` | Artigos exibidos no contexto |

### `help.doc.source`

Representa um arquivo Markdown físico.

Métodos principais:

| Método | Uso |
|---|---|
| `action_discover_installed_module_docs` | Descobre arquivos `docs/*.md` dos módulos instalados |
| `action_import_active_sources` | Importa todas as fontes ativas |
| `_import_contextual_blocks` | Importa blocos `HELP:ARTICLE` |

### `help.context.candidate`

Representa a cobertura de documentação.

Métodos:

| Método | Uso |
|---|---|
| `action_generate_candidates` | Gera o mapa de contextos a partir das views/actions/menus |
| `action_open_or_create_context` | Abre ou cria o contexto de ajuda |
| `action_refresh_coverage` | Recalcula situação/documentação |

## 7. Fluxo técnico recomendado

1. Desenvolvedor altera funcionalidade no módulo.
2. Atualiza `docs/01_DOCUMENTACAO_TECNICA.md` e docs funcionais correspondentes.
3. Se a mudança afeta uma tela, adiciona ou atualiza bloco em `docs/08_AJUDA_CONTEXTUAL.md`.
4. Administrador roda **Importar Documentação**.
5. Administrador abre **Mapa de Contextos** para verificar lacunas.
6. Contextos sem artigo são preenchidos por novos blocos Markdown ou edição manual.

## 8. Segurança

Usuários internos podem ler artigos, contextos, dicas e checklists. Administradores do sistema podem criar, editar, importar e configurar.

## 9. Regra enterprise

Não use XML como fonte principal de ajuda contextual. XML deve ser usado apenas para seed mínimo. A fonte oficial deve ser a documentação versionada do módulo, especialmente `docs/08_AJUDA_CONTEXTUAL.md`.
