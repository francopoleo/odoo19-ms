# Documentação Técnica — Conciliação Inteligente de Comprovantes de Aluguel

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Recebimento, OCR e conciliação inteligente de comprovantes de aluguel com parcelas e lançamentos financeiros.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `property_payment_proof` |
| Nome funcional | Conciliação Inteligente de Comprovantes de Aluguel |
| Versão | `19.0.1.0.0` |
| Aplicação | `True` |
| Instalável | `True` |
| Dependências | `property_core`, `account`, `mail` |

### Arquivos declarados no manifesto

- `security/ir.model.access.csv`
- `data/ir_sequence.xml`
- `wizard/bulk_upload_views.xml`
- `wizard/manual_payment_views.xml`
- `views/receipts_dashboard_views.xml`
- `views/property_payment_authorized_payer_views.xml`
- `views/property_payment_proof_views.xml`
- `views/payment_proof_agenda_views.xml`
- `views/property_contract_views.xml`
- `views/property_rent_views.xml`
- `views/menu_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `property.payment.proof`

- **Classe:** `PropertyPaymentProofAgenda`
- **Arquivo:** `models/payment_proof_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.payment.proof`, `common.agenda.mixin`


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
| `action_schedule_payment_proof_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.contract`

- **Classe:** `PropertyContract`
- **Arquivo:** `models/property_contract.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.contract`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `authorized_payer_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

### Model `property.payment.authorized.payer`

- **Classe:** `PropertyPaymentAuthorizedPayer`
- **Arquivo:** `models/property_payment_authorized_payer.py`
- **Descrição técnica:** Pagador Autorizado para Conciliação de Aluguel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `priority` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `tenant_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `vat` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `normalized_vat` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pix_key` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bank_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bank_account_hint` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `relation_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_normalized_vat` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_partner_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_check_vat_length` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `property.payment.proof`

- **Classe:** `PropertyPaymentProof`
- **Arquivo:** `models/property_payment_proof.py`
- **Descrição técnica:** Comprovante de Pagamento de Aluguel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `proof_file` | `Binary` | Não | Não | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `proof_filename` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mimetype` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `raw_text` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `extraction_log` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `payment_method` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `payment_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `debit_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `payer_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `payer_vat` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pix_key` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `normalized_payer_vat` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_pdf` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `receiver_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `transaction_id` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bank_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `rent_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `payment_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `match_line_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `suggested_match_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `confidence_score` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `matched_payload` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_late_payment` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `days_late` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `late_handling` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `calculated_fine` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `calculated_interest` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `late_fee_source_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `late_fee_proof_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_is_pdf` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_normalized_payer_vat` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_late_info` | Compute | Validar dependências, store, atualização automática e performance. |
| `_extract_pdf_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_image_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_text_from_file` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_parse_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_extract` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_rent_display_amount` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_rent_best_amount_diff` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_score_rent` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_match` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_use_match` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_approve_and_reconcile` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_print_receipt` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reject` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_calculate_late_fees` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_request_late_fee` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_defer_to_next_month` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_waive_late_fee` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.payment.proof.match`

- **Classe:** `PropertyPaymentProofMatch`
- **Arquivo:** `models/property_payment_proof.py`
- **Descrição técnica:** Sugestão de Conciliação de Comprovante


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `proof_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `rent_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `due_date` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `due_date_display` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount_due` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `score` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reason` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_due_date_display` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_select_match` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.rent`

- **Classe:** `PropertyRent`
- **Arquivo:** `models/property_rent.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.rent`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `payment_proof_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `payment_proof_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_payment_proof_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_payment_proofs` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_register_via_proof` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_manual_payment_wizard` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.receipts.dashboard`

- **Classe:** `PropertyReceiptsDashboard`
- **Arquivo:** `models/receipts_dashboard.py`
- **Descrição técnica:** Dashboard Operacional de Recebimentos


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `proof_ready_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_ready_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_reconciled_month_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_reconciled_month_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_attention_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_total_pending` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_draft_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_extracted_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_matched_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_review_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_failed_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_rejected_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_draft_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_extracted_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_matched_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_review_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_match_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `avg_score` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `high_score_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mid_score_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `low_score_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_late_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_late_no_handling` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_late_fee_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_late_defer_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_late_waive_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_late_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `proof_late_fee_pending_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `chart_weekly_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `chart_funnel_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `chart_method_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `chart_score_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_all` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_charts` | Compute | Validar dependências, store, atualização automática e performance. |
| `_proof_action` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_view_ready` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_draft` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_extracted` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_matched` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_review` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_failed` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_rejected` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_late_fee_pending` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_late_no_handling` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_reconciled_month` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_bulk_confirm_high_score` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_bulk_upload` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `property.payment.proof` | `models/payment_proof_agenda_ext.py` | Modelo `property.payment.proof` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_deadline, _agenda_get_description, action_schedule_payment_proof_activity |
| `property.contract` | `models/property_contract.py` | Modelo `property.contract` usado pelo módulo. | authorized_payer_ids | sem métodos relevantes |
| `property.payment.authorized.payer` | `models/property_payment_authorized_payer.py` | Pagador Autorizado para Conciliação de Aluguel | active, priority, contract_id, tenant_id, company_id, partner_id, name, vat | _compute_normalized_vat, _onchange_partner_id, _check_vat_length |
| `property.payment.proof` | `models/property_payment_proof.py` | Comprovante de Pagamento de Aluguel | name, company_id, proof_file, proof_filename, mimetype, raw_text, extraction_log, payment_method | create, _compute_is_pdf, _compute_normalized_payer_vat, _compute_late_info, _extract_pdf_text, _extract_image_text, _extract_text_from_file, _parse_text |
| `property.payment.proof.match` | `models/property_payment_proof.py` | Sugestão de Conciliação de Comprovante | proof_id, rent_id, contract_id, partner_id, due_date, due_date_display, amount_due, currency_id | _compute_due_date_display, action_select_match |
| `property.rent` | `models/property_rent.py` | Modelo `property.rent` usado pelo módulo. | payment_proof_ids, payment_proof_count | _compute_payment_proof_count, action_view_payment_proofs, action_register_via_proof, action_open_manual_payment_wizard |
| `property.receipts.dashboard` | `models/receipts_dashboard.py` | Dashboard Operacional de Recebimentos | name, currency_id, proof_ready_count, proof_ready_amount, proof_reconciled_month_count, proof_reconciled_month_amount, proof_attention_count, proof_total_pending | _compute_all, _compute_charts, _proof_action, action_view_ready, action_view_draft, action_view_extracted, action_view_matched, action_view_review |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_property_payment_proof_form_agenda_ext` | `property.payment.proof` | `views/payment_proof_agenda_views.xml` |
| `view_property_contract_form_payment_proof` | `property.contract` | `views/property_contract_views.xml` |
| `view_property_payment_authorized_payer_list` | `property.payment.authorized.payer` | `views/property_payment_authorized_payer_views.xml` |
| `view_property_payment_authorized_payer_form` | `property.payment.authorized.payer` | `views/property_payment_authorized_payer_views.xml` |
| `view_property_payment_proof_list` | `property.payment.proof` | `views/property_payment_proof_views.xml` |
| `view_property_payment_proof_form` | `property.payment.proof` | `views/property_payment_proof_views.xml` |
| `view_property_payment_proof_search` | `property.payment.proof` | `views/property_payment_proof_views.xml` |
| `view_property_rent_form_payment_proof` | `property.rent` | `views/property_rent_views.xml` |
| `view_property_receipts_dashboard_form` | `property.receipts.dashboard` | `views/receipts_dashboard_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_property_receipts_dashboard` | Dashboard de Recebimentos | `property_core.menu_property_financeiro` | `action_property_receipts_dashboard` | `views/menu_views.xml` |
| `menu_property_payment_proof` | Comprovantes de Pagamento | `property_core.menu_property_financeiro` | `action_property_payment_proof` | `views/menu_views.xml` |
| `menu_property_payment_proof_bulk_upload` | Upload em Lote | `property_core.menu_property_financeiro` | `action_property_payment_proof_bulk_upload` | `views/menu_views.xml` |
| `menu_property_payment_authorized_payer` | Pagadores Autorizados | `property_core.menu_property_financeiro` | `action_property_payment_authorized_payer` | `views/menu_views.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_property_payment_authorized_payer` | Pagadores Autorizados | `property.payment.authorized.payer` | `views/property_payment_authorized_payer_views.xml` |
| `action_property_payment_proof` | Comprovantes de Pagamento | `property.payment.proof` | `views/property_payment_proof_views.xml` |
| `action_property_receipts_dashboard` | Dashboard de Recebimentos | `property.receipts.dashboard` | `views/receipts_dashboard_views.xml` |


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
