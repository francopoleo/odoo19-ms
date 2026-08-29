# Documentação Técnica — Document Core

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Gestão documental com documentos, categorias, tipos, validação, revisão, vencimento, localização, segurança e agenda documental.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `document_core` |
| Nome funcional | Document Core |
| Versão | `19.0.1.16.0` |
| Aplicação | `True` |
| Instalável | `True` |
| Dependências | `mail`, `common_base` |

### Arquivos declarados no manifesto

- `security/document_security.xml`
- `security/ir.model.access.csv`
- `data/document_sequence_data.xml`
- `data/document_seed_data.xml`
- `data/document_core_data.xml`
- `views/document_views.xml`
- `views/document_agenda_views.xml`
- `views/document_type_views.xml`
- `views/document_dashboard_views.xml`
- `views/document_communication_views.xml`
- `views/document_menu_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `document.document`

- **Classe:** `DocumentDocumentAgenda`
- **Arquivo:** `models/document_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `document.document`, `common.agenda.mixin`


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
| `_agenda_get_activity_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_description` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_agenda_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_schedule_document_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `document.category`

- **Classe:** `DocumentCategory`
- **Arquivo:** `models/document_category.py`
- **Descrição técnica:** Categoria de Documento


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_access_level` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `allow_website_publish` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `type_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `type_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_type_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_unique_code` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `document.communication`

- **Classe:** `DocumentCommunication`
- **Arquivo:** `models/document_communication.py`
- **Descrição técnica:** Comunicação de Documento

- **Heranças:** `mail.thread`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `tracking_token` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email_message_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `external_message_id` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email_from` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email_to` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email_cc` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `channel_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `channel_origin` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sent_by_odoo` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `communication_date` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Html` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `partner_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `communication_event_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `is_version_related` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_tracking_token` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_subject` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_mark_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `document.dashboard`

- **Classe:** `DocumentDashboard`
- **Arquivo:** `models/document_dashboard.py`
- **Descrição técnica:** Painel Operacional Documental


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_documents` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `complete_documents` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `incomplete_documents` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `expired_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `expiring_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `missing_file_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_validation_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `review_overdue_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `review_due_soon_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `review_up_to_date_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `my_docs_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `my_expired_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `my_expiring_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `my_review_overdue_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `my_missing_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `default_get` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_doc_action` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_refresh` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_all_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_complete_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_incomplete_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_expired` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_expiring` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_missing_files` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_pending_validation` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_review_overdue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_review_due_soon` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_review_up_to_date` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_docs` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_expired` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_expiring` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_review_overdue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_missing` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_expiring` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_validation` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `document.document`

- **Classe:** `DocumentDocument`
- **Arquivo:** `models/document_document.py`
- **Descrição técnica:** Documento

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `color` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `content` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_number` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `version` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_type_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `category_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `category_code` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_sensitive` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `issue_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `effective_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `expiry_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `review_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `next_review_date` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `review_status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `received_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `alert_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `issuer` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `validated_by` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `validation_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_issue_date` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_expiry` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_review` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_validation` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_validated` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `superseded_by_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_complete` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_completion_state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `missing_requirements` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `missing_requirements_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `missing_requirements_html` | `Html` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `has_physical_original` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `physical_location_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `physical_reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_physical_original` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `access_level` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `allowed_group_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `website_published` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `website_visibility` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `allow_download` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `attachment_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `attachment_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `preview_attachment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `primary_attachment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `primary_attachment_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `primary_attachment_mimetype` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `preview_available` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `preview_kind` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `preview_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `access_summary` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `communication_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_is_document_manager` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sanitize_operator_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_check_operator_write_vals` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `name_get` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_attachment_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_ordered_attachments` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_attachment_preview_kind` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_attachment_content_url` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_select_primary_attachment` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_preview_fields` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_attachment_ids_preview_selection` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_compute_is_validated` | Compute | Validar dependências, store, atualização automática e performance. |
| `_get_missing_requirements` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_document_completion_depends` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_document_complete` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_document_completion_state` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_missing_requirements` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_missing_requirements_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_missing_requirements_html` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_next_review_date` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_review_status` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_status` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_access_summary` | Compute | Validar dependências, store, atualização automática e performance. |
| `_apply_default_rules_from_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_document_type_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `action_open_attachments` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_preview_primary_attachment` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_check_dates` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_validation_required` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_document_rules` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_schedule_expiry_activity` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_schedule_validation_activity` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_schedule_review_activity` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_cron_check_expiry` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cron_check_validation` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cron_check_review` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_sync_attachment_ownership` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `document.location`

- **Classe:** `DocumentLocation`
- **Arquivo:** `models/document_location.py`
- **Descrição técnica:** Localização Física de Documento


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `site_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `room` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `cabinet` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `shelf` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `drawer` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `box` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `folder` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `responsible_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `display_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_display_name` | Compute | Validar dependências, store, atualização automática e performance. |

### Model `document.type`

- **Classe:** `DocumentType`
- **Arquivo:** `models/document_type.py`
- **Descrição técnica:** Tipo de Documento


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `category_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `scope` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `default_access_level` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `allow_website_publish` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `website_default_visibility` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `requires_issue_date` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_expiry` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_review` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_validation` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_physical_original` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_sensitive` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `review_cycle_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `allowed_file_types` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_document_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_unique_code` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_review_cycle_days` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `document.document` | `models/document_agenda_ext.py` | Modelo `document.document` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_deadline, _agenda_get_activity_type, _agenda_get_description, _sync_agenda_defaults, action_schedule_document_activity, create, write |
| `document.category` | `models/document_category.py` | Categoria de Documento | name, code, sequence, description, active, default_access_level, allow_website_publish, type_ids | _compute_type_count, _check_unique_code |
| `document.communication` | `models/document_communication.py` | Comunicação de Documento | tracking_token, email_message_id, external_message_id, email_from, email_to, email_cc, channel_type, channel_origin | _get_tracking_token, _normalize_subject, create, action_mark_done |
| `document.dashboard` | `models/document_dashboard.py` | Painel Operacional Documental | name, total_documents, complete_documents, incomplete_documents, expired_count, expiring_count, missing_file_count, pending_validation_count | default_get, _doc_action, action_refresh, action_view_all_documents, action_view_complete_documents, action_view_incomplete_documents, action_view_expired, action_view_expiring |
| `document.document` | `models/document_document.py` | Documento | active, sequence, color, name, description, content, reference, document_number | _is_document_manager, _sanitize_operator_vals, _check_operator_write_vals, name_get, _compute_attachment_count, _ordered_attachments, _attachment_preview_kind, _attachment_content_url |
| `document.location` | `models/document_location.py` | Localização Física de Documento | name, code, sequence, company_id, site_name, room, cabinet, shelf | _compute_display_name |
| `document.type` | `models/document_type.py` | Tipo de Documento | name, code, sequence, active, category_id, description, scope, default_access_level | _compute_document_count, _check_unique_code, _check_review_cycle_days |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_document_document_form_agenda_ext` | `document.document` | `views/document_agenda_views.xml` |
| `view_document_document_calendar` | `document.document` | `views/document_agenda_views.xml` |
| `view_document_communication_list` | `document.communication` | `views/document_communication_views.xml` |
| `view_document_communication_form` | `document.communication` | `views/document_communication_views.xml` |
| `view_document_communication_search` | `document.communication` | `views/document_communication_views.xml` |
| `view_document_dashboard_form` | `document.dashboard` | `views/document_dashboard_views.xml` |
| `view_document_category_list` | `document.category` | `views/document_type_views.xml` |
| `view_document_category_form` | `document.category` | `views/document_type_views.xml` |
| `view_document_category_search` | `document.category` | `views/document_type_views.xml` |
| `view_document_type_list` | `document.type` | `views/document_type_views.xml` |
| `view_document_type_form` | `document.type` | `views/document_type_views.xml` |
| `view_document_type_search` | `document.type` | `views/document_type_views.xml` |
| `view_document_location_list` | `document.location` | `views/document_type_views.xml` |
| `view_document_location_form` | `document.location` | `views/document_type_views.xml` |
| `view_document_location_search` | `document.location` | `views/document_type_views.xml` |
| `view_document_document_kanban` | `document.document` | `views/document_views.xml` |
| `view_document_document_list` | `document.document` | `views/document_views.xml` |
| `view_document_document_form` | `document.document` | `views/document_views.xml` |
| `view_document_document_search` | `document.document` | `views/document_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_document_calendar` | Agenda Documental | `document_core.menu_document_monitoring` | `common_base.action_common_agenda_calendar_document` | `views/document_agenda_views.xml` |
| `menu_document_root` | Documentos | `` | `` | `views/document_menu_views.xml` |
| `menu_document_dashboard` | Painel Operacional | `menu_document_root` | `action_document_dashboard` | `views/document_menu_views.xml` |
| `menu_document_operation` | Operação Documental | `menu_document_root` | `` | `views/document_menu_views.xml` |
| `menu_document_documents` | Todos os Documentos | `menu_document_operation` | `action_document_document` | `views/document_menu_views.xml` |
| `menu_document_monitoring` | Acompanhamento | `menu_document_root` | `` | `views/document_menu_views.xml` |
| `menu_document_pending_validation` | Pendentes de Validação Formal | `menu_document_monitoring` | `action_document_document_pending_validation` | `views/document_menu_views.xml` |
| `menu_document_without_files` | Sem Arquivo Anexado | `menu_document_monitoring` | `action_document_document_without_files` | `views/document_menu_views.xml` |
| `menu_document_expiring` | A Vencer | `menu_document_monitoring` | `action_document_document_expiring` | `views/document_menu_views.xml` |
| `menu_document_expired` | Vencidos | `menu_document_monitoring` | `action_document_document_expired` | `views/document_menu_views.xml` |
| `menu_document_with_files` | Com Arquivos | `menu_document_monitoring` | `action_document_document_with_files` | `views/document_menu_views.xml` |
| `menu_document_config` | Configuração Documental | `menu_document_root` | `` | `views/document_menu_views.xml` |
| `menu_document_type` | Tipos de Documento e Regras | `menu_document_config` | `action_document_type` | `views/document_menu_views.xml` |
| `menu_document_category` | Categorias Documentais | `menu_document_config` | `action_document_category` | `views/document_menu_views.xml` |
| `menu_document_location` | Localizações Físicas | `menu_document_config` | `action_document_location` | `views/document_menu_views.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_document_document_calendar` | Agenda Documental | `document.document` | `views/document_agenda_views.xml` |
| `action_document_communication` | Comunicações de Documento | `document.communication` | `views/document_communication_views.xml` |
| `action_document_dashboard` | Painel Operacional | `document.dashboard` | `views/document_dashboard_views.xml` |
| `action_document_category` | Categorias Documentais | `document.category` | `views/document_type_views.xml` |
| `action_document_type` | Tipos de Documento | `document.type` | `views/document_type_views.xml` |
| `action_document_location` | Localizações Físicas | `document.location` | `views/document_type_views.xml` |
| `action_document_document` | Todos os Documentos | `document.document` | `views/document_views.xml` |
| `action_document_document_with_files` | Documentos com Arquivos | `document.document` | `views/document_views.xml` |
| `action_document_document_without_files` | Documentos sem Arquivos | `document.document` | `views/document_views.xml` |
| `action_document_document_expiring` | Documentos a Vencer | `document.document` | `views/document_views.xml` |
| `action_document_document_expired` | Documentos Vencidos | `document.document` | `views/document_views.xml` |
| `action_document_document_pending_validation` | Pendentes de Validação | `document.document` | `views/document_views.xml` |


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
