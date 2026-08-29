# Guia de Deprecação de Modelos de Contatos

## Timeline de Deprecação

### ✅ v19.0 (ATUAL)
- **Status:** Modelos deprecados, mas ainda funcionais
- **Ação do usuário:** Migre para novo sistema quando possível
- **Menus:** Ocultos, acesse via Contatos (res.partner)
- **Aviso:** Banners de deprecação em todos os formulários antigos

### 🔜 v20.0 (PRÓXIMA)
- Remover menus do menu principal
- Aumentar avisos de deprecação
- Possível remoção de funcionalidades antigas
- Documentação de migração obrigatória

### ❌ v21.0 (FINAL)
- **Remoção:** Todos os modelos específicos deletados
- Apenas res.partner com categorias será suportado
- Sem opção de fallback

## Modelos Deprecados

| Modelo | Substituto | Categoria |
|--------|-----------|-----------|
| `property.owner` | `res.partner` | Proprietário |
| `property.broker` | `res.partner` | Corretor |
| `property.tenant` | `res.partner` | Inquilino |
| `property.buyer` | `res.partner` | Comprador |
| `property.seller` | `res.partner` | Vendedor |
| `property.investor` | `res.partner` | Investidor |
| `property.brokerage` | `res.partner` | Corretora |
| `property.developer` | `res.partner` | Construtora |
| `property.lead` | `res.partner` | Lead |

## Migração Manual de Dados

Se você criou contacts nos modelos antigos e quer garantir que migram:

### 1. Verificar Dados Migrados
```
Menu: Contatos
Filtro: Categoria = [Proprietário]
Resultado: Deve aparecer todos os property.owner migrados
```

### 2. Completar Informações Faltando
```
1. Abra contact em Contatos
2. Aba: Papéis Imobiliários
3. Preencha campos específicos (CRECI, banco, etc)
4. Salve
```

### 3. Validar Migração Completa
```
Para cada categoria:
- property.owner → contar em property.owner table
- res.partner com categoria Proprietário → deve ser igual

Se números não batem:
- Migração automática pode ter falhado
- Migre manualmente via Contatos
```

## O que Muda em Cada Versão

### v19.0 → v20.0

**Antes (v19.0):**
```
Menu Relacionamento
├─ Pessoas (usando res.partner)
└─ Contatos Imobiliários (usando property.owner, property.broker, etc)
```

**Depois (v20.0):**
```
Menu CRM
└─ Contatos (res.partner)
   ├─ Filtro: Proprietários
   ├─ Filtro: Corretores
   └─ (etc...)

Menus antigos removidos
```

### v20.0 → v21.0

**Antes (v20.0):**
```
Modelos ainda existem (para compatibilidade)
property.owner, property.broker, etc.
```

**Depois (v21.0):**
```
Modelos deletados completamente
Apenas res.partner existe
```

## Código de Migração Customizado

Se você tem código customizado que usa modelos antigos:

### Encontrar Referências
```bash
grep -r "property\.owner" custom_addons/
grep -r "property\.broker" custom_addons/
# etc...
```

### Atualizar Código
**ANTES:**
```python
Owner = self.env['property.owner']
owners = Owner.search([])
for owner in owners:
    print(owner.name, owner.cpf_cnpj)
```

**DEPOIS:**
```python
Partner = self.env['res.partner']
category = self.env.ref('property_core.res_partner_category_property_owner')
owners = Partner.search([('category_ids', 'in', category.ids)])
for owner in owners:
    print(owner.name, owner.cpf_cnpj)
```

## Avisos e Logs

### Avisos na UI
- Todos os formulários antigos mostram banner vermelho
- Diz: "DEPRECATED: Este modelo será removido em v21.0"
- Link para usar Contatos em vez disso

### Logs de Deprecação
```
[DEPRECATION] Creating record in property.owner.
Use res.partner with property categories instead.

[DEPRECATION] Updating record in property.owner.
Use res.partner with property categories instead.
```

Verifique logs em: Configurações → Logs → Filtro: "DEPRECATION"

## FAQ

### P: Meus dados antigos desaparecerão?
**R:** Não. Migração automática copia dados para res.partner. Models antigos continuam existindo em v19-20. Deletados em v21.

### P: Posso continuar usando property.owner?
**R:** Sim, até v21.0. Mas é deprecado. Use res.partner em vez disso.

### P: Como saber se migração funcionou?
**R:** Menu Contatos → Filtro por categoria → verifique dados lá.

### P: Preciso refazer meus customizações?
**R:** Sim, se usam models antigos. Atualize para usar res.partner + categorias.

### P: E se eu tiver código em production?
**R:** Você tem v19 e v20 para atualizar. v21 remove tudo. Comece migração agora.

## Checklist de Migração

- [ ] Verificar dados migrados em Contatos
- [ ] Completar informações faltando (CRECI, banco, etc)
- [ ] Atualizar código customizado para usar res.partner
- [ ] Testar relatórios e reports com novo sistema
- [ ] Atualizar documentação interna
- [ ] Treinar usuários no novo fluxo
- [ ] Remover dependências de models antigos
- [ ] Planejar upgrade para v21.0

## Contato

Para dúvidas sobre deprecação:
1. Veja logs: Configurações → Logs
2. Teste migração: Contatos → Filtros
3. Reporte bugs em GitHub issues
