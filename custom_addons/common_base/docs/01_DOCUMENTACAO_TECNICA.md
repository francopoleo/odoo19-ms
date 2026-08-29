# Documentação Técnica — Common Base

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Base compartilhada com padrões de agenda, atividades, segurança e componentes reutilizáveis para os demais módulos.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `common_base` |
| Nome funcional | Common Base |
| Versão | `19.0.1.0.0` |
| Aplicação | `True` |
| Instalável | `True` |
| Dependências | `mail`, `calendar`, `base` |

### Arquivos declarados no manifesto

- `security/common_security.xml`
- `security/ir.model.access.csv`
- `data/common_sequence_data.xml`
- `data/common_config_data.xml`
- `data/common_agenda_data.xml`
- `data/common_agenda_security_data.xml`
- `views/common_tag_views.xml`
- `views/common_config_views.xml`
- `views/access_overview_views.xml`
- `views/common_menu_views.xml`
- `views/common_agenda_calendar_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `access.overview`

- **Classe:** `AccessOverview`
- **Arquivo:** `models/access_overview.py`
- **Descrição técnica:** Visão Geral de Permissões


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `module` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `model_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `group_id` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `perm_read` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `perm_write` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `perm_create` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `perm_unlink` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_auto_init` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `init` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `common.agenda.event`

- **Classe:** `CommonAgendaEvent`
- **Arquivo:** `models/common_agenda_event.py`
- **Descrição técnica:** Agenda Geral

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `agenda_module` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `agenda_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `start` | `Datetime` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `stop` | `Datetime` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `duration_hours` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `all_day` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `location` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `user_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `responsible_user_ids` | `Many2many` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `visibility` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `visible_user_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `source_model` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source_res_id` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source_key` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source_ref` | `Reference` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `color` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_duration_hours` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_color` | Compute | Validar dependências, store, atualização automática e performance. |
| `_selection_source_ref` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_source_ref` | Compute | Validar dependências, store, atualização automática e performance. |
| `_agenda_user_is_manager` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_default_access_domain` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_open_source` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_mark_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_archive` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_scheduled` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `unlink` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `cleanup_legacy_agenda_rules` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `backfill_from_old_calendar_events` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `common.agenda.mixin`

- **Classe:** `CommonAgendaMixin`
- **Arquivo:** `models/common_agenda_mixin.py`
- **Descrição técnica:** Agenda e Atividades Operacionais


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `agenda_responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `agenda_deadline` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `agenda_start` | `Datetime` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `agenda_stop` | `Datetime` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `agenda_duration_hours` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `agenda_location` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `agenda_notes` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `agenda_visibility` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `agenda_viewer_user_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `agenda_calendar_event_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `agenda_calendar_synced` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_agenda_calendar_synced` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_agenda_start_duration` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_agenda_get_title` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_description` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_location` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_deadline` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_module` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_activity_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_responsible_users` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_visible_users` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_visibility` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_partners` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_start_stop` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_prepare_event_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_write_calendar_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_prepare_activity_meta_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_agenda_schedule_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_agenda_sync_calendar` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_agenda_sync_activity_and_calendar` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_agenda_open_calendar_event` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_agenda_remove_calendar_event` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_agenda_datetime_from_date` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `common.communication.base`

- **Classe:** `CommonCommunicationBase`
- **Arquivo:** `models/common_communication.py`
- **Descrição técnica:** Base para Comunicações Rastreáveis


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

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_tracking_token` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `common.config`

- **Classe:** `CommonConfig`
- **Arquivo:** `models/common_config.py`
- **Descrição técnica:** Configurações Gerais


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `governance_followup_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `governance_reminder_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `governance_silence_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_late_fee` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_interest_per_day` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `enable_auto_followup` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `enable_email_notifications` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `unlink` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `get_config` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `common.mixin`

- **Classe:** `CommonMixin`
- **Arquivo:** `models/common_mixin.py`
- **Descrição técnica:** Mixin com campos comuns


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `tag_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_default_company` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_archive` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_unarchive` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_attachments` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `common.sequence`

- **Classe:** `CommonSequence`
- **Arquivo:** `models/common_sequence.py`
- **Descrição técnica:** Sequência Numérica


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `prefix` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `suffix` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `padding` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `start_number` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `next_number` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_next_number` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_format_number` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `get_next` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `next_by_code` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `common.tag`

- **Classe:** `CommonTag`
- **Arquivo:** `models/common_tag.py`
- **Descrição técnica:** Tag Genérica


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `color` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `category` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `usage_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_usage_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_unique_name` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `action_toggle_active` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `res.partner`

- **Classe:** `ResPartnerContactResolver`
- **Arquivo:** `models/partner_resolution.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `res.partner`


#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `resolve_contact` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_resolve_contact_extended` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_resolver_cache` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `access.overview` | `models/access_overview.py` | Visão Geral de Permissões | module, model_name, group_id, perm_read, perm_write, perm_create, perm_unlink | _auto_init, init |
| `common.agenda.event` | `models/common_agenda_event.py` | Agenda Geral | name, active, agenda_module, agenda_type, state, start, stop, duration_hours | _compute_duration_hours, _compute_color, _selection_source_ref, _compute_source_ref, _agenda_user_is_manager, _default_access_domain, action_open_source, action_mark_done |
| `common.agenda.mixin` | `models/common_agenda_mixin.py` | Agenda e Atividades Operacionais | agenda_responsible_id, agenda_deadline, agenda_start, agenda_stop, agenda_duration_hours, agenda_location, agenda_notes, agenda_visibility | _compute_agenda_calendar_synced, _onchange_agenda_start_duration, _agenda_get_title, _agenda_get_description, _agenda_get_location, _agenda_get_deadline, _agenda_get_type, _agenda_get_module |
| `common.communication.base` | `models/common_communication.py` | Base para Comunicações Rastreáveis | tracking_token, email_message_id, external_message_id, email_from, email_to, email_cc, channel_type, channel_origin | _get_tracking_token |
| `common.config` | `models/common_config.py` | Configurações Gerais | name, company_id, governance_followup_days, governance_reminder_days, governance_silence_days, default_late_fee, default_interest_per_day, enable_auto_followup | unlink, get_config |
| `common.mixin` | `models/common_mixin.py` | Mixin com campos comuns | active, company_id, tag_ids | _get_default_company, action_archive, action_unarchive, action_open_attachments |
| `common.sequence` | `models/common_sequence.py` | Sequência Numérica | name, code, company_id, prefix, suffix, padding, start_number, next_number | _get_next_number, _format_number, get_next, next_by_code |
| `common.tag` | `models/common_tag.py` | Tag Genérica | name, sequence, color, active, company_id, category, description, usage_count | _compute_usage_count, _check_unique_name, action_toggle_active |
| `res.partner` | `models/partner_resolution.py` | Modelo `res.partner` usado pelo módulo. | sem campos declarados no arquivo analisado | resolve_contact, _resolve_contact_extended, _resolver_cache |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_access_overview_list` | `access.overview` | `views/access_overview_views.xml` |
| `view_access_overview_search` | `access.overview` | `views/access_overview_views.xml` |
| `view_common_agenda_calendar_event_calendar` | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `view_common_agenda_calendar_event_list` | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `view_common_agenda_calendar_event_form` | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `view_common_agenda_calendar_event_search` | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `view_common_config_form` | `common.config` | `views/common_config_views.xml` |
| `view_common_tag_list` | `common.tag` | `views/common_tag_views.xml` |
| `view_common_tag_form` | `common.tag` | `views/common_tag_views.xml` |
| `view_common_tag_search` | `common.tag` | `views/common_tag_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_access_overview` | Permissões por Módulo | `base.menu_administration` | `action_access_overview` | `views/access_overview_views.xml` |
| `menu_common_agenda_root` | Agenda Geral | `` | `` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_my` | Minha Agenda | `menu_common_agenda_root` | `action_common_agenda_calendar_my` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_all` | Calendário Geral | `menu_common_agenda_root` | `action_common_agenda_calendar_all` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_property_root` | Imóveis | `menu_common_agenda_root` | `` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_property_all` | Todos de Imóveis | `menu_common_agenda_property_root` | `action_common_agenda_calendar_property` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_property_inspection` | Vistorias | `menu_common_agenda_property_root` | `action_common_agenda_calendar_inspection` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_property_maintenance` | Manutenções | `menu_common_agenda_property_root` | `action_common_agenda_calendar_maintenance` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_property_contract` | Contratos | `menu_common_agenda_property_root` | `action_common_agenda_calendar_contract` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_governance_root` | Governança | `menu_common_agenda_root` | `` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_governance_all` | Todos de Governança | `menu_common_agenda_governance_root` | `action_common_agenda_calendar_governance` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_governance_case` | Marcos dos Casos | `menu_common_agenda_governance_root` | `action_common_agenda_calendar_governance_case` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_governance_response_deadline` | Prazos de Resposta | `menu_common_agenda_governance_root` | `action_common_agenda_calendar_governance_response_deadline` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_governance_resolution_deadline` | Prazos de Resolução | `menu_common_agenda_governance_root` | `action_common_agenda_calendar_governance_resolution_deadline` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_governance_followup` | Follow-ups | `menu_common_agenda_governance_root` | `action_common_agenda_calendar_governance_followup` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_governance_pending` | Pendências | `menu_common_agenda_governance_root` | `action_common_agenda_calendar_pending` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_governance_meeting` | Compromissos | `menu_common_agenda_governance_root` | `action_common_agenda_calendar_governance_meeting` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_document_root` | Documentos | `menu_common_agenda_root` | `` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_document_all` | Todos de Documentos | `menu_common_agenda_document_root` | `action_common_agenda_calendar_document` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_document_item` | Documentos | `menu_common_agenda_document_root` | `action_common_agenda_calendar_document_item` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_document_dossier` | Dossiês | `menu_common_agenda_document_root` | `action_common_agenda_calendar_dossier` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_financial_root` | Financeiro | `menu_common_agenda_root` | `` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_financial_all` | Todos do Financeiro | `menu_common_agenda_financial_root` | `action_common_agenda_calendar_financial` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_financial_rent` | Parcelas / Aluguéis | `menu_common_agenda_financial_root` | `action_common_agenda_calendar_rent` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_financial_adjustment` | Reajustes | `menu_common_agenda_financial_root` | `action_common_agenda_calendar_rent_adjustment` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_financial_amendment` | Aditivos | `menu_common_agenda_financial_root` | `action_common_agenda_calendar_contract_amendment` | `views/common_agenda_calendar_views.xml` |
| `menu_common_agenda_financial_payment_proof` | Comprovantes | `menu_common_agenda_financial_root` | `action_common_agenda_calendar_payment_proof` | `views/common_agenda_calendar_views.xml` |
| `menu_common_root` | Configurações | `` | `` | `views/common_menu_views.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_access_overview` | Permissões por Módulo | `access.overview` | `views/access_overview_views.xml` |
| `action_common_agenda_calendar_my` | Minha Agenda | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_all` | Agenda Geral | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_property` | Agenda de Imóveis | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_inspection` | Vistorias | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_maintenance` | Manutenções | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_governance` | Agenda de Governança | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_governance_case` | Marcos dos Casos | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_governance_response_deadline` | Prazos de Resposta | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_governance_resolution_deadline` | Prazos de Resolução | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_governance_followup` | Follow-ups de Governança | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_pending` | Pendências de Governança | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_governance_meeting` | Compromissos de Governança | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_document` | Agenda Documental | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_document_item` | Documentos | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_dossier` | Dossiês | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_financial` | Agenda Financeira | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_contract` | Contratos | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_rent` | Parcelas / Aluguéis | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_rent_adjustment` | Reajustes | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_contract_amendment` | Aditivos | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_agenda_calendar_payment_proof` | Comprovantes | `common.agenda.event` | `views/common_agenda_calendar_views.xml` |
| `action_common_tag` | Tags | `common.tag` | `views/common_tag_views.xml` |


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
