# Arquitetura Geral

## Camadas

| Camada | Responsabilidade | Módulos principais |
| --- | --- | --- |
| Base comum | Mixins, configuração, comunicação, Agenda Geral | `common_base` |
| Ajuda e aprendizagem | Biblioteca, contexto, onboarding e métricas | `common_help_center` |
| Imobiliário | Imóveis, contratos, parcelas, mídias, vistorias e manutenções | `property_core` e auxiliares |
| Documental | Documentos, categorias, tipos, dossiês, storage | `document_core`, `document_dossier`, `document_s3_storage` |
| Governança | Casos, pendências, comunicação e SLA | `governance` e integradores |
| Financeiro/localização | Comprovantes, PIX, Brasil/LATAM | `property_payment_proof`, `payment_pix`, `l10n_br_*`, `account_latam_*` |

## Agenda, atividades e calendário

| Recurso | Model | Uso correto |
| --- | --- | --- |
| Atividade | `mail.activity` | Tarefa individual, lembrete, cobrança e pendência simples. |
| Agenda Geral | `common.agenda.event` | Marco operacional, vistoria, manutenção, prazo formal e compromisso de governança/documento. |
| Calendário nativo | `calendar.event` | Reuniões pessoais/nativas do Odoo. |

## Documentação e ajuda contextual

A documentação oficial fica nos arquivos Markdown dos módulos. A Central de Ajuda importa esses arquivos e cria artigos no Odoo. Contextos de ajuda são declarados em `docs/08_AJUDA_CONTEXTUAL.md`.
