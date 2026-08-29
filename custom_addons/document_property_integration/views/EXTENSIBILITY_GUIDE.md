# Extensibilidade de property.asset Form

## Como adicionar tabs na view de property.asset

Quando você quer adicionar campos/páginas do seu módulo no formulário de property.asset, use xpath para inserir antes da tab `tab_notes_comms`.

### Exemplo: document_property_integration

Se você quer adicionar uma tab de documentos vinculados:

```xml
<!-- property_asset_ext_views.xml -->
<record id="view_property_asset_form_ext_documents" model="ir.ui.view">
    <field name="name">property.asset.form.ext.documents</field>
    <field name="model">property.asset</field>
    <field name="inherit_id" ref="property_core.view_property_asset_form"/>
    <field name="arch" type="xml">
        <xpath expr="//page[@id='tab_notes_comms']" position="before">
            <page string="Documentos" id="tab_documents">
                <field name="document_ids" mode="list,kanban">
                    <!-- Seu conteúdo aqui -->
                </field>
            </page>
        </xpath>
    </field>
</record>
```

### Padrão de IDs

As tabs base usam IDs previsíveis:
- `tab_location` - Localização
- `tab_characteristics` - Características Físicas
- `tab_financial` - Valores
- `tab_operations` - Operações (Contratos, Vistorias, Manutenção)
- `tab_gallery` - Galeria
- `tab_other_media` - Outras Mídias
- `tab_notes_comms` - Observações & Comunicações

**Use sempre `tab_notes_comms` como ponto de inserção** para manter ordem consistente:
- Módulos core: antes de `tab_notes_comms`
- Documentos/Governance: antes de `tab_notes_comms`
- Extensões customizadas: antes de `tab_notes_comms`

### Ordem recomendada

1. Localização, Características, Valores (dados básicos)
2. Operações (Contratos, Vistorias, Manutenção)
3. Galeria, Outras Mídias (conteúdo)
4. **Documentos** (se document_core instalado)
5. **Casos de Governança** (se governance instalado)
6. **Extensões customizadas**
7. Observações & Comunicações (sempre por último)

### Localização segura para inserção

Sempre use xpath com `position="before"` na tab `tab_notes_comms`:

```xml
<xpath expr="//page[@id='tab_notes_comms']" position="before">
    <!-- seu novo tab aqui -->
</xpath>
```

Isso garante que:
- Suas mudanças não quebram se tabs base são reordenadas
- Você não sobrescreve acidentalmente tabs existentes
- Múltiplos módulos podem adicionar tabs sem conflito
