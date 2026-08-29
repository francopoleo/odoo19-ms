# Guia de Implementação - Central de Ajuda

## 1. Estratégia enterprise

A documentação deve ser mantida no repositório, dentro dos módulos. A Central de Ajuda importa esses arquivos e oferece visualização contextual dentro do Odoo.

## 2. Fluxo de atualização quando houver nova funcionalidade

1. Implementar a funcionalidade.
2. Atualizar `01_DOCUMENTACAO_TECNICA.md` se mudou model, campo, método ou regra.
3. Atualizar `02_MANUAL_USUARIO.md` se mudou fluxo de usuário.
4. Atualizar `04_GUIA_TESTES.md` com teste de regressão.
5. Atualizar `07_CHANGELOG_FUNCIONAL.md`.
6. Se afetou uma tela, atualizar `08_AJUDA_CONTEXTUAL.md`.
7. Rodar **Importar Documentação** no Odoo.
8. Conferir **Mapa de Contextos**.

## 3. Como criar ajuda contextual de forma versionada

Cada módulo deve ter:

```text
modulo/docs/08_AJUDA_CONTEXTUAL.md
```

Esse arquivo contém blocos curtos e práticos.

## 4. Como auditar se está tudo documentado

Use:

```text
Central de Ajuda > Ajuda Contextual > Mapa de Contextos
```

Audite principalmente:

- Sem contexto
- Contexto sem artigo
- Models principais sem form/list documentados
- Fluxos novos sem artigos contextuais

## 5. Critérios de aceite

Uma entrega funcional só deve ser aceita quando:

- Documentação técnica atualizada.
- Manual do usuário atualizado, se aplicável.
- Guia de testes atualizado.
- Changelog funcional atualizado.
- Contexto de ajuda criado para telas novas ou alteradas.
- Mapa de Contextos sem lacunas críticas para os módulos principais.
