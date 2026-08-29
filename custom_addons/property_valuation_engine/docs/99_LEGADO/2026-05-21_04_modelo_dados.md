# 04 — Modelo de Dados

## Visão geral dos modelos

O módulo cria os seguintes modelos:

| Modelo | Finalidade |
|---|---|
| `property.valuation.run` | Execução/histórico de estimativa |
| `property.valuation.source` | Fonte dos dados utilizados |
| `property.valuation.factor` | Fatores de ajuste configuráveis |
| `property.price.m2.reference` | Referência de valor por m² |
| `property.market.comparable` | Imóveis comparáveis de mercado |
| `property.valuation.algorithm` | Algoritmos disponíveis |

Também herda:

| Modelo | Alteração |
|---|---|
| `property.asset` | Adiciona campos e botões de valuation |

## `property.valuation.run`

É o registro mais importante do módulo. Cada cálculo gera uma execução independente.

### Campos principais

- `name`: código sequencial;
- `asset_id`: imóvel avaliado;
- `valuation_date`: data da estimativa;
- `valuation_type`: locação ou venda;
- `state`: status do fluxo;
- `algorithm_code`: método usado;
- `area_m2`: área considerada;
- `city`: cidade;
- `neighborhood`: bairro;
- `asset_use_type`: tipo de uso;
- `standard`: padrão;
- `conservation`: conservação;
- `reference_id`: referência m² principal;
- `comparable_ids`: comparáveis usados;
- `source_ids`: fontes usadas;
- `base_price_m2`: valor m² da referência;
- `comparable_price_m2`: valor m² ponderado dos comparáveis;
- `adjusted_price_m2`: valor m² ajustado;
- `calculated_value`: valor sugerido;
- `low_value`: faixa inferior;
- `high_value`: faixa superior;
- `confidence_score`: confiança;
- `approved_value`: valor aprovado;
- `approved_by_id`: aprovador;
- `approved_date`: data da aprovação;
- `calculation_notes`: memória de cálculo.

## `property.valuation.source`

Representa a origem da informação.

Tipos comuns:

- interno;
- portal;
- índice;
- pesquisa manual;
- planilha;
- laudo;
- outro.

Campos relevantes:

- `name`;
- `source_type`;
- `reliability_score`;
- `url`;
- `notes`;
- `company_id`.

## `property.valuation.factor`

Configura multiplicadores para ajuste de valor.

Tipos atuais:

- `standard`: padrão construtivo;
- `conservation`: estado de conservação;
- `location`: localização;
- `liquidity`: liquidez;
- `vacancy`: vacância.

Na carga inicial, o módulo já inclui fatores para:

### Padrão

| Código | Multiplicador |
|---|---:|
| `low` | 0,85 |
| `medium` | 1,00 |
| `high` | 1,15 |
| `premium` | 1,30 |

### Conservação

| Código | Multiplicador |
|---|---:|
| `new` | 1,08 |
| `good` | 1,00 |
| `regular` | 0,92 |
| `needs_renovation` | 0,80 |

## `property.price.m2.reference`

Tabela de referência base.

Campos:

- finalidade: venda ou locação;
- tipo de uso;
- padrão;
- cidade;
- bairro;
- valor m²;
- validade inicial;
- validade final;
- fonte;
- confiança.

## `property.market.comparable`

Cadastro de imóveis comparáveis.

Campos:

- nome;
- imóvel interno relacionado;
- fonte;
- referência externa;
- URL;
- data da pesquisa;
- finalidade;
- tipo de uso;
- padrão;
- conservação;
- cidade;
- bairro;
- endereço/referência;
- área;
- valor total;
- valor m² calculado;
- peso manual;
- indicador de negócio interno fechado.

## `property.valuation.algorithm`

Cadastro dos algoritmos/métodos.

Métodos atuais:

- `simple_m2`;
- `comparables`;
- `hybrid`.

## Relacionamento simplificado

```text
property.asset
   └── property.valuation.run
          ├── property.price.m2.reference
          ├── property.market.comparable
          ├── property.valuation.source
          └── property.valuation.algorithm
```
