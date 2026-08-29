# 09 — Troubleshooting

## Erro: menu não aparece

### Causa provável

Usuário sem grupo de valuation ou XML ID do menu raiz do `property_core` diferente.

### Verificar

O menu raiz esperado é:

```xml
property_core.menu_property_root
```

### Correção

1. Confirmar que o usuário está no grupo **Usuário de Valuation**.
2. Atualizar a lista de aplicativos.
3. Atualizar o módulo.
4. Confirmar que `property_core` está instalado.

## Erro: External ID not found: property_core.menu_property_root

### Causa

O menu raiz do `property_core` tem outro XML ID ou o arquivo de menus ainda não foi carregado.

### Correção

Trocar no arquivo `views/valuation_menus.xml`:

```xml
parent="property_core.menu_property_root"
```

pelo XML ID real do menu raiz de imóveis.

## Erro: Não há dados suficientes para calcular

### Mensagem provável

```text
Não há dados suficientes para calcular. Cadastre uma referência de valor m² ou imóveis comparáveis para a mesma finalidade.
```

### Causa

Não existe referência m² ou comparável compatível com venda/locação.

### Correção

Cadastrar pelo menos uma referência em:

```text
Imóveis > Valuation > Mercado > Referências m²
```

ou cadastrar comparáveis em:

```text
Imóveis > Valuation > Mercado > Comparáveis
```

## Erro: Informe a área de valuation

### Causa

O imóvel não tem área preenchida.

### Correção

Preencher no imóvel:

```text
Área para valuation m²
```

## Erro: record rule bloqueando registros

### Causa

Registro criado em outra empresa ou usuário sem acesso multiempresa.

### Correção

- verificar `company_id` do registro;
- verificar empresas permitidas do usuário;
- criar referências globais com `company_id` vazio quando fizer sentido.

## Erro externo: Wrong value for document.type.scope: 'legal'

Esse erro não pertence ao módulo `property_valuation_engine`. Ele indica falha na carga do módulo `document_core`.

Mensagem típica:

```text
ValueError: Wrong value for document.type.scope: 'legal'
```

### Causa

O campo `scope` do modelo `document.type` é um `Selection` e não possui o valor técnico `legal`.

Pelo padrão dos documentos imobiliários, documentos jurídicos usam categoria jurídica, mas o `scope` deve apontar o contexto operacional, como:

- `asset`;
- `contract`;
- `owner`;
- `broker`;
- `governance`.

### Correção do registro informado no erro

Trocar:

```xml
<field name="scope">legal</field>
```

por um escopo válido. Para documento jurídico diverso, a opção mais segura costuma ser:

```xml
<field name="scope">governance</field>
```

ou, se o documento for genérico do imóvel:

```xml
<field name="scope">asset</field>
```

Exemplo corrigido:

```xml
<record id="doc_type_legal_misc_document" model="document.type">
    <field name="name">Documento Jurídico Diverso</field>
    <field name="code">legal_misc_document</field>
    <field name="sequence">999</field>
    <field name="category_id" ref="document_core.doc_category_legal"/>
    <field name="scope">governance</field>
    <field name="default_access_level">legal</field>
    <field name="allow_website_publish" eval="False"/>
    <field name="website_default_visibility">portal</field>
    <field name="requires_issue_date" eval="False"/>
    <field name="requires_expiry" eval="False"/>
    <field name="requires_review" eval="False"/>
    <field name="requires_physical_original" eval="False"/>
    <field name="is_sensitive" eval="True"/>
    <field name="allowed_file_types">pdf,doc,docx,xlsx,jpg,jpeg,png,msg,eml</field>
</record>
```

## Comando de atualização após correção

```bash
docker compose exec web odoo -d sua_base -u document_core --stop-after-init
```

Depois:

```bash
docker compose exec web odoo -d sua_base -u property_valuation_engine --stop-after-init
```

## Erro: Definição de visualização search inválida

### Sintoma

```text
Definição de visualização property.valuation.source.search inválida
```

### Causa

Algumas instalações Odoo 19 personalizadas podem ser mais rígidas na validação de filtros e agrupamentos em `search views`.

### Correção aplicada

As `search views` foram simplificadas para campos de busca básicos, removendo filtros e agrupamentos declarados no XML inicial. Os filtros avançados podem ser reintroduzidos depois, um por um, validando no ambiente real.

## Menu Valuation não aparece dentro de Imóveis

### Causa mais comum

O menu `Imóveis > Valuation` usa os grupos:

- `property_valuation_engine.group_property_valuation_user`
- `property_valuation_engine.group_property_valuation_manager`

Se o usuário atual não tiver um desses grupos, o Odoo oculta o menu completamente.

### Correção aplicada nesta versão

A partir da versão `19.0.1.0.5`, o módulo cria uma ponte automática:

- `property_core.group_property_manager` implica `property_valuation_engine.group_property_valuation_manager`
- `base.group_system` implica `property_valuation_engine.group_property_valuation_manager`

Assim, Gestores de Imóveis e Administradores técnicos passam a ver o menu após atualização do módulo.

### Comando recomendado

```bash
docker compose exec web odoo -d ms -u property_valuation_engine --stop-after-init
```

Depois reinicie o serviço web e faça logout/login no Odoo, ou recarregue a página com limpeza de cache do navegador.

### Verificação manual

Em **Configurações > Usuários**, confirme se o usuário possui um dos grupos:

- Gestor de Valuation
- Usuário de Valuation
- Gestor de Imóveis
- Administração / Configurações
