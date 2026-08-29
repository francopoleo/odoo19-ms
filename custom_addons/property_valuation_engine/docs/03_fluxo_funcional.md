# 03 — Fluxo Funcional de Uso

## Fluxo resumido

```text
Cadastrar fonte
   ↓
Cadastrar referência m²
   ↓
Cadastrar comparáveis de mercado
   ↓
Preencher dados de valuation no imóvel
   ↓
Calcular estimativa de locação ou venda
   ↓
Revisar memória de cálculo
   ↓
Aprovar ou rejeitar
   ↓
Usar valor aprovado como referência gerencial
```

## 1. Configurar fontes

Menu:

```text
Imóveis > Valuation > Configuração > Fontes
```

Exemplos de fontes:

- contrato interno fechado;
- pesquisa manual;
- portal imobiliário;
- FipeZAP;
- DataZap;
- laudo interno;
- planilha importada;
- avaliação bancária;
- pesquisa de concorrente.

Campos importantes:

- nome;
- tipo da fonte;
- confiabilidade;
- URL;
- empresa.

## 2. Configurar referências m²

Menu:

```text
Imóveis > Valuation > Mercado > Referências m²
```

Uma referência m² representa um valor base para uma combinação de:

- cidade;
- bairro/região;
- finalidade: venda ou locação;
- tipo de uso;
- padrão;
- período de validade;
- fonte.

Exemplo:

```text
Barueri / Alphaville
Locação
Comercial
Padrão alto
R$ 55,00/m²
Confiança: 80%
```

## 3. Cadastrar comparáveis

Menu:

```text
Imóveis > Valuation > Mercado > Comparáveis
```

Um comparável pode ser:

- imóvel interno já locado;
- proposta recebida;
- imóvel anunciado em portal;
- pesquisa de mercado;
- dado importado de planilha;
- negócio fechado.

Campos principais:

- título;
- cidade;
- bairro;
- tipo de uso;
- padrão;
- conservação;
- área;
- valor total;
- valor por m² calculado;
- peso manual;
- fonte;
- data da pesquisa;
- URL.

## 4. Preencher aba de valuation no imóvel

No imóvel, revisar:

- área considerada;
- cidade;
- bairro;
- tipo de uso;
- padrão;
- conservação;
- fator localização;
- fator liquidez;
- fator vacância.

Se a área específica de valuation não for preenchida, o motor tenta localizar campos de área existentes no `property_core`, como `area_m2`, `area`, `built_area` ou `total_area`.

## 5. Calcular estimativa

No imóvel, usar os botões:

- **Calcular locação**;
- **Calcular venda**.

O sistema cria um registro em `property.valuation.run`, calcula os valores e abre a tela da estimativa.

## 6. Revisar resultado

A estimativa apresenta:

- valor m² base;
- valor m² por comparáveis;
- valor m² ajustado;
- valor sugerido;
- faixa inferior;
- faixa superior;
- confiança;
- comparáveis usados;
- fontes usadas;
- memória de cálculo.

## 7. Aprovar ou rejeitar

Estados disponíveis:

```text
Rascunho > Calculado > Revisado > Aprovado
                         ↓
                      Rejeitado
```

A aprovação grava:

- valor aprovado;
- usuário aprovador;
- data de aprovação;
- status aprovado.

## 8. Uso gerencial do valor aprovado

O valor aprovado pode ser usado como base futura para:

- proposta comercial;
- anúncio;
- negociação;
- revisão de aluguel;
- análise patrimonial;
- relatório executivo;
- comparação com contratos vigentes;
- estudo de vacância;
- decisão de venda ou retenção.
