# 02 — Instalação e Integração com property_core

## Estrutura esperada

O módulo deve ficar em:

```text
custom_addons/property_valuation_engine
```

Estrutura principal:

```text
property_valuation_engine/
 ├── __init__.py
 ├── __manifest__.py
 ├── README.md
 ├── docs/
 ├── models/
 ├── views/
 ├── security/
 ├── data/
 └── static/
```

## Dependências

No `__manifest__.py`, o módulo depende de:

```python
"depends": [
    "base",
    "property_core",
]
```

Isso garante que o módulo só seja instalado depois do núcleo imobiliário.

## Integração com o menu do property_core

O arquivo `views/valuation_menus.xml` usa o menu raiz do `property_core`:

```xml
parent="property_core.menu_property_root"
```

Esse XML ID foi identificado no arquivo de menus do `property_core`, onde o menu raiz é:

```xml
<menuitem id="menu_property_root" name="Imóveis" ... />
```

## Integração com o cadastro de imóveis

O módulo herda o modelo:

```python
_inherit = "property.asset"
```

A herança adiciona campos de valuation sem alterar a estrutura principal do módulo imobiliário.

Campos adicionados ao imóvel:

- `valuation_area_m2`;
- `valuation_city`;
- `valuation_neighborhood`;
- `valuation_use_type`;
- `valuation_standard`;
- `valuation_conservation`;
- `valuation_location_factor`;
- `valuation_liquidity_factor`;
- `valuation_vacancy_factor`;
- `valuation_run_ids`;
- `estimated_rent_value`;
- `estimated_sale_value`;
- `valuation_confidence_score`.

## Comando de atualização

Em ambiente Docker:

```bash
docker compose exec web odoo -d sua_base -u property_valuation_engine --stop-after-init
```

Em ambiente local:

```bash
./odoo-bin -d sua_base -u property_valuation_engine --stop-after-init
```

## Ordem recomendada de instalação

1. Instalar ou atualizar `property_core`.
2. Confirmar que o menu **Imóveis** aparece.
3. Copiar `property_valuation_engine` para `custom_addons`.
4. Atualizar lista de aplicativos.
5. Instalar `property_valuation_engine`.
6. Liberar os grupos de acesso aos usuários.
7. Cadastrar fontes e referências m² iniciais.
8. Rodar primeira estimativa em um imóvel de teste.

## Cuidados ao atualizar

Antes de atualizar em produção:

- fazer backup do banco;
- testar em base de homologação;
- verificar se `property_core.menu_property_root` existe;
- verificar se o modelo `property.asset` está instalado;
- garantir que usuários tenham grupos de valuation.
