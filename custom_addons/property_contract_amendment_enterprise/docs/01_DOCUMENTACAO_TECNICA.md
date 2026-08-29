# Documentação Técnica — Contratos e Aditivos Imobiliários Empresarial

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Gestão empresarial de aditivos contratuais, alterações controladas, recálculo de parcelas, documentos e auditoria.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `property_contract_amendment_enterprise` |
| Nome funcional | Contratos e Aditivos Imobiliários Empresarial |
| Versão | `19.0.1.5.0` |
| Aplicação | `True` |
| Instalável | `True` |
| Dependências | `base`, `mail`, `account`, `analytic`, `property_core` |

### Arquivos declarados no manifesto

- `security/security.xml`
- `security/ir.model.access.csv`
- `data/sequence.xml`
- `data/amendment_reason_data.xml`
- `views/amendment_views.xml`
- `views/amendment_agenda_views.xml`
- `views/rent_schedule_views.xml`
- `views/billing_views.xml`
- `views/billing_impact_views.xml`
- `views/financial_adjustment_views.xml`
- `views/document_views.xml`
- `views/approval_views.xml`
- `views/obligation_views.xml`
- `views/option_views.xml`
- `views/config_views.xml`
- `views/menu.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `property.contract.amendment`

- **Classe:** `PropertyContractAmendment`
- **Arquivo:** `models/amendment.py`
- **Descrição técnica:** Aditivo Contratual

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_number` | `Integer` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amendment_type` | `Selection` | Sim | Não | Sim | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `amendment_reason_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_scope` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `economic_effect` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `risk_level` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `signature_method` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `instrument_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sign_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `signature_completed_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `effective_date` | `Date` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `retroactive_effect` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `retroactive_from` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `retroactive_to` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `execution_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `applied_date` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `applied_by` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `is_applied` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_approval` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `approval_state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `commercial_impact` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `financial_impact` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `legal_impact` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `operational_impact` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_financial_update` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_party_update` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_term_update` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_guarantee_update` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_asset_update` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_billing_recalculation` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `requires_accounting_adjustment` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `old_summary_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_summary_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `summary_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `legal_basis` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `clauses_affected` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `unchanged_clauses_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `changes_json` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `note` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `change_line_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `approval_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `term_history_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `rent_schedule_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `financial_adjustment_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `billing_impact_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `billing_impact_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `billing_impact_total_delta` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `has_pending_billing_impacts` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_billing_impact_summary` | Compute | Validar dependências, store, atualização automática e performance. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_amendment_classification` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `action_submit_legal` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_approve` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_send_to_signature` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_mark_signed` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_ready_to_apply` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_simulate_billing_impact` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_apply_billing_impact` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reverse_billing_impact` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_apply` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_apply_change_lines` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_apply_financial_lines` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_apply_billing_impacts` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_simulate_billing_impacts` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_find_billing_plans_for_period` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_find_next_open_billing_plan` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_billing_impact_from_schedule` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_billing_impact_from_financial_adjustment` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_schedule_signed_amount` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_schedule_impact_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_application_rule` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_create_version_snapshot` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.contract.amendment.change`

- **Classe:** `PropertyContractAmendmentChange`
- **Arquivo:** `models/amendment.py`
- **Descrição técnica:** Alteração de Aditivo Contratual


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `amendment_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `change_category` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `field_key` | `Selection` | Sim | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `field_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `field_label` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `value_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `old_value_char` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_value_char` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `old_value_float` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_value_float` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `old_value_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_value_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `old_value_partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `new_value_partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `old_value_bool` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_value_bool` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `effective_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_applied` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `applied_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_controlled_field_values` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_field_key_fill_defaults` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_fill_old_value_from_contract` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_old_value_display` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_new_value_display` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_contract_write_value` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.contract.version`

- **Classe:** `PropertyContractVersion`
- **Arquivo:** `models/amendment.py`
- **Descrição técnica:** Versão Consolidada do Contrato


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `version_number` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source_amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `effective_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `created_by` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `terms_snapshot_json` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `terms_snapshot_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_current` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.contract.term.history`

- **Classe:** `PropertyContractTermHistory`
- **Arquivo:** `models/amendment.py`
- **Descrição técnica:** Histórico de Termos Contratuais


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `source_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `source_id` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `field_name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `field_label` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `old_value` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_value` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `effective_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `applied_date` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `applied_by` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `reason` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.contract.amendment`

- **Classe:** `PropertyContractAmendmentAgenda`
- **Arquivo:** `models/amendment_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.contract.amendment`, `common.agenda.mixin`


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
| `action_schedule_amendment_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.contract.approval`

- **Classe:** `PropertyContractApproval`
- **Arquivo:** `models/approval.py`
- **Descrição técnica:** Aprovação Contratual

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `approval_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `required_group_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `approver_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `requested_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `approved_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rejected_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `comments` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `action_approve` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reject` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.contract.billing.plan`

- **Classe:** `PropertyContractBillingPlan`
- **Arquivo:** `models/billing.py`
- **Descrição técnica:** Plano de Cobrança do Contrato


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `period_start` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `period_end` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `due_date` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `base_rent_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `discount_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `extra_charge_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `tax_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_amount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `invoice_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `source_amendment_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_adjustment_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `line_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `original_total_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amendment_delta_amount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amended_total_amount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `has_amendment_adjustment` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amendment_applied_date` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amendment_effective_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_total` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_amendment_amounts` | Compute | Validar dependências, store, atualização automática e performance. |

### Model `property.contract.billing.line`

- **Classe:** `PropertyContractBillingLine`
- **Arquivo:** `models/billing.py`
- **Descrição técnica:** Linha do Plano de Cobrança


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `billing_plan_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `rent_schedule_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `line_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `quantity` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `percentage` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `period_start` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `period_end` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `analytic_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

### Model `property.contract.billing.impact`

- **Classe:** `PropertyContractBillingImpact`
- **Arquivo:** `models/billing_impact.py`
- **Descrição técnica:** Parcela Afetada por Aditivo

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `amendment_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `billing_plan_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `created_billing_plan_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `rent_schedule_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `financial_adjustment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `impact_source_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `impact_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `application_rule` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `billing_status` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `period_start` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `period_end` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `due_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `original_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `delta_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `original_base_rent_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_base_rent_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `original_discount_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_discount_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `original_extra_charge_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_extra_charge_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_retroactive` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `applied_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `applied_by` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `reversed_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reversed_by` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_billing_status` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_apply` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reverse` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_apply_one` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_apply_to_existing_billing_plan` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_create_complementary_billing_plan` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_reverse_one` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_billing_line_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.contract.amendment.reason`

- **Classe:** `PropertyContractAmendmentReason`
- **Arquivo:** `models/config.py`
- **Descrição técnica:** Motivo de Aditivo Contratual


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `category` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.contract.financial.reason`

- **Classe:** `PropertyContractFinancialReason`
- **Arquivo:** `models/config.py`
- **Descrição técnica:** Motivo Financeiro Contratual


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `impact_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.contract.document.type`

- **Classe:** `PropertyContractDocumentType`
- **Arquivo:** `models/config.py`
- **Descrição técnica:** Tipo de Documento Contratual


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.contract`

- **Classe:** `PropertyContract`
- **Arquivo:** `models/contract_extension.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.contract`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `issuer` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `original_partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `current_partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `original_monthly_rent` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_base_rent` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_effective_rent` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_discount_amount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_extra_charge_amount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_discount_until` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_start_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_end_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_guarantee_type` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_adjustment_index` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `current_payment_day` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_purpose` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_jurisdiction` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `consolidated_terms_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `legal_status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `operational_status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `amendment_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `version_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `rent_schedule_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `billing_plan_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `financial_adjustment_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `obligation_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `option_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `term_history_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `current_version_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_amendment_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `has_pending_amendments` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `has_unapplied_amendments` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `next_rent_change_date` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_contract_counts` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_current_financials` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_next_rent_change_date` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_open_amendments` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_rent_schedule` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.contract.document`

- **Classe:** `PropertyContractDocument`
- **Arquivo:** `models/document.py`
- **Descrição técnica:** Documento Contratual

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_type_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `file` | `Binary` | Não | Não | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `file_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `issuer` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `signature_provider` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `envelope_id` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `signature_status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `sent_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `signed_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `completed_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `signers_json` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `certificate_file` | `Binary` | Não | Não | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `certificate_file_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `certificate_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `checksum` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `version` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_final` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.contract.financial.adjustment`

- **Classe:** `PropertyContractFinancialAdjustment`
- **Arquivo:** `models/financial_adjustment.py`
- **Descrição técnica:** Ajuste Financeiro Contratual

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `adjustment_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `financial_reason_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount` | `Monetary` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference_period_start` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference_period_end` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `apply_method` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `apply_to_invoice_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `generated_invoice_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `generated_credit_note_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

### Model `property.contract.obligation`

- **Classe:** `PropertyContractObligation`
- **Arquivo:** `models/obligation.py`
- **Descrição técnica:** Obrigação Contratual

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `obligation_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `responsible_party` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `due_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `recurrence` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `penalty` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source_clause` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.contract.option`

- **Classe:** `PropertyContractOption`
- **Arquivo:** `models/option.py`
- **Descrição técnica:** Opção Contratual

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `option_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notice_start_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notice_deadline` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `exercise_deadline` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `exercised_at` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `exercise_document_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.contract.rent.schedule`

- **Classe:** `PropertyContractRentSchedule`
- **Arquivo:** `models/rent_schedule.py`
- **Descrição técnica:** Tabela de Valores do Contrato

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amendment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `charge_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `financial_reason_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amount_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `percentage` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `base_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `start_date` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `end_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `due_day` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `billing_frequency` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `billing_period_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `is_base_rent` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_discount` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_extra_charge` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_temporary` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_recurring` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_retroactive` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_proratable` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proration_method` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `tax_included` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `analytic_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_onchange_charge_type` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_check_dates` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_overlapping_base_rent` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_is_date_in_range` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `property.contract.amendment` | `models/amendment.py` | Aditivo Contratual | name, sequence, contract_id, amendment_number, amendment_type, amendment_reason_id, amendment_scope, economic_effect | _compute_billing_impact_summary, create, _onchange_amendment_classification, action_submit_legal, action_approve, action_send_to_signature, action_mark_signed, action_ready_to_apply |
| `property.contract.amendment.change` | `models/amendment.py` | Alteração de Aditivo Contratual | amendment_id, contract_id, sequence, change_category, field_key, field_name, field_label, value_type | _controlled_field_values, create, write, _onchange_field_key_fill_defaults, _fill_old_value_from_contract, _get_old_value_display, _get_new_value_display, _get_contract_write_value |
| `property.contract.version` | `models/amendment.py` | Versão Consolidada do Contrato | contract_id, version_number, source_amendment_id, effective_date, created_by, terms_snapshot_json, terms_snapshot_html, is_current | create |
| `property.contract.term.history` | `models/amendment.py` | Histórico de Termos Contratuais | contract_id, source_type, source_id, amendment_id, field_name, field_label, old_value, new_value | sem métodos relevantes |
| `property.contract.amendment` | `models/amendment_agenda_ext.py` | Modelo `property.contract.amendment` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_deadline, _agenda_get_description, action_schedule_amendment_activity |
| `property.contract.approval` | `models/approval.py` | Aprovação Contratual | contract_id, amendment_id, approval_type, required_group_id, approver_id, status, requested_at, approved_at | action_approve, action_reject |
| `property.contract.billing.plan` | `models/billing.py` | Plano de Cobrança do Contrato | contract_id, period_start, period_end, due_date, base_rent_amount, discount_amount, extra_charge_amount, tax_amount | _compute_total, _compute_amendment_amounts |
| `property.contract.billing.line` | `models/billing.py` | Linha do Plano de Cobrança | billing_plan_id, contract_id, amendment_id, rent_schedule_id, sequence, line_type, name, amount | sem métodos relevantes |
| `property.contract.billing.impact` | `models/billing_impact.py` | Parcela Afetada por Aditivo | amendment_id, contract_id, billing_plan_id, created_billing_plan_id, rent_schedule_id, financial_adjustment_id, name, impact_source_type | _compute_name, _compute_billing_status, action_apply, action_reverse, _apply_one, _apply_to_existing_billing_plan, _create_complementary_billing_plan, _reverse_one |
| `property.contract.amendment.reason` | `models/config.py` | Motivo de Aditivo Contratual | name, code, category, description, active | sem métodos relevantes |
| `property.contract.financial.reason` | `models/config.py` | Motivo Financeiro Contratual | name, code, impact_type, description, active | sem métodos relevantes |
| `property.contract.document.type` | `models/config.py` | Tipo de Documento Contratual | name, code, sequence, active | sem métodos relevantes |
| `property.contract` | `models/contract_extension.py` | Modelo `property.contract` usado pelo módulo. | company_id, currency_id, issuer, original_partner_id, current_partner_id, original_monthly_rent, current_base_rent, current_effective_rent | _compute_contract_counts, _compute_current_financials, _compute_next_rent_change_date, action_open_amendments, action_open_rent_schedule |
| `property.contract.document` | `models/document.py` | Documento Contratual | contract_id, amendment_id, document_type_id, document_type, name, file, file_name, issuer | sem métodos relevantes |
| `property.contract.financial.adjustment` | `models/financial_adjustment.py` | Ajuste Financeiro Contratual | contract_id, amendment_id, adjustment_type, financial_reason_id, name, amount, reference_period_start, reference_period_end | sem métodos relevantes |
| `property.contract.obligation` | `models/obligation.py` | Obrigação Contratual | contract_id, amendment_id, obligation_type, responsible_party, name, description, due_date, recurrence | sem métodos relevantes |
| `property.contract.option` | `models/option.py` | Opção Contratual | contract_id, amendment_id, option_type, name, notice_start_date, notice_deadline, exercise_deadline, status | sem métodos relevantes |
| `property.contract.rent.schedule` | `models/rent_schedule.py` | Tabela de Valores do Contrato | contract_id, amendment_id, name, sequence, charge_type, financial_reason_id, amount_type, amount | _onchange_charge_type, _check_dates, _check_overlapping_base_rent, _is_date_in_range |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_property_contract_amendment_form_agenda_ext` | `property.contract.amendment` | `views/amendment_agenda_views.xml` |
| `view_property_contract_amendment_tree` | `property.contract.amendment` | `views/amendment_views.xml` |
| `view_property_contract_amendment_form` | `property.contract.amendment` | `views/amendment_views.xml` |
| `view_property_contract_approval_tree` | `property.contract.approval` | `views/approval_views.xml` |
| `view_property_contract_approval_form` | `property.contract.approval` | `views/approval_views.xml` |
| `view_property_contract_billing_impact_tree` | `property.contract.billing.impact` | `views/billing_impact_views.xml` |
| `view_property_contract_billing_impact_form` | `property.contract.billing.impact` | `views/billing_impact_views.xml` |
| `view_property_contract_billing_plan_tree` | `property.contract.billing.plan` | `views/billing_views.xml` |
| `view_property_contract_billing_plan_form` | `property.contract.billing.plan` | `views/billing_views.xml` |
| `view_property_contract_amendment_reason_tree` | `property.contract.amendment.reason` | `views/config_views.xml` |
| `view_property_contract_amendment_reason_form` | `property.contract.amendment.reason` | `views/config_views.xml` |
| `view_property_contract_financial_reason_tree` | `property.contract.financial.reason` | `views/config_views.xml` |
| `view_property_contract_financial_reason_form` | `property.contract.financial.reason` | `views/config_views.xml` |
| `view_property_contract_document_type_tree` | `property.contract.document.type` | `views/config_views.xml` |
| `view_property_contract_document_type_form` | `property.contract.document.type` | `views/config_views.xml` |
| `view_property_contract_document_tree` | `property.contract.document` | `views/document_views.xml` |
| `view_property_contract_document_form` | `property.contract.document` | `views/document_views.xml` |
| `view_property_contract_financial_adjustment_tree` | `property.contract.financial.adjustment` | `views/financial_adjustment_views.xml` |
| `view_property_contract_financial_adjustment_form` | `property.contract.financial.adjustment` | `views/financial_adjustment_views.xml` |
| `view_property_contract_obligation_tree` | `property.contract.obligation` | `views/obligation_views.xml` |
| `view_property_contract_obligation_form` | `property.contract.obligation` | `views/obligation_views.xml` |
| `view_property_contract_option_tree` | `property.contract.option` | `views/option_views.xml` |
| `view_property_contract_option_form` | `property.contract.option` | `views/option_views.xml` |
| `view_property_contract_rent_schedule_tree` | `property.contract.rent.schedule` | `views/rent_schedule_views.xml` |
| `view_property_contract_rent_schedule_form` | `property.contract.rent.schedule` | `views/rent_schedule_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_property_contract_amendment_root` | Aditivos Contratuais | `property_core.menu_property_root` | `action_property_contract_amendment` | `views/menu.xml` |
| `menu_property_contract_amendments` | Todos os Aditivos | `menu_property_contract_amendment_root` | `action_property_contract_amendment` | `views/menu.xml` |
| `menu_property_contract_rent_schedule` | Tabela de Valores | `menu_property_contract_amendment_root` | `action_property_contract_rent_schedule` | `views/menu.xml` |
| `menu_property_contract_billing_plan` | Plano de Cobrança | `menu_property_contract_amendment_root` | `action_property_contract_billing_plan` | `views/menu.xml` |
| `menu_property_contract_billing_impact` | Parcelas Afetadas | `menu_property_contract_amendment_root` | `action_property_contract_billing_impact` | `views/menu.xml` |
| `menu_property_contract_financial_adjustment` | Ajustes Financeiros | `menu_property_contract_amendment_root` | `action_property_contract_financial_adjustment` | `views/menu.xml` |
| `menu_property_contract_documents` | Documentos Contratuais | `menu_property_contract_amendment_root` | `action_property_contract_document` | `views/menu.xml` |
| `menu_property_contract_obligations` | Obrigações | `menu_property_contract_amendment_root` | `action_property_contract_obligation` | `views/menu.xml` |
| `menu_property_contract_options` | Opções Contratuais | `menu_property_contract_amendment_root` | `action_property_contract_option` | `views/menu.xml` |
| `menu_property_contract_config` | Configuração de Aditivos | `menu_property_contract_amendment_root` | `` | `views/menu.xml` |
| `menu_property_contract_amendment_reason` | Motivos de Aditivo | `menu_property_contract_config` | `action_property_contract_amendment_reason` | `views/menu.xml` |
| `menu_property_contract_financial_reason` | Motivos Financeiros | `menu_property_contract_config` | `action_property_contract_financial_reason` | `views/menu.xml` |
| `menu_property_contract_document_type` | Tipos de Documento | `menu_property_contract_config` | `action_property_contract_document_type` | `views/menu.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_property_contract_amendment` | Aditivos | `property.contract.amendment` | `views/amendment_views.xml` |
| `action_property_contract_approval` | Aprovações | `property.contract.approval` | `views/approval_views.xml` |
| `action_property_contract_billing_impact` | Parcelas Afetadas | `property.contract.billing.impact` | `views/billing_impact_views.xml` |
| `action_property_contract_billing_plan` | Plano de Cobrança | `property.contract.billing.plan` | `views/billing_views.xml` |
| `action_property_contract_amendment_reason` | Motivos de Aditivo | `property.contract.amendment.reason` | `views/config_views.xml` |
| `action_property_contract_financial_reason` | Motivos Financeiros | `property.contract.financial.reason` | `views/config_views.xml` |
| `action_property_contract_document_type` | Tipos de Documento | `property.contract.document.type` | `views/config_views.xml` |
| `action_property_contract_document` | Documentos | `property.contract.document` | `views/document_views.xml` |
| `action_property_contract_financial_adjustment` | Ajustes Financeiros | `property.contract.financial.adjustment` | `views/financial_adjustment_views.xml` |
| `action_property_contract_obligation` | Obrigações | `property.contract.obligation` | `views/obligation_views.xml` |
| `action_property_contract_option` | Opções | `property.contract.option` | `views/option_views.xml` |
| `action_property_contract_rent_schedule` | Tabela de Valores | `property.contract.rent.schedule` | `views/rent_schedule_views.xml` |


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
