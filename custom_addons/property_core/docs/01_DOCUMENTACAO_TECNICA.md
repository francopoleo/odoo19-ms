# Documentação Técnica — Property Core

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Gestão de imóveis, contratos, documentos, galeria, mídias, vistorias, manutenções, aluguéis e Agenda Geral operacional.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `property_core` |
| Nome funcional | Property Core |
| Versão | `19.0.6.2.1` |
| Aplicação | `True` |
| Instalável | `True` |
| Dependências | `mail`, `common_base`, `governance`, `portal`, `website`, `account`, `document_core` |

### Arquivos declarados no manifesto

- `security/property_security.xml`
- `security/ir.model.access.csv`
- `report/property_contract_report.xml`
- `report/owner_statement_report.xml`
- `report/portfolio_report.xml`
- `report/delinquency_report.xml`
- `report/profitability_report.xml`
- `report/owner_repasse_report.xml`
- `report/property_rent_receipt_report.xml`
- `data/property_activity_types.xml`
- `data/property_index_data.xml`
- `data/property_cron.xml`
- `data/property_binary_tracking_cleanup.xml`
- `data/property_rent_receipt_sequence.xml`
- `data/property_rent_payment_sequence.xml`
- `data/email_templates.xml`
- `data/property_asset_silva.xml`
- `data/property_taxonomy_data.xml`
- `data/property_media_category_data.xml`
- `views/property_stakeholder_type_views.xml`
- `views/property_stakeholder_profile_views.xml`
- `views/property_tenant_views.xml`
- `views/property_buyer_views.xml`
- `views/property_seller_views.xml`
- `views/property_investor_views.xml`
- `views/property_brokerage_views.xml`
- `views/property_developer_views.xml`
- `views/property_partner_ext_views.xml`
- `views/property_accounting_settings_views.xml`
- `views/property_owner_views.xml`
- `views/property_complex_views.xml`
- `views/property_asset_views.xml`
- `views/property_asset_communication_views.xml`
- `views/property_contract_views.xml`
- `views/property_contract_enterprise_views.xml`
- `views/property_rent_views.xml`
- `views/property_rent_enterprise_views.xml`
- `views/property_media_category_views.xml`
- `views/property_media_views.xml`
- `views/property_inspection_views.xml`
- `views/property_maintenance_views.xml`
- `views/property_agenda_views.xml`
- `wizard/property_media_bulk_wizard_views.xml`
- `views/property_acquisition_views.xml`
- `views/property_index_views.xml`
- `views/property_rent_adjustment_views.xml`
- `views/property_lead_views.xml`
- `views/property_broker_views.xml`
- `views/property_broker_assignment_views.xml`
- `views/property_commission_views.xml`
- `views/property_owner_repasse_views.xml`
- `views/property_dashboard_views.xml`
- `views/website_templates.xml`
- `views/portal_templates.xml`
- `views/property_menu_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `document.document`

- **Classe:** `DocumentPropertyExt`
- **Arquivo:** `models/document_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `document.document`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `complex_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `owner_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `broker_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `authorized_broker_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `media_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `media_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_media_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_get_broker_for_user` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `can_user_view_document` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_access_summary` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_property_link` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `ir.actions.report`

- **Classe:** `IrActionsReport`
- **Arquivo:** `models/ir_actions_report_patch.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `ir.actions.report`


#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_build_wkhtmltopdf_args` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `res.config.settings`

- **Classe:** `ResConfigSettings`
- **Arquivo:** `models/property_accounting.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `res.config.settings`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `property_rent_journal_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `property_rent_income_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `property_repasse_journal_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `property_repasse_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

### Model `property.acquisition`

- **Classe:** `PropertyAcquisition`
- **Arquivo:** `models/property_acquisition.py`
- **Descrição técnica:** Aquisição de Imóvel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `color` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `priority` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `asset_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `address` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `city` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `state_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `neighborhood` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `zip_code` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_area` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `useful_area` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `seller_partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `seller_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `buyer_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `investor_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `developer_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `broker_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asking_price` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `offer_price` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `agreed_price` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `estimated_renovation` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `estimated_rent` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_investment` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `roi_annual` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `discount_pct` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `prospect_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `expected_close_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `close_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dd_legal_docs` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dd_registration` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dd_iptu_clear` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dd_environmental` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dd_structural` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dd_notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dd_progress` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `cancellation_reason` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `stage` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_financials` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_dd_progress` | Compute | Validar dependências, store, atualização automática e performance. |
| `_expand_stages` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_set_analysis` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_negotiation` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_due_diligence` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_closing` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_close` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_asset` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reset` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_onchange_zip_code` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_search_zip_code_data` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_search_zip_code` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_check_prices` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.inspection`

- **Classe:** `PropertyInspectionAgenda`
- **Arquivo:** `models/property_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.inspection`, `common.agenda.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `agenda_responsible_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `agenda_partner_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_agenda_get_title` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_description` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_deadline` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_activity_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_partners` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_agenda_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_schedule` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.maintenance`

- **Classe:** `PropertyMaintenanceAgenda`
- **Arquivo:** `models/property_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.maintenance`, `common.agenda.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `agenda_responsible_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `agenda_partner_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_agenda_get_title` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_description` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_deadline` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_activity_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_agenda_get_partners` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_agenda_defaults` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_schedule` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.contract`

- **Classe:** `PropertyContractAgenda`
- **Arquivo:** `models/property_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.contract`, `common.agenda.mixin`


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
| `action_schedule_contract_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.rent`

- **Classe:** `PropertyRentAgenda`
- **Arquivo:** `models/property_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.rent`, `common.agenda.mixin`


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
| `action_schedule_rent_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.rent.adjustment`

- **Classe:** `PropertyRentAdjustmentAgenda`
- **Arquivo:** `models/property_agenda_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.rent.adjustment`, `common.agenda.mixin`


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
| `action_schedule_rent_adjustment_activity` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.asset`

- **Classe:** `PropertyAsset`
- **Arquivo:** `models/property_asset.py`
- **Descrição técnica:** Imóvel

- **Heranças:** `mail.thread`, `mail.activity.mixin`, `common.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `display_name_full` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `registration` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `iptu_number` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `legal_description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `address` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `address_number` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `address_complement` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `neighborhood` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `city` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `state_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `zip_code` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `country_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `complex_address` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `image_1920` | `Image` | Não | Não | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `image_512` | `Image` | Não | Sim | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `bedrooms` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bathrooms` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `parking_spots` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `construction_year` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `construction_standard` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `permitted_use` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `total_area` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `useful_area` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `land_area` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_value` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `market_value` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rental_value` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `current_monthly_rent` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `iptu_annual` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `foro_annual` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `condominium_monthly` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_annual_costs` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `website_published` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `website_visibility` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `website_lead_policy` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `authorized_broker_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `exclusive_broker_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `is_exclusive` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `hide_when_unavailable` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `show_unavailable_on_website` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `publish_start_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `publish_end_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `website_access_summary` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `complex_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `unit_identifier` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `unit_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `floor` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `gla` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `owner_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `inspection_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `maintenance_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `media_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `gallery_media_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `other_media_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `communication_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active_contract_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active_contract_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `media_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `kanban_location` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `kanban_alert_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `kanban_alert_level` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `kanban_alert_summary` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `governance_case_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `tag_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `inspection_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `maintenance_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `maintenance_open_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `init` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_media_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_kanban_indicators` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_media` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_bulk_media_wizard` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_gallery_media_wizard` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_other_media_wizard` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_compute_governance_case_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_governance_cases` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_compute_display_name_full` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_complex_address` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_total_annual_costs` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_contract_stats` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_website_access_summary` | Compute | Validar dependências, store, atualização automática e performance. |
| `_is_in_publication_window` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_is_status_website_eligible` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_brokers_allowed_to_view` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_broker_for_user` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `can_user_view_on_website` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `can_user_submit_interest` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_exclusive_broker` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_complex_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_zip_code` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_check_publication_dates` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_areas` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_characteristics` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_search_zip_code_data` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_search_zip_code` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_available` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_rented` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_for_sale` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_negotiating` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_maintenance` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_inactive` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_contracts` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_compute_document_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_phase4_counts` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_inspections` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_maintenance` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.asset.communication`

- **Classe:** `PropertyAssetCommunication`
- **Arquivo:** `models/property_asset_communication.py`
- **Descrição técnica:** Comunicação de Imóvel

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
| `asset_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Html` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `partner_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `responsible_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `requires_action` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `action_deadline` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_tracking_token` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_subject` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_mark_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_create_task` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.broker`

- **Classe:** `PropertyBroker`
- **Arquivo:** `models/property_broker.py`
- **Descrição técnica:** Corretor de Imóveis

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `user_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `creci` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `brokerage_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `is_company` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `acquisition_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `lead_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `assignment_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_commission_paid` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_broker_partner_category` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_partner_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_partner` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_partner_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_compute_stats` | Compute | Validar dependências, store, atualização automática e performance. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_view_acquisitions` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_leads` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_commissions` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_assignments` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.broker.assignment`

- **Classe:** `PropertyBrokerAssignment`
- **Arquivo:** `models/property_broker_assignment.py`
- **Descrição técnica:** Mandato de Corretor

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `broker_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `assignment_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `exclusive` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `start_date` | `Date` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `end_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `commission_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `governance_case_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_governance_case_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_status` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_dates` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_exclusivity` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_dispute` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_governance_cases` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cron_check_expiry` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.brokerage`

- **Classe:** `PropertyBrokerage`
- **Arquivo:** `models/property_brokerage.py`
- **Descrição técnica:** Imobiliária

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `partner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `broker_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.buyer`

- **Classe:** `PropertyBuyer`
- **Arquivo:** `models/property_buyer.py`
- **Descrição técnica:** Comprador

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `partner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `budget_min` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `budget_max` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.commission`

- **Classe:** `PropertyCommission`
- **Arquivo:** `models/property_commission.py`
- **Descrição técnica:** Comissão de Corretor

- **Heranças:** `mail.thread`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `broker_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `acquisition_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `base_value` | `Monetary` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_value` | `Monetary` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `deal_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `due_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `payment_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_asset` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_commission` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_broker_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_acquisition_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_contract_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `action_pay` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_check_rate` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `action_cron_commission_reminder` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.complex`

- **Classe:** `PropertyComplex`
- **Arquivo:** `models/property_complex.py`
- **Descrição técnica:** Complexo / Edifício

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `complex_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `owner_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `address` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `address_number` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `neighborhood` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `city` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `state_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `zip_code` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `country_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `latitude` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `longitude` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `image_1920` | `Image` | Não | Não | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `image_512` | `Image` | Não | Sim | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `land_area` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_gla` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `construction_year` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `floors` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `parking_total` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `construction_standard` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `registration` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `iptu_number` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `legal_description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_value` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `iptu_annual` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `foro_annual` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `condominium_monthly` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_annual_costs` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `unit_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `units_rented` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `units_available` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `occupancy_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_monthly_rent` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `noi_monthly` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `tag_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `init` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_financials` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_zip_code` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_search_zip_code_data` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_search_zip_code` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_units` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.contract`

- **Classe:** `PropertyContract`
- **Arquivo:** `models/property_contract.py`
- **Descrição técnica:** Contrato de Locação

- **Heranças:** `mail.thread`, `mail.activity.mixin`, `common.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `original_filename` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `asset_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `tenant_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `broker_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `assignment_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `commission_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `guarantor_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_link_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `tenant_profile_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `broker_link_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `assignment_link_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sign_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `start_date` | `Date` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `end_date` | `Date` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `duration_months` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `monthly_rent` | `Monetary` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `deposit_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_value` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `journal_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `income_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `adjustment_index` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `adjustment_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `adjustment_period_months` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_adjustment_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `next_adjustment_date` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `alert_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `days_to_expiry` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `months_active` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_expiring` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `rent_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_open_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_late_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_received` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_pending` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `adjustment_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `adjustment_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `governance_case_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `jurisdiction` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `witness_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `additional_clauses` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `inspection_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `maintenance_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_auto_init` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_relation_button_counts` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_open_asset` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_tenant_profile` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_broker` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_assignment` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_compute_adjustment_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_adjustments` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_compute_rent_stats` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_rents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_generate_rents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_compute_governance_case_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_governance_cases` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_onchange_tenant_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_partner_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_compute_duration` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_total_value` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_next_adjustment` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_expiry_info` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_is_expiring` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_asset_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_assignment_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_check_dates` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_values` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `action_activate` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_renewing` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_defaulting` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_late` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_close` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_commission` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_print_contract` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cron_check_late` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cron_check_adjustment_due` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_compute_document_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_phase4_counts` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_inspections` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_maintenance` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.dashboard`

- **Classe:** `PropertyDashboard`
- **Arquivo:** `models/property_dashboard.py`
- **Descrição técnica:** Dashboard de Imóveis


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_total` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_available` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_rented` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_maintenance` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_for_sale` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_active` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_expiring` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_renewing` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_defaulting` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `monthly_revenue` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_open_total` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_late_total` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_received_month` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `late_rent_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `maintenance_open` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `maintenance_emergency` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `inspection_scheduled` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_expiring` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `document_expired` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `acquisition_pipeline` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `acquisition_closing` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `broker_active` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `owner_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_pending_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_pending_total` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `assignment_active` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `alert_contracts_expiring_30` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `alert_late_rents` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `alert_maintenance_emergency` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `alert_documents_expired` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `alert_assignment_expiring_7` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `occupancy_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `collection_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `revenue_growth` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `repasse_pending_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `repasse_pending_total` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_potential_monthly` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_potential_annual` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_costs_monthly` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_deterioration_monthly` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_total_burden_monthly` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_days_avg` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_over_90_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_over_180_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_aging_risk` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_standard_risk` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_never_rented` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `idle_yield_loss_pct` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `chart_received_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `chart_portfolio_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `growth_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `chart_vacancy_html` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_all` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_charts` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.developer`

- **Classe:** `PropertyDeveloper`
- **Arquivo:** `models/property_developer.py`
- **Descrição técnica:** Incorporadora

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `partner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.index`

- **Classe:** `PropertyIndex`
- **Arquivo:** `models/property_index.py`
- **Descrição técnica:** Índice de Reajuste

- **Heranças:** `mail.thread`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `bcb_series_code` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `value_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `value_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `coverage_from` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `coverage_to` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_sync` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `months_back` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_check_unique_code` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_compute_bcb_series_code` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_coverage` | Compute | Validar dependências, store, atualização automática e performance. |
| `_fetch_bcb_data` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_sync_from_bcb` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `get_accumulated_rate` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.index.value`

- **Classe:** `PropertyIndexValue`
- **Arquivo:** `models/property_index.py`
- **Descrição técnica:** Valor Mensal do Índice


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `index_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `year` | `Integer` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `month` | `Integer` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `month_label` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `value_pct` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_check_unique_period` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_compute_month_label` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_cron_sync_all_indexes` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.inspection`

- **Classe:** `PropertyInspection`
- **Arquivo:** `models/property_inspection.py`
- **Descrição técnica:** Vistoria de Imóvel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `inspection_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `asset_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `scheduled_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `inspector_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `present_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `overall_condition` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `report` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `observations` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `attachment_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `attachment_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `media_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `media_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_attachment_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_media_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_schedule` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reset_draft` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_media` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_bulk_media_wizard` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_documents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.investor`

- **Classe:** `PropertyInvestor`
- **Arquivo:** `models/property_investor.py`
- **Descrição técnica:** Investidor

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `partner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `investment_profile` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.lead`

- **Classe:** `PropertyLead`
- **Arquivo:** `models/property_lead.py`
- **Descrição técnica:** Interesse em Imóvel

- **Heranças:** `mail.thread`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `interest_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `message` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source_channel` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `submitter_user_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `access_profile` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `broker_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_lead_partner_category` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_partner` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_set_contacted` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_qualified` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_set_lost` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.maintenance`

- **Classe:** `PropertyMaintenance`
- **Arquivo:** `models/property_maintenance.py`
- **Descrição técnica:** Manutenção de Imóvel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `maintenance_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `priority` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `responsible_party` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `asset_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `vendor_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `request_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `scheduled_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `completion_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `cost_estimate` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `cost_actual` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `attachment_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `attachment_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `media_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `media_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_attachment_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_media_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_quote` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_schedule` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_start` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_done` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reset_draft` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_media` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_bulk_media_wizard` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_check_costs` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.media.category`

- **Classe:** `PropertyMediaCategory`
- **Arquivo:** `models/property_media.py`
- **Descrição técnica:** Categoria de Mídia Imobiliária


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `applicable_purpose` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `default_content_kind` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `publishable_default` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.media`

- **Classe:** `PropertyMedia`
- **Arquivo:** `models/property_media.py`
- **Descrição técnica:** Mídia do Imóvel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `display_name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `purpose` | `Selection` | Sim | Não | Sim | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `category_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `content_kind` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `media_role` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `visibility_level` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `website_published` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `publication_state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `allow_download` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_cover` | `Boolean` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `inspection_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `maintenance_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `image_1920` | `Image` | Não | Não | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `image_512` | `Image` | Não | Sim | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `file_data` | `Binary` | Não | Não | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `file_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `file_mimetype` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `file_size` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `file_size_human` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `caption` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `location_note` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `date_taken` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `taken_by` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `tag_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `init` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_display_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_file_meta` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_purpose` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_category_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_content_kind` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_binary_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_role_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_check_context_link` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_binary_consistency` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_publication_rules` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_is_cover_unique` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `action_disable_binary_tracking` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cleanup_binary_conflicts` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.migration.helper`

- **Classe:** `PropertyMigrationHelper`
- **Arquivo:** `models/property_migration_helper.py`
- **Descrição técnica:** Property Migration Helper


#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `init` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.owner`

- **Classe:** `PropertyOwner`
- **Arquivo:** `models/property_owner.py`
- **Descrição técnica:** Proprietário de Imóvel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `cpf_cnpj` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `street` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `city` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `state_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_company` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bank_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bank_agency` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `bank_account` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pix_key` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `repasse_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `repasse_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active_contract_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_monthly_income` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_annual_costs` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `net_monthly` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_stats` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_repasse_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_owner_partner_category` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_partner_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_sync_partner` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_partner_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_view_assets` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_generate_statement` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_repasses` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.owner.repasse`

- **Classe:** `PropertyOwnerRepasse`
- **Arquivo:** `models/property_owner_repasse.py`
- **Descrição técnica:** Repasse Mensal ao Proprietário

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `owner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `period_month` | `Integer` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `period_year` | `Integer` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `date_from` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `date_to` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `rent_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `commission_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `maintenance_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `management_fee_pct` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_total` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_total` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `maintenance_total` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `management_fee` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `gross_amount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `net_amount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `payment_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `account_move_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_totals` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_period` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `action_load_data` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_confirm` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_register_payment` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_send_repasse_email` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reset_draft` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_account_move` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_create_repasse_move` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.owner.statement`

- **Classe:** `PropertyOwnerStatement`
- **Arquivo:** `models/property_owner_statement.py`
- **Descrição técnica:** Extrato do Proprietário


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `owner_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `date_from` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `date_to` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `rent_income` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `commission_total` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `maintenance_total` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `fixed_costs_total` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `gross_income` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_deductions` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `net_result` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `commission_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `maintenance_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_totals` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_print` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `res.partner`

- **Classe:** `ResPartner`
- **Arquivo:** `models/property_partner_ext.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `res.partner`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `mobile` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_stakeholder_profile_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `has_property_stakeholder_profile` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_stakeholder_profile_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_owner_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_broker_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_tenant_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_buyer_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_seller_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_investor_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_brokerage_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_developer_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_lead_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_has_property_stakeholder_profile` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_property_stakeholder_display_counts` | Compute | Validar dependências, store, atualização automática e performance. |
| `_open_partner_related` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_view_property_stakeholder_profiles` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_new_property_stakeholder_profile` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_owners` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_brokers` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_tenants` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_buyers` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_sellers` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_investors` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_brokerages` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_developers` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_property_leads` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_resolve_contact_extended` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.rent`

- **Classe:** `PropertyRent`
- **Arquivo:** `models/property_rent.py`
- **Descrição técnica:** Parcela de Aluguel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `competence_month` | `Integer` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `competence_year` | `Integer` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `due_date` | `Date` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `payment_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `amount` | `Monetary` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `discount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `fine` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `interest` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount_paid` | `Monetary` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount_due` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `account_move_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `receipt_number` | `Char` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `receipt_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `receipt_state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `payment_method` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `payment_notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `days_late` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notified_d1` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notified_d5` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notified_d15` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notified_d30` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_amount_due` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_days_late` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_amount` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_amount_paid` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `action_open` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_register_payment` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_issue_rent_receipt` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_print_receipt` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_account_move` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_create_accounting_entry` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_reset_draft` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cron_check_late_rents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.rent.adjustment`

- **Classe:** `PropertyRentAdjustment`
- **Arquivo:** `models/property_rent_adjustment.py`
- **Descrição técnica:** Reajuste de Aluguel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `index_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `index_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `period_months` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `period_start` | `Date` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `index_period` | `Char` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `index_rate` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `months_found` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `previous_rent` | `Monetary` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `new_rent` | `Monetary` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `adjustment_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `adjustment_pct` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `adjustment_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `effective_date` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_index_id` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_period_start` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_index_period` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_new_rent` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_adjustment_value` | Compute | Validar dependências, store, atualização automática e performance. |
| `_onchange_contract_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `action_fetch_rate` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_apply` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_create_renewal` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_cancel` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reset_draft` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_check_index_rate` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.rent.line`

- **Classe:** `PropertyRentLine`
- **Arquivo:** `models/property_rent_enterprise.py`
- **Descrição técnica:** Composição da Parcela de Aluguel


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `rent_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `charge_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount` | `Monetary` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `origin` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `calculation_base` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `calculation_note` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_check_amount_sign` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `property.rent.payment`

- **Classe:** `PropertyRentPayment`
- **Arquivo:** `models/property_rent_enterprise.py`
- **Descrição técnica:** Recebimento de Parcela de Aluguel

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `partner_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `company_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Não | Sim | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `payment_date` | `Date` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount` | `Monetary` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `payment_method` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `journal_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `account_move_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_view_account_move` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.contract`

- **Classe:** `PropertyContract`
- **Arquivo:** `models/property_rent_enterprise.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.contract`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `rent_due_day` | `Integer` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `late_fee_percent` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `late_interest_percent_month` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `late_grace_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `penalty_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `interest_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `discount_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_check_rent_due_day` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_onchange_rent_due_day_warning` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_safe_due_date` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_next_due_after` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prorata_amount` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_generate_rents` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.rent`

- **Classe:** `PropertyRent`
- **Arquivo:** `models/property_rent_enterprise.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.rent`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `period_start` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `period_end` | `Date` | Não | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `rent_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `days_charged` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `cycle_days` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `calculation_note` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `installment_ref` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `line_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `payment_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `payment_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount_rent` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount_penalty` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount_interest` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `amount_discount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `residual_amount` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_charge_calculation_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_payment_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_enterprise_totals` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_amount_due` | Compute | Validar dependências, store, atualização automática e performance. |
| `_ensure_base_rent_line` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_config_account` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_account_for_charge` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_calculate_late_charges` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_recalculate_late_charges` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_view_payments` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_register_payment` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_prepare_credit_lines_for_payment` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_create_accounting_entry` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `res.config.settings`

- **Classe:** `ResConfigSettings`
- **Arquivo:** `models/property_rent_enterprise.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `res.config.settings`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `property_rent_penalty_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `property_rent_interest_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `property_rent_discount_account_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

### Model `property.seller`

- **Classe:** `PropertySeller`
- **Arquivo:** `models/property_seller.py`
- **Descrição técnica:** Vendedor

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `partner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.stakeholder.profile`

- **Classe:** `PropertyStakeholderProfile`
- **Arquivo:** `models/property_stakeholder_profile.py`
- **Descrição técnica:** Perfil Imobiliário do Contato

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `display_name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `partner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stakeholder_type_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `role_status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `company_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `start_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `end_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `user_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `brokerage_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `registration_number` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_display_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_unique_partner_type` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_check_dates` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_sync_partner_tag` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_operational_model_map` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_operational_model_name` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_operational_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_find_operational_record` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ensure_operational_record` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_open_partner` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_open_operational_record` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.stakeholder.type`

- **Classe:** `PropertyStakeholderType`
- **Arquivo:** `models/property_stakeholder_type.py`
- **Descrição técnica:** Tipo de Stakeholder Imobiliário


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `category_group` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_person_role` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_company_role` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `can_receive_commission` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `can_have_portal_access` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `can_be_website_actor` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `default_partner_tag_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_check_unique_code` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `property.tenant`

- **Classe:** `PropertyTenant`
- **Arquivo:** `models/property_tenant.py`
- **Descrição técnica:** Locatário

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `partner_id` | `Many2one` | Sim | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `stakeholder_profile_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Não | Sim | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `email` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `phone` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mobile` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_contract_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ensure_profile` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_view_contracts` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `document.document` | `models/document_ext.py` | Modelo `document.document` usado pelo módulo. | complex_id, asset_id, contract_id, owner_id, broker_id, authorized_broker_ids, media_ids, media_count | _compute_media_count, _get_broker_for_user, can_user_view_document, _compute_access_summary, _check_property_link |
| `ir.actions.report` | `models/ir_actions_report_patch.py` | Modelo `ir.actions.report` usado pelo módulo. | sem campos declarados no arquivo analisado | _build_wkhtmltopdf_args |
| `res.config.settings` | `models/property_accounting.py` | Modelo `res.config.settings` usado pelo módulo. | property_rent_journal_id, property_rent_income_account_id, property_repasse_journal_id, property_repasse_account_id | sem métodos relevantes |
| `property.acquisition` | `models/property_acquisition.py` | Aquisição de Imóvel | name, reference, color, priority, asset_type, address, city, state_name | _compute_financials, _compute_dd_progress, _expand_stages, action_set_analysis, action_set_negotiation, action_set_due_diligence, action_set_closing, action_close |
| `property.inspection` | `models/property_agenda_ext.py` | Modelo `property.inspection` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_description, _agenda_get_deadline, _agenda_get_activity_type, _agenda_get_partners, _sync_agenda_defaults, action_schedule, create |
| `property.maintenance` | `models/property_agenda_ext.py` | Modelo `property.maintenance` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_description, _agenda_get_deadline, _agenda_get_activity_type, _agenda_get_partners, _sync_agenda_defaults, action_schedule, create |
| `property.contract` | `models/property_agenda_ext.py` | Modelo `property.contract` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_deadline, _agenda_get_activity_type, _agenda_get_description, action_schedule_contract_activity |
| `property.rent` | `models/property_agenda_ext.py` | Modelo `property.rent` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_deadline, _agenda_get_activity_type, action_schedule_rent_activity |
| `property.rent.adjustment` | `models/property_agenda_ext.py` | Modelo `property.rent.adjustment` usado pelo módulo. | agenda_responsible_ids, agenda_partner_ids | _agenda_get_title, _agenda_get_deadline, _agenda_get_activity_type, action_schedule_rent_adjustment_activity |
| `property.asset` | `models/property_asset.py` | Imóvel | name, reference, display_name_full, asset_type, status, registration, iptu_number, legal_description | init, _compute_media_count, _compute_kanban_indicators, action_view_media, action_open_bulk_media_wizard, action_open_gallery_media_wizard, action_open_other_media_wizard, _compute_governance_case_count |
| `property.asset.communication` | `models/property_asset_communication.py` | Comunicação de Imóvel | tracking_token, email_message_id, external_message_id, email_from, email_to, email_cc, channel_type, channel_origin | _get_tracking_token, _normalize_subject, create, action_mark_done, action_create_task |
| `property.broker` | `models/property_broker.py` | Corretor de Imóveis | name, stakeholder_profile_id, partner_id, stakeholder_profile_id, user_id, creci, active, email | _broker_partner_category, _prepare_partner_vals, _ensure_profile, _sync_partner, _onchange_partner_id, _compute_stats, create, write |
| `property.broker.assignment` | `models/property_broker_assignment.py` | Mandato de Corretor | name, reference, asset_id, broker_id, assignment_type, exclusive, start_date, end_date | _compute_name, _compute_governance_case_count, _compute_status, _check_dates, _check_exclusivity, action_cancel, action_open_dispute, action_view_governance_cases |
| `property.brokerage` | `models/property_brokerage.py` | Imobiliária | partner_id, stakeholder_profile_id, active, name, email, phone, mobile, broker_ids | _ensure_profile, create, write |
| `property.buyer` | `models/property_buyer.py` | Comprador | partner_id, stakeholder_profile_id, active, name, email, phone, mobile, budget_min | _ensure_profile, create, write |
| `property.commission` | `models/property_commission.py` | Comissão de Corretor | name, reference, commission_type, broker_id, acquisition_id, contract_id, asset_id, company_id | _compute_name, _compute_asset, _compute_commission, _onchange_broker_id, _onchange_acquisition_id, _onchange_contract_id, action_pay, action_cancel |
| `property.complex` | `models/property_complex.py` | Complexo / Edifício | name, reference, active, complex_type, owner_id, company_id, address, address_number | init, _compute_financials, _onchange_zip_code, _search_zip_code_data, action_search_zip_code, action_view_units, action_view_documents, create |
| `property.contract` | `models/property_contract.py` | Contrato de Locação | name, reference, original_filename, contract_type, asset_id, tenant_id, partner_id, broker_id | _auto_init, _compute_relation_button_counts, action_open_asset, action_open_tenant_profile, action_open_broker, action_open_assignment, _compute_adjustment_count, action_view_adjustments |
| `property.dashboard` | `models/property_dashboard.py` | Dashboard de Imóveis | name, asset_total, asset_available, asset_rented, asset_maintenance, asset_for_sale, contract_active, contract_expiring | _compute_all, _compute_charts, action_view_documents |
| `property.developer` | `models/property_developer.py` | Incorporadora | partner_id, stakeholder_profile_id, active, name, email, phone, mobile, notes | _ensure_profile, create, write |
| `property.index` | `models/property_index.py` | Índice de Reajuste | name, code, bcb_series_code, value_ids, value_count, coverage_from, coverage_to, last_sync | _check_unique_code, _compute_bcb_series_code, _compute_coverage, _fetch_bcb_data, action_sync_from_bcb, get_accumulated_rate |
| `property.index.value` | `models/property_index.py` | Valor Mensal do Índice | index_id, year, month, month_label, value_pct | _check_unique_period, _compute_month_label, action_cron_sync_all_indexes |
| `property.inspection` | `models/property_inspection.py` | Vistoria de Imóvel | name, reference, inspection_type, asset_id, contract_id, company_id, scheduled_date, date | _compute_name, _compute_attachment_count, _compute_media_count, action_schedule, action_done, action_cancel, action_reset_draft, action_view_media |
| `property.investor` | `models/property_investor.py` | Investidor | partner_id, stakeholder_profile_id, active, name, email, phone, mobile, investment_profile | _ensure_profile, create, write |
| `property.lead` | `models/property_lead.py` | Interesse em Imóvel | name, email, phone, stakeholder_profile_id, partner_id, asset_id, interest_type, message | _lead_partner_category, _ensure_profile, _sync_partner, action_set_contacted, action_set_qualified, action_set_lost, create, write |
| `property.maintenance` | `models/property_maintenance.py` | Manutenção de Imóvel | name, reference, description, maintenance_type, priority, responsible_party, asset_id, contract_id | _compute_attachment_count, _compute_media_count, action_quote, action_schedule, action_start, action_done, action_cancel, action_reset_draft |
| `property.media.category` | `models/property_media.py` | Categoria de Mídia Imobiliária | name, code, sequence, active, applicable_purpose, default_content_kind, publishable_default, description | sem métodos relevantes |
| `property.media` | `models/property_media.py` | Mídia do Imóvel | name, display_name, sequence, active, company_id, purpose, category_id, content_kind | init, _compute_display_name, _compute_file_meta, _onchange_purpose, _onchange_category_id, _onchange_content_kind, create, write |
| `property.migration.helper` | `models/property_migration_helper.py` | Property Migration Helper | sem campos declarados no arquivo analisado | init |
| `property.owner` | `models/property_owner.py` | Proprietário de Imóvel | name, stakeholder_profile_id, partner_id, cpf_cnpj, active, email, phone, mobile | _compute_stats, _compute_repasse_count, _owner_partner_category, _prepare_partner_vals, _ensure_profile, _sync_partner, _onchange_partner_id, create |
| `property.owner.repasse` | `models/property_owner_repasse.py` | Repasse Mensal ao Proprietário | name, reference, owner_id, period_month, period_year, date_from, date_to, state | _compute_name, _compute_totals, _onchange_period, action_load_data, action_confirm, action_register_payment, _send_repasse_email, action_cancel |
| `property.owner.statement` | `models/property_owner_statement.py` | Extrato do Proprietário | owner_id, date_from, date_to, currency_id, rent_income, rent_count, commission_total, maintenance_total | _compute_totals, action_print |
| `res.partner` | `models/property_partner_ext.py` | Modelo `res.partner` usado pelo módulo. | mobile, property_stakeholder_profile_ids, has_property_stakeholder_profile, property_stakeholder_profile_count, property_owner_count, property_broker_count, property_tenant_count, property_buyer_count | _compute_has_property_stakeholder_profile, _compute_property_stakeholder_display_counts, _open_partner_related, action_view_property_stakeholder_profiles, action_new_property_stakeholder_profile, action_view_property_owners, action_view_property_brokers, action_view_property_tenants |
| `property.rent` | `models/property_rent.py` | Parcela de Aluguel | name, reference, contract_id, asset_id, partner_id, company_id, competence_month, competence_year | _compute_name, _compute_amount_due, _compute_days_late, _check_amount, _check_amount_paid, action_open, action_register_payment, _issue_rent_receipt |
| `property.rent.adjustment` | `models/property_rent_adjustment.py` | Reajuste de Aluguel | name, reference, contract_id, asset_id, partner_id, company_id, currency_id, index_type | _compute_index_id, _compute_period_start, _compute_index_period, _compute_name, _compute_new_rent, _compute_adjustment_value, _onchange_contract_id, action_fetch_rate |
| `property.rent.line` | `models/property_rent_enterprise.py` | Composição da Parcela de Aluguel | rent_id, sequence, company_id, currency_id, partner_id, contract_id, charge_type, name | _check_amount_sign |
| `property.rent.payment` | `models/property_rent_enterprise.py` | Recebimento de Parcela de Aluguel | name, rent_id, contract_id, asset_id, partner_id, company_id, currency_id, payment_date | create, action_view_account_move |
| `property.contract` | `models/property_rent_enterprise.py` | Modelo `property.contract` usado pelo módulo. | rent_due_day, late_fee_percent, late_interest_percent_month, late_grace_days, penalty_account_id, interest_account_id, discount_account_id | _check_rent_due_day, _onchange_rent_due_day_warning, _safe_due_date, _next_due_after, _prorata_amount, action_generate_rents |
| `property.rent` | `models/property_rent_enterprise.py` | Modelo `property.rent` usado pelo módulo. | period_start, period_end, rent_type, days_charged, cycle_days, calculation_note, installment_ref, line_ids | _compute_payment_count, _compute_enterprise_totals, _compute_amount_due, _ensure_base_rent_line, _get_config_account, _get_account_for_charge, _calculate_late_charges, action_recalculate_late_charges |
| `res.config.settings` | `models/property_rent_enterprise.py` | Modelo `res.config.settings` usado pelo módulo. | property_rent_penalty_account_id, property_rent_interest_account_id, property_rent_discount_account_id | sem métodos relevantes |
| `property.seller` | `models/property_seller.py` | Vendedor | partner_id, stakeholder_profile_id, active, name, email, phone, mobile, notes | _ensure_profile, create, write |
| `property.stakeholder.profile` | `models/property_stakeholder_profile.py` | Perfil Imobiliário do Contato | display_name, active, partner_id, stakeholder_type_id, role_status, company_id, start_date, end_date | _compute_display_name, _check_unique_partner_type, _check_dates, _sync_partner_tag, _operational_model_map, _get_operational_model_name, _prepare_operational_vals, _find_operational_record |
| `property.stakeholder.type` | `models/property_stakeholder_type.py` | Tipo de Stakeholder Imobiliário | name, code, category_group, sequence, active, is_person_role, is_company_role, can_receive_commission | _check_unique_code |
| `property.tenant` | `models/property_tenant.py` | Locatário | partner_id, stakeholder_profile_id, active, name, email, phone, mobile, notes | _compute_contract_count, create, write, _ensure_profile, action_view_contracts |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `res_config_settings_view_property_accounting` | `res.config.settings` | `views/property_accounting_settings_views.xml` |
| `view_property_acquisition_list` | `property.acquisition` | `views/property_acquisition_views.xml` |
| `view_property_acquisition_kanban` | `property.acquisition` | `views/property_acquisition_views.xml` |
| `view_property_acquisition_form` | `property.acquisition` | `views/property_acquisition_views.xml` |
| `view_property_acquisition_search` | `property.acquisition` | `views/property_acquisition_views.xml` |
| `view_property_acquisition_pivot` | `property.acquisition` | `views/property_acquisition_views.xml` |
| `view_property_inspection_form_agenda_ext` | `property.inspection` | `views/property_agenda_views.xml` |
| `view_property_inspection_calendar` | `property.inspection` | `views/property_agenda_views.xml` |
| `view_property_maintenance_form_agenda_ext` | `property.maintenance` | `views/property_agenda_views.xml` |
| `view_property_maintenance_calendar` | `property.maintenance` | `views/property_agenda_views.xml` |
| `view_property_contract_form_agenda_ext` | `property.contract` | `views/property_agenda_views.xml` |
| `view_property_rent_form_agenda_ext` | `property.rent` | `views/property_agenda_views.xml` |
| `view_property_rent_adjustment_form_agenda_ext` | `property.rent.adjustment` | `views/property_agenda_views.xml` |
| `view_property_asset_communication_list` | `property.asset.communication` | `views/property_asset_communication_views.xml` |
| `view_property_asset_communication_form` | `property.asset.communication` | `views/property_asset_communication_views.xml` |
| `view_property_asset_communication_search` | `property.asset.communication` | `views/property_asset_communication_views.xml` |
| `view_property_asset_list` | `property.asset` | `views/property_asset_views.xml` |
| `view_property_asset_form` | `property.asset` | `views/property_asset_views.xml` |
| `view_property_asset_kanban` | `property.asset` | `views/property_asset_views.xml` |
| `view_property_asset_search` | `property.asset` | `views/property_asset_views.xml` |
| `view_property_broker_assignment_list` | `property.broker.assignment` | `views/property_broker_assignment_views.xml` |
| `view_property_broker_assignment_form` | `property.broker.assignment` | `views/property_broker_assignment_views.xml` |
| `view_property_broker_assignment_search` | `property.broker.assignment` | `views/property_broker_assignment_views.xml` |
| `view_property_broker_list` | `property.broker` | `views/property_broker_views.xml` |
| `view_property_broker_form` | `property.broker` | `views/property_broker_views.xml` |
| `view_property_broker_search` | `property.broker` | `views/property_broker_views.xml` |
| `view_property_brokerage_list` | `property.brokerage` | `views/property_brokerage_views.xml` |
| `view_property_brokerage_form` | `property.brokerage` | `views/property_brokerage_views.xml` |
| `view_property_buyer_list` | `property.buyer` | `views/property_buyer_views.xml` |
| `view_property_buyer_form` | `property.buyer` | `views/property_buyer_views.xml` |
| `view_property_commission_list` | `property.commission` | `views/property_commission_views.xml` |
| `view_property_commission_form` | `property.commission` | `views/property_commission_views.xml` |
| `view_property_commission_search` | `property.commission` | `views/property_commission_views.xml` |
| `view_property_complex_list` | `property.complex` | `views/property_complex_views.xml` |
| `view_property_complex_form` | `property.complex` | `views/property_complex_views.xml` |
| `view_property_complex_search` | `property.complex` | `views/property_complex_views.xml` |
| `view_property_contract_form_enterprise_finance` | `property.contract` | `views/property_contract_enterprise_views.xml` |
| `view_property_contract_list` | `property.contract` | `views/property_contract_views.xml` |
| `view_property_contract_form` | `property.contract` | `views/property_contract_views.xml` |
| `view_property_contract_kanban` | `property.contract` | `views/property_contract_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_property_agenda` | Agenda Operacional | `property_core.menu_property_operations` | `` | `views/property_agenda_views.xml` |
| `menu_property_calendar_all` | Calendário Geral de Imóveis | `menu_property_agenda` | `common_base.action_common_agenda_calendar_property` | `views/property_agenda_views.xml` |
| `menu_property_inspection_calendar` | Vistorias no Calendário | `menu_property_agenda` | `common_base.action_common_agenda_calendar_inspection` | `views/property_agenda_views.xml` |
| `menu_property_maintenance_calendar` | Manutenções no Calendário | `menu_property_agenda` | `common_base.action_common_agenda_calendar_maintenance` | `views/property_agenda_views.xml` |
| `menu_property_root` | Imóveis | `` | `` | `views/property_menu_views.xml` |
| `menu_property_dashboard` | Dashboard | `menu_property_root` | `action_property_dashboard` | `views/property_menu_views.xml` |
| `menu_property_cadastros` | Cadastros | `menu_property_root` | `` | `views/property_menu_views.xml` |
| `menu_property_comercial` | Comercial | `menu_property_root` | `` | `views/property_menu_views.xml` |
| `menu_property_corretores` | Corretores | `menu_property_root` | `` | `views/property_menu_views.xml` |
| `menu_property_financeiro` | Financeiro | `menu_property_root` | `` | `views/property_menu_views.xml` |
| `menu_property_operations` | Operações | `menu_property_root` | `` | `views/property_menu_views.xml` |
| `menu_property_complex` | Complexos | `menu_property_cadastros` | `action_property_complex` | `views/property_menu_views.xml` |
| `menu_property_asset` | Imóveis | `menu_property_cadastros` | `action_property_asset` | `views/property_menu_views.xml` |
| `menu_property_owner` | Proprietários | `menu_property_cadastros` | `action_property_owner` | `views/property_menu_views.xml` |
| `menu_property_contract` | Contratos | `menu_property_comercial` | `action_property_contract` | `views/property_menu_views.xml` |
| `menu_property_rent` | Parcelas | `menu_property_comercial` | `action_property_rent` | `views/property_menu_views.xml` |
| `menu_property_acquisition` | Aquisições | `menu_property_comercial` | `action_property_acquisition` | `views/property_menu_views.xml` |
| `menu_property_lead` | Leads do Website | `menu_property_comercial` | `action_property_lead` | `views/property_menu_views.xml` |
| `menu_property_broker` | Corretores | `menu_property_corretores` | `action_property_broker` | `views/property_menu_views.xml` |
| `menu_property_broker_assignment` | Mandatos | `menu_property_corretores` | `action_property_broker_assignment` | `views/property_menu_views.xml` |
| `menu_property_commission` | Comissões | `menu_property_corretores` | `action_property_commission` | `views/property_menu_views.xml` |
| `menu_property_rent_adjustment` | Reajustes | `menu_property_financeiro` | `action_property_rent_adjustment` | `views/property_menu_views.xml` |
| `menu_property_index` | Índices de Reajuste | `menu_property_financeiro` | `action_property_index` | `views/property_menu_views.xml` |
| `menu_property_owner_repasse` | Repasses ao Proprietário | `menu_property_financeiro` | `action_property_owner_repasse` | `views/property_menu_views.xml` |
| `menu_property_inspection` | Vistorias | `menu_property_operations` | `action_property_inspection` | `views/property_menu_views.xml` |
| `menu_property_maintenance` | Manutenções | `menu_property_operations` | `action_property_maintenance` | `views/property_menu_views.xml` |
| `menu_property_media` | Mídias e Fotos | `menu_property_operations` | `` | `views/property_menu_views.xml` |
| `menu_property_media_all` | Todas as Mídias | `menu_property_media` | `action_property_media` | `views/property_menu_views.xml` |
| `menu_property_media_site_review` | Revisão para Site | `menu_property_media` | `action_property_media_site_review` | `views/property_menu_views.xml` |
| `menu_property_media_category` | Categorias de Mídia | `menu_property_media` | `action_property_media_category` | `views/property_menu_views.xml` |
| `menu_property_relationships` | Relacionamentos | `menu_property_root` | `` | `views/property_menu_views.xml` |
| `menu_property_rel_people` | Pessoas | `menu_property_relationships` | `` | `views/property_menu_views.xml` |
| `menu_property_partner_contacts` | Contatos Imobiliários | `menu_property_rel_people` | `action_property_partner_contacts` | `views/property_menu_views.xml` |
| `menu_property_tenant` | Locatários | `menu_property_rel_people` | `action_property_tenant` | `views/property_menu_views.xml` |
| `menu_property_buyer` | Compradores | `menu_property_rel_people` | `action_property_buyer` | `views/property_menu_views.xml` |
| `menu_property_seller` | Vendedores | `menu_property_rel_people` | `action_property_seller` | `views/property_menu_views.xml` |
| `menu_property_investor` | Investidores | `menu_property_rel_people` | `action_property_investor` | `views/property_menu_views.xml` |
| `menu_property_rel_companies` | Empresas e Parceiros | `menu_property_relationships` | `` | `views/property_menu_views.xml` |
| `menu_property_brokerage` | Imobiliárias | `menu_property_rel_companies` | `action_property_brokerage` | `views/property_menu_views.xml` |
| `menu_property_developer` | Incorporadoras | `menu_property_rel_companies` | `action_property_developer` | `views/property_menu_views.xml` |
| ... | ... | ... | ... | 4 menus adicionais |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_property_acquisition` | Pipeline de Aquisição | `property.acquisition` | `views/property_acquisition_views.xml` |
| `action_property_inspection` |  | `` | `views/property_agenda_views.xml` |
| `action_property_inspection_calendar` | Agenda de Vistorias | `property.inspection` | `views/property_agenda_views.xml` |
| `action_property_maintenance` |  | `` | `views/property_agenda_views.xml` |
| `action_property_maintenance_calendar` | Agenda de Manutenções | `property.maintenance` | `views/property_agenda_views.xml` |
| `action_property_asset_communication` | Comunicações de Imóvel | `property.asset.communication` | `views/property_asset_communication_views.xml` |
| `action_property_asset` | Imóveis | `property.asset` | `views/property_asset_views.xml` |
| `action_property_broker_assignment` | Mandatos | `property.broker.assignment` | `views/property_broker_assignment_views.xml` |
| `action_property_broker` | Corretores | `property.broker` | `views/property_broker_views.xml` |
| `action_property_brokerage` | Imobiliárias | `property.brokerage` | `views/property_brokerage_views.xml` |
| `action_property_buyer` | Compradores | `property.buyer` | `views/property_buyer_views.xml` |
| `action_property_commission` | Comissões | `property.commission` | `views/property_commission_views.xml` |
| `action_property_complex` | Complexos | `property.complex` | `views/property_complex_views.xml` |
| `action_property_contract` | Contratos de Locação | `property.contract` | `views/property_contract_views.xml` |
| `action_property_dashboard` | Dashboard | `property.dashboard` | `views/property_dashboard_views.xml` |
| `action_property_developer` | Incorporadoras | `property.developer` | `views/property_developer_views.xml` |
| `action_property_document_category` | Categorias Documentais | `document.category` | `views/property_document_type_views.xml` |
| `action_property_document_type` | Tipos de Documento | `document.type` | `views/property_document_type_views.xml` |
| `action_property_document_location` | Localizações Físicas | `document.location` | `views/property_document_type_views.xml` |
| `action_property_document` | Documentos | `document.document` | `views/property_document_views.xml` |
| `action_property_index` | Índices de Reajuste | `property.index` | `views/property_index_views.xml` |
| `action_property_inspection` | Vistorias | `property.inspection` | `views/property_inspection_views.xml` |
| `action_property_investor` | Investidores | `property.investor` | `views/property_investor_views.xml` |
| `action_property_lead` | Leads do Website | `property.lead` | `views/property_lead_views.xml` |
| `action_property_maintenance` | Manutenções | `property.maintenance` | `views/property_maintenance_views.xml` |
| `action_property_media_category` | Categorias de Mídia | `property.media.category` | `views/property_media_category_views.xml` |
| `action_property_media` | Mídias e Fotos | `property.media` | `views/property_media_views.xml` |
| `action_property_media_site_review` | Revisão para Site | `property.media` | `views/property_media_views.xml` |
| `action_property_owner_repasse` | Repasses ao Proprietário | `property.owner.repasse` | `views/property_owner_repasse_views.xml` |
| `action_property_owner` | Proprietários | `property.owner` | `views/property_owner_views.xml` |
| `action_property_partner_contacts` | Contatos Imobiliários | `res.partner` | `views/property_partner_ext_views.xml` |
| `action_property_rent_adjustment` | Reajustes de Aluguel | `property.rent.adjustment` | `views/property_rent_adjustment_views.xml` |
| `action_property_rent_payment` | Recebimentos de Aluguel | `property.rent.payment` | `views/property_rent_enterprise_views.xml` |
| `action_property_rent` | Parcelas de Aluguel | `property.rent` | `views/property_rent_views.xml` |
| `action_property_seller` | Vendedores | `property.seller` | `views/property_seller_views.xml` |
| `action_property_stakeholder_profile` | Perfis Imobiliários | `property.stakeholder.profile` | `views/property_stakeholder_profile_views.xml` |
| `action_property_stakeholder_type` | Tipos de Perfil Imobiliário | `property.stakeholder.type` | `views/property_stakeholder_type_views.xml` |
| `action_property_tenant` | Locatários | `property.tenant` | `views/property_tenant_views.xml` |


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
