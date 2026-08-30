# Guia de Desenvolvimento — MS ERP (Odoo 19)

> Manual de padrões e convenções para criação e manutenção de módulos customizados.
> Siga este guia como referência ao criar novos módulos ou ao pedir ajuda a uma IA.

---

## Índice

1. [Estrutura de módulo](#1-estrutura-de-módulo)
2. [Manifest](#2-manifest)
3. [Herança de modelos](#3-herança-de-modelos)
4. [Sistema de mensagens — `message_post`](#4-sistema-de-mensagens--message_post)
5. [Sistema de atividades — `activity_schedule`](#5-sistema-de-atividades--activity_schedule)
6. [Tipos de atividade customizados](#6-tipos-de-atividade-customizados)
7. [Templates de e-mail](#7-templates-de-e-mail)
8. [Crons — processamento automático](#8-crons--processamento-automático)
9. [Sequências](#9-sequências)
10. [Mixin base](#10-mixin-base)
11. [Convenções de nomenclatura](#11-convenções-de-nomenclatura)
12. [Checklist para novo módulo](#12-checklist-para-novo-módulo)

---

## 1. Estrutura de módulo

```
custom_addons/{nome_modulo}/
├── __init__.py
├── __manifest__.py
├── data/
│   ├── {modulo}_activity_types.xml   ← tipos de atividade do módulo
│   ├── {modulo}_cron.xml             ← crons
│   └── {modulo}_data.xml             ← dados iniciais (sequências, configs)
├── models/
│   ├── __init__.py
│   └── {modulo}_{entidade}.py
├── report/
│   └── {modulo}_{entidade}_report.xml
├── security/
│   ├── {modulo}_security.xml
│   └── ir.model.access.csv
└── views/
    ├── {modulo}_{entidade}_views.xml
    └── {modulo}_menu_views.xml
```

---

## 2. Manifest

```python
{
    "name": "Nome do Módulo",
    "version": "19.0.1.0.0",          # major.minor.patch seguindo o módulo pai
    "category": "Real Estate",
    "summary": "Uma linha descrevendo o módulo",
    "author": "MS ERP",
    "license": "LGPL-3",
    "depends": ["mail", "common_base"],  # sempre incluir mail se usar thread/activity
    "data": [
        "security/{modulo}_security.xml",
        "security/ir.model.access.csv",
        "data/{modulo}_activity_types.xml",  # ANTES dos crons
        "data/{modulo}_cron.xml",
        "data/{modulo}_data.xml",
        "views/{modulo}_{entidade}_views.xml",
        "views/{modulo}_menu_views.xml",
    ],
    "installable": True,
    "application": True,               # True apenas para módulos principais
}
```

**Ordem obrigatória no `data`:** security → activity_types → crons → dados → views

---

## 3. Herança de modelos

### Modelo principal (entidade com registro próprio)

```python
class MinhaEntidade(models.Model):
    _name = "meu_modulo.entidade"
    _description = "Descrição da Entidade"
    _inherit = ["mail.thread", "mail.activity.mixin", "common.mixin"]
    _order = "create_date desc"

    name = fields.Char("Nome", required=True, tracking=True)
    company_id = fields.Many2one(...)   # já vem do common.mixin
    active = fields.Boolean(...)        # já vem do common.mixin
```

### Modelo auxiliar (sem chatter, sem atividades)

```python
class MinhaEntidadeAux(models.Model):
    _name = "meu_modulo.entidade_aux"
    _description = "Auxiliar"
    # Sem _inherit de mail — não precisa de chatter
```

### Extensão de modelo existente

```python
class ResPartnerExt(models.Model):
    _inherit = "res.partner"            # estende sem criar novo modelo
    meu_campo = fields.Char(...)
```

**Regra:** Todo modelo principal que aparece em menus deve herdar `mail.thread` + `mail.activity.mixin`. Modelos de linha/detalhe (ex: parcelas de aluguel) não precisam.

---

## 4. Sistema de mensagens — `message_post`

Use `message_post` para **registro de auditoria e histórico** — eventos que já aconteceram, sem esperar ação do usuário.

```python
# Registro simples no chatter
self.message_post(
    body=_("Contrato vencido automaticamente em %s.") % today
)

# Notificar parceiro externo (aparece no chatter + envia e-mail)
self.message_post(
    body=_("Parcela vencida há %s dias. Regularize o pagamento.") % days,
    partner_ids=[self.partner_id.id],
    subtype_xmlid="mail.mt_comment",    # mt_comment envia e-mail; mt_note não envia
)

# Registrar mudança de status
record.message_post(body=_("Status alterado para: %s") % novo_status)
```

### Quando usar `message_post` vs `activity_schedule`

| Situação | Use |
|---|---|
| Algo aconteceu (evento passado) | `message_post` |
| Alguém precisa fazer algo (tarefa futura) | `activity_schedule` |
| Notificar parceiro externo por e-mail | `message_post` com `partner_ids` |
| Alertar usuário interno | `activity_schedule` |
| Cron detectou vencimento | ambos: `message_post` (log) + `activity_schedule` (alerta) |

---

## 5. Sistema de atividades — `activity_schedule`

Use `activity_schedule` para **criar tarefas que exigem ação do usuário** — vencimentos, follow-ups, cobranças, aprovações.

### Criação de atividade

```python
record.activity_schedule(
    "meu_modulo.mail_activity_type_meu_tipo",   # XML ID do tipo customizado
    date_deadline=data_limite,
    summary=_("Resumo claro — máx. ~60 chars — %s") % identificador,
    note=_("Detalhe completo: o quê, de onde, o que fazer."),
    user_id=responsavel.id,
)
```

### Prevenção de duplicatas (OBRIGATÓRIO em crons)

Sempre verificar antes de criar para evitar spam de atividades:

```python
already = record.activity_ids.filtered(
    lambda a: "palavra_chave" in (a.summary or "").lower()
)
if not already:
    record.activity_schedule(...)
```

A verificação é feita no **próprio registro** (`record.activity_ids`), não em `activity_type_id.res_model` (esse campo é do tipo, não da atividade).

### Padrão completo para cron com atividade

```python
def _schedule_expiry_activity(self):
    """Cria atividade de vencimento. Seguro para chamar múltiplas vezes."""
    today = date.today()
    for rec in self:
        if not rec.expiry_date:
            continue
        days_left = (rec.expiry_date - today).days
        if not (0 <= days_left <= (rec.alert_days or 30)):
            continue
        already = rec.activity_ids.filtered(
            lambda a: "vencimento" in (a.summary or "").lower()
        )
        if already:
            continue
        rec.activity_schedule(
            "meu_modulo.mail_activity_type_meu_tipo",
            date_deadline=rec.expiry_date,
            summary=_("Vence em %s dias — %s") % (days_left, rec.name),
            note=_("O registro '%s' vence em %s. Providencie renovação.") % (
                rec.name, rec.expiry_date
            ),
            user_id=rec.create_uid.id,
        )

@api.model
def action_cron_check_expiry(self):
    """Cron diário."""
    docs = self.search([
        ("expiry_date", "!=", False),
        ("status", "in", ["valid", "expiring"]),
    ])
    docs._schedule_expiry_activity()
```

### Disparo imediato no create/write

Para que a atividade apareça **sem esperar o cron**, chamar `_schedule_expiry_activity` no create e write:

```python
@api.model_create_multi
def create(self, vals_list):
    records = super().create(vals_list)
    records._schedule_expiry_activity()
    return records

def write(self, vals):
    res = super().write(vals)
    if "expiry_date" in vals or "alert_days" in vals:
        self._schedule_expiry_activity()
    return res
```

---

## 6. Tipos de atividade customizados

**Nunca usar `mail.mail_activity_data_todo`** em código automatizado. Sempre criar um tipo específico por módulo.

### Arquivo: `data/{modulo}_activity_types.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">

        <record id="mail_activity_type_{modelo}_{evento}" model="mail.activity.type">
            <field name="name">Nome Legível para o Usuário</field>
            <field name="icon">fa-{icone}</field>
            <field name="decoration_type">warning</field>  <!-- warning | danger | success | info -->
            <field name="category">default</field>
            <field name="res_model">meu_modulo.modelo</field>  <!-- OBRIGATÓRIO — restringe ao modelo -->
            <field name="delay_count">1</field>
            <field name="delay_unit">days</field>
        </record>

    </data>
</odoo>
```

### Convenção de XML IDs

```
{modulo}.mail_activity_type_{modelo_sufixo}_{evento}

Exemplos:
  property_core.mail_activity_type_document_expiry
  property_core.mail_activity_type_contract_expiry
  property_core.mail_activity_type_rent_overdue
  governance.activity_type_followup
  governance.activity_type_response_check
```

### Ícones disponíveis (Font Awesome 4)

| Ícone | Uso sugerido |
|---|---|
| `fa-file-text-o` | documentos |
| `fa-file-text` | contratos |
| `fa-exclamation-circle` | cobrança, urgente |
| `fa-bell` | follow-up, lembrete |
| `fa-check-circle` | verificação, aprovação |
| `fa-wrench` | manutenção |
| `fa-search` | vistoria, auditoria |
| `fa-id-card` | credenciais, mandato |
| `fa-calendar` | agendamento |
| `fa-money` | financeiro |

### Decoration types (cor do badge)

| Valor | Cor | Quando usar |
|---|---|---|
| `warning` | laranja | atenção, prazo próximo, follow-up |
| `danger` | vermelho | urgente, vencido, cobrança |

> **Odoo 19:** apenas `warning` e `danger` são valores aceitos. `success` e `info` causam erro na instalação.

### `res_model` — regra fundamental

O campo `res_model` restringe o tipo ao modelo correto. Isso:
- Garante que o tipo só aparece disponível no modelo certo
- Faz o usuário ver na lista de atividades **de onde vem** cada item
- Impede uso acidental em modelos errados

```xml
<!-- CERTO: tipo específico, aparece só em property.document -->
<field name="res_model">property.document</field>

<!-- ERRADO: genérico, aparece em qualquer modelo -->
<!-- (omitir res_model deixa disponível para todos) -->
```

### Tipos de atividade por módulo

#### `property_core`

| XML ID | Nome | Modelo |
|---|---|---|
| `mail_activity_type_document_expiry` | Vencimento de Documento | `property.document` |
| `mail_activity_type_contract_expiry` | Vencimento de Contrato | `property.contract` |
| `mail_activity_type_broker_assignment` | Mandato de Corretor | `property.broker.assignment` |
| `mail_activity_type_rent_overdue` | Cobrança de Aluguel | `property.rent` |
| `mail_activity_type_inspection` | Vistoria de Imóvel | `property.inspection` |
| `mail_activity_type_maintenance` | Manutenção de Imóvel | `property.maintenance` |

#### `governance`

| XML ID | Nome | Modelo |
|---|---|---|
| `activity_type_followup` | Follow-up de Governança | `governance.case` |
| `activity_type_response_check` | Acompanhar Resposta | `governance.case` |

---

## 7. Templates de e-mail

Para comunicação **com parceiros externos** (clientes, fornecedores).

### Arquivo: `data/mail_templates.xml` ou `data/email_templates.xml`

```xml
<record id="mail_template_{modulo}_{evento}" model="mail.template">
    <field name="name">Nome do Template</field>
    <field name="model_id" ref="{modulo}.model_{modelo_underscore}"/>
    <field name="subject">Assunto: {{ object.name }}</field>
    <field name="body_html" type="html">
        <p>Olá <t t-out="object.partner_id.name"/>,</p>
        <p>Mensagem aqui.</p>
    </field>
    <field name="email_to">{{ object.partner_id.email }}</field>
    <field name="auto_delete" eval="True"/>
</record>
```

### Envio no código

```python
template = self.env.ref("meu_modulo.mail_template_xxx", raise_if_not_found=False)
if template and self.partner_id and self.partner_id.email:
    try:
        template.send_mail(self.id, force_send=False)
    except Exception:
        self.message_post(body=_("Falha ao enviar e-mail."))
```

**Regra:** sempre `raise_if_not_found=False` e sempre dentro de `try/except` para não quebrar o cron.

---

## 8. Crons — processamento automático

### Arquivo: `data/{modulo}_cron.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">

        <record id="cron_{modulo}_{descricao}" model="ir.cron">
            <field name="name">{Área}: {Descrição da tarefa}</field>
            <field name="model_id" ref="{modulo}.model_{modelo_underscore}"/>
            <field name="state">code</field>
            <field name="code">model.action_cron_{nome}()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>  <!-- minutes | hours | days | weeks | months -->
            <field name="active" eval="True"/>
        </record>

    </data>
</odoo>
```

### Convenção de nomes

```
id:     cron_{modulo}_{o_que_faz}
name:   "{Área}: {Descrição legível}"
método: action_cron_{o_que_faz}

Exemplos:
  cron_property_check_document_expiry
  cron_governance_check_overdue
  Imóveis: Alertar Documentos a Vencer
  Governança: Verificar Casos em Atraso
```

### Estrutura do método cron

```python
@api.model
def action_cron_{nome}(self):
    """Descrição do que o cron faz."""
    records = self.search([...])
    for rec in records:
        try:
            # lógica aqui
            pass
        except Exception as e:
            _logger.error("Cron {nome} falhou para %s: %s", rec.id, e)
```

---

## 9. Sequências

Usar `common.sequence` para gerar referências automáticas em todos os modelos.

### Registrar sequência (em `common_base/data/common_sequence_data.xml`)

```xml
<record id="sequence_{modulo}_{modelo}" model="common.sequence">
    <field name="name">Nome da Sequência</field>
    <field name="code">meu_modulo.modelo</field>
    <field name="prefix">PRE-</field>
    <field name="padding">5</field>
    <field name="next_number">1</field>
</record>
```

### Usar no modelo

```python
reference = fields.Char("Referência", readonly=True, copy=False, default="New")

@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get("reference", "New") == "New":
            vals["reference"] = (
                self.env["common.sequence"].sudo().next_by_code("meu_modulo.modelo") or "New"
            )
    return super().create(vals_list)
```

---

## 10. Mixin base

Todo modelo principal deve herdar `common.mixin` (definido em `common_base`).

### O que o `common.mixin` já fornece

- `active` — arquivo/desarquiva registros
- `company_id` — multi-empresa
- `tag_ids` — tags para classificação
- `action_archive()` / `action_unarchive()`
- `action_open_attachments()`

### Não duplicar campos que o mixin já tem

```python
# ERRADO — duplica o que common.mixin já tem
active = fields.Boolean("Ativo", default=True)
company_id = fields.Many2one("res.company", ...)

# CERTO — apenas herdar
_inherit = ["mail.thread", "mail.activity.mixin", "common.mixin"]
```

---

## 11. Convenções de nomenclatura

### Modelos Python

```
_name:  "{modulo}.{entidade}"          → property.document, governance.case
classe: {Modulo}{Entidade}             → PropertyDocument, GovernanceCase
```

### Campos

```
Many2one:   {entidade}_id              → asset_id, contract_id, partner_id
One2many:   {entidade}_ids             → document_ids, rent_ids
Many2many:  {entidade}_ids             → tag_ids, partner_ids
Computed:   _compute_{campo}           → _compute_status, _compute_attachment_count
Onchange:   _onchange_{campo}          → _onchange_asset_id
Constraint: _check_{regra}             → _check_dates, _check_link
```

### XML IDs

```
view:       {modulo}_{entidade}_view_{tipo}       → property_document_view_list
action:     action_{modulo}_{entidade}            → action_property_document
menu:       menu_{modulo}_{entidade}              → menu_property_document
cron:       cron_{modulo}_{descricao}             → cron_property_check_expiry
activity:   mail_activity_type_{modelo}_{evento}  → mail_activity_type_document_expiry
template:   mail_template_{modulo}_{evento}       → mail_template_property_contrato_vencendo
security:   {modulo}_group_{nivel}                → property_group_manager
```

### Métodos

```
Cron:           action_cron_{descricao}()
Ação de botão:  action_{verbo}()
Cálculo:        _schedule_{descricao}()    (privado, reutilizável)
Stage:          action_set_{stage}()
```

---

## 12. Checklist para novo módulo

Ao criar um novo módulo, verificar:

### Estrutura
- [ ] `__manifest__.py` com `depends` incluindo `mail` e `common_base`
- [ ] `data/` com arquivos na ordem correta no manifest
- [ ] `security/ir.model.access.csv` com permissões para todos os modelos
  - **Coluna `model_id:id`:** usar `model_{nome_com_underscores}` SEM prefixo de módulo (ex: `model_property_index`, não `property_core.model_property_index`). O Odoo resolve no namespace do módulo automaticamente. Usar prefixo causa erro pois o `ir.model.data` dos novos modelos ainda não existe quando o CSV é processado.

### Modelos
- [ ] Modelos principais herdam `mail.thread`, `mail.activity.mixin`, `common.mixin`
- [ ] Campo `reference` com sequência via `common.sequence`
- [ ] Campos de data com `tracking=True` para auditoria
- [ ] `_order` definido

### Atividades
- [ ] Arquivo `data/{modulo}_activity_types.xml` criado
- [ ] Cada tipo tem `res_model` definido
- [ ] XML IDs seguem a convenção `mail_activity_type_{modelo}_{evento}`
- [ ] Nenhum `activity_schedule` usa `mail.mail_activity_data_todo`
- [ ] Crons com atividades têm verificação de duplicata

### Crons
- [ ] Arquivo `data/{modulo}_cron.xml` com `noupdate="1"`
- [ ] Método do cron com `@api.model` e tratamento de exceção
- [ ] Nomes de cron seguem `{Área}: {Descrição}`

### E-mails
- [ ] Templates com `raise_if_not_found=False`
- [ ] Envio dentro de `try/except`
- [ ] Verificação de `partner_id.email` antes de enviar

---

## Referência rápida — Fluxo de comunicação por evento

```
Evento detectado pelo cron
├── message_post(...)                         # log no chatter (auditoria)
├── activity_schedule(tipo_customizado, ...)  # tarefa para usuário interno
└── template.send_mail(...)                   # e-mail para parceiro externo (se aplicável)

Evento iniciado pelo usuário (botão)
├── message_post(...)                         # log da ação
└── activity_schedule(...)                    # próxima etapa (se houver)

Mudança de status/etapa
└── message_post(...)                         # registro automático via tracking=True
                                              # (não precisa chamar explicitamente se o campo tem tracking)
```