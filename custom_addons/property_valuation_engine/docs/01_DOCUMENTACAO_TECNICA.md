# Documentação Técnica — Property Valuation Engine

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Motor de avaliação e estimativa de valor com critérios, comparáveis e histórico.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `property_valuation_engine` |
| Nome funcional | Property Valuation Engine |
| Versão | `19.0.1.0.5` |
| Aplicação | `False` |
| Instalável | `True` |
| Dependências | `base`, `property_core` |

### Arquivos declarados no manifesto

- `security/valuation_security.xml`
- `security/ir.model.access.csv`
- `security/valuation_record_rules.xml`
- `data/valuation_sequence_data.xml`
- `data/valuation_algorithm_data.xml`
- `data/valuation_factor_data.xml`
- `views/valuation_source_views.xml`
- `views/valuation_factor_views.xml`
- `views/price_m2_reference_views.xml`
- `views/market_comparable_views.xml`
- `views/valuation_algorithm_views.xml`
- `views/valuation_run_views.xml`
- `views/property_asset_valuation_views.xml`
- `views/valuation_menus.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `property.market.comparable`

- **Classe:** `PropertyMarketComparable`
- **Arquivo:** `models/market_comparable.py`
- **Descrição técnica:** Imóvel Comparável de Mercado


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `source_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `external_reference` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `url` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `date_observed` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `asset_use_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `standard` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `conservation` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `city` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `neighborhood` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `address` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `area_m2` | `Float` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_price` | `Monetary` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `price_m2` | `Monetary` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `weight` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `is_internal_closed_deal` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_price_m2` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_positive_values` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `property.price.m2.reference`

- **Classe:** `PropertyPriceM2Reference`
- **Arquivo:** `models/price_m2_reference.py`
- **Descrição técnica:** Referência de Valor por m²


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `valuation_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `asset_use_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `standard` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `city` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `neighborhood` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `price_m2` | `Monetary` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valid_from` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valid_to` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `source_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `confidence_score` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_name` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_values` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `property.asset`

- **Classe:** `PropertyAsset`
- **Arquivo:** `models/property_asset.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.asset`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `valuation_area_m2` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_city` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_neighborhood` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_use_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `valuation_standard` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `valuation_conservation` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `valuation_location_factor` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_liquidity_factor` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_vacancy_factor` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_run_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `valuation_run_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `latest_valuation_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `latest_rent_valuation_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `latest_sale_valuation_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `estimated_rent_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `estimated_sale_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_confidence_score` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_valuation_currency` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_valuation_summary` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_pve_calculate_rent` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_pve_calculate_sale` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_pve_open_valuation_runs` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.valuation.algorithm`

- **Classe:** `PropertyValuationAlgorithm`
- **Arquivo:** `models/valuation_algorithm.py`
- **Descrição técnica:** Algoritmo de Valuation Imobiliário


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `version` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `formula` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

### Model `property.valuation.factor`

- **Classe:** `PropertyValuationFactor`
- **Arquivo:** `models/valuation_factor.py`
- **Descrição técnica:** Fator de Ajuste de Valuation Imobiliário


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `code` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `factor_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `multiplier` | `Float` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_check_multiplier` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `property.valuation.run`

- **Classe:** `PropertyValuationRun`
- **Arquivo:** `models/valuation_run.py`
- **Descrição técnica:** Execução de Estimativa de Valor Imobiliário


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `currency_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `asset_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `valuation_date` | `Date` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `valuation_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `algorithm_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `algorithm_code` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `algorithm_version` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `area_m2` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `city` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `neighborhood` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_use_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `standard` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `conservation` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `reference_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `source_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `comparable_ids` | `Many2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `comparable_count` | `Integer` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `base_price_m2` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `comparable_price_m2` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `adjusted_price_m2` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `location_factor` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `standard_factor` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `conservation_factor` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `liquidity_factor` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `vacancy_factor` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `calculated_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `low_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `high_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `confidence_score` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `margin_percent` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `approved_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `approved_by_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `approved_date` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `review_notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `calculation_notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_compute_comparable_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `_check_positive_numeric_values` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `create_from_asset` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_values_from_asset` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_calculate` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_mark_reviewed` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_approve` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reject` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_calculate_values` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_open_form` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_select_best_reference` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_select_comparables` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_comparable_similarity_score` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_weighted_comparable_price` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_hybrid_price_m2` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_factor_multiplier` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_calculate_confidence` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_range_margin` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_build_calculation_notes` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_asset_company` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_asset_value` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_use_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_standard` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_normalize_conservation` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_safe_float` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_norm` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.valuation.source`

- **Classe:** `PropertyValuationSource`
- **Arquivo:** `models/valuation_source.py`
- **Descrição técnica:** Fonte de Dados de Valuation Imobiliário


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Sim | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `source_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `url` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `reliability_score` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_check_reliability_score` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `property.market.comparable` | `models/market_comparable.py` | Imóvel Comparável de Mercado | name, active, company_id, currency_id, asset_id, source_id, external_reference, url | _compute_price_m2, _check_positive_values |
| `property.price.m2.reference` | `models/price_m2_reference.py` | Referência de Valor por m² | name, active, company_id, currency_id, valuation_type, asset_use_type, standard, city | _compute_name, _check_values |
| `property.asset` | `models/property_asset.py` | Modelo `property.asset` usado pelo módulo. | valuation_area_m2, valuation_city, valuation_neighborhood, valuation_use_type, valuation_standard, valuation_conservation, valuation_location_factor, valuation_liquidity_factor | _compute_valuation_currency, _compute_valuation_summary, action_pve_calculate_rent, action_pve_calculate_sale, action_pve_open_valuation_runs |
| `property.valuation.algorithm` | `models/valuation_algorithm.py` | Algoritmo de Valuation Imobiliário | name, code, version, sequence, active, description, formula | sem métodos relevantes |
| `property.valuation.factor` | `models/valuation_factor.py` | Fator de Ajuste de Valuation Imobiliário | name, code, sequence, active, company_id, factor_type, multiplier, description | _check_multiplier |
| `property.valuation.run` | `models/valuation_run.py` | Execução de Estimativa de Valor Imobiliário | name, active, company_id, currency_id, asset_id, valuation_date, valuation_type, state | create, _compute_comparable_count, _check_positive_numeric_values, create_from_asset, _prepare_values_from_asset, action_calculate, action_mark_reviewed, action_approve |
| `property.valuation.source` | `models/valuation_source.py` | Fonte de Dados de Valuation Imobiliário | name, sequence, active, company_id, source_type, url, reliability_score, notes | _check_reliability_score |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_property_market_comparable_list` | `property.market.comparable` | `views/market_comparable_views.xml` |
| `view_property_market_comparable_form` | `property.market.comparable` | `views/market_comparable_views.xml` |
| `view_property_market_comparable_search` | `property.market.comparable` | `views/market_comparable_views.xml` |
| `view_property_price_m2_reference_list` | `property.price.m2.reference` | `views/price_m2_reference_views.xml` |
| `view_property_price_m2_reference_form` | `property.price.m2.reference` | `views/price_m2_reference_views.xml` |
| `view_property_price_m2_reference_search` | `property.price.m2.reference` | `views/price_m2_reference_views.xml` |
| `view_property_asset_valuation_list` | `property.asset` | `views/property_asset_valuation_views.xml` |
| `view_property_asset_valuation_form` | `property.asset` | `views/property_asset_valuation_views.xml` |
| `view_property_asset_valuation_search` | `property.asset` | `views/property_asset_valuation_views.xml` |
| `view_property_valuation_algorithm_list` | `property.valuation.algorithm` | `views/valuation_algorithm_views.xml` |
| `view_property_valuation_algorithm_form` | `property.valuation.algorithm` | `views/valuation_algorithm_views.xml` |
| `view_property_valuation_factor_list` | `property.valuation.factor` | `views/valuation_factor_views.xml` |
| `view_property_valuation_factor_form` | `property.valuation.factor` | `views/valuation_factor_views.xml` |
| `view_property_valuation_factor_search` | `property.valuation.factor` | `views/valuation_factor_views.xml` |
| `view_property_valuation_run_list` | `property.valuation.run` | `views/valuation_run_views.xml` |
| `view_property_valuation_run_form` | `property.valuation.run` | `views/valuation_run_views.xml` |
| `view_property_valuation_run_search` | `property.valuation.run` | `views/valuation_run_views.xml` |
| `view_property_valuation_run_pivot` | `property.valuation.run` | `views/valuation_run_views.xml` |
| `view_property_valuation_run_graph` | `property.valuation.run` | `views/valuation_run_views.xml` |
| `view_property_valuation_source_list` | `property.valuation.source` | `views/valuation_source_views.xml` |
| `view_property_valuation_source_form` | `property.valuation.source` | `views/valuation_source_views.xml` |
| `view_property_valuation_source_search` | `property.valuation.source` | `views/valuation_source_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_property_valuation_root` | Valuation | `property_core.menu_property_root` | `` | `views/valuation_menus.xml` |
| `menu_property_valuation_operations` | Operações | `menu_property_valuation_root` | `` | `views/valuation_menus.xml` |
| `menu_property_asset_valuation` | Imóveis para Valuation | `menu_property_valuation_operations` | `action_property_asset_valuation` | `views/valuation_menus.xml` |
| `menu_property_valuation_run` | Estimativas | `menu_property_valuation_operations` | `action_property_valuation_run` | `views/valuation_menus.xml` |
| `menu_property_valuation_market` | Mercado | `menu_property_valuation_root` | `` | `views/valuation_menus.xml` |
| `menu_property_price_m2_reference` | Referências m² | `menu_property_valuation_market` | `action_property_price_m2_reference` | `views/valuation_menus.xml` |
| `menu_property_market_comparable` | Comparáveis | `menu_property_valuation_market` | `action_property_market_comparable` | `views/valuation_menus.xml` |
| `menu_property_valuation_configuration` | Configuração | `menu_property_valuation_root` | `` | `views/valuation_menus.xml` |
| `menu_property_valuation_source` | Fontes | `menu_property_valuation_configuration` | `action_property_valuation_source` | `views/valuation_menus.xml` |
| `menu_property_valuation_factor` | Fatores | `menu_property_valuation_configuration` | `action_property_valuation_factor` | `views/valuation_menus.xml` |
| `menu_property_valuation_algorithm` | Algoritmos | `menu_property_valuation_configuration` | `action_property_valuation_algorithm` | `views/valuation_menus.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_property_market_comparable` | Comparáveis | `property.market.comparable` | `views/market_comparable_views.xml` |
| `action_property_price_m2_reference` | Referências m² | `property.price.m2.reference` | `views/price_m2_reference_views.xml` |
| `action_property_asset_valuation` | Imóveis para Valuation | `property.asset` | `views/property_asset_valuation_views.xml` |
| `action_property_valuation_algorithm` | Algoritmos | `property.valuation.algorithm` | `views/valuation_algorithm_views.xml` |
| `action_property_valuation_factor` | Fatores | `property.valuation.factor` | `views/valuation_factor_views.xml` |
| `action_property_valuation_run` | Estimativas | `property.valuation.run` | `views/valuation_run_views.xml` |
| `action_property_valuation_source` | Fontes | `property.valuation.source` | `views/valuation_source_views.xml` |


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
