# Documentação Técnica — Governance & Audit

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Gestão de casos de governança, SLA, pendências, comunicações institucionais e marcos críticos na Agenda Geral.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `governance` |
| Nome funcional | Governance & Audit |
| Versão | `19.0.1.1.4` |
| Aplicação | `True` |
| Instalável | `True` |
| Dependências | `mail`, `common_base` |

### Arquivos declarados no manifesto

- `security/governance_security.xml`
- `security/ir.model.access.csv`
- `data/governance_stage_data.xml`
- `data/governance_case_type_data.xml`
- `data/governance_sla_rule_data.xml`
- `data/governance_email_channel_data.xml`
- `data/governance_activity_data.xml`
- `data/mail_templates.xml`
- `data/governance_cron.xml`
- `views/governance_case_participant_views.xml`
- `views/governance_case_type_template_views.xml`
- `views/governance_case_views.xml`
- `views/governance_case_operational_views.xml`
- `views/governance_agenda_views.xml`
- `views/governance_dashboard_views.xml`
- `views/governance_case_response_views.xml`
- `views/governance_case_communication_email_ext_views.xml`
- `views/governance_sla_rule_views.xml`
- `views/governance_email_channel_views.xml`
- `views/governance_case_type_email_ext_views.xml`
- `views/governance_case_email_ext_views.xml`
- `views/governance_menu_views.xml`
- `views/governance_email_test_views.xml`
- `views/governance_menu_email_ext_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `governance.case`

- **Classe:** `GovernanceCaseAgenda`
- **Arquivo:** `models/governance_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `governance.case`, `common.agenda.mixin`


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
| `_governance_case_is_closed` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_governance_case_marker_domain` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_governance_prepare_marker_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_governance_sync_marker` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_governance_close_case_markers` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_sync_governance_agenda_markers` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_schedule_case_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_governance_sync_agenda_complete` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `governance.case.pending`

- **Classe:** `GovernancePendingAgenda`
- **Arquivo:** `models/governance_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `governance.case.pending`, `common.agenda.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `agenda_responsible_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `agenda_partner_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_agenda_get_title` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_deadline` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_activity_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_description` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_agenda_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_pending_agenda_state` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `governance.case.communication`

- **Classe:** `GovernanceCommunicationAgenda`
- **Arquivo:** `models/governance_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `governance.case.communication`, `common.agenda.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `agenda_responsible_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `agenda_partner_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_agenda_get_title` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_description` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_agenda_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_communication_agenda_state` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `governance.case`

- **Classe:** `GovernanceCase`
- **Arquivo:** `models/governance_case.py`
- **Descrição técnica:** Caso de Governança

- **Heranças:** `mail.thread`, `mail.activity.mixin`, `common.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Html` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `origin_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_deadline` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `stage_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `status` | `Selection` | Não | Sim | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `tag_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `case_type_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `case_type_color` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `stage_color` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `priority` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `type_sla_days` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `require_primary_participant` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_followup_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_create_followup_activity` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `resolution_deadline` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `participant_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `communication_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `pending_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `response_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `participant_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `communication_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_open_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_volume` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `checklist_generated` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `checklist_progress` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `primary_partner_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `email_sent_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_followup_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `days_without_response` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_overdue` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `followup_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `followup_activity_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `has_open_pendings` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_response_attention` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `next_action_date` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `work_queue_status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `response_state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `last_communication_datetime` | `Datetime` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `next_pending_due_date` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `open_required_pending_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `overdue_pending_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_due_7d_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_request_open_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `aging_bucket` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `sla_status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_type_stage_colors` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_type_settings` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_sla_days` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_resolution_deadline` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_is_overdue` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_days_without_response` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_response_deadline` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_participant_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_operational_counts` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_checklist_progress` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_primary_partner` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_queue_fields` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_operational_status` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_executive_kpis` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_followup_activity_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_case_type_id_apply_defaults` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_sync_partner_ids_from_participants` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ensure_required_primary_participant` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_create_initial_followup_activity_if_needed` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_stage_by_type_or_default` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_apply_stage_transition` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_create_default_pendings_from_case_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_generate_default_pendings` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_participants` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_communications` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_pendings` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_required_pendings` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_response_requests` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_overdue_pendings` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_pending_due_7d` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_responses` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_activities` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_next_pending` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_new_communication` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_new_response` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_new_pending` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_check_dates` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_primary_participant_required` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_stage_allowed_by_case_type` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `action_cron_check_overdue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cron_schedule_followups` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cron_schedule_operational_alerts` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_send_followup_email` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_validate_transition_requirements` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_log_first_contact` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_waiting` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_no_response` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_send_email` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_register_response` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_register_no_response` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_close` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_work_queue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_my_queue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_read_group_stage_ids` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `governance.case.communication`

- **Classe:** `GovernanceCaseCommunication`
- **Arquivo:** `models/governance_case_communication.py`
- **Descrição técnica:** Comunicação do Caso de Governança

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
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `communication_datetime` | `Datetime` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `communication_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `direction` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `participant_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `note` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_response` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_deadline` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_received` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_tracking_token` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_subject` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_participant_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_case_from_communication` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_open_case` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_register_response` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_create_pending` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `governance.case.communication`

- **Classe:** `GovernanceCaseCommunication`
- **Arquivo:** `models/governance_case_communication_email_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `governance.case.communication`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `partner_match_source` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `partner_match_confidence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `governance.case`

- **Classe:** `GovernanceCase`
- **Arquivo:** `models/governance_case_email_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `governance.case`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `email_channel_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `message_origin` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `requires_triage` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `triage_done` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `triage_notes` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `incoming_email_from` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `incoming_email_to` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `incoming_email_cc` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_inbound_email_datetime` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_outbound_email_datetime` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `resolution_sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `followup_sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `effective_sla_rule_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_effective_sla_rule` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_email_sla_rule_fields` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_sla_days` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_response_deadline` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_email_channel_id_apply_defaults` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_check_email_channel_case_type_consistency` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_apply_case_type_defaults_to_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_apply_email_channel_defaults_to_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_email_channel_from_message` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_or_create_partner_from_email` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_register_email_communication_from_message` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `message_new` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `message_update` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_mark_triage_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `governance.case.participant`

- **Classe:** `GovernanceCaseParticipant`
- **Arquivo:** `models/governance_case_participant.py`
- **Descrição técnica:** Participante do Caso de Governança


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `role` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `is_primary` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `note` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_contact_channels` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_unique_participant_role` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_single_primary` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `unlink` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_primary_flag` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_is_primary` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |

### Model `governance.case.pending`

- **Classe:** `GovernanceCasePending`
- **Arquivo:** `models/governance_case_pending.py`
- **Descrição técnica:** Pendência do Caso de Governança

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `participant_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `communication_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `template_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `response_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stage_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `description` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `due_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `required` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `priority` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `date_done` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_overdue` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `age_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `deadline_bucket` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_pending_metrics` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_participant_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `action_mark_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reopen` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_case` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `governance.case.response`

- **Classe:** `GovernanceCaseResponse`
- **Arquivo:** `models/governance_case_response.py`
- **Descrição técnica:** Resposta do Caso de Governança

- **Heranças:** `mail.thread`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `communication_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `participant_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `response_date` | `Date` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `outcome` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `close_open_pendings` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `note` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_onchange_participant_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_case_from_response` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_open_case` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `governance.case.type`

- **Classe:** `GovernanceCaseType`
- **Arquivo:** `models/governance_case_type.py`
- **Descrição técnica:** Tipo de Caso de Governança


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `color` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_priority` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `require_primary_participant` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_followup_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_create_followup_activity` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `require_response_before_done` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `require_required_pendings_done` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `require_no_open_pendings_to_close` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `allowed_stage_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `initial_stage_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `waiting_stage_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `no_response_stage_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `done_stage_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `closed_stage_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `pending_template_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `pending_template_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_pending_template_count` | Compute | Validar dependências, store, atualização automática e performance. |

### Model `governance.case.type`

- **Classe:** `GovernanceCaseType`
- **Arquivo:** `models/governance_case_type_email_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `governance.case.type`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `default_responsible_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `response_sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `resolution_sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `followup_sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sla_low_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sla_medium_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sla_high_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sla_critical_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_email_alias` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_email_from` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_email_reply_to` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_email_to` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email_subject_prefix` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email_template_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `email_default_cc` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email_default_body` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `require_email_response` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email_channel_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `email_channel_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_email_channel_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_open_email_channels` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_check_sla_defaults_non_negative` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_onchange_resolution_sla_days_sync_legacy` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_followup_sla_days_sync_legacy` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |

### Model `governance.case.type.pending.template`

- **Classe:** `GovernanceCaseTypePendingTemplate`
- **Arquivo:** `models/governance_case_type_template.py`
- **Descrição técnica:** Modelo de Pendência por Tipo de Caso


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `case_type_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_deadline_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `priority` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `assign_to_responsible` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `required` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `governance.dashboard`

- **Classe:** `GovernanceDashboard`
- **Arquivo:** `models/governance_dashboard.py`
- **Descrição técnica:** Painel Operacional de Governança


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_active_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_urgent_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_attention_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_ok_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_critical_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_high_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_overdue_sla_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_due_soon_sla_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_on_track_sla_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_waiting_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_no_response_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `response_open_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_open_total` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_overdue_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_today_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_next7_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_my_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_my_urgent_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_my_overdue_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pending_my_today_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_planned_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_sent_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_waiting_status_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_partial_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_no_response_status_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_done_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_closed_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `default_get` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_case_action` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_pending_action` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_comm_action` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_refresh` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_active` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_urgent` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_attention` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_ok` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_critical` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_high` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_overdue_sla` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_due_soon_sla` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_on_track_sla` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_waiting` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_no_response` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_response_open` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_pending_all` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_pending_overdue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_pending_today` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_pending_next7` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_cases` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_urgent` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_pending_overdue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_my_pending_today` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_status_planned` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_status_sent` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_status_waiting` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_status_partial` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_status_no_response` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_status_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_status_closed` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_cases` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_work_queue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_my_queue` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_pendings` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_communications` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_shortcut_executive` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `governance.email.channel`

- **Classe:** `GovernanceEmailChannel`
- **Arquivo:** `models/governance_email_channel.py`
- **Descrição técnica:** Canal de E-mail de Governança

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `alias_name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `alias_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `alias_email` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `case_type_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `allowed_case_type_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `auto_assign_type` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_triage` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `priority` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `create_case_from_email` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `update_existing_case` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_add_sender_as_participant` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `require_response_by_default` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_alias_email` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_alias_name` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_default_type_allowed` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_company_consistency` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_case_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_alias_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_create_or_update_alias` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_alias` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_case_type` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_cases` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_find_by_message_recipients` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `governance.email.test`

- **Classe:** `GovernanceEmailTest`
- **Arquivo:** `models/governance_email_test.py`
- **Descrição técnica:** Teste de E-mail da Governança

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `external_email` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `outbound_email` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reply_to_email` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `test_token` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `subject` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `body_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `channel_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `case_type_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `case_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sent_message_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sent_mail_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sent_datetime` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_check_datetime` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `received_datetime` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bounce_datetime` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `fetch_executed_datetime` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `inbound_found` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bounce_found` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `outbound_sent_ok` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mail_state` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `failure_reason` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `result_summary` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `diagnostic_log` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_default_name` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_build_subject` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_build_body_html` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_generate_token` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_subject` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_append_log` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_find_default_channel` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_or_create_external_partner` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_prepare_case` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_create_or_send_mail` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_send_test_email` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_fetch_incoming_mail` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_search_token_in_mail_messages` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_search_token_in_communications` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_check_results` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_fetch_and_check` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_set_result_summary` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_open_case` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reset_test` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `governance.sla.rule`

- **Classe:** `GovernanceSlaRule`
- **Arquivo:** `models/governance_sla_rule.py`
- **Descrição técnica:** Regra de SLA de Governança


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `case_type_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `priority` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `response_sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `resolution_sla_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `followup_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_create_followup_activity` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_positive_days` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `get_effective_rule` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `governance.stage`

- **Classe:** `GovernanceStage`
- **Arquivo:** `models/governance_stage.py`
- **Descrição técnica:** Etapa de Governança


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `fold` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `color` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `mail.compose.message`

- **Classe:** `MailComposeMessage`
- **Arquivo:** `models/mail_compose_message.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `mail.compose.message`


#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_governance_get_target_cases` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_governance_log_sent_email` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_send_mail` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_action_send_mail` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `governance.case` | `models/governance_agenda_ext.py` | Modelo `governance.case` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_deadline, _agenda_get_activity_type, _agenda_get_description, _sync_agenda_defaults, _governance_case_is_closed, _governance_case_marker_domain, _governance_prepare_marker_vals |
| `governance.case.pending` | `models/governance_agenda_ext.py` | Modelo `governance.case.pending` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_type, _agenda_get_deadline, _agenda_get_activity_type, _agenda_get_description, _sync_agenda_defaults, _sync_pending_agenda_state, create |
| `governance.case.communication` | `models/governance_agenda_ext.py` | Modelo `governance.case.communication` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_type, _agenda_get_description, _sync_agenda_defaults, _sync_communication_agenda_state, create, write |
| `governance.case` | `models/governance_case.py` | Caso de Governança | name, reference, description, origin_date, response_deadline, response_date, stage_id, status | _compute_type_stage_colors, _compute_type_settings, _compute_sla_days, _compute_resolution_deadline, _compute_is_overdue, _compute_days_without_response, _compute_response_deadline, _compute_participant_count |
| `governance.case.communication` | `models/governance_case_communication.py` | Comunicação do Caso de Governança | tracking_token, email_message_id, external_message_id, email_from, email_to, email_cc, channel_type, channel_origin | _get_tracking_token, _normalize_subject, _onchange_participant_id, create, write, _sync_case_from_communication, action_open_case, action_register_response |
| `governance.case.communication` | `models/governance_case_communication_email_ext.py` | Modelo `governance.case.communication` usado pelo módulo. | partner_match_source, partner_match_confidence | sem métodos relevantes |
| `governance.case` | `models/governance_case_email_ext.py` | Modelo `governance.case` usado pelo módulo. | email_channel_id, message_origin, requires_triage, triage_done, triage_notes, incoming_email_from, incoming_email_to, incoming_email_cc | _get_effective_sla_rule, _compute_email_sla_rule_fields, _compute_sla_days, _compute_response_deadline, _onchange_email_channel_id_apply_defaults, _check_email_channel_case_type_consistency, _apply_case_type_defaults_to_vals, _apply_email_channel_defaults_to_vals |
| `governance.case.participant` | `models/governance_case_participant.py` | Participante do Caso de Governança | sequence, active, case_id, company_id, partner_id, role, is_primary, note | _compute_contact_channels, _check_unique_participant_role, _check_single_primary, create, write, unlink, _normalize_primary_flag, _onchange_is_primary |
| `governance.case.pending` | `models/governance_case_pending.py` | Pendência do Caso de Governança | name, case_id, company_id, participant_id, partner_id, communication_id, template_id, response_id | _compute_pending_metrics, _onchange_participant_id, action_mark_done, action_reopen, action_cancel, action_open_case |
| `governance.case.response` | `models/governance_case_response.py` | Resposta do Caso de Governança | name, case_id, company_id, communication_id, participant_id, partner_id, responsible_id, response_date | _onchange_participant_id, create, write, _sync_case_from_response, action_open_case |
| `governance.case.type` | `models/governance_case_type.py` | Tipo de Caso de Governança | name, code, description, color, sequence, active, default_priority, sla_days | _compute_pending_template_count |
| `governance.case.type` | `models/governance_case_type_email_ext.py` | Modelo `governance.case.type` usado pelo módulo. | company_id, default_responsible_id, response_sla_days, resolution_sla_days, followup_sla_days, sla_low_days, sla_medium_days, sla_high_days | _compute_email_channel_count, action_open_email_channels, _check_sla_defaults_non_negative, _onchange_resolution_sla_days_sync_legacy, _onchange_followup_sla_days_sync_legacy |
| `governance.case.type.pending.template` | `models/governance_case_type_template.py` | Modelo de Pendência por Tipo de Caso | case_type_id, sequence, active, name, description, default_deadline_days, priority, assign_to_responsible | sem métodos relevantes |
| `governance.dashboard` | `models/governance_dashboard.py` | Painel Operacional de Governança | name, case_active_count, case_urgent_count, case_attention_count, case_ok_count, case_critical_count, case_high_count, case_overdue_sla_count | default_get, _case_action, _pending_action, _comm_action, action_refresh, action_view_active, action_view_urgent, action_view_attention |
| `governance.email.channel` | `models/governance_email_channel.py` | Canal de E-mail de Governança | name, sequence, active, company_id, alias_name, alias_id, alias_email, case_type_id | _compute_alias_email, _check_alias_name, _check_default_type_allowed, _check_company_consistency, create, write, _prepare_case_defaults, _get_alias_defaults |
| `governance.email.test` | `models/governance_email_test.py` | Teste de E-mail da Governança | name, company_id, state, external_email, outbound_email, reply_to_email, test_token, subject | _default_name, create, _build_subject, _build_body_html, _generate_token, _normalize_subject, _append_log, _find_default_channel |
| `governance.sla.rule` | `models/governance_sla_rule.py` | Regra de SLA de Governança | name, sequence, active, company_id, case_type_id, priority, response_sla_days, resolution_sla_days | _compute_name, _check_positive_days, get_effective_rule |
| `governance.stage` | `models/governance_stage.py` | Etapa de Governança | name, sequence, status, fold, color | sem métodos relevantes |
| `mail.compose.message` | `models/mail_compose_message.py` | Modelo `mail.compose.message` usado pelo módulo. | sem campos declarados no arquivo analisado | _governance_get_target_cases, _governance_log_sent_email, action_send_mail, _action_send_mail |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_governance_case_form_agenda_ext` | `governance.case` | `views/governance_agenda_views.xml` |
| `view_governance_case_pending_form_agenda_ext` | `governance.case.pending` | `views/governance_agenda_views.xml` |
| `view_governance_case_communication_form_agenda_ext` | `governance.case.communication` | `views/governance_agenda_views.xml` |
| `view_governance_case_calendar` | `governance.case` | `views/governance_agenda_views.xml` |
| `view_governance_case_communication_list_email_ext` | `governance.case.communication` | `views/governance_case_communication_email_ext_views.xml` |
| `view_governance_case_communication_form_email_ext` | `governance.case.communication` | `views/governance_case_communication_email_ext_views.xml` |
| `view_governance_case_list_email_ext` | `governance.case` | `views/governance_case_email_ext_views.xml` |
| `view_governance_case_form_email_ext` | `governance.case` | `views/governance_case_email_ext_views.xml` |
| `view_governance_case_search_email_ext` | `governance.case` | `views/governance_case_email_ext_views.xml` |
| `view_governance_case_communication_list` | `governance.case.communication` | `views/governance_case_operational_views.xml` |
| `view_governance_case_communication_form` | `governance.case.communication` | `views/governance_case_operational_views.xml` |
| `view_governance_case_communication_search` | `governance.case.communication` | `views/governance_case_operational_views.xml` |
| `view_governance_case_pending_list` | `governance.case.pending` | `views/governance_case_operational_views.xml` |
| `view_governance_case_pending_form` | `governance.case.pending` | `views/governance_case_operational_views.xml` |
| `view_governance_case_pending_search` | `governance.case.pending` | `views/governance_case_operational_views.xml` |
| `view_governance_case_participant_list` | `governance.case.participant` | `views/governance_case_participant_views.xml` |
| `view_governance_case_participant_form` | `governance.case.participant` | `views/governance_case_participant_views.xml` |
| `view_governance_case_participant_search` | `governance.case.participant` | `views/governance_case_participant_views.xml` |
| `view_governance_case_response_list` | `governance.case.response` | `views/governance_case_response_views.xml` |
| `view_governance_case_response_form` | `governance.case.response` | `views/governance_case_response_views.xml` |
| `view_governance_case_response_search` | `governance.case.response` | `views/governance_case_response_views.xml` |
| `view_governance_case_type_list_email_ext` | `governance.case.type` | `views/governance_case_type_email_ext_views.xml` |
| `view_governance_case_type_form_email_ext` | `governance.case.type` | `views/governance_case_type_email_ext_views.xml` |
| `view_governance_case_type_pending_template_list` | `governance.case.type.pending.template` | `views/governance_case_type_template_views.xml` |
| `view_governance_case_type_pending_template_form` | `governance.case.type.pending.template` | `views/governance_case_type_template_views.xml` |
| `view_governance_case_type_pending_template_search` | `governance.case.type.pending.template` | `views/governance_case_type_template_views.xml` |
| `view_governance_case_list` | `governance.case` | `views/governance_case_views.xml` |
| `view_governance_case_form` | `governance.case` | `views/governance_case_views.xml` |
| `view_governance_case_search` | `governance.case` | `views/governance_case_views.xml` |
| `view_governance_case_kanban` | `governance.case` | `views/governance_case_views.xml` |
| `view_governance_case_pivot` | `governance.case` | `views/governance_case_views.xml` |
| `view_governance_case_graph` | `governance.case` | `views/governance_case_views.xml` |
| `view_governance_stage_list` | `governance.stage` | `views/governance_case_views.xml` |
| `view_governance_tag_list` | `common.tag` | `views/governance_case_views.xml` |
| `view_governance_tag_form` | `common.tag` | `views/governance_case_views.xml` |
| `view_governance_case_type_list` | `governance.case.type` | `views/governance_case_views.xml` |
| `view_governance_case_type_form` | `governance.case.type` | `views/governance_case_views.xml` |
| `view_governance_dashboard_form` | `governance.dashboard` | `views/governance_dashboard_views.xml` |
| `view_governance_case_kanban_queue` | `governance.case` | `views/governance_dashboard_views.xml` |
| `view_governance_case_queue_list` | `governance.case` | `views/governance_dashboard_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_governance_pending_calendar` | Agenda de Pendências | `governance.menu_governance_monitoring_root` | `common_base.action_common_agenda_calendar_pending` | `views/governance_agenda_views.xml` |
| `menu_governance_calendar` | Agenda de Governança | `governance.menu_governance_monitoring_root` | `common_base.action_common_agenda_calendar_governance` | `views/governance_agenda_views.xml` |
| `menu_governance_email_tests_monitoring` | Testes de E-mail | `menu_governance_monitoring_root` | `action_governance_email_test` | `views/governance_email_test_views.xml` |
| `menu_governance_email_tests_config` | Testes de E-mail | `menu_governance_config` | `action_governance_email_test` | `views/governance_email_test_views.xml` |
| `menu_governance_email_channels_registry` | Canais de E-mail | `menu_governance_registry_root` | `action_governance_email_channel` | `views/governance_menu_email_ext_views.xml` |
| `menu_governance_email_channels_config` | Canais de E-mail | `menu_governance_config` | `action_governance_email_channel` | `views/governance_menu_email_ext_views.xml` |
| `menu_governance_sla_rules_config` | Regras de SLA | `menu_governance_config` | `action_governance_sla_rule` | `views/governance_menu_email_ext_views.xml` |
| `menu_governance_root` | Governança | `` | `` | `views/governance_menu_views.xml` |
| `menu_governance_operation_root` | Operação Diária | `menu_governance_root` | `` | `views/governance_menu_views.xml` |
| `menu_governance_monitoring_root` | Monitoramento e Alertas | `menu_governance_root` | `` | `views/governance_menu_views.xml` |
| `menu_governance_registry_root` | Cadastros Operacionais | `menu_governance_root` | `` | `views/governance_menu_views.xml` |
| `menu_governance_dashboard` | Painel Operacional | `menu_governance_root` | `action_governance_dashboard` | `views/governance_menu_views.xml` |
| `menu_governance_cases` | Central de Casos | `menu_governance_operation_root` | `action_governance_case` | `views/governance_menu_views.xml` |
| `menu_governance_work_queue` | Fila Geral | `menu_governance_operation_root` | `action_governance_work_queue` | `views/governance_menu_views.xml` |
| `menu_governance_my_work_queue` | Minha Operação | `menu_governance_operation_root` | `action_governance_my_work_queue` | `views/governance_menu_views.xml` |
| `menu_governance_communications` | Comunicações | `menu_governance_operation_root` | `action_governance_case_communication` | `views/governance_menu_views.xml` |
| `menu_governance_pendings` | Pendências | `menu_governance_operation_root` | `action_governance_case_pending` | `views/governance_menu_views.xml` |
| `menu_governance_responses` | Respostas Formais | `menu_governance_operation_root` | `action_governance_case_response` | `views/governance_menu_views.xml` |
| `menu_governance_executive_panel` | Painel Executivo | `menu_governance_monitoring_root` | `action_governance_executive_panel` | `views/governance_menu_views.xml` |
| `menu_governance_attention_cases` | Casos em Atenção | `menu_governance_monitoring_root` | `action_governance_case_attention` | `views/governance_menu_views.xml` |
| `menu_governance_response_attention` | Solicitações sem Resposta | `menu_governance_monitoring_root` | `action_governance_case_response_attention` | `views/governance_menu_views.xml` |
| `menu_governance_required_pendings` | Pendências Obrigatórias | `menu_governance_monitoring_root` | `action_governance_case_required_pendings` | `views/governance_menu_views.xml` |
| `menu_governance_pending_overdue` | Pendências Atrasadas | `menu_governance_monitoring_root` | `action_governance_case_pending_overdue` | `views/governance_menu_views.xml` |
| `menu_governance_pending_next_7` | Pendências Próx. 7 Dias | `menu_governance_monitoring_root` | `action_governance_case_pending_next_7` | `views/governance_menu_views.xml` |
| `menu_governance_tags_root` | Tags e Classificações | `menu_governance_registry_root` | `action_governance_tag` | `views/governance_menu_views.xml` |
| `menu_governance_types_registry` | Tipos de Caso | `menu_governance_registry_root` | `action_governance_case_type` | `views/governance_menu_views.xml` |
| `menu_governance_participants_registry` | Participantes | `menu_governance_registry_root` | `action_governance_case_participant` | `views/governance_menu_views.xml` |
| `menu_governance_config` | Administração | `menu_governance_root` | `` | `views/governance_menu_views.xml` |
| `menu_governance_stages` | Etapas | `menu_governance_config` | `action_governance_stage` | `views/governance_menu_views.xml` |
| `menu_governance_case_types` | Tipos de Caso | `menu_governance_config` | `action_governance_case_type` | `views/governance_menu_views.xml` |
| `menu_governance_tags` | Tags | `menu_governance_config` | `action_governance_tag` | `views/governance_menu_views.xml` |
| `menu_governance_participants` | Participantes | `menu_governance_config` | `action_governance_case_participant` | `views/governance_menu_views.xml` |
| `menu_governance_pending_templates` | Modelos de Checklist | `menu_governance_config` | `action_governance_case_type_pending_template` | `views/governance_menu_views.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_governance_case_calendar` | Agenda de Governança | `governance.case` | `views/governance_agenda_views.xml` |
| `action_governance_case_communication` | Comunicações | `governance.case.communication` | `views/governance_case_operational_views.xml` |
| `action_governance_case_pending` | Pendências | `governance.case.pending` | `views/governance_case_operational_views.xml` |
| `action_governance_case_attention` | Casos em Atenção | `governance.case` | `views/governance_case_operational_views.xml` |
| `action_governance_case_response_attention` | Solicitações sem Resposta | `governance.case.communication` | `views/governance_case_operational_views.xml` |
| `action_governance_case_required_pendings` | Pendências Obrigatórias | `governance.case.pending` | `views/governance_case_operational_views.xml` |
| `action_governance_case_pending_overdue` | Pendências Atrasadas | `governance.case.pending` | `views/governance_case_operational_views.xml` |
| `action_governance_case_pending_next_7` | Pendências Próx. 7 Dias | `governance.case.pending` | `views/governance_case_operational_views.xml` |
| `action_governance_case_participant` | Participantes | `governance.case.participant` | `views/governance_case_participant_views.xml` |
| `action_governance_case_response` | Respostas Formais | `governance.case.response` | `views/governance_case_response_views.xml` |
| `action_governance_case_type_pending_template` | Modelos de Pendência | `governance.case.type.pending.template` | `views/governance_case_type_template_views.xml` |
| `action_governance_case` | Casos de Governança | `governance.case` | `views/governance_case_views.xml` |
| `action_governance_stage` | Etapas | `governance.stage` | `views/governance_case_views.xml` |
| `action_governance_tag` | Tags de Governança | `common.tag` | `views/governance_case_views.xml` |
| `action_governance_case_type` | Tipos de Caso | `governance.case.type` | `views/governance_case_views.xml` |
| `action_governance_dashboard` | Painel Operacional | `governance.dashboard` | `views/governance_dashboard_views.xml` |
| `action_governance_work_queue` | Fila Geral | `governance.case` | `views/governance_dashboard_views.xml` |
| `action_governance_my_work_queue` | Minha Operação | `governance.case` | `views/governance_dashboard_views.xml` |
| `action_governance_executive_panel` | Painel Executivo | `governance.case` | `views/governance_dashboard_views.xml` |
| `action_governance_email_channel` | Canais de E-mail | `governance.email.channel` | `views/governance_email_channel_views.xml` |
| `action_governance_email_test` | Testes de E-mail | `governance.email.test` | `views/governance_email_test_views.xml` |
| `action_governance_sla_rule` | Regras de SLA | `governance.sla.rule` | `views/governance_sla_rule_views.xml` |


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
