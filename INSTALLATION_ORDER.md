# Ordem de Instalação dos Módulos Odoo 19 MS

## ⚠️ IMPORTANTE
Instale os módulos nesta ordem para evitar erros de dependências não resolvidas.

## Ordem Recomendada

### Fase 1: Módulos Base (Dependências)
1. **common_base** - Base comum com utilitários
2. **common_help_center** - Central de ajuda (depende de common_base)

### Fase 2: Módulos Principais
3. **property_core** - Sistema imobiliário principal (depende de common_base)
4. **document_core** - Gestão de documentos (depende de common_base)
5. **governance** - Governança e auditoria (depende de common_base)

### Fase 3: Integrações e Extensões
6. **property_valuation_engine** - Motor de avaliação (depende de property_core)
7. **governance_property_integration** - Integração governance ↔ property (depende de governance + property_core)
8. **document_governance_integration** - Integração documents ↔ governance (depende de document_core + governance)
9. **property_condominium_enterprise** - Gestão de condomínios (depende de property_core)
10. **property_contract_amendment_enterprise** - Aditivos de contrato (depende de property_core)
11. **property_contract_history** - Histórico de contratos (depende de property_core)
12. **property_payment_proof** - Comprovante de pagamento (depende de property_core)
13. **property_portal_integration** - Portal de propriedade (depende de property_core)
14. **property_website_integration** - Website integration (depende de property_core)
15. **property_demo_enterprise_seed** - Dados demo (depende de property_core + document_core + governance)

### Fase 4: Localização Brasileira
16. **account_addons/l10n_br_base** - Base BR (depende de account)
17. **account_addons/l10n_br_coa** - Plano de contas BR (depende de l10n_br_base)
18. **account_addons/l10n_br_crm** - CRM BR (depende de l10n_br_base)
19. **account_addons/l10n_br_hr** - RH BR (depende de l10n_br_base)
20. **account_addons/l10n_br_resource** - Recursos BR (depende de l10n_br_base)
21. **account_addons/l10n_br_zip** - CEP BR (depende de l10n_br_base)
22. **account_addons/l10n_br_currency_rate_update** - Taxa cambial BR (depende de l10n_br_base)
23. **account_addons/l10n_br_account_due_list** - Contas a pagar/receber BR (depende de l10n_br_base)

### Fase 5: Utilitários
24. **utils_addons/auto_database_backup** - Backup automático
25. **utils_addons/code_backend_theme** - Tema backend
26. **utils_addons/dynamic_accounts_report** - Relatórios dinâmicos

## Instalação Rápida (Linha de Comando)

Se preferir instalar via CLI no boot do Odoo:

```bash
./odoo-bin -d ms -i base,common_base,common_help_center,property_core,document_core,governance,property_valuation_engine,governance_property_integration,document_governance_integration --stop-after-init
```

Então adicione os outros módulos via interface web ou CLI.

## Resolução de Erros

Se encontrar erro de dependência:
1. Verifique se todos os módulos da "Fase 1" foram instalados
2. Não pule fases - siga a ordem rigorosamente
3. Se erro persistir, reinicie Odoo após cada fase

## Atualização Automática

Os `__manifest__.py` foram configurados com dependências corretas. Isso significa:
- Quando você instala `governance`, ele automaticamente instala `common_base`
- Quando você instala `governance_property_integration`, ele instala `governance` e `property_core`
- E assim por diante...

Então é seguro usar **"Instalar Tudo"** se as dependências estiverem corretas!
