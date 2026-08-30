# Análise dos módulos e estratégia de massa de testes

## Módulos analisados

Foram identificados módulos de base comum, central de ajuda, documentos, dossiês, governança, imóveis, contratos, OCR, comprovantes de pagamento e valuation:

- `account_latam_provisional_post`
- `common_base`
- `common_help_center`
- `document_core`
- `document_dossier`
- `document_dossier_governance`
- `document_dossier_property`
- `document_s3_storage`
- `governance`
- `governance_documents`
- `governance_property`
- `l10n_br_partner_cep_identity`
- `payment_pix`
- `property_contract_amendment_enterprise`
- `property_contract_history`
- `property_contract_ocr_template`
- `property_core`
- `property_document_portal`
- `property_payment_proof`
- `property_valuation_engine`

## O que já existia

- `property_core` já traz uma base grande de imóveis em XML.
- `document_core` já traz categorias e tipos documentais suficientes para o ramo imobiliário.
- `document_dossier` já traz processos base de dossiê para governança, compra, venda, locação, vistoria e genérico.

## Lacunas identificadas

A base enviada ainda não tinha uma carga integrada de homologação para:

- contratos ativos;
- contratos encerrados/inativos;
- contratos inadimplentes;
- parcelas abertas, pagas, parciais e atrasadas;
- recebimentos confirmados;
- comprovantes conciliados;
- dossiês aplicados a contratos com documentos completos e pendentes;
- casos de governança vinculados a contratos/imóveis;
- aditivos e impactos contratuais;
- vistorias, manutenções e dados de valuation.

## Decisão de arquitetura

A estratégia adotada foi criar um módulo separado chamado `property_demo_enterprise_seed`.

Motivos:

1. Evita poluir módulos produtivos com dados fictícios.
2. Permite instalar/desinstalar a massa de teste de forma controlada.
3. Usa o sufixo `(DEMO-IMOB)` nos nomes para facilitar a leitura; a limpeza mantém compatibilidade com massas antigas que usavam prefixo.
4. Usa XML apenas para cadastros estáveis, como templates de dossiê.
5. Usa Python para dados relacionais e volumosos, onde CSV/XML ficariam frágeis.

## Por que não usar apenas importação CSV do Odoo

A importação do Odoo funciona bem para cadastros simples. Para esse cenário, ela é frágil porque:

- contratos geram parcelas por regra;
- parcelas têm composição, status, vencimentos e recebimentos;
- comprovantes precisam linkar contrato, parcela e recebimento;
- dossiês aplicam templates e criam documentos esperados;
- governança cruza participantes, casos, imóveis e contratos;
- aditivos usam seleção controlada de campos e impactos.

Por isso o melhor caminho é manter a massa de teste como módulo técnico instalável, com wizard para volume e reconstrução.
