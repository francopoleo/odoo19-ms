# Documentação Técnica — Brasil - Contatos: CEP e Documentos

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Extensão de contatos para padrões brasileiros: CEP, CPF, RG, CNPJ e campos fiscais.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `l10n_br_partner_cep_identity` |
| Nome funcional | Brasil - Contatos: CEP e Documentos |
| Versão | `19.0.1.0.0` |
| Aplicação | `False` |
| Instalável | `True` |
| Dependências | `base`, `contacts` |

### Arquivos declarados no manifesto

- `views/res_partner_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `res.partner`

- **Classe:** `ResPartner`
- **Arquivo:** `models/res_partner.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `res.partner`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `br_person_type` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `br_cpf` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_cnpj` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_rg` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_rg_issuer` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_rg_issuer_state_id` | `Many2one` | Não | Não | Não | Relacionamento usado para vínculo, contexto ou configuração dinâmica. |
| `br_rg_issue_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_birth_date` | `Date` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_mother_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_legal_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_trade_name` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_state_tax_number` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_municipal_tax_number` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_district` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_ibge_code` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_zip_source` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `br_zip_lookup_date` | `Datetime` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `br_zip_lookup_status` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `br_zip_lookup_message` | `Text` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_compute_br_person_type` | Compute | Validar dependências, store, atualização automática e performance. |
| `_inverse_br_person_type` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_only_digits` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_format_cpf` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_format_cnpj` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_format_zip` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_is_valid_cpf` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_is_valid_cnpj` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_check_br_documents` | Validação/constraint | Testar valor válido, valor inválido e mensagem funcional. |
| `_onchange_br_cpf` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `_onchange_br_cnpj` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_prepare_br_document_vals` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_onchange_zip_lookup_br` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `action_lookup_zip_br` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |
| `_notify_zip_lookup` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_lookup_zip_values` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_http_get_json` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_request_brasilapi_cep` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_request_viacep` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_apply_zip_values` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `res.partner` | `models/res_partner.py` | Modelo `res.partner` usado pelo módulo. | br_person_type, br_cpf, br_cnpj, br_rg, br_rg_issuer, br_rg_issuer_state_id, br_rg_issue_date, br_birth_date | _compute_br_person_type, _inverse_br_person_type, _only_digits, _format_cpf, _format_cnpj, _format_zip, _is_valid_cpf, _is_valid_cnpj |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `res_partner_view_form_inherit_br_cep_identity` | `res.partner` | `views/res_partner_views.xml` |
| `res_partner_view_tree_inherit_br_cep_identity` | `res.partner` | `views/res_partner_views.xml` |
| `res_partner_view_search_inherit_br_cep_identity` | `res.partner` | `views/res_partner_views.xml` |


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
