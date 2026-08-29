# Documentação Técnica — Property Contract OCR Templates

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Configuração de templates, regex e regras de extração para diferentes modelos de contratos imobiliários.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `property_contract_ocr_template` |
| Nome funcional | Property Contract OCR Templates |
| Versão | `19.0.1.1.0` |
| Aplicação | `False` |
| Instalável | `True` |
| Dependências | `property_contract_history` |

### Arquivos declarados no manifesto

- `security/ir.model.access.csv`
- `views/property_contract_ocr_template_views.xml`
- `views/property_contract_history_views.xml`
- `data/lease_template_data.xml`
- `data/default_templates.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `property.contract.history`

- **Classe:** `PropertyContractHistory`
- **Arquivo:** `models/property_contract_history.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `property.contract.history`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `ocr_template_id` | `Many2one` | Não | Não | Sim | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `ocr_template_auto_detected` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `ocr_force_template` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_is_generic_filename` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_infer_filename_from_binary` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_find_original_attachment_filename` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_write_ocr_log` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_safe_notify` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_detect_file_kind` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_binary_file_data` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_find_tessdata_dir` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_available_tesseract_languages` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_choose_tesseract_lang` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_image_for_ocr` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_tesseract_image_to_string` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_tesseract_debug` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_python_ocr_debug` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_debug_ocr_environment` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_debug_ocr_file` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_extract_pdf_text_direct` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ocr_image_bytes` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ocr_pdf_pymupdf` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_ocr_pdf_pdf2image` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_extract_text_for_template` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_detect_ocr_template` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_create_template_lines` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_map_template_line_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_apply_template_payload` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_extract_by_template` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `action_extract` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |

### Model `property.contract.ocr.template`

- **Classe:** `PropertyContractOcrTemplate`
- **Arquivo:** `models/property_contract_ocr_template.py`
- **Descrição técnica:** Template OCR de Contrato Imobiliário

- **Heranças:** `mail.thread`, `mail.activity.mixin`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `active` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Sim | Não | Sim | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `company_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `document_kind` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `min_auto_detect_score` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `contract_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `extraction_mode` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `page_limit` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_detect_pattern` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `auto_detect_keywords` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `description` | `Html` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `line_ids` | `One2many` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_field_name_label_map` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_candidate_templates` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_score_template_against_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_auto_detect_from_text` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_install_default_templates` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `extract_payload` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `property.contract.ocr.template.line`

- **Classe:** `PropertyContractOcrTemplateLine`
- **Arquivo:** `models/property_contract_ocr_template.py`
- **Descrição técnica:** Linha do Template OCR de Contrato


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `template_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `sequence` | `Integer` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `field_id` | `Many2one` | Sim | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `field_name` | `Char` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `field_label` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `field_ttype` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `value_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `value_mode` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `pattern` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `dotall` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `required` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `confidence` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `fixed_value_char` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `fixed_value_float` | `Float` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `fixed_value_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `fixed_value_selection` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `decimal_separator` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `thousand_separator` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `section_key` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `notes` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_onchange_field_id` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_extract_raw_regex` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_fixed_value` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `extract_value` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_convert_value` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_parse_amount` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_parse_date` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `property.contract.history` | `models/property_contract_history.py` | Modelo `property.contract.history` usado pelo módulo. | ocr_template_id, ocr_template_auto_detected, ocr_force_template | _is_generic_filename, _infer_filename_from_binary, _find_original_attachment_filename, write, create, _write_ocr_log, _safe_notify, _detect_file_kind |
| `property.contract.ocr.template` | `models/property_contract_ocr_template.py` | Template OCR de Contrato Imobiliário | active, sequence, name, company_id, document_kind, min_auto_detect_score, contract_type, extraction_mode | _get_field_name_label_map, _get_candidate_templates, _score_template_against_text, _auto_detect_from_text, action_install_default_templates, extract_payload |
| `property.contract.ocr.template.line` | `models/property_contract_ocr_template.py` | Linha do Template OCR de Contrato | template_id, sequence, name, field_id, field_name, field_label, field_ttype, value_type | _onchange_field_id, _extract_raw_regex, _fixed_value, extract_value, _convert_value, _parse_amount, _parse_date |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_property_contract_history_form_ocr_template_ext` | `property.contract.history` | `views/property_contract_history_views.xml` |
| `view_property_contract_history_list_ocr_template_ext` | `property.contract.history` | `views/property_contract_history_views.xml` |
| `view_property_contract_ocr_template_list` | `property.contract.ocr.template` | `views/property_contract_ocr_template_views.xml` |
| `view_property_contract_ocr_template_form` | `property.contract.ocr.template` | `views/property_contract_ocr_template_views.xml` |
| `view_property_contract_ocr_template_search` | `property.contract.ocr.template` | `views/property_contract_ocr_template_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_property_contract_ocr_template` | Templates OCR | `property_contract_history.menu_property_contract_history_root` | `action_property_contract_ocr_template` | `views/property_contract_ocr_template_views.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_property_contract_ocr_template` | Templates OCR de Contrato | `property.contract.ocr.template` | `views/property_contract_ocr_template_views.xml` |


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
