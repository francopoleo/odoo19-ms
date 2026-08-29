1
# Configuração Inicial — Property Core

## 1. Pré-requisitos

| Requisito | Versão |
|---|---|
| Odoo | 19.0 Community |
| Python | 3.10+ |
| PostgreSQL | 14+ |
| Módulos Odoo | `mail`, `account`, `portal`, `website`, `governance` |
| Módulo externo | `base_accounting_kit` (Cybrosys) — para relatórios contábeis |

## 2. Instalação

### 2.1 Adicionar ao addons_path

No arquivo `odoo.conf`:
```ini
addons_path = addons,custom_addons,account_addons
```

### 2.2 Instalar o módulo

**Via interface**: Configurações → Apps → Pesquisar "Property Core" → Instalar

**Via CLI** (recomendado para primeira instalação):
```bash
python odoo-bin -c odoo.conf -d SEU_BANCO -i property_core --stop-after-init
```

### 2.3 Atualizar após mudanças

```bash
python odoo-bin -c odoo.conf -d SEU_BANCO -u property_core --stop-after-init
```

---

## 3. Configuração Contábil

> **Obrigatório** para que os pagamentos de aluguel gerem lançamentos contábeis.

### 3.1 Acessar configurações

**Configurações → Contabilidade → seção "Imóveis"**

| Campo | Descrição | Exemplo |
|---|---|---|
| Diário de Recebimento | Diário onde os valores entram (banco/caixa) | `Banco Principal` |
| Conta de Receita | Conta creditada nos recebimentos | `3.1.1 - Receita de Aluguéis` |

### 3.2 Criar Conta de Receita (se não existir)

**Contabilidade → Configuração → Plano de Contas → Novo**

```
Código:     3.1.1
Nome:       Receita de Aluguéis
Tipo:       Receita (income)
```

### 3.3 Configuração por contrato (opcional)

Cada contrato pode ter seu próprio diário/conta, sobrepondo o padrão:

**Contrato → grupo "Contabilidade"** → Diário Contábil + Conta de Receita

---

## 4. Configuração de Segurança

### 4.1 Grupos disponíveis

| Grupo | Acesso |
|---|---|
| `property.group_property_user` | Visualização e operações básicas |
| `property.group_property_manager` | Acesso completo incluindo configurações |

### 4.2 Atribuir grupos

**Configurações → Usuários → selecionar usuário → aba "Imóveis"**

---

## 5. Configuração de Sequências

As sequências são gerenciadas pelo módulo `common_base`. Padrões:

| Modelo | Prefixo | Exemplo |
|---|---|---|
| `property.asset` | `IMP/` | `IMP/2025/0001` |
| `property.contract` | `CT/` | `CT/2025/0001` |
| `property.rent` | `ALC/` | `ALC/2025/0001` |
| `property.owner` | `PROP-OWN/` | `PROP-OWN/0001` |
| `property.broker` | `COR/` | `COR/0001` |
| `property.broker.assignment` | `ASN/` | `ASN/0001` |
| `property.commission` | `COM/` | `COM/0001` |

---

## 6. Configuração de Crons

Os crons são ativados automaticamente na instalação. Verificar em:
**Configurações → Técnico → Automações → Ações Agendadas**

| Cron | Frequência | Função |
|---|---|---|
| Imóveis: Verificar Contratos Vencidos | Diário | Marca contratos como A Vencer / Atrasado |
| Imóveis: Régua de Inadimplência | Diário | D+1, D+5, D+15, D+30 nas parcelas |
| Imóveis: Verificar Mandatos Expirados | Diário | Avisa mandatos a vencer em 7 dias |
| Imóveis: Lembrete Comissões Pendentes | Semanal | Lembra comissões não pagas |

---

## 7. Portal do Proprietário

Para que o proprietário acesse o portal:

1. Criar `res.partner` para o proprietário
2. Ativar acesso ao portal: **Contatos → Proprietário → Ação → Conceder Acesso ao Portal**
3. Em `property.owner`, vincular o campo **Contato / Acesso Portal** ao parceiro criado
4. O proprietário acessa: `http://seu-odoo/my/properties`

---

## 8. Verificação Rápida Pós-Instalação

Execute este checklist após instalar:

- [ ] Menu "Imóveis" aparece na barra principal
- [ ] Dashboard carrega sem erros
- [ ] Consegue criar um Imóvel
- [ ] Consegue criar um Proprietário
- [ ] Consegue criar um Contrato
- [ ] Parcelas são geradas ao ativar contrato
- [ ] Configurações → Contabilidade → seção "Imóveis" existe
- [ ] Crons aparecem em Configurações → Técnico → Ações Agendadas