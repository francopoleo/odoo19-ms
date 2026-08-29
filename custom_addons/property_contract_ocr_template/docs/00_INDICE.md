# Índice — Property Contract OCR Templates

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## Objetivo do módulo

Configuração de templates, regex e regras de extração para diferentes modelos de contratos imobiliários.

## Área funcional

**Templates OCR de Contrato**

## Público-alvo

- Técnico OCR
- Administrador funcional
- Operador de implantação

## Documentos disponíveis

| Arquivo | Uso |
|---|---|
| `01_DOCUMENTACAO_TECNICA.md` | Models, campos, métodos, menus, integrações e regras técnicas. |
| `02_MANUAL_USUARIO.md` | Fluxos com exemplos e orientação operacional. |
| `03_CONFIGURACAO_INICIAL.md` | Configuração funcional e técnica após instalação. |
| `04_GUIA_TESTES.md` | Roteiros de teste funcional, segurança e regressão. |
| `05_GUIA_IMPLEMENTACAO.md` | Implantação, ordem de atualização, aceite e rollback. |
| `06_TROUBLESHOOTING.md` | Problemas comuns, causa provável e solução. |
| `07_CHANGELOG_FUNCIONAL.md` | Histórico funcional das mudanças. |
| `08_AJUDA_CONTEXTUAL.md` | Fonte versionada dos artigos curtos usados no drawer da Central de Ajuda. |

## Como manter atualizado

1. Ao alterar tela, model, campo, menu ou fluxo, atualize os arquivos afetados.
2. Se a alteração impactar o usuário, atualize `02_MANUAL_USUARIO.md` e `08_AJUDA_CONTEXTUAL.md`.
3. Se a alteração impactar configuração, atualize `03_CONFIGURACAO_INICIAL.md`.
4. Se a alteração impactar teste, atualize `04_GUIA_TESTES.md`.
5. Rode a importação em **Central de Ajuda > Configuração > Importar Documentação**.
6. Verifique **Central de Ajuda > Ajuda Contextual > Mapa de Contextos** para saber se há telas sem documentação.
