# Manual de Uso — Governance & Audit

> **Regra central: se não está no sistema, não existe institucionalmente.**

---

## O que é um Caso de Governança?

É o registro de qualquer situação que precisa ser controlada, acompanhada e auditada.

Exemplos do dia a dia:

- Locatário não respondeu notificação
- Documentação do imóvel está irregular
- Fornecedor não enviou contrato
- Proposta enviada sem retorno
- Vistoria não foi agendada
- Reclamação de vizinho sobre imóvel

---

## Como Acessar

**Governança → Casos**

Ou pelo smart button diretamente em qualquer **Imóvel** ou **Contrato**.

---

## Criando um Caso

### Passo 1 — Preencher os campos principais

| Campo | O que colocar | Exemplo |
|---|---|---|
| Assunto | Título objetivo | "Contrato não enviado - Loja Centro" |
| Tipo | Categoria do caso | Jurídico / Documental / Financeiro... |
| Prioridade | Urgência | Baixo / Médio / Alto / Crítico |
| Responsável | Quem vai acompanhar | Seu nome |
| Envolvidos | Parceiros relacionados | Empresa XYZ |
| Tags | Classificação livre | Locatário, Urgente... |

### Tipos disponíveis

| Tipo | Quando usar |
|---|---|
| Jurídico | Ações judiciais, notificações extrajudiciais, liminares |
| Documental | Documentação faltante, matrícula irregular, contratos não assinados |
| Compliance | Irregularidades legais, licenças, obrigações regulatórias |
| Financeiro | Inadimplência, cobrança, débitos, repasses atrasados |
| Operacional | Manutenção, vistoria, problemas no imóvel |
| Reclamação | Reclamações de locatários, proprietários ou vizinhos |

### Prioridade e SLA

O sistema calcula automaticamente o **Prazo de Resolução** com base na prioridade:

| Prioridade | Prazo | Quando usar |
|---|---|---|
| Crítico | 3 dias | Liminar judicial, embargo, situação de risco imediato |
| Alto | 7 dias | Notificação formal, inadimplência grave, disputa contratual |
| Médio | 15 dias | Documentação faltante, reclamação, pendência operacional |
| Baixo | 30 dias | Acompanhamento, informação, registro de histórico |

### Passo 2 — Escrever a descrição

Use sempre este formato:

```
Contexto:
O que aconteceu e quando.

Compromisso ou situação:
O que foi prometido ou está pendente.

Situação atual:
O que ainda está faltando.

Objetivo:
Por que este caso está sendo registrado.
```

### Passo 3 — Vincular ao Imóvel ou Contrato (se aplicável)

Na aba **Imóveis e Contratos**, selecione os registros relacionados.

Ou crie o caso diretamente do imóvel/contrato usando o smart button — o vínculo é feito automaticamente.

---

## Fluxo de Trabalho

### 1. Planejado → Enviar

Quando você registrar a comunicação, clique em **Marcar E-mail Enviado**.

O sistema irá:
- registrar a data de envio
- criar atividades de follow-up automáticas
- iniciar o controle de prazo

### 2. Aguardar Resposta

Clique em **Aguardar Resposta** para indicar que a comunicação foi feita e você aguarda retorno.

### 3a. Resposta Recebida

Ao receber resposta, clique em **Registrar Resposta**.

O sistema cria uma atividade de acompanhamento para avaliar se a resposta atendeu ao caso.

### 3b. Sem Resposta (Silêncio)

Se não houver retorno dentro do prazo, clique em **Sem Resposta**.

> Este é um dos registros mais importantes do sistema. Documenta o silêncio como fato auditável.

### 4. Concluir

Quando o caso for resolvido: **Concluir**.

### 5. Encerrar

Para arquivar definitivamente: **Encerrar**.

---

## Follow-up Automático

Ao enviar um caso, o sistema cria lembretes automáticos na sua agenda para:

- Primeiro follow-up (verificar retorno)
- Segundo follow-up (solicitar status)
- Registrar silêncio se não houver resposta

Os prazos são configurados em **Configurações → Governança**.

---

## Criando Casos a partir de Imóveis e Contratos

Em qualquer formulário de **Imóvel** ou **Contrato**, você verá um botão **Governança** com a contagem de casos vinculados.

Para criar um caso já vinculado:
1. Abra o imóvel ou contrato
2. Clique no smart button **Governança**
3. Clique em **Criar**
4. O caso já vem com o vínculo preenchido

---

## Comunicação no Chatter

Toda comunicação deve ser registrada dentro do caso.

- Use o chatter para enviar mensagens e e-mails
- Anexe documentos diretamente no caso
- O histórico é completo e imutável

> Nunca use e-mail externo sem registrar no caso. Isso quebra a rastreabilidade.

---

## Exemplos Práticos

### Exemplo 1 — Locatário inadimplente

**Assunto:** Inadimplência - João Silva - Apto 42
**Tipo:** Financeiro
**Prioridade:** Alto
**Envolvidos:** João Silva
**Contrato vinculado:** Contrato #LOC-0042

**Descrição:**
```
Contexto: Parcela de março/2026 não foi paga até a data de vencimento (10/03).

Compromisso: Contrato prevê pagamento até dia 10 de cada mês.

Situação atual: Parcela vencida, sem contato do locatário.

Objetivo: Registrar inadimplência e iniciar cobrança formal.
```

**Fluxo:** Planejado → Enviar notificação → Aguardar → Sem resposta → Encerrar com registro

---

### Exemplo 2 — Documentação irregular do imóvel

**Assunto:** Matrícula desatualizada - Imóvel Rua das Flores 120
**Tipo:** Documental
**Prioridade:** Médio
**Imóvel vinculado:** Rua das Flores 120

**Descrição:**
```
Contexto: Matrícula do imóvel está desatualizada no cartório (última atualização 2018).

Compromisso: Proprietário precisa providenciar atualização para venda.

Situação atual: Documentação pendente.

Objetivo: Registrar pendência e acompanhar providência do proprietário.
```

---

### Exemplo 3 — Notificação judicial recebida

**Assunto:** Notificação extrajudicial - Disputa de divisa - Imóvel Av. Brasil 500
**Tipo:** Jurídico
**Prioridade:** Crítico
**Imóvel vinculado:** Av. Brasil 500

**Descrição:**
```
Contexto: Recebemos notificação extrajudicial em 29/03/2026 sobre disputa de divisa com vizinho.

Compromisso: Prazo de 5 dias para resposta formal.

Situação atual: Notificação recebida, aguardando orientação jurídica.

Objetivo: Registrar urgência, acionar advogado e acompanhar prazo.
```

---

## Erros Comuns — Nunca Faça Isso

- "Vou lembrar depois" → crie o caso agora
- "Está no meu e-mail" → registre no chatter do caso
- "Está no WhatsApp" → transcreva para o caso
- "Não é importante" → se precisar provar depois, será importante

---

## Resumo Rápido

| Situação | Ação no sistema |
|---|---|
| Aconteceu algo relevante | Criar caso |
| Comunicação enviada | Marcar E-mail Enviado |
| Aguarda retorno | Aguardar Resposta |
| Resposta recebida | Registrar Resposta |
| Silêncio | Marcar Sem Resposta |
| Problema resolvido | Concluir |
| Finalizado | Encerrar |