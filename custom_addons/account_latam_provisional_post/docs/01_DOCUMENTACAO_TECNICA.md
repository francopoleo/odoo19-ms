# Documentação Técnica — Documento Fiscal Provisório LATAM/Brasil

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Permite confirmação de documentos fiscais com número provisório e substituição posterior pelo número real.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `account_latam_provisional_post` |
| Nome funcional | Documento Fiscal Provisório LATAM/Brasil |
| Versão | `19.0.1.0.0` |
| Aplicação | `False` |
| Instalável | `True` |
| Dependências | `account`, `l10n_latam_invoice_document` |

### Arquivos declarados no manifesto

- `views/account_move_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `account.move`

- **Classe:** `AccountMove`
- **Arquivo:** `models/account_move.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `account.move`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `l10n_latam_is_provisional_document` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_l10n_latam_is_provisional_document` | Compute | Validar dependências, store, atualização automática e performance. |
| `_post` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_check_l10n_latam_documents` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_onchange_name_warning` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_check_real_fiscal_number_before_payment` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |

### Model `account.payment`

- **Classe:** `AccountPayment`
- **Arquivo:** `models/account_payment.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `account.payment`


#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `action_post` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `account.move` | `models/account_move.py` | Modelo `account.move` usado pelo módulo. | l10n_latam_is_provisional_document | _compute_l10n_latam_is_provisional_document, _post, _check_l10n_latam_documents, _onchange_name_warning, _check_real_fiscal_number_before_payment |
| `account.payment` | `models/account_payment.py` | Modelo `account.payment` usado pelo módulo. | sem campos declarados no arquivo analisado | action_post |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `view_move_form_latam_provisional_document` | `account.move` | `views/account_move_views.xml` |


### Menus

_Sem menus próprios identificados em views/._


### Actions

_Sem actions próprias identificadas._


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
