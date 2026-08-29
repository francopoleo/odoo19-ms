# Guia Prático de Governança e Auditoria

> Exemplos reais de uso do módulo `governance` integrado ao `property_core`.

---

## Sumário

1. [Arquitetura: o que vai onde?](#1-arquitetura-o-que-vai-onde)
2. [Ação de Despejo (Eviction)](#2-ação-de-despejo)
3. [Inadimplência com Escalada Jurídica](#3-inadimplência-com-escalada-jurídica)
4. [Disputa de Comissão de Corretor](#4-disputa-de-comissão-de-corretor)
5. [Notificação Extrajudicial por Danos ao Imóvel](#5-notificação-extrajudicial-por-danos)
6. [Auditoria de Documentos Vencidos](#6-auditoria-de-documentos-vencidos)
7. [Compliance: IPTU Não Pago pelo Locatário](#7-compliance-iptu-não-pago)
8. [Renovação Contestada de Contrato Comercial](#8-renovação-contestada-contrato-comercial)
9. [Referência: Tipos, Prioridades e SLA](#9-referência-tipos-prioridades-e-sla)
10. [Fluxo de Etapas](#10-fluxo-de-etapas)

---

## 1. Arquitetura: o que vai onde?

### Regra geral

| Situação | Módulo | Raciocínio |
|---|---|---|
| Contrato assinado, ativo, parcelas geradas | `property_core` | Operação normal |
| Reajuste de aluguel (IGP-M, IPCA) | `property_core` | Fluxo automatizado |
| Vistoria de entrada/saída | `property_core` | Operação técnica |
| Manutenção agendada | `property_core` | Operação técnica |
| **Locatário inadimplente há 30+ dias** | `governance` | Passou do operacional |
| **Notificação formal / carta de cobrança** | `governance` | Comunicação com SLA |
| **Ação de despejo** | `governance` | Processo jurídico |
| **Disputa de comissão** | `governance` | Conflito entre partes |
| **Dano ao imóvel com contestação** | `governance` | Conflito com evidências |
| **Auditoria de conformidade** | `governance` | Controle interno |
| **IPTU ou condomínio em nome errado** | `governance` | Compliance documental |

### Por que não criar um modelo `property.legal_case`?

O `governance.case` já fornece:
- Fluxo com etapas configuráveis (Kanban)
- SLA por prioridade com alertas automáticos
- Rastreamento de e-mails enviados/respondidos
- Atividades de follow-up
- Vínculo nativo com contratos, imóveis e mandatos
- Histórico de mensagens (chatter)
- Tags e tipos configuráveis

Criar um modelo separado seria duplicar tudo isso. O correto é **usar `governance.case` com tipo "Jurídico"** e vincular ao contrato.

---

## 2. Ação de Despejo

### Contexto

O locatário do imóvel AP-204 está inadimplente há 3 meses. Notificações foram enviadas sem sucesso. O proprietário decidiu iniciar ação judicial.

### Passo a passo no sistema

**1. No contrato (property_core):**
- Abra o contrato `CTR-0042`
- Status já foi para `Inadimplente` automaticamente pelo cron
- Clique em **"Ver Casos de Governança"** → **"Novo Caso"**

**2. Criação do caso (governance):**

```
Assunto:       Ação de Despejo – AP-204 – João da Silva
Tipo:          Jurídico
Prioridade:    Crítico (3)
Responsável:   [advogado responsável]
Envolvidos:    [locatário] [fiador] [proprietário]
Contratos:     CTR-0042
Imóveis:       AP-204

Descrição:
Locatário inadimplente desde 01/01/2026 (3 meses).
Tentativas de contato: 3 ligações, 2 e-mails, 1 notificação extrajudicial.
Advogado contratado: Escritório Souza & Lima.
Número do processo: 1001234-00.2026.8.26.0000
Vara: 2ª Vara Cível – Comarca de Barueri
```

**3. Documentos anexados ao caso:**
- Notificação extrajudicial (PDF) — `property.document` vinculado ao `case_id`
- Extrato de inadimplência (relatório de parcelas em atraso)
- Comprovante de tentativas de contato

**4. Fluxo do caso:**

```
Planejado
  ↓ [Enviar E-mail] → notifica locatário/fiador formalmente
E-mail Enviado
  ↓ [Aguardar] → prazo SLA 5 dias (Crítico)
Aguardando Resposta
  ↓ [Sem Resposta] → SLA vencido, nenhum contato
Sem Resposta          ← cron detecta e cria atividade de urgência
  ↓ [Encerrar]
Encerrado             ← processo judicial em andamento externo
```

> **Nota:** A ação judicial em si corre fora do ERP (sistema judicial). O `governance.case` rastreia a comunicação, SLA de respostas e documentação. Atualize o caso com notas de audiências e intimações no chatter.

**5. Encerramento:**
Quando despejo concluído e imóvel desocupado:
- Feche o caso de governança (status `closed`)
- No contrato: `action_close()` → status `Encerrado`
- Agende vistoria de saída em `property.inspection` (tipo `exit`)
- Atualize status do imóvel para `available` ou `maintenance`

---

## 3. Inadimplência com Escalada Jurídica

### Contexto

Locatário pagou parcialmente 2 meses. O cron já marcou o contrato como `Inadimplente`. A régua de cobranças enviou notificações D+1, D+5, D+15. Sem resposta.

### Fluxo recomendado

```
[property.rent]  parcelas com status "late"
      ↓
[property.contract]  status = "defaulting"  (automático via cron)
      ↓
[governance.case]  Tipo: Financeiro → Jurídico
```

**Criação do caso Financeiro (cobrança):**

```
Assunto:    Cobrança Extrajudicial – CTR-0055 – Maria Santos
Tipo:       Financeiro
Prioridade: Alto (2)
Contratos:  CTR-0055

Descrição:
Parcelas em aberto: Fev/2026 (R$ 2.800), Mar/2026 (R$ 2.800) = R$ 5.600
Aceitar acordo: sim, com multa de 10%
Prazo para regularização: 10 dias úteis
```

Se o acordo não for feito, crie um **segundo caso vinculado**:

```
Assunto:    Ação de Cobrança Judicial – CTR-0055
Tipo:       Jurídico
Prioridade: Crítico
Imóveis:    AP-108
Contratos:  CTR-0055
Tags:       cobrança-judicial, 2026
```

Nos dois casos, os documentos (cartas, boletos, extratos) ficam em `property.document` com `case_id` preenchido — aparecem automaticamente na aba "Documentos" do caso.

---

## 4. Disputa de Comissão de Corretor

### Contexto

O corretor alega que faz jus à comissão de venda do imóvel CAS-12, mas o proprietário contesta que o mandato já havia expirado.

### Passo a passo

**1. A partir do mandato (broker.assignment):**
- Abra o mandato `MND-0008`
- Clique em **"Abrir Disputa"** → cria `governance.case` automaticamente com tipo "Jurídico" e link ao mandato

**2. O caso criado:**

```
Assunto:    Disputa de Comissão – Corretor Pedro Alves – CAS-12
Tipo:       Jurídico
Prioridade: Médio (1)
Mandatos:   MND-0008
Imóveis:    CAS-12
Envolvidos: [corretor] [proprietário]
```

**3. Evidências:**
- Anexe o mandato original (data de vigência)
- Anexe a proposta de compra com data
- Adicione nota no chatter com linha do tempo dos fatos

**4. Resolução:**
- Acordo parcial → etapa `Resposta Parcial` → depois `Concluído`
- Sem acordo → etapa `Sem Resposta` → encaminhar para arbitragem externa → `Encerrado`

---

## 5. Notificação Extrajudicial por Danos ao Imóvel

### Contexto

Vistoria de saída (exit inspection) revelou danos ao imóvel além do desgaste normal. Locatário contesta o laudo.

### Fluxo

```
[property.inspection]  tipo: exit, condição: poor
      ↓  gera relatório com fotos
[governance.case]  Tipo: Jurídico ou Reclamação
```

**Caso:**

```
Assunto:    Ressarcimento por Danos – AP-301 – Saída Carlos Ferreira
Tipo:       Reclamação → (se não resolvida) → Jurídico
Prioridade: Médio
Imóveis:    AP-301
Contratos:  CTR-0067

Descrição:
Laudo de vistoria de saída (VIS-0023) aponta:
- Pintura danificada em 3 cômodos (R$ 1.200)
- Porta do banheiro quebrada (R$ 350)
- Piso arranhado na sala (R$ 800)
Total reclamado: R$ 2.350

Locatário contesta pintura. Concorda com porta e piso (R$ 1.150).
```

**Documentos vinculados:**
- Laudo de vistoria de entrada (VIS-0001) com fotos
- Laudo de vistoria de saída (VIS-0023) com fotos
- Orçamentos de reparo (3 fornecedores)

**Resolução:**
- Acordo alcançado: `Concluído`
- Retenção do depósito caução via `property.owner.repasse` (ajuste manual)
- Se depósito insuficiente: seguir para cobrança judicial (novo caso tipo "Jurídico")

---

## 6. Auditoria de Documentos Vencidos

### Contexto

O gestor quer auditar periodicamente se todos os imóveis têm AVCB, habite-se e laudos técnicos vigentes.

### Como o sistema suporta isso

**Automático (property_core):**
- Cron `Imóveis: Alertar Documentos a Vencer` roda diariamente
- Documentos com `expiry_date` dentro de `alert_days` geram atividade "Vencimento de Documento"
- Documentos vencidos ficam com status `expired` (badge vermelho)

**Auditoria formal (governance):**

```
Assunto:    Auditoria Documental Semestral – Carteira Comercial 1S/2026
Tipo:       Documental
Prioridade: Médio
Tags:       auditoria-2026, comercial

Descrição:
Escopo: 12 imóveis comerciais
Checklist:
☐ AVCB vigente
☐ Habite-se arquivado
☐ Laudo elétrico (SPDA) ≤ 5 anos
☐ Laudo de elevadores (mensal)
☐ Contrato de seguro incêndio ativo
```

**Como vincular os achados:**
- Para cada pendência, abra um `property.document` do tipo correto com `case_id` = este caso de auditoria
- Ou crie sub-casos filhos (use tags como `auditoria-2026 / pendente`)

**Encerramento:**
- Quando todos os documentos estiverem regularizados: `Concluído`
- Registre no chatter o resumo executivo da auditoria

---

## 7. Compliance: IPTU Não Pago pelo Locatário

### Contexto

O contrato prevê que o locatário paga o IPTU. O sistema de gestão municipal mostra débito em nome do proprietário (que repassou a obrigação contratualmente).

**Caso:**

```
Assunto:    IPTU 2026 não quitado – AP-204 – Obrigação do Locatário
Tipo:       Compliance
Prioridade: Alto
Imóveis:    AP-204
Contratos:  CTR-0042
Envolvidos: [locatário] [proprietário]

Descrição:
Contrato cláusula 8.2: IPTU de responsabilidade do locatário.
IPTU 2026 no valor de R$ 3.400 com vencimento 31/03/2026.
Prefeitura de Barueri – Guia nº 20260012345.
Proprietário foi notificado por falta de pagamento.

Ação requerida:
1. Notificar locatário imediatamente (prazo 5 dias)
2. Se não quitado: reter do depósito caução
3. Se depósito insuficiente: ação de regresso
```

**Documentos:**
- Cláusula do contrato (já em `property.document` tipo `contract`)
- Guia do IPTU 2026 (anexar no caso)
- Notificação enviada ao locatário

---

## 8. Renovação Contestada de Contrato Comercial

### Contexto

Locatário comercial solicita revisão do valor na renovação. O proprietário propõe reajuste de 15% (IPCA acumulado). O locatário oferece 8%.

```
Assunto:    Negociação de Renovação – Sala 101 – Empresa XYZ
Tipo:       Jurídico
Prioridade: Médio
Imóveis:    SAL-101
Contratos:  CTR-0030 (vigente, vencimento 30/06/2026)
Envolvidos: [locatário PJ] [proprietário] [corretor]

Descrição:
Reajuste IPCA 12 meses (Abr/25–Mar/26): 14,8%
Proposta proprietário: +15% → R$ 8.500/mês
Proposta locatário: +8% → R$ 7.848/mês
Mediação prevista para 15/05/2026.
```

**Fluxo:**
1. Cron detecta `next_adjustment_date` ≤ hoje → cria `property.rent.adjustment` em rascunho
2. Gestor verifica que há contestação → cria `governance.case` vinculado ao contrato
3. Negocia via chatter (mantém histórico)
4. Acordo: aplica `property.rent.adjustment.action_apply()` com valor negociado
5. Fecha o caso de governança como `Concluído`

---

## 9. Referência: Tipos, Prioridades e SLA

### Tipos de Caso (`governance.case.type`)

| Tipo | Cor | Uso típico em imóveis |
|---|---|---|
| **Jurídico** | Vermelho | Despejo, cobrança judicial, disputa de comissão |
| **Financeiro** | Amarelo | Inadimplência, acordo de parcelamento, IPTU |
| **Documental** | Cinza | Regularização de documentos, habite-se pendente |
| **Compliance** | Azul | Obrigações contratuais, seguros, laudos |
| **Operacional** | Verde | Manutenção contestada, acesso negado, vaga de garagem |
| **Reclamação** | Laranja | Danos ao imóvel, barulho, vizinhança |

### Prioridades e SLA automático

| Prioridade | SLA (dias) | Uso típico |
|---|---|---|
| Baixo (0) | 30 dias | Auditoria preventiva, documentação |
| Médio (1) | 15 dias | Negociação de renovação, reclamações |
| Alto (2) | 7 dias | Inadimplência, IPTU em débito |
| Crítico (3) | 3 dias | Ação de despejo, reintegração de posse |

> O campo `resolution_deadline` é calculado automaticamente: `origin_date + sla_days`.
> O cron diário detecta casos com `resolution_deadline < hoje` e os marca como `is_overdue = True`.

---

## 10. Fluxo de Etapas

```
┌─────────────┐
│  Planejado  │ ← caso criado, aguardando ação
└──────┬──────┘
       │ [Enviar E-mail]
┌──────▼──────┐
│E-mail Enviad│ ← notificação formal enviada, data registrada
└──────┬──────┘
       │ [Marcar como Aguardando]
┌──────▼──────┐
│ Aguardando  │ ← dentro do SLA, cron monitora
└──────┬──────┘
       │                    │
       │ [Registrar         │ [Sem Resposta]
       │  Resposta]         │ (SLA vencido)
┌──────▼──────┐      ┌──────▼──────┐
│  Resposta   │      │ Sem Resposta│ ← cron cria atividade urgente
│  Parcial    │      └──────┬──────┘
└──────┬──────┘             │
       │ [Concluir]         │ [Encerrar]
┌──────▼──────┐      ┌──────▼──────┐
│  Concluído  │      │  Encerrado  │
└──────┬──────┘      └─────────────┘
       │ [Encerrar]
┌──────▼──────┐
│  Encerrado  │ ← arquivo final, imutável
└─────────────┘
```

### Regras importantes

- **Não pule etapas** no Kanban — cada etapa registra uma data e ação específica
- **"Encerrado" ≠ "Concluído"**: encerrado significa arquivado (pode ser sem resolução); concluído significa que a questão foi resolvida
- **Sempre documente no chatter** datas de audiências, acordos verbais e ligações relevantes
- **Vincule documentos** ao `case_id` — eles aparecem automaticamente na aba "Documentos" do caso

---

## Dicas de Uso Diário

**Filtrando o que precisa de atenção:**
- Governança → filtro **"Atrasado"** → casos com `is_overdue = True`
- Governança → agrupar por **"Responsável"** → ver carga de cada gestor
- Imóveis → Contratos → filtro **"Inadimplente"** → alimentar casos jurídicos

**Tags recomendadas para property_core:**
- `despejo-2026`, `judicial`, `acordo`, `urgente`, `aguardando-advogado`

**Quando criar um caso novo vs. atualizar o existente:**
- Mesma questão, nova fase → atualize o caso existente (chatter + etapa)
- Nova questão sobre o mesmo imóvel → novo caso (vinculado ao mesmo imóvel/contrato)
- Exemplo: inadimplência virou despejo → **novo caso** tipo Jurídico, referencie o caso financeiro no chatter

---

*Documento gerado em 2026-04-04 · módulos: `governance` v19.0.1.0.0 + `property_core` v19.0.2.7.0*