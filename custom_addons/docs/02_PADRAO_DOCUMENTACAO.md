# Padrão de Documentação

Todo módulo deve manter a pasta `docs/` com a seguinte estrutura.

| Arquivo | Finalidade | Vai para biblioteca? | Vai para drawer contextual? |
| --- | --- | --- | --- |
| `00_INDICE.md` | Índice do módulo | Sim | Não |
| `01_DOCUMENTACAO_TECNICA.md` | Models, campos, métodos, views, segurança e integrações | Sim | Não, salvo artigos técnicos específicos |
| `02_MANUAL_USUARIO.md` | Uso funcional e fluxos do usuário | Sim | Não, salvo trechos contextualizados |
| `03_CONFIGURACAO_INICIAL.md` | Configuração pós-instalação | Sim | Não |
| `04_GUIA_TESTES.md` | Casos de teste e critérios de aceite | Sim | Não |
| `05_GUIA_IMPLEMENTACAO.md` | Implantação, atualização e rollback | Sim | Não |
| `06_TROUBLESHOOTING.md` | Erros comuns e soluções | Sim | Sim, se referenciado por contexto |
| `07_CHANGELOG_FUNCIONAL.md` | Histórico funcional de alterações | Sim | Não |
| `08_AJUDA_CONTEXTUAL.md` | Artigos curtos por tela/campo/fluxo | Sim | Sim |
| `99_LEGADO/` | Preservação de documentos antigos | Não obrigatório | Não |

## Bloco padrão de ajuda contextual

```markdown
<!-- HELP:ARTICLE
code: nome_modulo.model.form.fluxo
module: nome_modulo
model: model.name
view_type: form
category: Área Funcional
context_name: Nome do Contexto
title: Título do artigo
article_type: flow
scope: flow
audience: user
sequence: 10
-->
# Título do artigo

Texto curto, exemplo prático, resultado esperado e boas práticas.
<!-- /HELP:ARTICLE -->
```

## Regras de qualidade

| Situação | Documento obrigatório |
| --- | --- |
| Novo model/campo/método | `01_DOCUMENTACAO_TECNICA.md`, `04_GUIA_TESTES.md`, `07_CHANGELOG_FUNCIONAL.md` |
| Novo fluxo/tela | `02_MANUAL_USUARIO.md`, `08_AJUDA_CONTEXTUAL.md`, `04_GUIA_TESTES.md` |
| Nova configuração | `03_CONFIGURACAO_INICIAL.md`, `05_GUIA_IMPLEMENTACAO.md` |
| Novo erro conhecido | `06_TROUBLESHOOTING.md` |
