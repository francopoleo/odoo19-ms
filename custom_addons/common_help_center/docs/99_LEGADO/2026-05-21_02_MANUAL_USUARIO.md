# Manual do Usuário - Central de Ajuda

## 1. Para que serve

A Central de Ajuda concentra manuais, documentação técnica, guias de configuração, testes e ajuda contextual dos módulos do sistema.

## 2. Como usar o botão Ajuda

1. Abra uma tela do sistema, por exemplo **Documentos**.
2. Clique em **Ajuda** no topo.
3. O painel lateral mostra o contexto atual, como `document.document / form`.
4. Leia os artigos do contexto.
5. Use **Abrir tela completa** se precisar editar ou administrar o artigo.

## 3. Diferença entre Biblioteca e Ajuda Contextual

| Área | Uso |
|---|---|
| Biblioteca | Documentos completos, manuais e documentação técnica |
| Ajuda Contextual | Artigos curtos ligados à tela atual |
| Mapa de Contextos | Lista telas detectadas e o que ainda falta documentar |

## 4. Como importar documentação

1. Acesse **Central de Ajuda > Configuração > Importar Documentação**.
2. Marque **Varrer módulos instalados**.
3. Marque **Importar fontes ativas**.
4. Marque **Gerar mapa de contextos**.
5. Clique em **Executar**.

Você pode rodar esse processo várias vezes. O sistema não deve duplicar os artigos porque usa códigos técnicos.

## 5. Como saber se está tudo documentado

1. Acesse **Central de Ajuda > Ajuda Contextual > Mapa de Contextos**.
2. Filtre por **Sem contexto**.
3. Filtre por **Contexto sem artigo**.
4. Para cada item, clique em **Abrir/Criar Contexto**.
5. Vincule artigo existente ou crie um bloco em `docs/08_AJUDA_CONTEXTUAL.md` no módulo correspondente.

## 6. Exemplo prático

### Situação

A tela `document.document / form` não mostra ajuda sobre criação de documento.

### Correção recomendada

No módulo `document_core`, criar ou atualizar:

```text
document_core/docs/08_AJUDA_CONTEXTUAL.md
```

Com um bloco:

```markdown
<!-- HELP:ARTICLE
code: document_core.document_document.form.create
module: document_core
model: document.document
view_type: form
category: Documentos
context_name: Formulário de Documento
title: Como criar um novo documento
article_type: flow
scope: flow
audience: user
sequence: 10
-->
# Como criar um novo documento

1. Acesse Documentos > Todos os Documentos.
2. Clique em Novo.
3. Preencha nome, categoria, tipo e responsável.
4. Anexe o arquivo principal.
5. Salve e acompanhe pendências, validação e vencimento.
<!-- /HELP:ARTICLE -->
```

Depois rode **Importar Documentação**.

## 7. Boas práticas

- Não coloque manuais completos no drawer contextual.
- Use o drawer para orientação curta e prática.
- Use a Biblioteca para documentos longos.
- Atualize a documentação junto com a funcionalidade.
- Use o Mapa de Contextos para auditar lacunas.
