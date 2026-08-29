# Manual do Usuário — Central de Ajuda

## 1. Visão geral

Central de Ajuda integrada ao Odoo para importar documentação Markdown, exibir biblioteca, ajuda contextual, trilhas, checklists, feedback e métricas.

Este manual explica como usar o módulo no dia a dia, quais fluxos seguir e como diferenciar atividades, Agenda Geral, documentos, mídias e registros operacionais.

## 2. Quem usa

- Usuários finais que precisam de ajuda contextual
- Administradores que mantêm documentação
- Equipe técnica que audita cobertura

## 3. Conceitos importantes

| Conceito | O que significa | Exemplo |
| --- | --- | --- |
| Registro principal | Objeto central do processo | Imóvel, documento, caso, dossiê, comprovante |
| Atividade | Tarefa/cobrança individual no chatter | Pendência Operacional para João até 22/05 |
| Agenda Geral | Marco operacional com data, responsável e visibilidade | Vistoria em 24/05 às 09:00 |
| Documento | Arquivo formal com tipo, categoria, validade e revisão | Certidão, contrato, laudo |
| Histórico | Mensagens, alterações e decisões do processo | Chatter do registro |

## 4. Menus principais

| Menu XML ID | Arquivo | Observação |
| --- | --- | --- |
| menu_help_root | views/help_menu_views.xml |  name="Central de Ajuda" sequence="95" web_icon="common_help_center,static/descr |
| menu_help_home | views/help_menu_views.xml |  name="Início" parent="menu_help_root" action="action_help_article" sequence="1" |
| menu_help_library | views/help_menu_views.xml |  name="Biblioteca" parent="menu_help_root" sequence="10"/ |
| menu_help_all_articles | views/help_menu_views.xml |  name="Todos os Artigos" parent="menu_help_library" action="action_help_article" |
| menu_help_manual | views/help_menu_views.xml |  name="Manual do Usuário" parent="menu_help_library" action="action_help_article |
| menu_help_technical | views/help_menu_views.xml |  name="Documentação Técnica" parent="menu_help_library" action="action_help_arti |
| menu_help_troubleshooting | views/help_menu_views.xml |  name="Troubleshooting" parent="menu_help_library" action="action_help_article_t |
| menu_help_contextual_root | views/help_menu_views.xml |  name="Ajuda Contextual" parent="menu_help_root" sequence="20"/ |
| menu_help_context_candidates | views/help_menu_views.xml |  name="Mapa de Contextos" parent="menu_help_contextual_root" action="action_help |
| menu_help_contexts | views/help_menu_views.xml |  name="Contextos de Ajuda" parent="menu_help_contextual_root" action="action_hel |
| menu_help_tips | views/help_menu_views.xml |  name="Dicas por Tela" parent="menu_help_contextual_root" action="action_help_ti |
| menu_help_checklists | views/help_menu_views.xml |  name="Checklists" parent="menu_help_contextual_root" action="action_help_checkl |
| menu_help_learning_path_root | views/help_menu_views.xml |  name="Onboarding" parent="menu_help_root" sequence="30"/ |
| menu_help_learning_path | views/help_menu_views.xml |  name="Trilhas de Aprendizado" parent="menu_help_learning_path_root" action="act |
| menu_help_checklist_progress | views/help_menu_views.xml |  name="Progresso dos Checklists" parent="menu_help_learning_path_root" action="a |
| menu_help_intelligence_root | views/help_menu_views.xml |  name="Inteligência Operacional" parent="menu_help_root" sequence="40"/ |
| menu_help_suggestion_rule | views/help_menu_views.xml |  name="Regras Inteligentes" parent="menu_help_intelligence_root" action="action_ |
| menu_help_metrics | views/help_menu_views.xml |  name="Métricas de Uso" parent="menu_help_intelligence_root" action="action_help |
| menu_help_feedback_root | views/help_menu_views.xml |  name="Feedback" parent="menu_help_root" sequence="50"/ |
| menu_help_feedback | views/help_menu_views.xml |  name="Avaliações" parent="menu_help_feedback_root" action="action_help_feedback |
| menu_help_config_root | views/help_menu_views.xml |  name="Configuração" parent="menu_help_root" sequence="90"/ |
| menu_help_categories | views/help_menu_views.xml |  name="Categorias" parent="menu_help_config_root" action="action_help_category"  |
| menu_help_tags | views/help_menu_views.xml |  name="Tags" parent="menu_help_config_root" action="action_help_tag" sequence="2 |
| menu_help_doc_sources | views/help_menu_views.xml |  name="Fontes Markdown" parent="menu_help_config_root" action="action_help_doc_s |
| menu_help_import | views/help_menu_views.xml |  name="Importar Documentação" parent="menu_help_config_root" action="action_help |



## 5. Fluxos operacionais com exemplos

### Fluxo 1: Importar documentação

**Situação**  
Importar Markdown dos módulos instalados.

**Dados de exemplo**

| Campo | Exemplo |
| --- | --- |
| Opção | Varrer módulos instalados |
| Opção | Importar fontes ativas |
| Opção | Gerar mapa de contextos |



**Passo a passo**

1. Acesse o menu correspondente do módulo.
2. Clique em **Novo** ou abra o registro existente.
3. Preencha os campos obrigatórios e o responsável.
4. Anexe documentos/mídias quando o fluxo exigir.
5. Use **Agendar atividade** para tarefa simples.
6. Use **Agenda Geral** apenas para marcos operacionais relevantes.
7. Salve e valide o resultado nos menus de acompanhamento.

**Resultado esperado**

- Artigos criados/atualizados
- Contextos gerados a partir de HELP:ARTICLE
- Mapa indica telas pendentes

### Fluxo 2: Usar ajuda contextual

**Situação**  
Abrir o drawer de ajuda em uma tela.

**Dados de exemplo**

| Campo | Exemplo |
| --- | --- |
| Tela | document.document / form |
| Botão | Ajuda |



**Passo a passo**

1. Acesse o menu correspondente do módulo.
2. Clique em **Novo** ou abra o registro existente.
3. Preencha os campos obrigatórios e o responsável.
4. Anexe documentos/mídias quando o fluxo exigir.
5. Use **Agendar atividade** para tarefa simples.
6. Use **Agenda Geral** apenas para marcos operacionais relevantes.
7. Salve e valide o resultado nos menus de acompanhamento.

**Resultado esperado**

- Artigos curtos aparecem primeiro
- Documentos completos ficam na biblioteca

### Fluxo 3: Auditar cobertura

**Situação**  
Usar Mapa de Contextos para saber o que falta.

**Dados de exemplo**

| Campo | Exemplo |
| --- | --- |
| Situação | Sem contexto |
| Ação | Criar bloco em docs/08_AJUDA_CONTEXTUAL.md |



**Passo a passo**

1. Acesse o menu correspondente do módulo.
2. Clique em **Novo** ou abra o registro existente.
3. Preencha os campos obrigatórios e o responsável.
4. Anexe documentos/mídias quando o fluxo exigir.
5. Use **Agendar atividade** para tarefa simples.
6. Use **Agenda Geral** apenas para marcos operacionais relevantes.
7. Salve e valide o resultado nos menus de acompanhamento.

**Resultado esperado**

- Cobertura documentada por model/view/campo

## 6. Boas práticas

- Use nomes claros e padronizados nos registros.
- Evite criar duplicidades; atualize o registro original quando o prazo mudar.
- Prefira cancelar/arquivar em vez de excluir quando houver histórico.
- Preencha responsável principal antes de criar atividades ou agendas.
- Use a Central de Ajuda para validar o fluxo diretamente pela tela.

## 7. Erros comuns

| Erro | Como evitar |
| --- | --- |
| Criar agenda para toda tarefa simples | Use atividade para lembretes e Agenda Geral só para marcos críticos. |
| Registro não aparece para usuário correto | Revise responsáveis, equipe, participantes e regras de acesso. |
| Documento ou mídia no lugar errado | Use os campos específicos do fluxo em vez de anexos soltos no chatter. |
| Ajuda contextual vazia | Atualize `docs/08_AJUDA_CONTEXTUAL.md` e rode a importação da Central de Ajuda. |


## Referência dinâmica de campos, opções e filtros

A Central de Ajuda agora exibe, no drawer contextual, uma seção gerada em tempo real chamada **Campos, opções e filtros desta tela**.

Essa seção não substitui os artigos documentados em `docs/08_AJUDA_CONTEXTUAL.md`; ela complementa o fluxo com as opções realmente existentes no ambiente atual.

Ela pode listar:

| Item | Origem | Uso |
| --- | --- | --- |
| Campos obrigatórios | `fields_get()` do model atual | Ajuda o usuário a saber o mínimo para salvar o formulário |
| Opções fixas | Campos `selection` | Mostra todos os valores possíveis, como situação, prioridade, finalidade, tipo de conteúdo |
| Categorias, tipos e cadastros relacionados | Campos `many2one`/`many2many` relevantes | Mostra categorias, tipos, etapas, responsáveis, empresas, tags e outros cadastros ativos |
| Filtros e agrupamentos | Search views (`ir.ui.view` type `search`) | Mostra filtros de lista e opções de agrupamento disponíveis na tela |

### Como usar na documentação dos módulos

Nos artigos contextuais, documente o **fluxo de negócio** e deixe a Central complementar com opções dinâmicas. Exemplo:

```markdown
<!-- HELP:ARTICLE
code: document_core.document_document.form.create
module: document_core
model: document.document
view_type: form
category: Gestão Documental
context_name: Formulário de Documento
title: Como criar um novo documento
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como criar um novo documento

1. Preencha o nome do documento.
2. Escolha a categoria e o tipo documental.
3. Anexe o arquivo principal.
4. Informe responsável, validade ou revisão quando necessário.
5. Salve e acompanhe o documento nos menus de monitoramento.

Abaixo do artigo, a Central exibirá automaticamente as categorias, tipos, campos obrigatórios e filtros disponíveis no ambiente atual.
<!-- /HELP:ARTICLE -->
```

### Regra enterprise

- O artigo contextual deve explicar **quando e por que preencher**.
- A referência dinâmica deve mostrar **quais opções existem agora**.
- Categorias e tipos não devem ser escritos manualmente no artigo se forem cadastros configuráveis, porque podem mudar por empresa/cliente.
- Quando uma nova funcionalidade criar campo, seleção, categoria, filtro ou agrupamento, atualize o fluxo no `08_AJUDA_CONTEXTUAL.md` e rode a importação da Central de Ajuda.
