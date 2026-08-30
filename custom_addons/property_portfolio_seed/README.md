# Silva Empreendimentos - Portfólio Imobiliário

Módulo opcional para carregar a carteira de imóveis da **Silva Empreendimentos**.

Atualmente, os registros são baseados na listagem KMS disponível no projeto.
Essa relação não é fixa: deve ser atualizada sempre que a lista real da Silva
Empreendimentos mudar, incluindo novos imóveis, alterações cadastrais ou ativos
retirados da carteira.

O módulo carrega somente registros de `property.asset`. Ele não cria usuários,
contratos, documentos, dossiês, casos de governança ou dados fictícios de
demonstração.

## Atualização da carteira

Revise e atualize:

```text
custom_addons/property_portfolio_seed/data/property_asset_silva.xml
```

Ao adicionar ou alterar registros, mantenha IDs XML estáveis sempre que o
imóvel continuar sendo o mesmo. Para uma nova carga em uma base de teste,
instale ou atualize o módulo:

```bash
./.venv/bin/python odoo-bin --conf=odoo.conf -d ms \
  -u property_portfolio_seed --stop-after-init
```

O módulo é opcional e não faz parte do reset padrão. Isso permite iniciar uma
base limpa e carregar a carteira da Silva Empreendimentos somente quando for
necessário.
