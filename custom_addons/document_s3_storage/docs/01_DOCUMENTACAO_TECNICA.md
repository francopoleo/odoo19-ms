# Documentação Técnica — Document S3 Storage

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo técnico

Integração de documentos com S3/DigitalOcean Spaces, mantendo metadados e segurança no Odoo.

## 2. Manifesto e dependências

| Item | Valor |
|---|---|
| Módulo técnico | `document_s3_storage` |
| Nome funcional | Document S3 Storage |
| Versão | `19.0.1.0.0` |
| Aplicação | `False` |
| Instalável | `True` |
| Dependências | `document_core`, `base`, `base_setup` |

### Arquivos declarados no manifesto

- `views/res_config_settings_views.xml`

## 3. Estrutura técnica do módulo

- `models/`: regras de negócio, campos e métodos Python.
- `views/`: menus, actions e views XML.
- `security/`: grupos, ACLs e regras de acesso.
- `data/`: dados iniciais, tipos, categorias e parâmetros.
- `docs/`: documentação versionada e fonte da Central de Ajuda.


## 4. Models e funções


### Model `ir.attachment`

- **Classe:** `IrAttachment`
- **Arquivo:** `models/ir_attachment.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `ir.attachment`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `storage_location` | `Selection` | Não | Não | Não | Opções fixas exibidas dinamicamente pela Central de Ajuda no drawer. |
| `s3_key` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_get_s3_config` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_s3_config_from_settings` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_is_s3_enabled` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_s3_client` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_get_s3_bucket` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_generate_s3_key` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_upload_to_s3` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_download_from_s3` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `create` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `write` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `unlink` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `read` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |

### Model `res.config.settings`

- **Classe:** `ResConfigSettings`
- **Arquivo:** `models/res_config_settings.py`
- **Descrição técnica:** não declarada no código; manter esta descrição atualizada quando o model evoluir.

- **Heranças:** `res.config.settings`


#### Campos documentados

| Campo | Tipo | Obrigatório | Store | Tracking | Uso esperado |
|---|---|---:|---:|---:|---|
| `s3_enabled` | `Boolean` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `s3_endpoint` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `s3_access_key` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `s3_secret_key` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `s3_bucket` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |
| `s3_region` | `Char` | Não | Não | Não | Campo operacional do fluxo; descreva no manual quando afetar usuário. |

#### Métodos e funções

| Método | Tipo inferido | O que documentar/testar |
|---|---|---|
| `_onchange_s3_enabled` | Onchange | Validar comportamento em formulário sem salvar e mensagens ao usuário. |
| `set_values` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `get_values` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `_test_s3_connection` | Método auxiliar | Documentar entrada, saída, regras e exceções quando afetar fluxo. |
| `action_test_s3_connection` | Ação de botão/fluxo | Validar permissões, mensagens, efeitos no registro, atividades e Agenda Geral. |


## 5. Resumo dos models

| Model | Arquivo | Objetivo técnico inferido | Campos principais | Métodos principais |
|---|---|---|---|---|
| `ir.attachment` | `models/ir_attachment.py` | Modelo `ir.attachment` usado pelo módulo. | storage_location, s3_key | _get_s3_config, _get_s3_config_from_settings, _is_s3_enabled, _get_s3_client, _get_s3_bucket, _generate_s3_key, _upload_to_s3, _download_from_s3 |
| `res.config.settings` | `models/res_config_settings.py` | Modelo `res.config.settings` usado pelo módulo. | s3_enabled, s3_endpoint, s3_access_key, s3_secret_key, s3_bucket, s3_region | _onchange_s3_enabled, set_values, get_values, _test_s3_connection, action_test_s3_connection |


## 6. Views, menus e actions

### Views

| XML ID | Model | Arquivo |
|---|---|---|
| `res_config_settings_view_form_s3_storage` | `res.config.settings` | `views/res_config_settings_views.xml` |


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
