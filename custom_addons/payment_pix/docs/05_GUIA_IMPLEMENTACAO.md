# Guia de Implementação — Payment Provider: PIX (BACEN)

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Escopo

Implementar o módulo `payment_pix` na base Odoo garantindo configuração funcional, segurança, documentação e testes de aceite.

## 2. Dependências

payment_custom, account_payment

## 3. Ordem recomendada

1. Atualizar dependências.
2. Atualizar este módulo.
3. Atualizar `common_help_center` quando houver mudanças nos docs.
4. Importar documentação.
5. Gerar Mapa de Contextos.
6. Executar Guia de Testes.
7. Homologar com usuário funcional.

## 4. Comandos

```bash
cd /Users/franco/Dev/odoo/odoo19-ms
./odoo-bin -d ms-teste -u payment_pix,common_help_center --stop-after-init
```

## 5. Pós-instalação

- Revisar menus.
- Revisar grupos.
- Criar dados mestres.
- Importar docs na Central de Ajuda.
- Abrir drawer nas principais telas.
- Validar opções dinâmicas.

## 6. Critérios de aceite

| Critério | Aceite |
|---|---|
| Fluxos principais executam sem traceback | Obrigatório |
| Documentação contextual aparece no drawer | Obrigatório |
| Mapa de Contextos sem lacunas críticas | Obrigatório |
| Usuário operacional não acessa configuração indevida | Obrigatório |
| Markdown renderiza tabelas e listas | Obrigatório |

## 7. Rollback

Se a atualização falhar:

1. Restaurar backup do módulo anterior.
2. Rodar update das dependências.
3. Limpar assets se houver erro frontend.
4. Revisar logs e aplicar hotfix específico.
