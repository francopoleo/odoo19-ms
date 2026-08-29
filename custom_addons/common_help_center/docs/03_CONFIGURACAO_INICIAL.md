# Configuração Inicial — Central de Ajuda

## 1. Pré-requisitos

| Dependência |
| --- |
| base |
| web |



## 2. Instalação

```bash
./odoo-bin -d ms -i common_help_center --stop-after-init
```

Para atualizar:

```bash
./odoo-bin -d ms -u common_help_center --stop-after-init
```

## 3. Dados mestres e configurações

| XML ID | Model | Arquivo |
| --- | --- | --- |
| help_category_overview | help.category | data/help_category_data.xml |
| help_category_system_help | help.category | data/help_category_data.xml |
| help_category_agenda | help.category | data/help_category_data.xml |
| help_category_document_core | help.category | data/help_category_data.xml |
| help_category_property_core | help.category | data/help_category_data.xml |
| help_category_governance | help.category | data/help_category_data.xml |
| help_category_document_dossier | help.category | data/help_category_data.xml |
| help_category_finance | help.category | data/help_category_data.xml |
| help_category_admin | help.category | data/help_category_data.xml |
| help_category_troubleshooting | help.category | data/help_category_data.xml |
| article_document_document_create | help.article | data/help_context_defaults_data.xml |
| article_document_document_list | help.article | data/help_context_defaults_data.xml |
| context_document_document_list | help.context | data/help_context_defaults_data.xml |
| context_document_document_form | help.context | data/help_context_defaults_data.xml |
| tip_document_document_form | help.tip | data/help_context_defaults_data.xml |
| checklist_document_document_form | help.checklist.template | data/help_context_defaults_data.xml |
| article_property_asset_form | help.article | data/help_context_defaults_data.xml |
| context_property_asset_form | help.context | data/help_context_defaults_data.xml |
| article_governance_case_form | help.article | data/help_context_defaults_data.xml |
| context_governance_case_form | help.context | data/help_context_defaults_data.xml |
| article_help_center_overview | help.article | data/help_default_content_data.xml |
| article_help_contextual_drawer | help.article | data/help_default_content_data.xml |
| article_help_agenda_activities | help.article | data/help_default_content_data.xml |
| article_help_error_troubleshooting | help.article | data/help_default_content_data.xml |
| tip_global_activities_agenda | help.tip | data/help_default_content_data.xml |
| tip_property_asset_docs | help.tip | data/help_default_content_data.xml |
| tip_governance_case_agenda | help.tip | data/help_default_content_data.xml |
| checklist_property_asset | help.checklist.template | data/help_default_content_data.xml |
| checklist_governance_case | help.checklist.template | data/help_default_content_data.xml |
| suggestion_missing_required | help.suggestion.rule | data/help_default_content_data.xml |
| suggestion_xml_view_error | help.suggestion.rule | data/help_default_content_data.xml |
| article_help_taxonomy_enterprise | help.article | data/help_enterprise_contexts_data.xml |
| article_document_validation_expiration | help.article | data/help_enterprise_contexts_data.xml |
| article_document_no_orphan | help.article | data/help_enterprise_contexts_data.xml |
| article_property_asset_list | help.article | data/help_enterprise_contexts_data.xml |
| article_property_asset_gallery_media | help.article | data/help_enterprise_contexts_data.xml |
| article_property_inspection_flow | help.article | data/help_enterprise_contexts_data.xml |
| article_property_maintenance_flow | help.article | data/help_enterprise_contexts_data.xml |
| article_property_media_flow | help.article | data/help_enterprise_contexts_data.xml |
| article_governance_case_list | help.article | data/help_enterprise_contexts_data.xml |
| article_governance_pending_flow | help.article | data/help_enterprise_contexts_data.xml |
| article_agenda_general_flow | help.article | data/help_enterprise_contexts_data.xml |
| context_help_article_form | help.context | data/help_enterprise_contexts_data.xml |
| context_document_document_list | help.context | data/help_enterprise_contexts_data.xml |
| context_document_document_form | help.context | data/help_enterprise_contexts_data.xml |
| context_property_asset_list | help.context | data/help_enterprise_contexts_data.xml |
| context_property_asset_form | help.context | data/help_enterprise_contexts_data.xml |
| context_property_inspection_form | help.context | data/help_enterprise_contexts_data.xml |
| context_property_maintenance_form | help.context | data/help_enterprise_contexts_data.xml |
| context_property_media_form | help.context | data/help_enterprise_contexts_data.xml |
| context_governance_case_list | help.context | data/help_enterprise_contexts_data.xml |
| context_governance_case_form | help.context | data/help_enterprise_contexts_data.xml |
| context_governance_pending_form | help.context | data/help_enterprise_contexts_data.xml |
| context_common_agenda_event_list | help.context | data/help_enterprise_contexts_data.xml |
| context_common_agenda_event_form | help.context | data/help_enterprise_contexts_data.xml |
| group_help_user | res.groups | security/help_security.xml |
| group_help_admin | res.groups | security/help_security.xml |
| group_help_technical | res.groups | security/help_security.xml |
| base.group_user | res.groups | security/help_security.xml |
| base.group_system | res.groups | security/help_security.xml |



## 4. Checklist de configuração

- [ ] Instalar dependências.
- [ ] Atualizar lista de aplicativos.
- [ ] Instalar/atualizar `common_help_center`.
- [ ] Revisar grupos e permissões.
- [ ] Configurar categorias/tipos aplicáveis.
- [ ] Criar dados mestres mínimos.
- [ ] Rodar os testes funcionais do `04_GUIA_TESTES.md`.
- [ ] Importar documentação na Central de Ajuda.
- [ ] Validar Mapa de Contextos.

## 5. Central de Ajuda

Após instalar ou alterar documentação:

1. Abra **Central de Ajuda > Configuração > Importar Documentação**.
2. Marque **Varrer módulos instalados**, **Importar fontes ativas** e **Gerar mapa de contextos**.
3. Execute a importação.
4. Corrija itens sem contexto ou sem artigo.
