# Governance & Audit — Odoo 19

## Visão Geral

O módulo **Governance** é o núcleo de controle, auditoria e memória institucional do ERP.

Registra, acompanha e estrutura qualquer situação que exige rastreabilidade:

- compromissos assumidos
- comunicações críticas
- pendências e cobranças
- respostas e ausências de resposta (silêncio)
- disputas contratuais e documentais
- casos vinculados a imóveis e contratos

> **Se não está no governance, não existe institucionalmente.**

---

## Objetivo

Garantir que nenhuma informação crítica dependa de memória humana.

Tudo deve estar: registrado, rastreável, contextualizado, auditável.

---

## Entidade Principal — `governance.case`

Um caso representa qualquer situação que precisa ser controlada:

| Exemplo | Tipo sugerido |
|---|---|
| Documentação irregular do imóvel | Documental |
| Locatário inadimplente | Financeiro |
| Notificação extrajudicial | Jurídico |
| Vistoria não realizada | Operacional |
| Reclamação de vizinho | Reclamação |
| Renovação não regulamentada | Compliance |

---

## Campos Principais

| Campo | Descrição |
|---|---|
| Assunto | Título objetivo do caso |
| Referência | Código gerado automaticamente (GOV-XXXX) |
| Tipo | Jurídico / Documental / Compliance / Financeiro / Operacional / Reclamação |
| Prioridade | Baixo / Médio / Alto / Crítico |
| SLA (dias) | Calculado por prioridade: Crítico=3, Alto=7, Médio=15, Baixo=30 |
| Prazo de Resolução | Data de origem + SLA |
| Prazo para Resposta | Calculado por configuração global |
| Responsável | Usuário responsável pelo acompanhamento |
| Envolvidos | Parceiros relacionados ao caso |
| Tags | Classificação livre com cores |
| Imóveis Relacionados | Vínculos com `property.asset` |
| Contratos Relacionados | Vínculos com `property.contract` |
| Mandatos em Disputa | Vínculos com `property.broker.assignment` |

---

## SLA por Prioridade

| Prioridade | SLA | Uso típico |
|---|---|---|
| Crítico | 3 dias | Liminar judicial, embargo, urgência legal |
| Alto | 7 dias | Notificação formal, inadimplência grave |
| Médio | 15 dias | Pendência documental, reclamação |
| Baixo | 30 dias | Acompanhamento rotineiro |

---

## Ciclo de Vida do Caso

```
Planejado → E-mail Enviado → Aguardando Resposta → Resposta Parcial → Concluído → Encerrado
                                      ↓
                               Sem Resposta → Encerrado
```

| Etapa | Status | Significado |
|---|---|---|
| Planejado | planned | Caso criado, ainda não comunicado |
| E-mail Enviado | sent | Comunicação realizada |
| Aguardando Resposta | waiting | Aguardando retorno do envolvido |
| Resposta Parcial | partial | Resposta recebida, em análise |
| Sem Resposta | no_response | Silêncio registrado (auditável) |
| Concluído | done | Resolução confirmada |
| Encerrado | closed | Caso arquivado |

> **"Sem Resposta" é um estado válido e estratégico.** Registra o silêncio como fato.

---

## Follow-up Automático

Ao enviar um caso, o sistema cria atividades automáticas com base nas configurações globais:

- D+N → Follow-up leve
- D+N → Solicitar status
- D+N → Registrar silêncio

Os prazos são configuráveis em **Configurações → Common Base → Governança**.

---

## Integração com Imóveis e Contratos

A partir de qualquer **Imóvel** ou **Contrato**, é possível:

- Ver a contagem de casos vinculados (smart button)
- Abrir a lista de casos relacionados
- Criar um novo caso já vinculado ao registro

A vinculação é bidirecional — do caso você vê os imóveis/contratos, e do imóvel/contrato você vê os casos.

---

## Comunicação (Chatter)

Toda comunicação deve acontecer dentro do registro.

- histórico completo e imutável
- rastreabilidade com data e usuário
- vínculo automático ao caso
- prova institucional

> Nunca use e-mail externo sem registrar no caso correspondente.

---

## Classificação

Dois mecanismos complementares:

- **Tipo** (`case_type`): campo estruturado com valores fixos — garante consistência nos relatórios
- **Tags** (`common.tag`): classificação livre com cores — flexibilidade para casos específicos

---

## Segurança

| Perfil | Acesso |
|---|---|
| Usuário | Criar, editar e fechar casos |
| Manager (common_base) | Acesso completo incluindo configurações |

Casos são filtrados por empresa (`company_id`).

---

## Arquitetura

```
governance (este módulo)
└── governance.case          ← model principal
└── governance.stage         ← etapas do workflow

property_core (extensão)
└── governance.case          ← _inherit: adiciona asset_ids, contract_ids, assignment_ids
└── property.asset           ← _inherit: adiciona governance_case_count + smart button
└── property.contract        ← _inherit: adiciona governance_case_count + smart button
```

---

## Status do Módulo

- Estrutura base implementada
- Workflow com 7 etapas
- Tipo e prioridade com SLA automático
- Prazo de resolução calculado
- Integração bidirecional com property_core
- Smart buttons em Imóveis e Contratos
- Follow-up automático via cron
- Templates de e-mail (follow-up e aviso de silêncio)
- Tags com cores
- Filtros por tipo, prioridade, atraso
- Kanban com progresso por status

---

## Evolução Futura

- Dashboard de governança com indicadores
- Análise de risco por tipo/prioridade
- Detecção de padrões de silêncio
- Exportação para relatório de auditoria
- Integração com módulo financeiro