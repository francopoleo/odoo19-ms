# 01 — Visão Geral

## Nome técnico

`property_valuation_engine`

## Nome funcional

**Motor de Estimativa de Valor Imobiliário**

## Dependência principal

`property_core`

O módulo foi criado como complemento do núcleo imobiliário. Ele não substitui o `property_core`; ele herda o cadastro de imóveis e adiciona uma camada de análise, precificação e histórico de estimativas.

## Problema que o módulo resolve

Em uma operação imobiliária enterprise, o valor de venda ou locação não pode depender apenas de opinião manual, histórico informal ou pesquisa isolada. O sistema precisa manter uma memória estruturada de:

- valor por m² por região;
- padrão construtivo;
- conservação;
- imóveis comparáveis;
- fontes de dados;
- estimativas anteriores;
- aprovações gerenciais;
- justificativa do valor sugerido.

## Conceito central

O módulo calcula uma **faixa sugerida de valor** para venda ou locação de um imóvel.

Ele trabalha com três resultados principais:

- **valor sugerido**;
- **faixa inferior**;
- **faixa superior**;
- **score de confiança**.

A faixa é mais importante do que um valor único, porque o mercado imobiliário trabalha com intervalo provável, negociação, liquidez e percepção de valor.

## Escopo funcional atual

O módulo inclui:

- referências de valor por m²;
- fontes de dados;
- fatores de ajuste;
- imóveis comparáveis;
- cálculo por m² simples;
- cálculo por comparáveis ponderados;
- cálculo híbrido;
- histórico auditável;
- aprovação e rejeição;
- multiempresa;
- menus integrados ao `property_core`.

## O que o módulo não faz nesta versão

A versão atual ainda não faz:

- scraping automático de portais imobiliários;
- integração oficial com FipeZAP, DataZap ou APIs externas;
- regressão estatística avançada;
- IA preditiva treinada com histórico;
- geração de laudo técnico oficial;
- integração direta com anúncios externos.

Esses pontos estão previstos no roadmap.

## Localização no menu

O módulo aparece em:

```text
Imóveis > Valuation
```

Estrutura funcional:

```text
Imóveis
 └── Valuation
     ├── Operações
     │   ├── Imóveis para Valuation
     │   └── Estimativas
     ├── Mercado
     │   ├── Referências m²
     │   └── Comparáveis
     └── Configuração
         ├── Fontes
         ├── Fatores
         └── Algoritmos
```

## Princípio enterprise adotado

O valor final nunca deve ser apenas um número calculado. Cada estimativa precisa responder:

1. Qual imóvel foi avaliado?
2. Em qual data?
3. Com qual método?
4. Com qual área?
5. Com qual referência m²?
6. Quais comparáveis foram usados?
7. Quais fatores alteraram o valor?
8. Qual foi a confiança?
9. Quem aprovou?
10. Qual justificativa foi registrada?
