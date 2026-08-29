# Padrão de Documentação Dinâmica e Central de Ajuda

## Objetivo

Definir como todos os módulos Odoo devem manter documentação versionada, importável e contextual.

## Regras principais

1. Arquivos `docs/*.md` são a fonte oficial versionada.
2. `docs/08_AJUDA_CONTEXTUAL.md` alimenta o drawer contextual com blocos `HELP:ARTICLE`.
3. O campo `code` de cada artigo é obrigatório e deve ser único.
4. A Central de Ajuda pode ser reimportada sempre; ela atualiza pelo `code` e não deve duplicar.
5. Manuais completos ficam na Biblioteca; artigos curtos aparecem no drawer.
6. Opções configuráveis não devem ser listadas manualmente; a Central mostra dinamicamente.

## Estrutura obrigatória por módulo

```text
docs/
├── 00_INDICE.md
├── 01_DOCUMENTACAO_TECNICA.md
├── 02_MANUAL_USUARIO.md
├── 03_CONFIGURACAO_INICIAL.md
├── 04_GUIA_TESTES.md
├── 05_GUIA_IMPLEMENTACAO.md
├── 06_TROUBLESHOOTING.md
├── 07_CHANGELOG_FUNCIONAL.md
├── 08_AJUDA_CONTEXTUAL.md
└── 99_LEGADO/
```

## Bloco HELP:ARTICLE

```markdown
<!-- HELP:ARTICLE
code: modulo.model.form.fluxo
module: modulo
model: nome.model
view_type: form
category: Área Funcional
context_name: Formulário de Exemplo
title: Como executar o fluxo
article_type: flow
scope: flow
audience: user
sequence: 10
show_in_context: true
-->
# Como executar o fluxo

Explique o passo a passo, exemplos e boas práticas. Não liste opções configuráveis; a Central mostra dinamicamente.
<!-- /HELP:ARTICLE -->
```

## Como saber se está tudo documentado

1. Atualize módulos e docs.
2. Rode **Central de Ajuda > Configuração > Importar Documentação**.
3. Marque **Gerar mapa de contextos**.
4. Abra **Central de Ajuda > Ajuda Contextual > Mapa de Contextos**.
5. Corrija telas como **Sem contexto** ou **Contexto sem artigo**.

## Checklist antes de entregar nova funcionalidade

- [ ] Documentação técnica atualizada.
- [ ] Manual do usuário atualizado, se mudou fluxo.
- [ ] Guia de testes atualizado.
- [ ] Ajuda contextual criada ou ajustada.
- [ ] Importação testada sem duplicidade.
- [ ] Drawer mostra artigo certo e opções dinâmicas.
