# Governance Enterprise - Guia Completo de Uso

## 📋 Índice
1. [O que é Governance](#o-que-é-governance)
2. [Módulos Principais](#módulos-principais)
3. [Criar Caso de Governança](#criar-caso-de-governança)
4. [Canais de E-mail](#canais-de-e-mail)
5. [Integração com Documentos](#integração-com-documentos)
6. [Fluxos Práticos](#fluxos-práticos)
7. [Melhores Práticas](#melhores-práticas)
8. [Troubleshooting](#troubleshooting)

---

## O que é Governance?

O módulo **Governance** no Odoo 19 é um sistema completo de gestão de casos, comunicações e pendências. Serve para:

- **Rastrear solicitações** de governança, compliance, RH, legal, etc.
- **Gerenciar comunicações** com partes interessadas
- **Controlar pendências** e checklists obrigatórios
- **Registrar respostas** e documentação
- **Agendar alertas** e follow-ups automáticos

**Exemplo Real**: Uma empresa recebe uma solicitação de auditoria. Cria um Caso de Governança, registra comunicações com o auditor, acompanha documentos necessários e gera alertas quando prazos se aproximam.

---

## Módulos Principais

### 1. **governance** - Core do Sistema

Contém:
- Modelos de casos (`governance.case`)
- Tipos de casos (`governance.case.type`)
- Etapas (`governance.stage`)
- Canais de e-mail (`governance.email.channel`)
- SLA rules (`governance.sla.rule`)

**Quando usar**: Sempre que precisa rastrear um processo que tem múltiplas etapas, prazos e comunicações.

### 2. **governance_documents** - Integração com Documentos

Conecta casos de governance com o sistema de documentos:
- Auto-importação de anexos de e-mail
- Vinculação automática de documentos a casos
- Rastreamento de documentação completa

**Quando usar**: Quando o caso exige documentação e você quer organizar tudo automaticamente.

### 3. **governance** (Enterprise Features) - 4 Gaps Críticos

Novos campos e funcionalidades:
- **Identidade Institucional**: Configure email/reply-to por canal
- **Domínio Customizado**: Use domínio próprio para cada canal
- **Auto-import de Anexos**: Crie documento.document automaticamente
- **Cron de Alertas**: Atividades automáticas para itens vencidos

---

## Criar Caso de Governança

### Passo 1: Acessar Casos

Menu → Governança → Casos

Clique em **"Novo"** para criar um caso.

### Passo 2: Informações Básicas

```
Título: "Auditoria Interna Q2 2026"
Tipo: "Auditoria" (selecionado automaticamente pelo canal)
Responsável: "Gerente de Compliance"
```

### Passo 3: Configurar Canal de E-mail (Opcional)

Se o caso veio de e-mail:
1. O sistema detecta automaticamente o canal pelo destinatário
2. Popula tipo, prioridade e responsável conforme configurado no canal

**Exemplo**:
- E-mail enviado para: `governance@empresa.com.br`
- Sistema encontra canal "Governança Geral"
- Auto-popula: Tipo = Operacional, Prioridade = Médio, Responsável = Gerente de Governança

### Passo 4: Adicionar Participantes

Clique em **"Adicionar Linha"** na aba "Participantes":
- **Contato Principal**: A pessoa responsável pelo processo
- **Papel**: Claimant (reclamante), Other (outro)
- **É Primário**: Marca como contato principal

**Exemplo Prático**:
```
Participante 1: João Silva (Auditor) - Papel: Other
Participante 2: Maria Santos (Gerente) - Papel: Claimant - É Primário: ✓
```

### Passo 5: Criar Comunicações

Clique em **"Nova Comunicação"** para registrar interações:

```
Data: 2026-05-23
Tipo: E-mail (ou Telefone, Reunião, etc.)
Direção: Entrada (recebido) ou Saída (enviado)
Exige Resposta: ✓ (se esperamos uma volta)
Nota: "Recebido relatório preliminar de auditoria"
```

### Passo 6: Criar Pendências

Clique em **"Nova Pendência"** para itens que precisam ser feitos:

```
Nome: "Fornecer extratos bancários"
Data Vencimento: 2026-06-30
Obrigatório: ✓
Prioridade: Alto
Responsável: Maria Santos
Descrição: "Auditor solicitou extratos dos últimos 3 meses"
```

---

## Canais de E-mail

### O que é um Canal?

Um **Canal de E-mail** é uma caixa de entrada que cria casos automaticamente. Cada canal:
- Tem um alias (`governance@`, `juridico@`, etc.)
- Tem um tipo de caso padrão
- Tem responsável e prioridade
- Pode forçar identidade institucional

### Exemplo: Criar Canal "Juridico"

**Menu → Governança → Canais de E-mail → Novo**

```
Nome: "Juridico"
Alias: "juridico"
Empresa: Sua Empresa
Tipo Padrão: "Legal/Juridico"
Responsável: "Gerente Juridico"
Prioridade: "Alto"
```

**Comportamento de Entrada**:
```
☑ Criar caso para e-mail novo
☑ Atualizar caso existente por resposta
☑ Adicionar remetente como participante
☑ Entrada exige resposta por padrão
```

### Enterprise Features: Identidade Institucional

**Novo Grupo: "Identidade Institucional de Saída"**

```
Forçar Identidade Institucional: ☑ (marcado)
Remetente Institucional: "Juridico <juridico@empresa.com.br>"
Responder Para: "juridico-resp@empresa.com.br"
Domínio de Alias Customizado: "legal.empresa.com.br"
Importar Anexos Automaticamente: ☑ (marcado)
```

**O que acontece**:
1. E-mails enviados usam sempre `Juridico <juridico@empresa.com.br>`
2. Respostas vêm para `juridico-resp@empresa.com.br`
3. Alias usa `juridico@legal.empresa.com.br` (em vez do domínio global)
4. Anexos de e-mails recebidos viram `document.document` automaticamente

**Resultado**:
```
E-mail recebido:
├─ Caso criado automaticamente
├─ Participantes adicionados
├─ Documentos importados (automático!)
└─ E-mail de resposta usa identidade institucional
```

---

## Integração com Documentos

### Auto-import de Anexos

Quando ativado no canal:

```
Cliente envia e-mail com:
├─ Contrato.pdf
├─ Assinatura.jpg
└─ Cronograma.xlsx

Sistema cria automaticamente:
├─ document.document "Contrato.pdf" (Acesso: Governance)
├─ document.document "Assinatura.jpg" (Acesso: Governance)
└─ document.document "Cronograma.xlsx" (Acesso: Governance)

Todos vinculados ao case automaticamente!
```

### Configuração Manual

Se preferir criar documentos manualmente:

1. Abra o Caso de Governança
2. Clique em **"Documentos"** (aba inferior)
3. Clique em **"Novo"**
4. Preencha:
   ```
   Nome: "Parecer Juridico"
   Acesso: "Governance"
   Responsável: [seu nome]
   Tipo: "Parecer"
   ```
5. Faça upload do arquivo

**Vantagem**: Tudo fica vinculado e rastreável.

---

## Fluxos Práticos

### Fluxo 1: Compliance Check - Recepção até Fechamento

```
1️⃣ E-mail recebido em governance@empresa.com.br
   └─ Sistema cria Caso automaticamente (tipo: Operacional)

2️⃣ Gestor recebe notificação
   └─ Abre caso e adiciona participantes

3️⃣ Adiciona pendências obrigatórias
   └─ "Validar registros"
   └─ "Revisar documentação"
   └─ "Aprovar procedimentos"

4️⃣ Sistema cria atividades para follow-up
   └─ Lembrete em 3 dias (por SLA rule)
   └─ Alerta se vencer (cron operacional)

5️⃣ Conforme vai preenchendo:
   └─ Marca pendências como "Feito"
   └─ Registra comunicações
   └─ Uploda documentos

6️⃣ Quando 100% dos obrigatórios estão feitos:
   └─ Clica "Marcar como Concluído"
   └─ Caso vai para etapa "Done"

7️⃣ Encerra caso
   └─ Clica "Encerrar"
   └─ Todos os registros ficam histórico
```

### Fluxo 2: Auditoria com Documentação

```
SETUP:
├─ Criar tipo "Auditoria" com SLA 30 dias
├─ Criar canal "governance-audit@empresa.com.br"
├─ Ativar auto-import de anexos
└─ Criar checklist padrão (11 itens obrigatórios)

EXECUÇÃO:
├─ Auditor envia: "Iniciamos auditoria"
│  └─ Sistema cria Caso "Auditoria 2026"
│
├─ Auditor envia anexos:
│  ├─ formulario_auditoria.pdf
│  ├─ checklist_inicial.xlsx
│  └─ escopo_auditoria.docx
│  └─ Sistema cria 3 documentos automaticamente ✓
│
├─ Equipe interna responde:
│  ├─ Adiciona participantes
│  ├─ Cria 11 pendências (do checklist padrão)
│  └─ Atribui a responsáveis
│
├─ Follow-ups automáticos:
│  ├─ Dia 5: Lembrete de 25 dias restantes
│  ├─ Dia 25: Alerta de 5 dias
│  └─ Dia 28: Crítico, apenas 2 dias
│
├─ Conforme completa:
│  ├─ Upload "Registro de folha de pagamento.pdf"
│  ├─ Registra comunicação "Auditor validou"
│  ├─ Marca pendências como "Feito"
│  └─ Sistema atualiza progresso (%)
│
└─ Final: Caso vai a "Encerrado"
   └─ Histórico completo preservado
```

### Fluxo 3: Resposta Urgente com SLA

```
E-mail de cliente: "Preciso de 2 documentos em 24h"
  ↓
Caso criado com:
├─ Prioridade: Crítico
├─ SLA automático: 1 dia
├─ Responsável: Gerente RH
└─ Status: "Aguardando Resposta"

Sistema calcula:
├─ Data de Resposta: hoje + 1 dia
├─ Prazo de Resolução: hoje + 3 dias (por rule)
└─ Follow-up: hoje + 6 horas

Gerente RH recebe:
├─ Notificação imediata
├─ Atividade agendada para hoje 16h
└─ Caso destacado na "Fila de Trabalho"

Se não responder em 12h:
├─ Status muda para "Aguardando Resposta" (visual)
├─ Cor vermelha na lista (urgente)
└─ Sistema escalona para supervisor

Quando responde:
├─ Registra comunicação "Documentos enviados"
├─ Status vai para "Resposta Recebida"
├─ Cron de alertas limpa atividade antiga
└─ Caso passa para revisão
```

---

## Melhores Práticas

### ✅ Faça

1. **Use canais para agrupar tipos de solicitações**
   ```
   ✓ Um canal "Governance Geral" para entrada
   ✓ Um canal "Juridico" para questões legais
   ✓ Um canal "Auditoria" para auditorias internas
   ```

2. **Configure SLA rules para seus tipos**
   ```
   ✓ Auditoria: 30 dias
   ✓ Compliance: 15 dias
   ✓ Juridico: 20 dias
   ```

3. **Use tipos de caso com checklists padrão**
   ```
   ✓ Tipo "Auditoria" tem 11 pendências automáticas
   ✓ Usuário gasta 30 segundos menos por caso
   ✓ Garante que nada é esquecido
   ```

4. **Ative auto-import de anexos**
   ```
   ✓ Documentação fica organizada
   ✓ Tudo vinculado ao caso automaticamente
   ✓ Sem ação manual necessária
   ```

5. **Registre comunicações mesmo que verbal**
   ```
   ✓ "Teleconferência com auditor - validado"
   ✓ "Reunião presencial - assinado termo"
   ✓ Cria histórico completo
   ```

### ❌ Evite

1. **Não deixe casos sem participante principal**
   - Sempre marque alguém como "É Primário"
   - Sistema precisa saber quem é o contato

2. **Não ignore avisos de SLA**
   - Overdue é sinal de que algo travou
   - Desbloqueia impedimento ou escalona

3. **Não misture tipos de caso no mesmo canal**
   - Use canal separado para fluxos diferentes
   - Mantém contexto e responsabilidades claras

4. **Não esqueça de criar pendências obrigatórias**
   - Não deixe "Nenhuma pendência" quando há tarefas
   - Sistema não pode alertar sobre o esquecido

5. **Não feche caso com pendências abertas**
   - Se campo obrigatório de "case.type", sistema bloqueia
   - Força conclusão antes de encerrar

---

## Troubleshooting

### Problema: "Caso não foi criado ao enviar e-mail"

**Causas possíveis**:
1. Canal está inativo (`active` = False)
2. Alias não foi criado (botão "Criar/Atualizar Alias")
3. Campo `create_case_from_email` está marcado como False
4. E-mail foi para spam

**Solução**:
```
1. Menu → Governança → Canais
2. Abra o canal
3. Verifique se "Ativo" está marcado ✓
4. Clique "Criar/Atualizar Alias"
5. Clique "Criar caso para e-mail novo" ✓
```

### Problema: "Identidade institucional não está siendo usada"

**Causas**:
1. `force_institutional_identity` está False
2. Campo `institutional_email_from` vazio
3. Cache do browser (web assets antigos)

**Solução**:
```
1. Abra canal
2. Marque "Forçar Identidade Institucional" ✓
3. Preencha "Remetente Institucional": "Juridico <juridico@empresa.com.br>"
4. Salve
5. Hard refresh browser: Ctrl+Shift+R (ou Cmd+Shift+R no Mac)
```

### Problema: "Anexos não estão sendo importados como documentos"

**Causas**:
1. `auto_import_attachments` está False no canal
2. Módulo `governance_documents` não está instalado
3. Usuário não tem permissão em `document.document`

**Solução**:
```
1. Menu → Governança → Canais
2. Abra o canal
3. Marque "Importar Anexos Automaticamente" ✓
4. Verifique se governance_documents está em Módulos
5. Verifique permissões do usuário
```

### Problema: "Cron de alertas não está funcionando"

**Diagnóstico**:
```
Menu → Configurações → Automatização → Crons Agendados
Procure por "Governança: Alertas Operacionais"
```

**Se não existir**:
1. Atualizar módulo: `./odoo-bin -u governance`
2. Cron será criado automaticamente

**Se existir mas inativo**:
1. Clique no cron
2. Marque "Ativo" ✓
3. Clique "Execução Manual" para testar

**Se existir mas não cria atividades**:
```
Verifique:
1. Caso tem status não-finalizado? (sent, waiting, partial)
2. Caso tem response_state = "overdue"?
3. Responsável_id está preenchido?
4. Atividade tipo "Resposta em Atraso" existe no sistema?
```

### Problema: "Browser mostra erro 'force_institutional_identity undefined'"

**Causa**: Cache do browser com metadata antigos

**Solução Rápida**:
```
Hard Refresh: Ctrl+Shift+R (Windows/Linux) ou Cmd+Shift+R (Mac)
```

**Solução Manual**:
1. F12 (abrir DevTools)
2. Application → Local Storage
3. Selecione domínio
4. Clear All
5. F5 (refresh)

**Solução Nuclear**:
```bash
# Reiniciar servidor Odoo
./odoo-bin -c odoo.conf -d ms-teste --max-cron-threads=0
```

---

## Exemplos Completos por Indústria

### Exemplo: Empresa de Serviços Juridicos

```
CANAL: "Consultas"
├─ Alias: consultas
├─ Tipo Padrão: Parecer
├─ SLA: 10 dias
├─ Auto-import: Ativado
└─ Identidade: "Juridico <juridico@empresa.com.br>"

FLUXO:
1. Cliente envia: "Preciso parecer sobre contrato"
   └─ Cria caso automaticamente
2. Gerente atribui pendências: "Revisar contrato", "Pesquisar jurisprudência"
3. Gerente registra comunicações conforme progride
4. Cliente envia contrato em anexo
   └─ Documento criado automaticamente
5. Gerente completa parecer
6. Envia e-mail com parecer via Odoo
   └─ Registra como comunicação saída
7. Caso vai a "Concluído"
```

### Exemplo: Compliance & Risk

```
TIPO CASO: "Controle Interno"
├─ SLA: 15 dias
├─ Checklists automáticos: 8 itens
├─ Requer resposta: Sim
└─ Require primary participant: Sim

CANAL: "Compliance"
├─ Priority: Medium
├─ Responsible: Gerente Compliance
└─ Auto-import: Ativado

FLUXO:
1. Auditoria interna solicita
2. Sistema cria caso com 8 pendências
3. Gerente designa a equipes
4. Conforme completa, marca como "Feito"
5. Dashboard mostra progresso (0%, 25%, 50%... 100%)
6. Quando 100%: pode encerrar
7. Arquivo histórico com tudo rastreado
```

### Exemplo: RH & Conformidade

```
TIPO CASO: "Treinamento Obrigatório"
├─ SLA: 30 dias
├─ Participantes: Colaborador + Gerente
├─ Checklist: "Realizar teste", "Aprovar conclusão"
└─ Responsável Padrão: Gerente RH

FLUXO:
1. Email: "Novo treinamento disponível"
   └─ Cria caso para colaborador
2. Colaborador faz treinamento
3. Registra comunicação: "Treinamento concluído"
4. Gerente valida resultado
5. Marca pendência como "Feito"
6. Caso vai a "Concluído"
7. Relatório: "Quem não completou em 30 dias"
```

---

## Resumo: Os 3 Gaps Enterprise

| Gap | Campo | Benefício | Exemplo |
|-----|-------|-----------|---------|
| 1. Auto-import | `auto_import_attachments` | Sem action manual | E-mail + PDF → documento criado |
| 2. Identidade | `institutional_email_from` | Branding próprio | Juridico <juridico@empresa.com.br> |
| 3. Domínio | `domain_alias` | Domínio customizado | juridico@legal.empresa.com.br |
| 4. SLA Alerts | `cron_governance_operational_alerts` | Alertas automáticos | Atividade criada se vencer |

---

## Links Úteis

- **Menu Principal**: Governança → Casos
- **Canais**: Governança → Canais de E-mail
- **Tipos**: Configuração → Tipos de Caso
- **SLA Rules**: Configuração → Regras de SLA
- **Documentos**: Documentação → Documentos
- **Dashboard**: Governança → Dashboard Operacional

---

**Versão**: 1.0
**Data**: 2026-05-23
**Modulos**: governance, governance_documents
**Status**: Production Ready ✓
