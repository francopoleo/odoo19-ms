# Guia Prático de Gestão de Documentos — Document Core

> Documentação completa do módulo `document_core` v19.0.1.0.0 — Sistema centralizado de gestão, controle de vencimento e controle de acesso de documentos.

---

## Sumário

1. [O que é Document Core?](#1-o-que-é-document-core)
2. [Conceitos-chave](#2-conceitos-chave)
3. [Fluxo de Documentos](#3-fluxo-de-documentos)
4. [Como Cadastrar um Documento](#4-como-cadastrar-um-documento)
5. [Estados e Situações de Documentos](#5-estados-e-situações-de-documentos)
6. [Controle de Acesso](#6-controle-de-acesso)
7. [Vencimentos e Alertas](#7-vencimentos-e-alertas)
8. [Ciclos de Revisão Periódica](#8-ciclos-de-revisão-periódica)
9. [Vinculações (Links) com Outros Módulos](#9-vinculações-com-outros-módulos)
10. [Tipos de Documento Pré-configurados](#10-tipos-de-documento-pré-configurados)
11. [Dicas de Uso Diário](#11-dicas-de-uso-diário)

---

## 1. O que é Document Core?

**Document Core** é o módulo central de gestão documental do ERP. Ele fornece:

- **Repositório único** para todos os documentos da empresa (contratos, certidões, laudos, etc.)
- **Controle de vencimentos** automático — alerta quando documentos estão próximos de vencer
- **Histórico e rastreabilidade** — quem criou, editou, validou cada documento
- **Controle de acesso granular** — diferentes públicos (interno, jurídico, portal, público)
- **Armazenamento de arquivo físico** — rastreamento de onde o original repousa (sala, armário, caixa)
- **Vinculação com processos** — conecta a documentos: contratos, imóveis, governança, inspeções

### Quando usar

Registre no Document Core **todo documento que:**
- Tem validade ou data de vencimento
- Precisa ser compartilhado com terceiros (inquilinos, corretores, advogados)
- Exige cópia física guardada em local específico
- Precisa de aprovação ou validação formal
- Afeta compliance ou obrigações legais

---

## 2. Conceitos-chave

### Categoria de Documento
**Agrupamento lógico** por tipo de conteúdo. Ex: "Documentos Imobiliários", "Contratos", "Laudos Técnicos".
- Cada categoria define acesso padrão para todos seus tipos
- Facilita navegação e permissões em massa

### Tipo de Documento
**Definição específica** de um documento dentro de uma categoria. Ex: dentro de "Documentos Imobiliários" → "Habite-se", "AVCB", "Laudo Estrutural".
- Define regras obrigatórias (exige data de emissão? vencimento? original físico?)
- Define quem pode acessar por padrão
- Define se pode ser publicado no site do inquilino
- Aplicável a diferentes escopos (imóvel, contrato, governança, etc.)

### Documento
**Instância concreta** de um tipo. Ex: "Habite-se do AP-204, emitido em 2018".
- Rastreia datas (emissão, vigência, vencimento, revisão)
- Armazena arquivo digital (PDF, JPG, etc.)
- Rastreia localização física (se existe original em papel)
- Rastreia validação (quem aprovou, quando)
- Gera alertas automáticos ao se aproximar do vencimento

### Estados de Documento
| Estado | Significado | Quando usar |
|---|---|---|
| **Rascunho** | Documento em preparação, ainda não ativo | Criando/editando antes de publicar |
| **Vigente** | Documento ativo e sendo usado | Estado normal enquanto válido |
| **Substituído** | Foi supercedido por nova versão | Quando renovação é registrada |
| **Arquivado** | Documento histórico, sem validade prática | Após encerramento de contrato |
| **Cancelado** | Documento anulado, como se não tivesse existido | Erro de entrada ou retração |

### Situação de Documento (Baseada em Data)
Calculada automaticamente:

| Situação | Condição |
|---|---|
| **Válido** | Vencimento > hoje E (vencimento - hoje) > alert_days |
| **A Vencer** | 0 ≤ (vencimento - hoje) ≤ alert_days |
| **Vencido** | Vencimento < hoje |
| **Sem Vencimento** | Sem data de vencimento definida |

---

## 3. Fluxo de Documentos

```
REGISTRO INICIAL
      ↓
    [Documento criado em Rascunho ou Vigente]
      ↓
    [Sistema atribui referência automática: DOC/2026/00001]
      ↓
    [Validação (opcional): usuário aprova ou rejeita]
      ↓
  DOCUMENTO ATIVO
      ├→ [Vence em 30 dias] → Alerta automático (Atividade)
      ├→ [Venceu] → Marca como "Vencido" (badge vermelho)
      └→ [Renovação] → Link para novo documento via "Substituído por"
            ↓
      [Novo documento criado]
      ├→ Documento anterior marcado como "Substituído"
      └→ Novo documento em Vigente
            ↓
      [Fim da vigência do novo] → repetir ciclo

OU

ARQUIVO/CANCELAMENTO
      ↓
    [Estado = Arquivado | Cancelado]
      ↓
    [Imutável — não aparece em listas ativas]
```

---

## 4. Como Cadastrar um Documento

### Passo 1: Acessar o Formulário
1. Vá a **Documentos → Documentos** (ou acesse via link rápido em Imóvel/Contrato)
2. Clique em **"Novo"**

### Passo 2: Preencher Dados Básicos
```
┌─ IDENTIFICAÇÃO ──────────────────┐
│ Título *               [Habite-se AP-204]
│ Tipo de Documento *   [Habite-se]
│ Categoria (auto)      [Documentos Imobiliários]
│ Referência (auto)     [DOC/2026/00001]
│ Número / Protocolo    [12345.2018]  (opcional)
│ Versão                [1.0]  (use se há múltiplas versões)
└──────────────────────────────────┘
```

### Passo 3: Datas (variam por tipo)
```
┌─ DATAS ──────────────────────────┐
│ Data de Emissão       [01/06/2018]
│ Data de Vigência      [01/06/2018]   (data efetiva)
│ Data de Vencimento*   [31/12/2025]   (quando expira)
│ Data de Revisão       [15/03/2023]   (próx. inspeção)
│ Alertar com (dias)    [30]           (avisar antes de vencer)
└──────────────────────────────────┘
```

### Passo 4: Origem e Emitente
```
┌─ ORIGEM ─────────────────────────┐
│ Origem *              [Prefeitura]
│ Emitido por           [Prefeitura de Barueri]
│ Validado por (auto)   [Você - quando salvar]
│ Data de Validação     [auto - hoje]
└──────────────────────────────────┘
```

### Passo 5: Documento Físico (se aplicável)
```
┌─ DOCUMENTO FÍSICO ───────────────┐
│ Possui Original Físico □
│   Se SIM:
│   Localização Física  [Escritório SP / Sala 2 / Armário A]
│   Referência Física   [Caixa 5 - AP-204]
│   Exige Original      [✓] (campo somente leitura, definido pelo tipo)
└──────────────────────────────────┘
```

### Passo 6: Controle de Acesso
```
┌─ ACESSO E VISIBILIDADE ──────────┐
│ Nível de Acesso *     [Interno]  (auto do tipo)
│ Documento Sensível □  (rastreia acessos)
│ Disponível no Site □
│   Se SIM:
│   Visibilidade        [Somente Logado | Público | Corretores Autorizados]
│   Permitir Download □ (permite inquilino baixar arquivo)
│ Grupos Internos       [Jurídico, Financeiro] (quem vê internamente)
└──────────────────────────────────┘
```

### Passo 7: Arquivo Digital
```
Clique em [Adicionar Arquivo] ou arraste:
  - PDF recomendado
  - JPG, PNG se for imagem simples
  - Máximo 25 MB por arquivo
  - Pode ter múltiplos arquivos (versões antigas, anexos)
```

### Passo 8: Observações
```
Notas: Qualquer informação complementar
  - "Cópia de 2018, original em poder do cartório"
  - "Aguardando renovação"
  - Histórico de alterações
```

### Passo 9: Salvar
```
[Salvar] → Sistema:
  - Atribui referência (DOC/2026/00001)
  - Aplica regras do tipo (acesso, obrigações)
  - Agenda atividade de vencimento (se data = próximos 30 dias)
```

---

## 5. Estados e Situações de Documentos

### Estado (Manual — você define)

**Rascunho** `draft`
- Documento em edição
- Não aparece em listas de busca padrão
- Use para: preparação, validações pendentes
- Ação: Edite e salve quantas vezes quiser

**Vigente** `active`
- Documento pronto e sendo utilizado
- Aparece em todas as listas
- Use para: documentos em andamento
- Automático ao criar (ou defina manualmente)

**Substituído** `replaced`
- Este documento foi supercedido por outro mais novo
- Ainda pesquisável (auditoria), mas marcado como obsoleto
- Automático quando vincula "Substituído por"
- Use para: manter histórico sem poluir listas ativas

**Arquivado** `archived`
- Documento historicamente importante mas sem validade
- Não aparece em listas ativas
- Imutável (não edita)
- Use para: contratos encerrados, imóveis vendidos

**Cancelado** `cancelled`
- Documento anulado/retraído
- Não aparece em listas
- Imutável
- Use para: erros graves na entrada

### Situação (Automática — baseada em datas)

**Válido** ✓
- Vencimento > hoje E margens OK
- Badge verde
- Sem necessidade de ação

**A Vencer** ⚠️
- Próximo ao vencimento (dentro dos dias de alerta)
- Badge amarela
- Atividade automática criada
- Ação: procure renovar logo

**Vencido** ❌
- Vencimento < hoje
- Badge vermelha
- **Pode afetar compliance!**
- Ação urgente: renove ou justifique

**Sem Vencimento** ∞
- Não tem data de vencimento
- Badge cinza
- Exemplo: Título de propriedade, escritura pública

---

## 6. Controle de Acesso

O Document Core oferece **7 níveis de acesso**:

### Níveis Internos (empresa)

| Nível | Quem vê | Uso típico |
|---|---|---|
| **Interno** | Apenas funcionários | Documentos confidenciais da empresa |
| **Jurídico** | Equipes jurídica + financeira | Contratos, causas judiciais |
| **Financeiro** | Equipes financeira + contábil | Extratos, notas, comprovações |
| **Governança** | Equipes compliance + auditoria | Documentos de controle |

### Níveis Externos (portal/site)

| Nível | Quem vê | Uso típico |
|---|---|---|
| **Portal / Logado** | Inquilinos/corretores com acesso ao portal | Contratos já assinados, regulamento |
| **Corretores Autorizados** | Apenas corretores cadastrados | Fichas técnicas, fotos aéreas |
| **Público** | Qualquer um na internet | Regulamento condominial, estatuto |

### Como Definir Acesso

**Opção 1: Automático (recomendado)**
- Ao criar documento, selecione o **Tipo**
- Sistema **aplica acesso padrão do tipo automaticamente**
- Exemplo: tipo "Contrato" → acesso "Jurídico" por padrão

**Opção 2: Manual**
- Abra documento vigente
- Altere **"Nível de Acesso"** manualmente
- Marque **"Grupos Internos Autorizados"** (ex: Jurídico, Financeiro)

**Opção 3: Publicação no Site**
- Marque **"Disponível no Site"**
- Escolha **"Visibilidade"** (Público, Somente Logado, Corretores)
- Marque **"Permitir Download"** se quer que baix

em o arquivo

### Segurança — Documentos Sensíveis
```
┌─ RASTREAMENTO DE ACESSO ─────────┐
│ Ao marcar "Documento Sensível":
│ - Sistema registra cada acesso (quem, quando, de onde)
│ - Útil para documentos críticos (MPP, processos em segredo)
│ - Auditoria completa no chatter
└──────────────────────────────────┘
```

---

## 7. Vencimentos e Alertas

### Sistema Automático de Alertas

**Cron diário** executa `action_cron_check_expiry()`:
1. Busca documentos com vencimento próximo (nos próximos 30 dias por padrão)
2. Para cada um, cria **Atividade** no responsável
3. Atividade tem prazo = data de vencimento

### Como Funciona

**Exemplo 1: Documento vigente, 25 dias para vencer**
```
Data de hoje: 05/05/2026
Vencimento: 30/05/2026
Alert days: 30

Sistema:
  ✓ Calcula dias restantes = 25 dias
  ✓ 25 ≤ 30? → SIM
  ✓ Situação = "A Vencer" (amarela)
  ✓ Cria atividade: "Vence em 25 dias — Habite-se AP-204"
  ✓ Deadline da atividade = 30/05/2026
```

**Exemplo 2: Documento já vencido**
```
Data de hoje: 05/06/2026
Vencimento: 30/05/2026

Sistema:
  ✓ Situação = "Vencido" (vermelha)
  ✓ Pode bloquear certos processos (depende da integração)
  ✓ Atividade diária lembrando para renovar
```

### Personalizando Alertas

**Campo: "Alertar com (dias)"** — quando começar a avisar

```
Padrão: 30 dias (avisar um mês antes)

Para alterar:
- Documento com vencimento em 31/12/2026
- Hoje: 01/12/2026
- Se alert_days = 15, aviso começa 16/12
- Se alert_days = 60, aviso começa 01/11 (inclusive já passou!)
```

> **Dica:** Documentos que exigem processo longo de renovação (AVCB, Laudo Estrutural) — aumente alert_days para 60+ dias.

---

## 8. Ciclos de Revisão Periódica

Além do **vencimento** (data de expiração), documentos podem exigir **revisões periódicas** — auditorias internas para garantir que o documento continua relevante e correto.

### O que é Ciclo de Revisão?

Um documento pode estar **válido mas desatualizado**. Exemplo:
- Procuração jurídica de 2020: ainda vale 10 anos, mas precisa revisão anual
- Laudo estrutural: válido por 5 anos, mas exige vistoria anual
- Contrato: pode ter prazo longo, mas cláusulas precisam revisão anual

### Como Funciona

**Passo 1: Configurar no Tipo de Documento**
```
Abra: Tipos de Documento → [Tipo relevante]
├─ Aba "Regras"
├─ Campo: "Ciclo de Revisão (dias)"
└─ Exemplo: 90 dias
    (será revisado a cada 3 meses)
```

**Passo 2: Ao Criar o Documento**
```
Sistema calcula automaticamente:
├─ "Data de Revisão" = você preenche com data de hoje
├─ "Próxima Revisão" = Data Revisão + 90 dias (auto-calculado)
└─ "Situação de Revisão" = "Atualizado" 🟢
```

**Passo 3: Monitoramento Automático (Cron diário)**
```
Cron "Document Core: Verificar Ciclos de Revisão" executa:

Para cada documento com próxima_revisão definida:
  ├─ Se próxima_revisão > hoje + 30 dias
  │  └─ Situação = "Atualizado" 🟢 (sem ação)
  │
  ├─ Se próxima_revisão está nos próximos 30 dias
  │  ├─ Situação = "Revisão Próxima" 🟡
  │  └─ Cria atividade: "Revisar documento — [Nome]"
  │
  └─ Se próxima_revisão < hoje
     ├─ Situação = "Revisão Atrasada" 🔴
     └─ Cria atividade URGENTE: "Revisar documento — [Nome]"
```

### Estados de Revisão

| Estado | Situação | Ícone | Ação Necessária |
|---|---|---|---|
| **up_to_date** | Atualizado | 🟢 | Nenhuma — documento ok |
| **due_soon** | Revisão Próxima | 🟡 | Agendar revisão nos próximos 30 dias |
| **overdue** | Revisão Atrasada | 🔴 | **URGENTE** — revisar agora |
| **no_review** | Sem Revisão | ⚪ | Tipo não exige revisão periódica |

### Exemplo Prático — Procuração Jurídica

```
SITUAÇÃO INICIAL (28/04/2026)
├─ Documento: "Procuração Geral para Representação"
├─ Data de Revisão: 28/04/2026 (hoje)
├─ Tipo exige: 90 dias de ciclo
├─ Próxima Revisão: 27/07/2026 (auto-calculado)
└─ Situação de Revisão: 🟢 Atualizado

⏰ LINHA DO TEMPO

14/06/2026 (30 dias antes):
  ├─ Próxima Revisão: 27/07/2026
  ├─ Dias restantes: 43 dias
  ├─ Atividade CRIADA: "Revisar documento — Procuração..."
  ├─ Atribuída a: Campo "Responsável"
  └─ Prazo da atividade: 27/07/2026

26/07/2026 (1 dia antes):
  ├─ Próxima Revisão: 27/07/2026
  ├─ Dias restantes: 1 dia
  └─ Status: 🟡 "Revisão Próxima" (amarelo)

28/07/2026 (VENCEU!):
  ├─ Próxima Revisão: 27/07/2026
  ├─ Dias restantes: -1 dias
  ├─ Status: 🔴 "Revisão Atrasada" (vermelho)
  └─ Atividade escalonada (marca como urgente)

28/04/2027 (Usuário revisa):
  ├─ Abre o documento
  ├─ Aba "Validação & Vínculos"
  ├─ ALTERA: "Data de Revisão" = 28/04/2027 (hoje)
  ├─ [Sistema recalcula automaticamente]
  ├─ Próxima Revisão = 27/07/2027
  ├─ Situação de Revisão = 🟢 "Atualizado"
  ├─ Clica [SALVAR]
  └─ Atividade é marcada como feita ✓
```

### Passo-a-Passo: Como Revisar um Documento

**Cenário:** Você recebeu atividade "Revisar documento — Procuração..."

#### Opção 1: Revisar direto do formulário (recomendado)

```
1. Na lista de documentos, abra o que precisa revisão
   └─ Busque by: Status de Revisão = "Revisão Próxima/Atrasada"

2. Vá para aba "Validação & Vínculos"

3. Encontre o campo "Data de Revisão"
   ├─ Mostra: 15/04/2026 (data anterior)
   └─ Altere para: 28/04/2026 (hoje)

4. SALVAR (Ctrl+S ou botão [Salvar])
   └─ Sistema faz automaticamente:
      ├─ Recalcula "Próxima Revisão" = 28/04 + 90 = 27/07
      ├─ Muda "Situação Revisão" para 🟢 "Atualizado"
      ├─ Registra alteração no Chatter
      └─ Fecha a atividade pendente

5. Pronto! ✓ Revisão concluída
   └─ Próximo alerta em 60 dias
      (quando faltar 30 dias para 27/07)
```

#### Opção 2: Revisar via Atividade (mais prático)

```
1. No Chatter (aba "Atividades"), veja a atividade pendente
   └─ "Revisar documento — Procuração..."

2. Clique na atividade para abrir o documento
   └─ Sistema já sabe que você está respondendo

3. Altere "Data de Revisão" = hoje (28/04/2026)

4. SALVAR
   └─ Atividade é marcada automaticamente como feita ✓
```

### Visualização na Tela

#### ANTES de revisar:
```
┌─────────────────────────────────────┐
│ Validação & Vínculos                │
├─────────────────────────────────────┤
│ Data de Revisão: 15/04/2026 (ANTIGO)│
│ Próxima Revisão: 14/07/2026 ← VENCEU
│ Situação Revisão: 🔴 REVISÃO ATRASADA
│ Responsável: João Silva             │
└─────────────────────────────────────┘

Chatter:
  [!] Atividade pendente: "Revisar documento — ..."
      Criada: 14/06/2026
      Prazo: 14/07/2026 ❌ VENCIDA
```

#### ENQUANTO edita:
```
┌─────────────────────────────────────┐
│ Data de Revisão: [28/04/2026]  ✏️   │
│ Próxima Revisão: [RECALCULANDO...]  │
│ Situação Revisão: [ATUALIZANDO...]  │
│                                      │
│ [SALVAR]  [DESCARTAR]               │
└─────────────────────────────────────┘
```

#### DEPOIS de salvar:
```
┌─────────────────────────────────────┐
│ Data de Revisão: 28/04/2026 ✓ NOVO  │
│ Próxima Revisão: 27/07/2027 ✓ AUTO  │
│ Situação Revisão: 🟢 ATUALIZADO     │
│ Responsável: João Silva             │
└─────────────────────────────────────┘

Chatter:
  [✓] Atividade resolvida: "Revisar documento — ..."
      Realizada por: [Seu nome]
      Data: 28/04/2027
```

### Campos Envolvidos

| Campo | Tipo | Bloqueado? | Função |
|---|---|---|---|
| **Data de Revisão** | Date | ❌ Não | Você altera manualmente quando revisar |
| **Próxima Revisão** | Date | ✅ Sim (leitura) | Sistema calcula: Data Revisão + ciclo_dias |
| **Situação de Revisão** | Selection | ✅ Sim (leitura) | Sistema atualiza: up_to_date/due_soon/overdue |
| **Ciclo de Revisão (dias)** | Integer | ✅ Sim (tipo) | Definido no tipo de documento |
| **Responsável** | Many2one | ❌ Não | Quem recebe atividade de revisão |

### Checklist: Revisar um Documento

```
☐ 1. Documento mostra Status "Revisão Próxima" ou "Revisão Atrasada"
☐ 2. Abre aba "Validação & Vínculos"
☐ 3. Encontra campo "Data de Revisão"
☐ 4. Altera para data de hoje (ex: 28/04/2026)
☐ 5. SALVA (Ctrl+S)
☐ 6. Verifica se "Próxima Revisão" recalculou (agora +90 dias)
☐ 7. Verifica se "Situação Revisão" mudou para 🟢 "Atualizado"
☐ 8. Clica em "Marcar como feito" na atividade (se houver)
☐ 9. ✓ Revisão concluída! Próximo alerta em 60 dias
```

### Situações Especiais

#### Cenário 1: Documento com DOIS ciclos

Alguns documentos têm:
- **Ciclo de vencimento:** 365 dias (expiração legal)
- **Ciclo de revisão:** 90 dias (auditoria interna)

Ambos funcionam **independentemente**:
```
Data de Revisão: 28/04/2026 → Próxima Revisão: 27/07/2026
Data de Vencimento: 28/04/2027 → Próximo Alerta: 29/03/2027

Ao revisar:
  └─ Altere APENAS "Data de Revisão"
     └─ NÃO altere "Data de Vencimento" (outro ciclo!)
```

#### Cenário 2: Colocar data no futuro

Se você altera "Data de Revisão" para data futura:
```
Data de Revisão: 01/05/2026 (futuro)
  ├─ Próxima Revisão = 01/05 + 90 = 30/07/2026
  ├─ Situação = "Atualizado"
  └─ ⚠️ Mas documenta revisão que ainda não aconteceu!

Recomendação: Use sempre data de hoje para histórico correto
```

#### Cenário 3: Tipo sem ciclo de revisão

Se tipo tem "Ciclo de Revisão (dias)" = 0:
```
├─ Campo "Data de Revisão" fica visível (para histórico)
├─ Campo "Próxima Revisão" fica vazio
└─ "Situação Revisão" = "Sem Revisão" ⚪
    └─ Nenhuma atividade gerada
```

### Integração com Atividades

O sistema cria **automaticamente** atividades do tipo:
- **Ícone:** 🔄 (refresh)
- **Nome:** "Revisão de Documento"
- **Prazo:** Data da próxima revisão

Atividades aparecem em:
- **Chatter** do documento (aba "Atividades")
- **Meu Painel** (agenda do usuário responsável)
- **Busca de atividades:** Filtro "Revisão de Documento"

---

## 9. Vinculações com Outros Módulos

Document Core **integra-se** com:

### property_core (Imóveis)
```
Imóvel → aba "Documentos"
  ├→ Habite-se
  ├→ AVCB
  ├→ Laudo elétrico
  └→ Fotos/plantas

Sistema busca automaticamente documentos com:
  - Tipo de documento scope = "asset" (imóvel)
  - Vinculados ao imóvel (se implementado)
```

### property_core (Contratos)
```
Contrato → aba "Documentos"
  ├→ Contrato assinado (PDF)
  ├→ Termo aditivo
  ├→ Procuração
  └→ Empenho (para comercial)
```

### governance (Casos de Governança)
```
Caso Jurídico → aba "Documentos"
  ├→ Notificação extrajudicial
  ├→ Parecer jurídico
  ├→ Comprovante de envio
  └→ Resposta do demandado

Documentos aparecem automaticamente se
  case_id estiver preenchido no documento
```

### property_core (Inspeções)
```
Vistoria → aba "Documentos"
  ├→ Laudo de inspeção
  ├→ Fotos
  ├→ Relatório
  └→ Orçamentos de reparo
```

---

## 10. Tipos de Documento Pré-configurados

### Documentos Imobiliários
| Tipo | Exige Emissão | Exige Vencimento | Exige Revisão | Original Físico | Publicável |
|---|---|---|---|---|---|
| Habite-se | ✓ | — | — | ✓ | — |
| AVCB | ✓ | ✓ | ✓ (anual) | ✓ | — |
| Laudo Estrutural | ✓ | ✓ (5 anos) | ✓ (anual) | ✓ | — |
| Laudo Elétrico (SPDA) | ✓ | ✓ (5 anos) | ✓ (anual) | ✓ | — |
| Laudo Elevadores | ✓ | ✓ (mensal) | ✓ (mensal) | ✓ | — |
| Planta / Projeto | ✓ | — | — | ✓ | — |

### Documentos de Contrato
| Tipo | Publicável no Portal | Pode Download |
|---|---|---|
| Contrato Assinado | ✓ | ✓ (se público) |
| Termo Aditivo | ✓ | — |
| Procuração | — | — |
| Regulamento Condominial | ✓ | ✓ |

### Documentos Jurídicos
| Tipo | Sensível | Acesso Padrão |
|---|---|---|
| Parecer Jurídico | ✓ | Jurídico |
| Notificação Extrajudicial | ✓ | Jurídico |
| Sentença | ✓ | Jurídico |
| Acordo / Termo | — | Jurídico |

---

## 11. Dicas de Uso Diário

### ✓ Boas Práticas

1. **Use tipos pré-definidos** — não crie tipos ad hoc, padroniza acesso e validações
2. **Preencha datas corretamente** — sistema depende delas para alertas
3. **Alerta dias personalizados** — AVCB (60 dias), Laudo Estrutural (90 dias)
4. **Arquivo físico sempre** — especificamente para originais, rastreie localização
5. **Adicione observações** — "aguardando renovação", "cópia de X em poder de Y"
6. **Valide documentos críticos** — campo "Validado por" + data
7. **Substitua, não delete** — quando renovar, link "Substituído por" e marque como "Substituído"
8. **Sensível para confidencial** — marque e rastreie quem acessa

### ✗ Erros Comuns

- ❌ Deixar em "Rascunho" indefinidamente — use apenas para preparação
- ❌ Não definir data de vencimento — depois não há alerta
- ❌ Esquecer original físico — rastreamento quebrado
- ❌ Mudar acesso manualmente a cada documento — defina no **tipo** uma vez
- ❌ Deletar documento antigo — use estado "Arquivado" para manter histórico
- ❌ Criar tipos novos sem padronização — pergunte ao administrador primeiro

### Fluxo Rápido: Renovação de Documento

**Cenário:** AVCB de AP-204 vence 31/12/2025. Você renovou em 15/12/2025.

```
1. Abra documento antigo (AVCB 2024)
   Estado: Vigente → mude para Rascunho

2. Crie novo documento (AVCB 2025)
   Tipo: AVCB
   Data Emissão: 15/12/2025
   Data Vencimento: 31/12/2026
   Número: (novo código da certificação)
   Arquivo: [upload PDF novo]
   Salve

3. No documento novo:
   Abra documento antigo
   Campo "Substituído por" = [selecione documento novo]
   Documento antigo → auto-muda para "Substituído"

4. Pronto!
   ✓ Novo documento em vigente
   ✓ Antigo no histórico (auditoria)
   ✓ Sistema alertará novo vencimento
```

### Filtrando Documentos Críticos

**Governança → Menu de Documentos:**

```
[Documentos]
  └→ Filtro: "A Vencer" → mostra todos com amarelo
  └→ Filtro: "Vencido" → mostra críticos (vermelho)
  └→ Agrupar por: "Imóvel" ou "Tipo"
  └→ Buscar: "AVCB" ou "Laudo"
```

---

## Referência Rápida

### Campos Obrigatórios (variam por tipo)
- Título — sempre
- Tipo — sempre
- Data Emissão — se tipo exigir
- Data Vencimento — se tipo exigir
- Original Físico — se tipo exigir
- Localização Física — se Original Físico = SIM

### Datas Recomendadas
| Tipo | Emissão | Vencimento | Revisão |
|---|---|---|---|
| AVCB | Sim | Sim (1 ano) | Sim (anual) |
| Laudo Estrutural | Sim | Sim (5 anos) | Sim (anual) |
| Contrato | Sim | Sim (vigência) | — |
| Habite-se | Sim | — | — |
| Certidão | Sim | Sim (30 dias) | — |

### Ações Rápidas no Documento

| Ação | Atalho |
|---|---|
| Validar | Preencha "Validado por" + Data |
| Renovar | Crie novo, marque "Substituído por" |
| Arquivar | Estado = "Arquivado" |
| Cancelar | Estado = "Cancelado" |
| Publicar no site | Marque "Disponível no Site" |

---

## Suporte e Dúvidas

- **Documento vencido bloqueando processo?** → Renovar ou marcar como "Arquivado"
- **Alerta não chega?** → Verifique Atividades no menu lateral
- **Arquivo não sobe?** → Máximo 25 MB, formatos: PDF, JPG, PNG
- **Não consigo ver documento publicado?** → Verifique "Disponível no Site" + "Visibilidade" + nível de acesso

---

*Documentação gerada em 2026-04-28 — Document Core v19.0.1.0.0 + Odoo 19.0*