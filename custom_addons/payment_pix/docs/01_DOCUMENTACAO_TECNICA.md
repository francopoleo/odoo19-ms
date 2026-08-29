# Documentação Técnica — Payment Provider: PIX (BACEN)

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Provedor de pagamento PIX conforme fluxos de cobrança/recebimento integrados ao Odoo.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `payment_pix` |
| Nome funcional | Payment Provider: PIX (BACEN) |
| Versão | `1.0` |
| Aplicação | `False` |
| Instalável | `True` |
| Dependências | `payment_custom`, `account_payment` |

### Arquivos declarados no manifesto

- `views/payment_pix_templates.xml`
- `views/payment_provider_views.xml`
- `views/account_payment_register_views.xml`
- `views/account_payment_views.xml`
- `data/account_payment_method_data.xml`
- `data/payment_method_data.xml`
- `data/payment_provider_data.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `account.journal`

- **Classe:** `AccountJournal`
- **Arquivo:** `models/account_journal.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `account.journal`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `is_pix` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_pix_sync_payment_method_lines` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `account.payment`

- **Classe:** `AccountPayment`
- **Arquivo:** `models/account_payment.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `account.payment`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `is_pix` | `Boolean` | Não | Sim | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pix_e2e_id` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pix_partner_key` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pix_partner_key_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `pix_conta_origem_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `pix_conta_destino_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_is_pix` | Compute | Validar dependências, store, atualização automática e performance. |
| `_compute_pix_flow_accounts` | Compute | Validar dependências, store, atualização automática e performance. |

### Model `account.payment.method`

- **Classe:** `AccountPaymentMethod`
- **Arquivo:** `models/account_payment_method.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `account.payment.method`


#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_payment_method_information` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_payment_method_domain` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `account.payment.register`

- **Classe:** `AccountPaymentRegister`
- **Arquivo:** `models/account_payment_register.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `account.payment.register`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `is_pix` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_is_pix` | Compute | Validar dependências, store, atualização automática e performance. |

### Model `payment.provider`

- **Classe:** `PaymentProvider`
- **Arquivo:** `models/payment_provider.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `payment.provider`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `custom_mode` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `pix_key_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `pix_key` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pix_merchant_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `pix_merchant_city` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_check_pix_fields_before_enabling` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_get_default_payment_method_codes` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_recompute_pending_msg` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_pix_update_pending_msg` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_pix_ensure_pending_msg_is_set` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_pix_build_br_code` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_pix_build_qr_code_base64` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `account.journal` | `models/account_journal.py` | Modelo `account.journal` usado pelo módulo. | is_pix | create, write, _pix_sync_payment_method_lines |
| `account.payment` | `models/account_payment.py` | Modelo `account.payment` usado pelo módulo. | is_pix, pix_e2e_id, pix_partner_key, pix_partner_key_type, pix_conta_origem_id, pix_conta_destino_id | _compute_is_pix, _compute_pix_flow_accounts |
| `account.payment.method` | `models/account_payment_method.py` | Modelo `account.payment.method` usado pelo módulo. | sem campos declarados no arquivo analisado | _get_payment_method_information, _get_payment_method_domain |
| `account.payment.register` | `models/account_payment_register.py` | Modelo `account.payment.register` usado pelo módulo. | is_pix | _compute_is_pix |
| `payment.provider` | `models/payment_provider.py` | Modelo `payment.provider` usado pelo módulo. | custom_mode, pix_key_type, pix_key, pix_merchant_name, pix_merchant_city | _check_pix_fields_before_enabling, _get_default_payment_method_codes, action_recompute_pending_msg, _pix_update_pending_msg, _pix_ensure_pending_msg_is_set, _pix_build_br_code, _pix_build_qr_code_base64 |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_account_payment_register_form_pix` | `account.payment.register` | `views/account_payment_register_views.xml` |
| `view_account_payment_form_pix` | `account.payment` | `views/account_payment_views.xml` |
| `view_account_payment_pix_tree` | `account.payment` | `views/account_payment_views.xml` |
| `view_account_payment_pix_search` | `account.payment` | `views/account_payment_views.xml` |
| `view_account_journal_form_pix` | `account.journal` | `views/account_payment_views.xml` |
| `payment_provider_form_pix` | `payment.provider` | `views/payment_provider_views.xml` |


### Menus

| XML ID | Nome | Parent | Ação | Arquivo |
|---|---|---|---|---|
| `menu_account_pix` | PIX | `account.menu_finance` | `` | `views/account_payment_views.xml` |
| `menu_account_pix_all` | Todos os Movimentos | `menu_account_pix` | `action_account_payment_pix` | `views/account_payment_views.xml` |
| `menu_account_pix_inbound` | Entradas (Recebimentos) | `menu_account_pix` | `action_account_payment_pix_inbound` | `views/account_payment_views.xml` |
| `menu_account_pix_outbound` | Saídas (Pagamentos) | `menu_account_pix` | `action_account_payment_pix_outbound` | `views/account_payment_views.xml` |


### Actions

| XML ID | Nome | Model | Arquivo |
|---|---|---|---|
| `action_account_payment_pix` | Movimentos PIX | `account.payment` | `views/account_payment_views.xml` |
| `action_account_payment_pix_inbound` | Entradas PIX | `account.payment` | `views/account_payment_views.xml` |
| `action_account_payment_pix_outbound` | Saídas PIX | `account.payment` | `views/account_payment_views.xml` |


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
