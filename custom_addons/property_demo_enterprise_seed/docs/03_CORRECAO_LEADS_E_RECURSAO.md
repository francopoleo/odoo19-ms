# Correção de leads e recursão

Esta versão acompanha um ajuste no `property_core/models/property_lead.py`.

## Problema

Durante a criação de dados de teste, o model `property.lead` podia cair em:

```text
maximum recursion depth exceeded
```

A causa era a sincronização automática do contato mestre: `_sync_partner()` atribuía `rec.partner_id = partner` mesmo quando o parceiro já era o mesmo. Essa atribuição chamava `write()`, que chamava `_sync_partner()` novamente.

## Ajuste

- adicionado contexto `skip_property_lead_partner_sync`;
- escrita de `partner_id` somente quando o parceiro realmente mudou;
- uso de `stakeholder_type_prospect` para leads/prospects;
- substituição de `rec.user_id` por `submitter_user_id`;
- atualização segura de `stakeholder_profile_id`.

## Atualização recomendada

```bash
./odoo-bin -d SUA_BASE -u property_core,property_demo_enterprise_seed --stop-after-init
```
