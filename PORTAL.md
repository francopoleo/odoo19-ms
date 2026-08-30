# Portal, Website e Backend — Divisão de Navegação

Documento único que define **o que aparece em cada área** do sistema. Antes de adicionar link/card/menu, consulte esta divisão.

## 1. Website público — `/imoveis`

Sem login. Catálogo de imóveis para locação/venda.

| Rota | O quê | Módulo |
|---|---|---|
| `/imoveis` | Catálogo com filtros (tipo, cidade) | `property_website_integration` |
| `/imoveis/<id>` | Detalhe do imóvel + galeria | `property_website_integration` |
| `/imoveis/<id>/interesse` | POST — envia lead | `property_website_integration` |

## 2. Portal do cliente — `/my/home`

Área logada. Cards de resumo aparecem **só se o usuário tiver o vínculo**.

| Card | Rota | Condição | Módulo |
|---|---|---|---|
| Contratos de Locação | `/my/contracts` | inquilino com contrato | `property_portal_integration` |
| Parcelas de Aluguel | `/my/rents` | inquilino com parcela | `property_portal_integration` |
| Meus Imóveis | `/my/properties` | proprietário | `property_portal_integration` |
| Meus Documentos | `/my/documents` | qualquer partner com doc | `document_portal_integration` |
| Casos de Governança | `/my/governance` | responsável ou participante | `governance_portal_integration` |
| Condomínio | `/my/condominium` | vínculo condominial ativo | `property_condominium_enterprise` |

**Regras dos cards:**
- Contador vem de `_prepare_home_portal_values` (só chaves terminadas em `_count`).
- Dados não-counter (flags, contexto) vão em `_prepare_portal_layout_values` — nunca em `_prepare_home_portal_values`, senão o JS `/my/counters` quebra com `null.textContent`.
- XPath alvo: `//div[@id='portal_common_category']` (existe no `portal.portal_my_home` do Odoo 19).

## 3. Backend — `/odoo`

Gestão para funcionários (corretores, admin, contabilidade). **Não misturar com portal.** Menus definidos em cada módulo `property_*`, `document_*`, `governance*`.

## Armadilhas conhecidas

- **`/imoveis` 404**: `__init__.py` do módulo deve importar `controllers`; `request.render()` deve usar o XML ID com prefixo do módulo onde o template está definido (não de outro).
- **Portal cards não aparecem**: cards têm classe `d-none` por padrão; só somem quando o contador > 0 (via `placeholder_count` + JS) OU quando `config_card=True` é passado.
- **Ícones dos cards**: paths tipo `homemenu_icon_*.svg` **não existem** no Odoo 19. Ícones só renderizam se a customização `portal.portal_docs_entry_layout` ("Use Pictograms") estiver ativa. Hoje deixados sem ícone.




## Redefini a senha no banco de desenvolvimento local ms.

  Use exatamente:

  - Login: portal.locatario.demo@example.com
  - Login: portal.proprietario.demo@example.com
  - Login: portal.governanca.demo@example.com
  - Senha: DemoPortal2026!

  A senha diferencia maiúsculas, minúsculas e o !.

  O usuário portal.condominio.demo@example.com não foi criado separadamente: o acesso ao condomínio está no usuário proprietário, pois ele também possui vínculo condominial.