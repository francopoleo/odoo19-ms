# Documentação Técnica — Histórico de Contratos com OCR

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Upload, OCR e extração de dados de contratos históricos para criação ou atualização de registros imobiliários.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `property_contract_history` |
| Nome funcional | Histórico de Contratos com OCR |
| Versão | `19.0.1.0.2` |
| Aplicação | `False` |
| Instalável | `True` |
| Dependências | `property_core`, `property_payment_proof`, `mail` |

### Arquivos declarados no manifesto

- `security/ir.model.access.csv`
- `data/ir_sequence.xml`
- `views/property_contract_history_views.xml`
- `views/property_asset_views.xml`
- `views/menu_views.xml`
- `wizard/bulk_upload_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `property.asset`

- **Classe:** `PropertyAsset`
- **Arquivo:** `models/property_asset.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.asset`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `contract_history_count` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_history_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `last_contract_sync` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `last_contract_source_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_contract_history_count` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_view_contract_history` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_import_contract_history` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.contract.history`

- **Classe:** `PropertyContractHistory`
- **Arquivo:** `models/property_contract_history.py`
- **Descrição técnica:** Histórico de Contratos com OCR

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `state` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `contract_file` | `Binary` | Não | Não | Não | Arquivo/imagem; validar tamanho, origem e regra de anexo. |
| `contract_filename` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `mimetype` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `raw_text` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `extraction_log` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `matched_payload` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `parser_used` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `asset_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `contract_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sync_to_asset` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `party1_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `party1_vat` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `party2_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `party2_vat` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sign_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `start_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `end_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `renewal_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `monthly_amount` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `total_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `deposit_value` | `Monetary` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `currency_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `address` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `address_complement` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `neighborhood` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `city` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `zip_code` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `property_description` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `synced_to_asset_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sync_timestamp` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sync_log` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `superseded_by_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `line_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `history_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ocr_image_to_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_pdf_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_pdf_with_pymupdf_ocr` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_pdf_with_pdf2image_ocr` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_pdf_as_image` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_image_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_text_from_file` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_parse_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_extract` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_manual_review` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_approve` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_safe_field_value` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_set_update_if_field_exists` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_score_property_match` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_find_asset` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_partner_from_extracted_party` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_is_valid_contract_value` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_put_if_contract_field_exists` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_put_first_existing_contract_field` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_put_all_existing_contract_fields` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_history_start_date_for_contract` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_history_end_date_for_contract` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_find_or_create_record_from_partner` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_contract_relation_value_from_partner` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_put_first_existing_contract_party_field` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_contract_values_from_history` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_create_contract_from_history` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_confirm_asset_association` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_sync_to_asset` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reject` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_contract` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_lines` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_view_history` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.contract.history.line`

- **Classe:** `PropertyContractHistoryLine`
- **Arquivo:** `models/property_contract_history_line.py`
- **Descrição técnica:** Campo Extraído de Contrato


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `history_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `field_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `label` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `raw_value` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `parsed_value` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `field_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `confidence` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `accepted` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_label` | Compute | Validar dependências, store, atualização automática e performance. |
| `action_accept` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_reject` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `property.asset` | `models/property_asset.py` | Modelo `property.asset` usado pelo módulo. | contract_history_count, contract_history_ids, last_contract_sync, last_contract_source_id | _compute_contract_history_count, action_view_contract_history, action_import_contract_history |
| `property.contract.history` | `models/property_contract_history.py` | Histórico de Contratos com OCR | name, company_id, contract_type, state, contract_file, contract_filename, mimetype, raw_text | create, _ocr_image_to_text, _extract_pdf_text, _extract_pdf_with_pymupdf_ocr, _extract_pdf_with_pdf2image_ocr, _extract_pdf_as_image, _extract_image_text, _extract_text_from_file |
| `property.contract.history.line` | `models/property_contract_history_line.py` | Campo Extraído de Contrato | history_id, field_name, label, raw_value, parsed_value, field_type, confidence, notes | _compute_label, action_accept, action_reject |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_property_asset_form_contract_history_ext` | `property.asset` | `views/property_asset_views.xml` |
| `view_property_asset_list_contract_history_ext` | `property.asset` | `views/property_asset_views.xml` |
| `view_property_contract_history_kanban` | `property.contract.history` | `views/property_contract_history_views.xml` |
| `view_property_contract_history_list` | `property.contract.history` | `views/property_contract_history_views.xml` |
| `view_property_contract_history_form` | `property.contract.history` | `views/property_contract_history_views.xml` |
| `view_property_contract_history_search` | `property.contract.history` | `views/property_contract_history_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_property_contract_history_root` | Contratos Históricos | `property_core.menu_property_root` | `` | `views/menu_views.xml` |
| `menu_property_contract_history` | Gerenciar Contratos | `menu_property_contract_history_root` | `action_property_contract_history` | `views/menu_views.xml` |
| `menu_property_contract_history_kanban` | Por Status | `menu_property_contract_history_root` | `action_property_contract_history_kanban` | `views/menu_views.xml` |
| `menu_property_contract_history_bulk_upload` | Upload em Lote | `menu_property_contract_history_root` | `action_property_contract_history_bulk_upload` | `views/menu_views.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_property_contract_history` | Histórico de Contratos | `property.contract.history` | `views/menu_views.xml` |
| `action_property_contract_history_kanban` | Contratos por Status | `property.contract.history` | `views/menu_views.xml` |
| `action_property_contract_history_bulk_upload` | Upload em Lote de Contratos | `property.contract.history.bulk.upload` | `views/menu_views.xml` |
| `action_property_asset_import_contract` | Importar Contrato Histórico | `property.contract.history` | `views/menu_views.xml` |


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
