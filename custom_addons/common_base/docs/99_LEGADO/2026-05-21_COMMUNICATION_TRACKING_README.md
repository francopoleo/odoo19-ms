# Sistema de Rastreamento Unificado de Comunicações

## Visão Geral

Sistema centralizado de comunicações rastreáveis que correlaciona emails, mensagens e documentos entre **Governança**, **Imóveis** e **Documentos** através de um **Token de Rastreamento Único**.

## Arquitetura

### Modelos Base

**`common.communication.base`** (AbstractModel em `common_base`)
- Fornece a estrutura comum de rastreamento
- Herdado por todos os modelos de comunicação
- **Não cria tabela no banco** - apenas define campos reutilizáveis

### Modelos Concretos

1. **`governance.case.communication`** (Governança)
   - Comunicações de casos de governança
   - Rastreamento de emails, telefonemas, reuniões
   - Herda: `mail.thread`, `common.communication.base`

2. **`property.asset.communication`** (Imóveis)
   - Comunicações de imóveis
   - Vinculação com contratos
   - Herda: `common.communication.base`, `mail.thread`

3. **`document.communication`** (Documentos)
   - Comunicações de documentos
   - Eventos: upload, validação, aprovação, rejeição, expiry
   - Herda: `common.communication.base`, `mail.thread`

## Token de Rastreamento

### O que é?

Um identificador único **gerado automaticamente** ao criar uma comunicação:

```
tracking_token = "a1b2c3d4e5f6g7h8i9j0k1l2"  # 32 caracteres hexadecimais
```

### Quando é criado?

- ✅ Automaticamente ao criar **qualquer** comunicação
- ✅ UUID único por registro
- ✅ Imutável após criação (readonly, copy=False)

### Como funciona?

#### Cenário 1: Caso de Governança com Imóvel Relacionado

```
Criar: governance.case (com asset_id vinculado)
  └─> Criar: governance.case.communication (token = "abc123")
        └─> Auto-link: property.asset.communication (mesmo token)
              └─> Resultado: Ambas as comunicações compartilham "abc123"
```

#### Cenário 2: Documento com Governança

```
Criar: document.document
  └─> Criar: document.communication (token = "xyz789")
        └─> Se vinculado a governance.case:
              └─> Auto-link: governance.case.communication (mesmo token)
```

## Campos de Rastreamento

Todos os modelos de comunicação possuem:

### Email
- `email_message_id` - Vinculação com `mail.message` do Odoo
- `external_message_id` - Message-ID do servidor IMAP/SMTP
- `email_from` - Remetente
- `email_to` - Destinatário
- `email_cc` - Cópia

### Correlação
- `related_governance_case_ids` - Many2many para casos de governança
- `related_asset_ids` - Many2many para imóveis
- `related_document_ids` - Many2many para documentos

### Metadados
- `channel_origin` - Identifica origem: 'governance', 'property', 'document'
- `channel_type` - Tipo: email, call, chat, meeting, task, document
- `sent_by_odoo` - Boolean: criada no Odoo ou importada
- `communication_date` - Timestamp da comunicação

## Casos de Uso

### 1. Rastreamento Completo de um Processo

**Situação**: Cliente envia email sobre problema em contrato de imóvel. Cria-se caso em Governança.

```
Email recebido em: governance@company.br
  └─> Cria: governance.case (asset_id = Imóvel A)
        └─> Cria: governance.case.communication (token_gov = "abc123")
              └─> Também cria: property.asset.communication (token = "abc123")
                    └─> Usuário vê no Imóvel A: comunicação relacionada ao caso
```

**Benefit**: Gerenciador de imóvel vê na aba Comunicações do Imóvel que há um caso ativo.

### 2. Documentos Vencidos

**Situação**: Documento vence, envia-se notificação. Abre-se caso em Governança.

```
Cron: document.expiry.check (daily)
  └─> Cria: document.communication (type='expiry_notice', token = "xyz789")
        └─> Usuário cria: governance.case (document_ids = [Doc A])
              └─> Vincula token "xyz789" automaticamente
                    └─> Resultado: Ambas aparecem correlacionadas
```

### 3. Pesquisa Unificada

**Query**: "Mostre todas as comunicações do imóvel X no último mês"

```python
# Buscar por imóvel
communications = env['property.asset.communication'].search([
    ('asset_id', '=', asset_id),
    ('communication_date', '>=', start_date),
])

# Depois, para cada comunicação, ver governança/documentos relacionados
for comm in communications:
    gov_cases = comm.related_governance_case_ids  # Links automáticos
    docs = comm.related_document_ids
```

## API de Métodos Úteis

### Encontrar por Token

```python
# Buscar todas as comunicações com um token
comms = env['common.communication.base'].find_by_tracking_token(token)
# Retorna dict com:
#   - comms['communications']
#   - comms['governance_cases']
#   - comms['assets']
#   - comms['documents']
```

### Vincular Manualmente

```python
# Se necessário vincular depois:
communication.link_to_governance_case(case)
communication.link_to_asset(asset)
communication.link_to_document(document)
```

## Fluxo de Email (Governança)

### Entrada de Email

```
Email → governance@company.br (alias)
  └─> GovernanceCase.message_new() (mail_thread)
        └─> Cria: governance.case
              └─> Cria: governance.case.communication
                    ├─ token = "auto-generated"
                    ├─ external_message_id = "Message-ID do servidor"
                    ├─ email_from = "client@example.com"
                    ├─ sent_by_odoo = False
                    └─ channel_origin = 'governance'
```

### Saída de Email

```
Usuário responde via Odoo
  └─> Cria: governance.case.communication
        ├─ token = "auto-generated" (novo)
        ├─ email_to = "client@example.com"
        ├─ sent_by_odoo = True
        └─ channel_origin = 'governance'
```

## Views

### property.asset.communication

**Acesso**: Imóvel → Aba "Comunicações"

- Lista todas as comunicações do imóvel
- Mostra casos de governança relacionados
- Permite criar tarefas
- Rastreamento de token visível

### document.communication

**Acesso**: Documento → Aba "Comunicações"

- Lista eventos do documento
- Upload, validação, rejeição
- Correlação com casos e imóveis

### governance.case (extensão)

**Campos novos**:
- `asset_ids` - Many2many com imóveis
- `document_ids` - Many2many com documentos
- `communication_tracking_token` - Token compartilhado

## Segurança

- **Readonly**: `tracking_token`, `external_message_id`, `email_*` fields
- **Índices**: tracking_token, external_message_id (busca rápida)
- **Acesso**: Controlado por grupos (grupo_governance_manager, etc.)

## Limites e Notas

- ⚠️ Token é **unique** no banco - não pode duplicar
- ⚠️ Email importado de servidor IMAP precisa de `external_message_id`
- ⚠️ Vinculação automática ocorre apenas se `asset_id` ou `document_id` está preenchido
- ✅ Multiple tokens simultâneos são permitidos (cada comunicação tem seu próprio)

## Roadmap Futuro

- [ ] Dashboard unificado de comunicações (todos os 3 módulos)
- [ ] Busca de texto completo em comunicações correlacionadas
- [ ] Notificações quando comunicações são vinculadas
- [ ] Histórico de alterações de vinculação
- [ ] Export de comunicações por token em formato HTML/PDF