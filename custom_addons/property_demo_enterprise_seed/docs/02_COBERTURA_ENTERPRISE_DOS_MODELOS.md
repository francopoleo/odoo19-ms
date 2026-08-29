# Cobertura enterprise da massa de testes

Este módulo foi ampliado depois da varredura dos módulos do projeto enviados no pacote `Archive(5).zip`.

A estratégia adotada não é criar um registro artificial para cada wizard/transient/view-model, porque isso poluiria a base e geraria registros sem valor funcional. A massa prioriza os modelos persistentes e os fluxos de negócio que precisam ser testados ponta a ponta.

## Famílias cobertas

| Família | Modelos principais exercitados |
|---|---|
| Imóveis e portfolio | `property.asset`, `property.complex`, `property.owner`, `property.tenant`, `property.media`, `property.media.category` |
| Contratos e financeiro | `property.contract`, `property.rent`, `property.rent.line`, `property.rent.payment`, `property.rent.adjustment`, `property.owner.repasse` |
| Corretores e comercial | `property.brokerage`, `property.broker`, `property.broker.assignment`, `property.commission`, `property.lead` |
| Compra/venda | `property.buyer`, `property.seller`, `property.investor`, `property.developer`, `property.acquisition` |
| Comprovantes e conciliação | `property.payment.proof`, `property.payment.proof.match`, `property.payment.authorized.payer` |
| Documentos e dossiês | `document.document`, `document.dossier.template`, `document.dossier.template.line`, `dossier.dossier`, `dossier.process` |
| Governança | `governance.case`, pendências, comunicações, vínculos com imóvel/contrato/mandato quando os módulos estiverem instalados |
| Aditivos | `property.contract.amendment`, `property.contract.amendment.change` |
| Vistoria e manutenção | `property.inspection`, `property.maintenance`, mídias vinculadas |
| OCR de contratos | `property.contract.history`, `property.contract.history.line`, `property.contract.ocr.template`, `property.contract.ocr.template.line` |
| Valuation | `property.valuation.source`, `property.price.m2.reference`, `property.market.comparable`, `property.valuation.run`, `property.valuation.algorithm/factor` quando disponíveis |
| Base comum | `common.tag`, `common.agenda.event`, `common.communication.base`, `common.config` |
| Central de ajuda | `help.category`, `help.tag`, `help.article`, `help.checklist.template`, `help.checklist.item`, `help.tip`, `help.context`, `help.suggestion.rule`, `help.learning.path`, `help.learning.step` |

## O que foi acrescentado na versão 19.0.1.0.4

- Corretores com CRECI e vínculo com imobiliárias.
- Mandatos de corretagem para locação/venda, inclusive alguns exclusivos.
- Comissões de corretor em estados diferentes: pendente, paga e cancelada.
- Proprietários com dados bancários e PIX.
- Repasses mensais ao proprietário com parcelas pagas, comissões e manutenções.
- Leads comerciais por imóvel com origem pública, portal, corretor e interna.
- Compradores, vendedores, investidores e incorporadoras.
- Oportunidades de aquisição com due diligence parcial e etapas de funil.
- Mídias de galeria pública e documentos técnicos internos.
- Templates OCR e históricos de contratos com linhas de extração.
- Registros básicos de central de ajuda, trilha, checklist e dicas.
- Agenda geral e comunicação rastreável.

## Modelos deliberadamente não populados em massa

Alguns modelos são dashboards, wizards, relatórios SQL ou assistentes transitórios. Eles são exercitados indiretamente quando os dados de negócio existem, mas não recebem registros persistidos em massa:

- dashboards (`property.dashboard`, `document.dashboard`, `governance.dashboard`, `property.receipts.dashboard`);
- wizards (`*.wizard`), exceto o próprio wizard do seed;
- modelos `_auto = False` ou visões analíticas;
- extensões `_inherit` de modelos do Odoo, que são preenchidas nos registros principais.

## Critério de segurança

Todos os novos registros usam o prefixo `DEMO-IMOB` em nomes, observações, códigos ou textos, permitindo limpeza pelo botão **Apagar massa DEMO-IMOB**.

O módulo continua com dependência dura apenas em `property_core`. As demais famílias são chamadas de forma condicional para evitar que uma falha temporária em `governance_documents`, `document_dossier`, `property_payment_proof`, OCR ou valuation impeça a instalação do seed.
