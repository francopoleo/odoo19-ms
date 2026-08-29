# Visão Geral do Projeto

Este pacote reúne módulos Odoo para gestão imobiliária, governança, documentação, dossiês, conciliação, localizações brasileiras, integrações e Central de Ajuda.

## Padrões enterprise adotados

| Padrão | Aplicação |
| --- | --- |
| Documentação versionada | Cada módulo mantém documentação em `docs/*.md`. |
| Ajuda contextual | Cada módulo pode manter `docs/08_AJUDA_CONTEXTUAL.md` com blocos `HELP:ARTICLE`. |
| Biblioteca no Odoo | A Central de Ajuda importa os Markdown e renderiza artigos navegáveis. |
| Agenda Geral | Compromissos operacionais usam `common.agenda.event`, separado do calendário nativo. |
| Atividades | Tarefas e cobranças individuais usam `mail.activity`. |
| Auditoria | Registros críticos devem preferir cancelar/arquivar em vez de excluir. |
| Segurança | Acesso deve considerar responsáveis, equipes, participantes e grupos administrativos. |

## Módulos do pacote

| Módulo | Nome funcional | Resumo |
| --- | --- | --- |
| account_latam_provisional_post | Documento Fiscal Provisório LATAM/Brasil | Permite confirmar faturas LATAM/Brasil com número fiscal provisório e exige número real no pagamento. |
| common_base | Common Base | Camada comum do projeto, incluindo mixins, configuração, sequências, tags, comunicação comum, Agenda Geral e padrões compartilhados. |
| common_help_center | Central de Ajuda | Central de Ajuda integrada ao Odoo para importar documentação Markdown, exibir biblioteca, ajuda contextual, trilhas, checklists, feedback e métricas. |
| document_core | Document Core | Módulo central de gestão documental com documentos, categorias, tipos, arquivos, validação, revisão, vencimentos, localizações e ajuda contextual. |
| document_dossier | Document Dossier - Aggregator | Aggregator and coordinator for document templates across business processes |
| document_dossier_governance | Document Dossier - Governance Integration | Integration between document dossiérs and governance cases |
| document_dossier_property | Document Dossier - Property Integration | Integration between document dossiérs and property assets/contracts |
| document_s3_storage | Document S3 Storage | S3/DigitalOcean Spaces integration for document storage |
| governance | Governance & Audit | Módulo de governança operacional para abertura, triagem, acompanhamento e encerramento de casos, com prazos, pendências, comunicações e marcos na Agenda Geral. |
| governance_documents | Governance Documents | Integração entre governança e document_core sem depender de property_core |
| governance_property | Governance Property | Integração entre governança, imóveis, contratos e mandatos |
| l10n_br_partner_cep_identity | Brasil - Contatos: CEP e Documentos | Extensão leve para contatos brasileiros: busca de CEP, CPF, RG, CNPJ e campos fiscais. |
| payment_pix | Payment Provider: PIX (BACEN) | Pagamentos instantâneos via PIX conforme especificação do Banco Central do Brasil. |
| property_contract_amendment_enterprise | Contratos e Aditivos Imobiliários Empresarial | Gestão empresarial de contratos, aditivos, seleção controlada, parcelas afetadas, recálculo financeiro, documentos e auditoria para Imóveis |
| property_contract_history | Histórico de Contratos com OCR | Upload e extração OCR de contratos históricos (aluguel, venda, financiamento) com sincronização para imóveis. |
| property_contract_ocr_template | Property Contract OCR Templates | Templates de OCR/regex para extrair dados de contratos imobiliários |
| property_core | Property Core | Módulo principal imobiliário para cadastro de imóveis, documentos, galeria, mídias, vistorias, manutenções, contratos, parcelas e integração com Agenda Geral. |
| property_document_portal | Property Document Portal | Portal access to property documents for tenants, brokers, and stakeholders |
| property_payment_proof | Conciliação Inteligente de Comprovantes de Aluguel | OCR/extração de comprovantes PIX/banco e conciliação inteligente com parcelas de aluguel. |
| property_valuation_engine | Property Valuation Engine | Motor enterprise de estimativa de valor imobiliário integrado ao property_core |



## Fluxo de manutenção da documentação

1. Alterar código e views do módulo.
2. Atualizar os documentos do próprio módulo em `docs/`.
3. Se a mudança afetar uma tela, atualizar `docs/08_AJUDA_CONTEXTUAL.md`.
4. Atualizar `07_CHANGELOG_FUNCIONAL.md`.
5. Instalar/atualizar o módulo no Odoo.
6. Na Central de Ajuda, executar **Importar Documentação**.
7. Validar o **Mapa de Contextos** para localizar telas sem ajuda.
