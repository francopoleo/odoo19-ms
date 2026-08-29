# Documentação Técnica — Document Dossier - Aggregator

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Agregação de documentos em dossiês, templates e checklists de completude por processo.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `document_dossier` |
| Nome funcional | Document Dossier - Aggregator |
| Versão | `19.0.2.1.2` |
| Aplicação | `False` |
| Instalável | `True` |
| Dependências | `document_core` |

### Arquivos declarados no manifesto

- `security/groups.xml`
- `security/ir.model.access.csv`
- `views/document_dossier_template_views.xml`
- `views/dossier_views.xml`
- `views/dossier_agenda_views.xml`
- `views/document_document_dossier_ext_views.xml`
- `views/dossier_menu_views.xml`
- `views/document_move_to_dossier_wizard_views.xml`
- `views/document_apply_template_wizard_views.xml`
- `views/dossier_assign_wizard_views.xml`
- `data/dossier_process_data.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `document.apply.template.wizard`

- **Classe:** `DocumentApplyTemplateWizard`
- **Arquivo:** `models/document_apply_template_wizard.py`
- **Descrição técnica:** Aplicar Template de Dossiê


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `dossier_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `template_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `create_only_missing` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `action_apply_template` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `document.document`

- **Classe:** `DocumentDocumentDossierExt`
- **Arquivo:** `models/document_document_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `document.document`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `dossier_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `dossier_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_dossier_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_dossiers` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_add_to_dossier` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `document.dossier.template`

- **Classe:** `DocumentDossierTemplate`
- **Arquivo:** `models/document_dossier_template.py`
- **Descrição técnica:** Template de Dossiê Documental


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `line_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `required_line_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_line_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_line_counts` | Compute | Validar dependências, store, atualização automática e performance. |

### Model `document.dossier.template.line`

- **Classe:** `DocumentDossierTemplateLine`
- **Arquivo:** `models/document_dossier_template.py`
- **Descrição técnica:** Item do Template de Dossiê


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `template_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_type_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `category_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `required` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_file` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_onchange_document_type_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_check_name` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `document.move.to.dossier.wizard`

- **Classe:** `DocumentMoveToDossierWizard`
- **Arquivo:** `models/document_move_to_dossier_wizard.py`
- **Descrição técnica:** Vincular Documento ao Dossiê


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `document_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `dossier_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `action_link` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_move` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `dossier.dossier`

- **Classe:** `DossierDossierAgenda`
- **Arquivo:** `models/dossier_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `dossier.dossier`, `mail.thread`, `mail.activity.mixin`, `common.agenda.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `agenda_responsible_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `agenda_partner_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_agenda_get_title` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_deadline` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_description` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_agenda_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_schedule_dossier_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `dossier.assign.wizard`

- **Classe:** `DossierAssignWizard`
- **Arquivo:** `models/dossier_assign_wizard.py`
- **Descrição técnica:** Atribuir Dossiê ao Registro


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `target_model` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `target_id` | `Integer` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `target_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mode` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `dossier_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `process_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `template_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `responsible_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `include_existing_documents` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `include_related_documents` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `create_template_documents` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `create_only_missing` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `default_get` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_default_dossier_name` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_default_description` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_default_process_id` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_default_responsible_id` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_process_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_get_target_record` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_create_or_select_dossier` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_link_dossier_to_target` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_assign_dossier` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `dossier.dossier`

- **Classe:** `DossierDossier`
- **Arquivo:** `models/dossier_dossier.py`
- **Descrição técnica:** Document Dossier - Aggregator for Document Collections


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `process_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `domain` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `target_model` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `target_res_id` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `target_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `target_display` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `responsible_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `created_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `target_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `closed_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `complete_documents` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `incomplete_documents` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `missing_requirements` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `completion_percent` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dossier_complete` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_domain` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_target_display` | Compute | Validar dependências, store, atualização automática e performance. |
| `_get_target_record` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_document_vals_from_target` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_document_domain_from_target` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_link_existing_documents_from_target` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_find_template_line_document` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_document_vals_from_template_line` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_apply_template` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `apply_templates` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_document_stats` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_completion_percent` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_dossier_complete` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_activate` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_close` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reopen` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_apply_template` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_incomplete` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `dossier.process`

- **Classe:** `DossierProcess`
- **Arquivo:** `models/dossier_process.py`
- **Descrição técnica:** Definição de Tipo de Processo/Fluxo para Dossiês


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `domain` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `template_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `template_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dossier_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_template_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_dossier_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_dossiérs` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `document.apply.template.wizard` | `models/document_apply_template_wizard.py` | Aplicar Template de Dossiê | dossier_id, template_id, create_only_missing | action_apply_template |
| `document.document` | `models/document_document_ext.py` | Modelo `document.document` usado pelo módulo. | dossier_ids, dossier_count | _compute_dossier_count, action_view_dossiers, action_add_to_dossier |
| `document.dossier.template` | `models/document_dossier_template.py` | Template de Dossiê Documental | active, sequence, name, code, description, line_ids, required_line_count, total_line_count | _compute_line_counts |
| `document.dossier.template.line` | `models/document_dossier_template.py` | Item do Template de Dossiê | template_id, sequence, name, document_type_id, category_id, required, requires_file, description | _onchange_document_type_id, _check_name |
| `document.move.to.dossier.wizard` | `models/document_move_to_dossier_wizard.py` | Vincular Documento ao Dossiê | document_id, dossier_id | action_link, action_move |
| `dossier.dossier` | `models/dossier_agenda_ext.py` | Modelo `dossier.dossier` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_deadline, _agenda_get_description, _sync_agenda_defaults, action_schedule_dossier_activity, create, write |
| `dossier.assign.wizard` | `models/dossier_assign_wizard.py` | Atribuir Dossiê ao Registro | target_model, target_id, target_name, mode, dossier_id, process_id, template_id, name | default_get, _default_dossier_name, _default_description, _default_process_id, _default_responsible_id, _onchange_process_id, _get_target_record, _create_or_select_dossier |
| `dossier.dossier` | `models/dossier_dossier.py` | Document Dossier - Aggregator for Document Collections | name, description, process_id, domain, target_model, target_res_id, target_name, target_display | _compute_domain, _compute_target_display, _get_target_record, _prepare_document_vals_from_target, _document_domain_from_target, _link_existing_documents_from_target, _find_template_line_document, _prepare_document_vals_from_template_line |
| `dossier.process` | `models/dossier_process.py` | Definição de Tipo de Processo/Fluxo para Dossiês | name, description, domain, sequence, active, template_ids, template_count, dossier_count | _compute_template_count, _compute_dossier_count, action_view_dossiérs |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_document_apply_template_wizard_form` | `document.apply.template.wizard` | `views/document_apply_template_wizard_views.xml` |
| `view_document_document_list_dossier_ext` | `document.document` | `views/document_document_dossier_ext_views.xml` |
| `view_document_document_form_dossier_ext` | `document.document` | `views/document_document_dossier_ext_views.xml` |
| `view_document_document_search_dossier_ext` | `document.document` | `views/document_document_dossier_ext_views.xml` |
| `view_document_dossier_template_list` | `document.dossier.template` | `views/document_dossier_template_views.xml` |
| `view_document_dossier_template_form` | `document.dossier.template` | `views/document_dossier_template_views.xml` |
| `view_document_dossier_template_search` | `document.dossier.template` | `views/document_dossier_template_views.xml` |
| `view_document_move_to_dossier_wizard_form` | `document.move.to.dossier.wizard` | `views/document_move_to_dossier_wizard_views.xml` |
| `view_dossier_dossier_form_agenda_ext` | `dossier.dossier` | `views/dossier_agenda_views.xml` |
| `view_dossier_dossier_calendar` | `dossier.dossier` | `views/dossier_agenda_views.xml` |
| `view_dossier_assign_wizard_form` | `dossier.assign.wizard` | `views/dossier_assign_wizard_views.xml` |
| `view_dossier_process_tree` | `dossier.process` | `views/dossier_views.xml` |
| `view_dossier_process_form` | `dossier.process` | `views/dossier_views.xml` |
| `view_dossier_process_search` | `dossier.process` | `views/dossier_views.xml` |
| `view_dossier_dossier_kanban` | `dossier.dossier` | `views/dossier_views.xml` |
| `view_dossier_dossier_tree` | `dossier.dossier` | `views/dossier_views.xml` |
| `view_dossier_dossier_form` | `dossier.dossier` | `views/dossier_views.xml` |
| `view_dossier_dossier_search` | `dossier.dossier` | `views/dossier_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_dossier_calendar` | Agenda de Dossiês | `document_dossier.menu_dossier_root` | `action_dossier_dossier_calendar` | `views/dossier_agenda_views.xml` |
| `menu_dossier_root` | Dossiês | `document_core.menu_document_root` | `` | `views/dossier_menu_views.xml` |
| `menu_dossier_dossier` | Meus Dossiês | `menu_dossier_root` | `action_dossier_dossier` | `views/dossier_menu_views.xml` |
| `menu_dossier_documents` | Documentos do Dossiê | `menu_dossier_root` | `action_dossier_documents` | `views/dossier_menu_views.xml` |
| `menu_dossier_standalone_documents` | Documentos Avulsos | `menu_dossier_root` | `action_dossier_standalone_documents` | `views/dossier_menu_views.xml` |
| `menu_dossier_missing_documents` | Documentos Faltantes | `menu_dossier_root` | `action_dossier_missing_documents` | `views/dossier_menu_views.xml` |
| `menu_dossier_process` | Tipos de Processo | `menu_dossier_root` | `action_dossier_process` | `views/dossier_menu_views.xml` |
| `menu_dossier_template` | Templates de Dossiê | `menu_dossier_root` | `action_dossier_template` | `views/dossier_menu_views.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_document_dossier_template` | Templates de Dossiê | `document.dossier.template` | `views/document_dossier_template_views.xml` |
| `action_dossier_dossier_calendar` | Agenda de Dossiês | `dossier.dossier` | `views/dossier_agenda_views.xml` |
| `action_dossier_process` | Tipos de Processo | `dossier.process` | `views/dossier_views.xml` |
| `action_dossier_dossier` | Dossiês | `dossier.dossier` | `views/dossier_views.xml` |
| `action_dossier_documents` | Documentos do Dossiê | `document.document` | `views/dossier_views.xml` |
| `action_dossier_standalone_documents` | Documentos Avulsos | `document.document` | `views/dossier_views.xml` |
| `action_dossier_missing_documents` | Documentos Faltantes | `document.document` | `views/dossier_views.xml` |
| `action_dossier_template` | Templates de Dossiê | `document.dossier.template` | `views/dossier_views.xml` |


## 7. Integração com Central de Ajuda

Este módulo deve manter artigos contextuais em `docs/08_AJUDA_CONTEXTUAL.md`. Cada artigo deve ter bloco `HELP:ARTICLE` com `code` único. A Central de Ajuda complementa automaticamente o texto com opções dinâmicas da tela, evitando documentação desatualizada.

## Padrão de documentação dinâmica

A Central de Ajuda v18 exibe automaticamente, no drawer da tela, uma seção chamada **Campos, opções e filtros desta tela**. Essa seção é gerada em tempo real a partir do Odoo e pode incluir:

| Informação dinâmica | Origem | Como deve aparecer na documentação |
|---|---|---|
| Campos obrigatórios | Definição do model/view | O texto explica a finalidade do campo e exemplos; a lista real é dinâmica. |
| Opções de campos `selection` | Código Python do model | O texto explica critérios de escolha; não repetir todas as opções manualmente. |
| Categorias, tipos, etapas e responsáveis | Cadastros relacionados por Many2one/Many2many | O texto explica a governança do cadastro; a Central mostra os valores atuais. |
| Filtros e agrupamentos | Search views do Odoo | O texto explica cenários de uso; a Central mostra filtros reais disponíveis. |
| Artigos contextuais | `docs/08_AJUDA_CONTEXTUAL.md` | Blocos `HELP:ARTICLE` com `code` único e escopo curto. |

### Como escrever o texto

- Use exemplos práticos com dados fictícios.
- Explique a consequência operacional de cada escolha.
- Evite colar listas extensas de opções configuráveis.
- Quando uma opção for crítica, explique o critério de uso, não apenas o nome.
- Se uma regra depender do cliente, documente a regra de configuração, não valores fixos.

## 8. Integração com Agenda Geral e atividades

- Use **Atividades** para tarefas individuais, cobranças e lembretes.
- Use **Agenda Geral** para marcos críticos, compromissos operacionais e prazos relevantes.
- Não use o calendário nativo do Odoo para compromissos operacionais específicos do ERP, salvo reuniões normais.
- Registros com histórico devem ser cancelados/arquivados, não excluídos sem necessidade.

## 9. Checklist técnico antes de entregar alteração

- [ ] Atualizar fields/methods neste documento.
- [ ] Atualizar manual quando mudar fluxo ou tela.
- [ ] Atualizar `08_AJUDA_CONTEXTUAL.md` quando mudar contexto do drawer.
- [ ] Rodar importação da Central de Ajuda.
- [ ] Revisar Mapa de Contextos.
- [ ] Testar permissões e visibilidade.
- [ ] Atualizar changelog funcional.
