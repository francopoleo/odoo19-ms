# Changelog Funcional — Central de Ajuda

## 2026-05-21

### Adicionado

- Documentação enterprise padronizada com oito arquivos principais.
- Arquivo `08_AJUDA_CONTEXTUAL.md` para artigos de contexto importáveis pela Central de Ajuda.
- Exemplos práticos e fluxos operacionais documentados.

### Alterado

- Documentação anterior preservada em `docs/99_LEGADO/`.
- Manual e documentação técnica reorganizados por padrão único.

### Corrigido

- Conteúdo de tabelas documentado para renderização correta no frontend da Central de Ajuda.

### Observação

Sempre que este módulo mudar, atualizar documentação técnica, manual, guia de testes e ajuda contextual quando aplicável.

## 2026-05-21 — v16

### Corrigido

- A importação de `docs/08_AJUDA_CONTEXTUAL.md` agora ignora arquivos sem blocos `HELP:ARTICLE` e sem metadados contextuais.
- Evita criação de artigos contextuais globais sem `code`, que causava erro de banco em `help.article.code`.
- Mantém a regra enterprise: ajuda contextual deve vir de blocos versionados e identificados por código único.


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

## 2026-05-21 — v21 Mapa completo de views

### Corrigido

- O Mapa de Contextos passou a varrer actions e menus por todos os modos de visualização declarados, não apenas o primeiro modo.
- O tipo técnico `tree` agora é normalizado para `list`.
- A cobertura agora considera `form`, `list`, `kanban`, `calendar`, `search`, `pivot`, `graph`, `activity`, `gantt`, `cohort`, `map` e `dashboard`.
- A documentação de Dossiês foi alinhada ao model real `dossier.dossier`.

### Resultado prático

Telas como Dossiês, que normalmente abrem em `kanban` mas também possuem lista e formulário, passam a aparecer corretamente no mapa de cobertura e podem receber ajuda contextual para cada modo de tela.
