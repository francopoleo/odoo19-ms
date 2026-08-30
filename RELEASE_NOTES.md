# Odoo 19 MS — Release v19.0.2

Data: 2026-08-30

## Destaques

- Base enterprise de configuração operacional, com tipos de caso, etapas,
  prioridades, canais, classificações, templates de pendências, dossiês e
  categorias documentais.
- Seed demo separado da instalação, executado explicitamente pelo backend,
  com dados identificados por `DEMO-IMOB`.
- Correção do vínculo dos usuários portal demo aos parceiros responsáveis por
  contratos e imóveis.
- Carga do catálogo demo atômica, sem deixar registros parciais em caso de
  falha.
- Correções de visibilidade e acesso do portal para contratos, parcelas,
  documentos, imóveis e dossiês.
- Melhorias nos cards da página inicial do portal e na kanban de contratos,
  incluindo cores semânticas para rascunho, ativo, encerrado e inadimplência.
- Correções de instalação, referências XML, integrações imobiliárias,
  governança, documentos, pagamentos PIX e histórico contratual.
- Script de instalação/reset da base de desenvolvimento atualizado para
  instalar a configuração enterprise sem carregar massa demo.

## Validação

- Reset completo da base `ms` executado com sucesso.
- 90 módulos carregados sem erro fatal.
- Base pós-reset sem imóveis, contratos, documentos, casos, dossiês ou
  usuários portal demo.
- `enterprise_configuration_seed` instalado.
- Seed demo e seed de portfólio não instalados automaticamente.
