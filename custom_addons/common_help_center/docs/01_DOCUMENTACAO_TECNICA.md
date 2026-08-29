# Documentação Técnica — Central de Ajuda

## 1. Objetivo técnico

Central de Ajuda integrada ao Odoo para importar documentação Markdown, exibir biblioteca, ajuda contextual, trilhas, checklists, feedback e métricas.

Este documento é a referência para manutenção técnica do módulo `common_help_center`. Ele deve ser atualizado sempre que houver alteração em models, campos, views, ações, segurança, integrações ou fluxos automáticos.

## 2. Manifesto

| Campo | Valor |
| --- | --- |
| Módulo técnico | `common_help_center` |
| Nome exibido | Central de Ajuda |
| Versão | 19.0.1.5.0 |
| Categoria | Productivity |
| Aplicação | True |
| Instalável | True |

## 3. Dependências

| Dependência |
| --- |
| base |
| web |



## 4. Estrutura de arquivos

| Tipo | Arquivo |
| --- | --- |
| Python | __init__.py |
| Python | __manifest__.py |
| Python | controllers/__init__.py |
| Python | controllers/help_controller.py |
| Python | models/__init__.py |
| Python | models/help_article.py |
| Python | models/help_category.py |
| Python | models/help_checklist.py |
| Python | models/help_context.py |
| Python | models/help_context_candidate.py |
| Python | models/help_doc_source.py |
| Python | models/help_feedback.py |
| Python | models/help_learning.py |
| Python | models/help_metric.py |
| Python | models/help_suggestion.py |
| Python | models/help_tag.py |
| Python | models/help_tip.py |
| Python | wizard/__init__.py |
| Python | wizard/help_import_wizard.py |
| XML | data/help_category_data.xml |
| XML | data/help_context_defaults_data.xml |
| XML | data/help_default_content_data.xml |
| XML | data/help_enterprise_contexts_data.xml |
| XML | security/help_security.xml |
| XML | static/src/components/help_systray/help_systray.xml |
| XML | views/help_article_views.xml |
| XML | views/help_category_views.xml |
| XML | views/help_checklist_views.xml |
| XML | views/help_context_candidate_views.xml |
| XML | views/help_context_views.xml |
| XML | views/help_doc_source_views.xml |
| XML | views/help_feedback_views.xml |
| XML | views/help_learning_views.xml |
| XML | views/help_menu_views.xml |
| XML | views/help_metric_views.xml |
| XML | views/help_suggestion_views.xml |
| XML | views/help_tag_views.xml |
| XML | views/help_tip_views.xml |
| XML | wizard/help_import_wizard_views.xml |
| CSV | security/ir.model.access.csv |



## 5. Models

| Model | Herda | Classe | Arquivo | Responsabilidade |
| --- | --- | --- | --- | --- |
| help.article | - | HelpArticle | models/help_article.py | Artigo da Central de Ajuda |
| help.category | - | HelpCategory | models/help_category.py | Categoria da Central de Ajuda |
| help.checklist.template | - | HelpChecklistTemplate | models/help_checklist.py | Template de Checklist da Central de Ajuda |
| help.checklist.item | - | HelpChecklistItem | models/help_checklist.py | Item de Checklist da Central de Ajuda |
| help.checklist.progress | - | HelpChecklistProgress | models/help_checklist.py | Progresso de Checklist da Central de Ajuda |
| help.context | - | HelpContext | models/help_context.py | Contexto de Ajuda |
| help.context.candidate | - | HelpContextCandidate | models/help_context_candidate.py | Mapa de Contextos de Ajuda |
| help.doc.source | - | HelpDocSource | models/help_doc_source.py | Fonte Markdown da Central de Ajuda |
| help.feedback | - | HelpFeedback | models/help_feedback.py | Feedback da Central de Ajuda |
| help.learning.path | - | HelpLearningPath | models/help_learning.py | Trilha de Aprendizado |
| help.learning.step | - | HelpLearningStep | models/help_learning.py | Passo da Trilha de Aprendizado |
| help.metric | - | HelpMetric | models/help_metric.py | Métrica de Uso da Central de Ajuda |
| help.suggestion.rule | - | HelpSuggestionRule | models/help_suggestion.py | Regra de Sugestão Inteligente da Central de Ajuda |
| help.tag | - | HelpTag | models/help_tag.py | Tag da Central de Ajuda |
| help.tip | - | HelpTip | models/help_tip.py | Dica Contextual da Central de Ajuda |



## Model: `help.article`

**Classe:** `HelpArticle`  
**Arquivo:** `models/help_article.py`  
**Descrição:** Artigo da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Título | Sim | - | - |
| `code` | Char | Código | Sim | - | - |
| `category_id` | Many2one | Categoria | Não | - | - |
| `tag_ids` | Many2many | Tags | Não | - | - |
| `module_name` | Char | Módulo | Não | - | - |
| `model_name` | Char | Model relacionado | Não | - | - |
| `view_type` | Selection | Tipo de View | Não | - | - |
| `menu_xmlid` | Char | XML ID do Menu | Não | - | - |
| `action_xmlid` | Char | XML ID da Ação | Não | - | - |
| `field_name` | Char | Campo relacionado | Não | - | - |
| `article_type` | Selection | Tipo | Sim | - | - |
| `content_scope` | Selection | Escopo | Sim | - | - |
| `show_in_context` | Boolean | Exibir no painel contextual | Não | - | Desmarque para documentos completos importados, como manuais integrais. Eles continuam na biblioteca, mas não poluem o drawer contextual. |
| `audience` | Selection | Público | Sim | - | - |
| `markdown_source` | Text | Markdown | Não | - | - |
| `content_html` | Html | Conteúdo | Não | - | - |
| `summary` | Text | Resumo | Não | - | - |
| `source_id` | Many2one | Fonte Markdown | Não | - | - |
| `checksum` | Char | Checksum | Não | - | - |
| `edited_in_odoo` | Boolean | Editado no Odoo | Não | - | - |
| `published` | Boolean | Publicado | Não | - | - |
| `sequence` | Integer | Sequência | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |
| `related_article_ids` | Many2many | Artigos relacionados | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `create` | Método | model_create_multi | Sem docstring no código; revisar quando alterar a função. |
| `write` | Método | - | Sem docstring no código; revisar quando alterar a função. |
| `action_render_markdown` | Action | - | Sem docstring no código; revisar quando alterar a função. |
| `action_open` | Action | - | Sem docstring no código; revisar quando alterar a função. |
| `_checksum` | Constraint | staticmethod | Sem docstring no código; revisar quando alterar a função. |
| `_markdown_to_html` | Método | model | Conversor Markdown para a Central de Ajuda.  Suporta títulos, listas, blocos de código, blockquotes, links simples, negrito/itálico e tabelas Markdown no padrão GitHub:  | Coluna A |
| `_allowed_audiences` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_base_article_domain` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_record_state_value` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_serialize_article` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `get_context_bundle` | Método | model | Retorna artigos, dicas, checklists e sugestões para o painel lateral.  `context_info` vem do frontend e pode conter: - resModel - viewType - resId - menuXmlid - actionXmlid |
| `get_drawer_article` | Método | model | Retorna um artigo completo para leitura dentro do drawer lateral. |
| `get_error_suggestions` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `log_article_open` | Método | model | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.category`

**Classe:** `HelpCategory`  
**Arquivo:** `models/help_category.py`  
**Descrição:** Categoria da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Nome | Sim | - | - |
| `code` | Char | Código | Sim | - | - |
| `parent_id` | Many2one | Categoria Pai | Não | - | - |
| `child_ids` | One2many | Subcategorias | Não | - | - |
| `sequence` | Integer | Sequência | Não | - | - |
| `description` | Text | Descrição | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `create` | Método | model_create_multi | Criação idempotente para dados-base.  Durante testes e reinstalações pode existir uma categoria criada por uma versão anterior sem o XML ID atual. Em vez de quebrar a instalação po |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.checklist.template`

**Classe:** `HelpChecklistTemplate`  
**Arquivo:** `models/help_checklist.py`  
**Descrição:** Template de Checklist da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Nome | Sim | - | - |
| `code` | Char | Código | Não | - | - |
| `description` | Text | Descrição | Não | - | - |
| `module_name` | Char | Módulo | Não | - | - |
| `model_name` | Char | Model | Não | - | - |
| `view_type` | Selection | Tipo de View | Não | - | - |
| `audience` | Selection | Público | Sim | - | - |
| `item_ids` | One2many | Itens | Não | - | - |
| `sequence` | Integer | Sequência | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `create` | Método | model_create_multi | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.checklist.item`

**Classe:** `HelpChecklistItem`  
**Arquivo:** `models/help_checklist.py`  
**Descrição:** Item de Checklist da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `template_id` | Many2one | Checklist | Sim | - | - |
| `name` | Char | Item | Sim | - | - |
| `description` | Text | Descrição | Não | - | - |
| `article_id` | Many2one | Artigo relacionado | Não | - | - |
| `sequence` | Integer | Sequência | Não | - | - |
| `required` | Boolean | Obrigatório | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.checklist.progress`

**Classe:** `HelpChecklistProgress`  
**Arquivo:** `models/help_checklist.py`  
**Descrição:** Progresso de Checklist da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `user_id` | Many2one | Usuário | Sim | - | - |
| `template_id` | Many2one | Checklist | Sim | - | - |
| `item_id` | Many2one | Item | Sim | - | - |
| `model_name` | Char | Model | Não | - | - |
| `record_id` | Integer | Registro | Não | - | - |
| `done` | Boolean | Concluído | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `toggle_progress` | Método | model | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.context`

**Classe:** `HelpContext`  
**Arquivo:** `models/help_context.py`  
**Descrição:** Contexto de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Nome | Sim | - | - |
| `category_id` | Many2one | Categoria/Área | Não | - | - |
| `context_kind` | Selection | Tipo de Contexto | Sim | - | - |
| `module_name` | Char | Módulo | Não | - | - |
| `model_name` | Char | Model | Não | - | - |
| `view_type` | Selection | Tipo de View | Não | - | - |
| `field_name` | Char | Campo | Não | - | - |
| `menu_xmlid` | Char | XML ID do Menu | Não | - | - |
| `action_xmlid` | Char | XML ID da Ação | Não | - | - |
| `article_ids` | Many2many | Artigos | Não | - | - |
| `priority` | Integer | Prioridade | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |
| `description` | Text | Descrição | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `action_open_articles` | Action | - | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.context.candidate`

**Classe:** `HelpContextCandidate`  
**Arquivo:** `models/help_context_candidate.py`  
**Descrição:** Mapa de Contextos de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Contexto | Não | Sim | - |
| `module_name` | Char | Módulo | Não | - | - |
| `model_name` | Char | Model | Não | - | - |
| `view_type` | Selection | Tipo de View | Não | - | - |
| `view_id` | Many2one | View Técnica | Não | - | - |
| `view_xmlid` | Char | XML ID da View | Não | - | - |
| `action_id` | Many2one | Ação | Não | - | - |
| `action_xmlid` | Char | XML ID da Ação | Não | - | - |
| `menu_id` | Many2one | Menu | Não | - | - |
| `menu_xmlid` | Char | XML ID do Menu | Não | - | - |
| `context_id` | Many2one | Contexto de Ajuda | Não | - | - |
| `article_count` | Integer | Artigos | Não | - | - |
| `has_context` | Boolean | Tem contexto | Não | - | - |
| `status` | Selection | Situação | Não | - | - |
| `last_scan_date` | Datetime | Última varredura | Não | - | - |
| `note` | Text | Observações | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `_compute_name` | Compute | depends | Sem docstring no código; revisar quando alterar a função. |
| `action_refresh_coverage` | Action | - | Sem docstring no código; revisar quando alterar a função. |
| `_refresh_coverage_values` | Método | - | Sem docstring no código; revisar quando alterar a função. |
| `action_open_or_create_context` | Action | - | Sem docstring no código; revisar quando alterar a função. |
| `action_generate_candidates` | Action | model | Gera um mapa dos contextos existentes no Odoo, parecido com o fluxo de traduções.  A ideia é listar telas técnicas possíveis, marcar o que já está documentado e permitir que o admi |
| `action_recompute_existing_coverage` | Action | model | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.doc.source`

**Classe:** `HelpDocSource`  
**Arquivo:** `models/help_doc_source.py`  
**Descrição:** Fonte Markdown da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Nome | Sim | - | - |
| `module_name` | Char | Módulo | Sim | - | - |
| `file_path` | Char | Caminho do Arquivo | Sim | - | - |
| `doc_type` | Selection | Tipo | Sim | - | - |
| `overwrite_policy` | Selection | Política de Reimportação | Sim | - | - |
| `article_id` | Many2one | Artigo | Não | - | - |
| `last_import_date` | Datetime | Última Importação | Não | - | - |
| `checksum` | Char | Checksum | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `action_import` | Action | - | Sem docstring no código; revisar quando alterar a função. |
| `_import_file` | Método | - | Sem docstring no código; revisar quando alterar a função. |
| `_upsert_article` | Método | - | Sem docstring no código; revisar quando alterar a função. |
| `_import_contextual_blocks` | Método | - | Importa blocos no padrão:  <!-- HELP:ARTICLE code: document.document.form.create title: Como criar um novo documento module: document_core model: document.document view_type: form  |
| `_import_contextual_article` | Método | - | Sem docstring no código; revisar quando alterar a função. |
| `_link_article_to_context_from_meta` | Método | - | Sem docstring no código; revisar quando alterar a função. |
| `action_discover_installed_module_docs` | Action | model | Descobre docs/*.md dos módulos instalados e cria fontes Markdown.  A descoberta é idempotente: pode ser rodada sempre, como o fluxo de traduções do Odoo. Se o arquivo já existe com |
| `action_import_active_sources` | Action | model | Sem docstring no código; revisar quando alterar a função. |
| `_find_module_path` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_extract_title` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_split_front_matter` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_parse_metadata` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_make_article_code` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_make_context_article_code` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_default_context_name` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_bool_from_meta` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_normalize_article_type` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_normalize_scope` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_normalize_audience` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_category_from_meta` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_category_for_module` | Método | model | Categoria funcional por módulo. |
| `_category_for_type` | Método | model | Sem docstring no código; revisar quando alterar a função. |
| `_audience_for_type` | Método | model | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.feedback`

**Classe:** `HelpFeedback`  
**Arquivo:** `models/help_feedback.py`  
**Descrição:** Feedback da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `article_id` | Many2one | Artigo | Sim | - | - |
| `user_id` | Many2one | Usuário | Sim | - | - |
| `rating` | Selection | Avaliação | Sim | - | - |
| `comment` | Text | Comentário | Não | - | - |
| `model_name` | Char | Model de Origem | Não | - | - |
| `record_id` | Integer | Registro de Origem | Não | - | - |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.learning.path`

**Classe:** `HelpLearningPath`  
**Arquivo:** `models/help_learning.py`  
**Descrição:** Trilha de Aprendizado

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Nome | Sim | - | - |
| `module_name` | Char | Módulo | Não | - | - |
| `description` | Text | Descrição | Não | - | - |
| `audience` | Selection | Público | Sim | - | - |
| `sequence` | Integer | Sequência | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |
| `step_ids` | One2many | Passos | Não | - | - |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.learning.step`

**Classe:** `HelpLearningStep`  
**Arquivo:** `models/help_learning.py`  
**Descrição:** Passo da Trilha de Aprendizado

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `learning_path_id` | Many2one | Trilha | Sim | - | - |
| `name` | Char | Nome | Sim | - | - |
| `description` | Text | Descrição | Não | - | - |
| `article_id` | Many2one | Artigo | Não | - | - |
| `sequence` | Integer | Sequência | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.metric`

**Classe:** `HelpMetric`  
**Arquivo:** `models/help_metric.py`  
**Descrição:** Métrica de Uso da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `event_type` | Selection | Tipo de Evento | Sim | - | - |
| `article_id` | Many2one | Artigo | Não | - | - |
| `user_id` | Many2one | Usuário | Sim | - | - |
| `model_name` | Char | Model | Não | - | - |
| `view_type` | Char | Tipo de View | Não | - | - |
| `menu_xmlid` | Char | XML ID do Menu | Não | - | - |
| `action_xmlid` | Char | XML ID da Ação | Não | - | - |
| `record_id` | Integer | ID do Registro | Não | - | - |
| `query` | Char | Busca | Não | - | - |
| `error_text` | Text | Erro / Texto analisado | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `log_event` | Método | model | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.suggestion.rule`

**Classe:** `HelpSuggestionRule`  
**Arquivo:** `models/help_suggestion.py`  
**Descrição:** Regra de Sugestão Inteligente da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Nome | Sim | - | - |
| `code` | Char | Código | Não | - | - |
| `rule_type` | Selection | Tipo de Regra | Sim | - | - |
| `pattern` | Char | Padrão / Regex | Não | - | - |
| `module_name` | Char | Módulo | Não | - | - |
| `model_name` | Char | Model | Não | - | - |
| `field_name` | Char | Campo | Não | - | - |
| `state_value` | Char | Situação / Status | Não | - | - |
| `tip_text` | Text | Sugestão curta | Não | - | - |
| `article_ids` | Many2many | Artigos sugeridos | Não | - | - |
| `sequence` | Integer | Sequência | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `create` | Método | model_create_multi | Sem docstring no código; revisar quando alterar a função. |
| `_matches_text` | Método | - | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.tag`

**Classe:** `HelpTag`  
**Arquivo:** `models/help_tag.py`  
**Descrição:** Tag da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Nome | Sim | - | - |
| `color` | Integer | Cor | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `create` | Método | model_create_multi | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## Model: `help.tip`

**Classe:** `HelpTip`  
**Arquivo:** `models/help_tip.py`  
**Descrição:** Dica Contextual da Central de Ajuda

### Campos principais

| Campo | Tipo | Rótulo/Comodel | Obrigatório | Store | Ajuda |
| --- | --- | --- | --- | --- | --- |
| `name` | Char | Título | Sim | - | - |
| `code` | Char | Código | Não | - | - |
| `content` | Text | Dica | Sim | - | - |
| `module_name` | Char | Módulo | Não | - | - |
| `model_name` | Char | Model | Não | - | - |
| `view_type` | Selection | Tipo de View | Não | - | - |
| `field_name` | Char | Campo | Não | - | - |
| `audience` | Selection | Público | Sim | - | - |
| `article_id` | Many2one | Artigo relacionado | Não | - | - |
| `sequence` | Integer | Sequência | Não | - | - |
| `active` | Boolean | Ativo | Não | - | - |

### Métodos e funções

| Método | Tipo | Decoradores | Descrição |
| --- | --- | --- | --- |
| `create` | Método | model_create_multi | Sem docstring no código; revisar quando alterar a função. |

### Regras de manutenção

- Atualizar este bloco quando campos ou métodos forem alterados.
- Criar caso de teste no `04_GUIA_TESTES.md` quando o método alterar fluxo funcional.
- Criar artigo contextual em `08_AJUDA_CONTEXTUAL.md` quando a mudança afetar tela ou usuário final.


## 6. Views

| View XML ID | Model | Nome | Arquivo |
| --- | --- | --- | --- |
| view_help_article_search | help.article | help.article.search | views/help_article_views.xml |
| view_help_article_list | help.article | help.article.list | views/help_article_views.xml |
| view_help_article_form | help.article | help.article.form | views/help_article_views.xml |
| view_help_category_list | help.category | help.category.list | views/help_category_views.xml |
| view_help_category_form | help.category | help.category.form | views/help_category_views.xml |
| view_help_checklist_template_list | help.checklist.template | help.checklist.template.list | views/help_checklist_views.xml |
| view_help_checklist_template_form | help.checklist.template | help.checklist.template.form | views/help_checklist_views.xml |
| view_help_checklist_template_search | help.checklist.template | help.checklist.template.search | views/help_checklist_views.xml |
| view_help_checklist_progress_list | help.checklist.progress | help.checklist.progress.list | views/help_checklist_views.xml |
| view_help_context_candidate_list | help.context.candidate | help.context.candidate.list | views/help_context_candidate_views.xml |
| view_help_context_candidate_form | help.context.candidate | help.context.candidate.form | views/help_context_candidate_views.xml |
| view_help_context_candidate_search | help.context.candidate | help.context.candidate.search | views/help_context_candidate_views.xml |
| view_help_context_list | help.context | help.context.list | views/help_context_views.xml |
| view_help_context_form | help.context | help.context.form | views/help_context_views.xml |
| view_help_doc_source_list | help.doc.source | help.doc.source.list | views/help_doc_source_views.xml |
| view_help_doc_source_form | help.doc.source | help.doc.source.form | views/help_doc_source_views.xml |
| view_help_feedback_list | help.feedback | help.feedback.list | views/help_feedback_views.xml |
| view_help_feedback_form | help.feedback | help.feedback.form | views/help_feedback_views.xml |
| view_help_learning_path_list | help.learning.path | help.learning.path.list | views/help_learning_views.xml |
| view_help_learning_path_form | help.learning.path | help.learning.path.form | views/help_learning_views.xml |
| view_help_metric_search | help.metric | help.metric.search | views/help_metric_views.xml |
| view_help_metric_list | help.metric | help.metric.list | views/help_metric_views.xml |
| view_help_metric_form | help.metric | help.metric.form | views/help_metric_views.xml |
| view_help_suggestion_rule_search | help.suggestion.rule | help.suggestion.rule.search | views/help_suggestion_views.xml |
| view_help_suggestion_rule_list | help.suggestion.rule | help.suggestion.rule.list | views/help_suggestion_views.xml |
| view_help_suggestion_rule_form | help.suggestion.rule | help.suggestion.rule.form | views/help_suggestion_views.xml |
| view_help_tag_list | help.tag | help.tag.list | views/help_tag_views.xml |
| view_help_tag_form | help.tag | help.tag.form | views/help_tag_views.xml |
| view_help_tip_search | help.tip | help.tip.search | views/help_tip_views.xml |
| view_help_tip_list | help.tip | help.tip.list | views/help_tip_views.xml |
| view_help_tip_form | help.tip | help.tip.form | views/help_tip_views.xml |



## 7. Menus

| Menu XML ID | Arquivo | Atributos |
| --- | --- | --- |
| menu_help_root | views/help_menu_views.xml |  name="Central de Ajuda" sequence="95" web_icon="common_help_center,static/descr |
| menu_help_home | views/help_menu_views.xml |  name="Início" parent="menu_help_root" action="action_help_article" sequence="1" |
| menu_help_library | views/help_menu_views.xml |  name="Biblioteca" parent="menu_help_root" sequence="10"/ |
| menu_help_all_articles | views/help_menu_views.xml |  name="Todos os Artigos" parent="menu_help_library" action="action_help_article" |
| menu_help_manual | views/help_menu_views.xml |  name="Manual do Usuário" parent="menu_help_library" action="action_help_article |
| menu_help_technical | views/help_menu_views.xml |  name="Documentação Técnica" parent="menu_help_library" action="action_help_arti |
| menu_help_troubleshooting | views/help_menu_views.xml |  name="Troubleshooting" parent="menu_help_library" action="action_help_article_t |
| menu_help_contextual_root | views/help_menu_views.xml |  name="Ajuda Contextual" parent="menu_help_root" sequence="20"/ |
| menu_help_context_candidates | views/help_menu_views.xml |  name="Mapa de Contextos" parent="menu_help_contextual_root" action="action_help |
| menu_help_contexts | views/help_menu_views.xml |  name="Contextos de Ajuda" parent="menu_help_contextual_root" action="action_hel |
| menu_help_tips | views/help_menu_views.xml |  name="Dicas por Tela" parent="menu_help_contextual_root" action="action_help_ti |
| menu_help_checklists | views/help_menu_views.xml |  name="Checklists" parent="menu_help_contextual_root" action="action_help_checkl |
| menu_help_learning_path_root | views/help_menu_views.xml |  name="Onboarding" parent="menu_help_root" sequence="30"/ |
| menu_help_learning_path | views/help_menu_views.xml |  name="Trilhas de Aprendizado" parent="menu_help_learning_path_root" action="act |
| menu_help_checklist_progress | views/help_menu_views.xml |  name="Progresso dos Checklists" parent="menu_help_learning_path_root" action="a |
| menu_help_intelligence_root | views/help_menu_views.xml |  name="Inteligência Operacional" parent="menu_help_root" sequence="40"/ |
| menu_help_suggestion_rule | views/help_menu_views.xml |  name="Regras Inteligentes" parent="menu_help_intelligence_root" action="action_ |
| menu_help_metrics | views/help_menu_views.xml |  name="Métricas de Uso" parent="menu_help_intelligence_root" action="action_help |
| menu_help_feedback_root | views/help_menu_views.xml |  name="Feedback" parent="menu_help_root" sequence="50"/ |
| menu_help_feedback | views/help_menu_views.xml |  name="Avaliações" parent="menu_help_feedback_root" action="action_help_feedback |
| menu_help_config_root | views/help_menu_views.xml |  name="Configuração" parent="menu_help_root" sequence="90"/ |
| menu_help_categories | views/help_menu_views.xml |  name="Categorias" parent="menu_help_config_root" action="action_help_category"  |
| menu_help_tags | views/help_menu_views.xml |  name="Tags" parent="menu_help_config_root" action="action_help_tag" sequence="2 |
| menu_help_doc_sources | views/help_menu_views.xml |  name="Fontes Markdown" parent="menu_help_config_root" action="action_help_doc_s |
| menu_help_import | views/help_menu_views.xml |  name="Importar Documentação" parent="menu_help_config_root" action="action_help |



## 8. Actions

| Action XML ID | Arquivo |
| --- | --- |
| action_help_article | views/help_article_views.xml |
| action_help_article_manual | views/help_article_views.xml |
| action_help_article_technical | views/help_article_views.xml |
| action_help_article_troubleshooting | views/help_article_views.xml |
| action_help_category | views/help_category_views.xml |
| action_help_checklist_template | views/help_checklist_views.xml |
| action_help_checklist_progress | views/help_checklist_views.xml |
| action_help_context_candidate | views/help_context_candidate_views.xml |
| action_help_context | views/help_context_views.xml |
| action_help_doc_source | views/help_doc_source_views.xml |
| action_help_feedback | views/help_feedback_views.xml |
| action_help_learning_path | views/help_learning_views.xml |
| action_help_metric | views/help_metric_views.xml |
| action_help_suggestion_rule | views/help_suggestion_views.xml |
| action_help_tag | views/help_tag_views.xml |
| action_help_tip | views/help_tip_views.xml |



## 9. Dados iniciais e registros XML

| XML ID | Model | Arquivo |
| --- | --- | --- |
| help_category_overview | help.category | data/help_category_data.xml |
| help_category_system_help | help.category | data/help_category_data.xml |
| help_category_agenda | help.category | data/help_category_data.xml |
| help_category_document_core | help.category | data/help_category_data.xml |
| help_category_property_core | help.category | data/help_category_data.xml |
| help_category_governance | help.category | data/help_category_data.xml |
| help_category_document_dossier | help.category | data/help_category_data.xml |
| help_category_finance | help.category | data/help_category_data.xml |
| help_category_admin | help.category | data/help_category_data.xml |
| help_category_troubleshooting | help.category | data/help_category_data.xml |
| article_document_document_create | help.article | data/help_context_defaults_data.xml |
| article_document_document_list | help.article | data/help_context_defaults_data.xml |
| context_document_document_list | help.context | data/help_context_defaults_data.xml |
| context_document_document_form | help.context | data/help_context_defaults_data.xml |
| tip_document_document_form | help.tip | data/help_context_defaults_data.xml |
| checklist_document_document_form | help.checklist.template | data/help_context_defaults_data.xml |
| article_property_asset_form | help.article | data/help_context_defaults_data.xml |
| context_property_asset_form | help.context | data/help_context_defaults_data.xml |
| article_governance_case_form | help.article | data/help_context_defaults_data.xml |
| context_governance_case_form | help.context | data/help_context_defaults_data.xml |
| article_help_center_overview | help.article | data/help_default_content_data.xml |
| article_help_contextual_drawer | help.article | data/help_default_content_data.xml |
| article_help_agenda_activities | help.article | data/help_default_content_data.xml |
| article_help_error_troubleshooting | help.article | data/help_default_content_data.xml |
| tip_global_activities_agenda | help.tip | data/help_default_content_data.xml |
| tip_property_asset_docs | help.tip | data/help_default_content_data.xml |
| tip_governance_case_agenda | help.tip | data/help_default_content_data.xml |
| checklist_property_asset | help.checklist.template | data/help_default_content_data.xml |
| checklist_governance_case | help.checklist.template | data/help_default_content_data.xml |
| suggestion_missing_required | help.suggestion.rule | data/help_default_content_data.xml |
| suggestion_xml_view_error | help.suggestion.rule | data/help_default_content_data.xml |
| article_help_taxonomy_enterprise | help.article | data/help_enterprise_contexts_data.xml |
| article_document_validation_expiration | help.article | data/help_enterprise_contexts_data.xml |
| article_document_no_orphan | help.article | data/help_enterprise_contexts_data.xml |
| article_property_asset_list | help.article | data/help_enterprise_contexts_data.xml |
| article_property_asset_gallery_media | help.article | data/help_enterprise_contexts_data.xml |
| article_property_inspection_flow | help.article | data/help_enterprise_contexts_data.xml |
| article_property_maintenance_flow | help.article | data/help_enterprise_contexts_data.xml |
| article_property_media_flow | help.article | data/help_enterprise_contexts_data.xml |
| article_governance_case_list | help.article | data/help_enterprise_contexts_data.xml |
| article_governance_pending_flow | help.article | data/help_enterprise_contexts_data.xml |
| article_agenda_general_flow | help.article | data/help_enterprise_contexts_data.xml |
| context_help_article_form | help.context | data/help_enterprise_contexts_data.xml |
| context_document_document_list | help.context | data/help_enterprise_contexts_data.xml |
| context_document_document_form | help.context | data/help_enterprise_contexts_data.xml |
| context_property_asset_list | help.context | data/help_enterprise_contexts_data.xml |
| context_property_asset_form | help.context | data/help_enterprise_contexts_data.xml |
| context_property_inspection_form | help.context | data/help_enterprise_contexts_data.xml |
| context_property_maintenance_form | help.context | data/help_enterprise_contexts_data.xml |
| context_property_media_form | help.context | data/help_enterprise_contexts_data.xml |
| context_governance_case_list | help.context | data/help_enterprise_contexts_data.xml |
| context_governance_case_form | help.context | data/help_enterprise_contexts_data.xml |
| context_governance_pending_form | help.context | data/help_enterprise_contexts_data.xml |
| context_common_agenda_event_list | help.context | data/help_enterprise_contexts_data.xml |
| context_common_agenda_event_form | help.context | data/help_enterprise_contexts_data.xml |
| group_help_user | res.groups | security/help_security.xml |
| group_help_admin | res.groups | security/help_security.xml |
| group_help_technical | res.groups | security/help_security.xml |
| base.group_user | res.groups | security/help_security.xml |
| base.group_system | res.groups | security/help_security.xml |



## 10. Assets

| Bundle | Arquivos |
| --- | --- |
| web.assets_backend | common_help_center/static/src/components/help_systray/help_systray.js<br/>common_help_center/static/src/components/help_systray/help_systray.xml<br/>common_help_center/static/src/components/help_systray/help_systray.scss |



## 11. Segurança

Arquivos de segurança detectados:

| Arquivo |
| --- |
| security/ir.model.access.csv |
| security/help_security.xml |



Checklist obrigatório:

- [ ] Validar ACLs em `ir.model.access.csv`.
- [ ] Validar record rules para multiempresa e responsabilidade.
- [ ] Validar menus com usuário operacional e administrador.
- [ ] Validar que usuários sem permissão não acessam registros por URL direta.

## 12. Integração com Agenda Geral e Atividades

Quando o módulo tiver prazos ou compromissos operacionais, a regra é:

| Situação | Recurso |
| --- | --- |
| Tarefa individual, cobrança ou lembrete | `mail.activity` |
| Marco operacional, vistoria, manutenção, prazo formal ou compromisso | `common.agenda.event` |
| Reunião pessoal/nativa | `calendar.event` |

## 13. Integração com Central de Ajuda

- Documentos completos devem ficar em `docs/00` a `docs/07`.
- Ajuda contextual deve ficar em `docs/08_AJUDA_CONTEXTUAL.md`.
- Rode a importação da Central de Ajuda depois de alterar qualquer documento.
- Use o Mapa de Contextos para verificar cobertura.


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

## Mapa de Contextos — cobertura completa de views

A Central de Ajuda gera o mapa de cobertura a partir de três origens técnicas:

1. `ir.ui.view`: views técnicas do módulo, incluindo `form`, `list/tree`, `kanban`, `calendar`, `search`, `pivot`, `graph`, `activity`, `gantt`, `cohort`, `map` e `dashboard`.
2. `ir.actions.act_window`: cada modo de visualização declarado em `view_mode` gera um candidato próprio.
3. `ir.ui.menu`: menus com action de janela também geram candidatos por modo de visualização.

O tipo técnico `tree` é normalizado como `list`, porque no uso funcional ambos representam lista.

### Critério de cobertura

Um contexto é considerado documentado quando existe pelo menos um artigo publicado, ativo e marcado para aparecer no painel contextual, compatível com:

- módulo;
- model;
- tipo de view;
- action/menu, quando aplicável;
- campo, quando for ajuda de campo.

### Boas práticas

- Para models operacionais principais, crie artigos para `list`, `form` e `kanban` quando existirem esses modos.
- Para actions que abrem primeiro em `kanban`, não presuma que o formulário estará coberto: documente `kanban` e `form` separadamente.
- Use o Mapa de Contextos como checklist de documentação, semelhante à análise de termos pendentes em tradução.
