# Changelog Funcional — Property Document Portal

## 2026-05-21

### Adicionado

- Padronização enterprise de documentação.
- `docs/08_AJUDA_CONTEXTUAL.md` como fonte versionada dos artigos contextuais.
- Orientação para uso da seção dinâmica **Campos, opções e filtros desta tela**.
- Exemplos práticos por fluxo operacional.
- Guia de testes incluindo validação da Central de Ajuda.

### Alterado

- Documentos completos passam a ficar na Biblioteca da Central.
- Drawer contextual passa a priorizar artigos curtos, fluxos e exemplos.
- Listas fixas de opções configuráveis foram substituídas por orientação de uso e leitura dinâmica.

### Governança documental

Toda nova alteração funcional deve atualizar:

1. `01_DOCUMENTACAO_TECNICA.md` quando mudar model/campo/método.
2. `02_MANUAL_USUARIO.md` quando mudar fluxo.
3. `04_GUIA_TESTES.md` quando mudar comportamento testável.
4. `08_AJUDA_CONTEXTUAL.md` quando mudar tela/contexto/drawer.
