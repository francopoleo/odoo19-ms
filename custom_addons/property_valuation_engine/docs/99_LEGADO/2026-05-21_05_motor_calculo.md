# 05 — Motor de Cálculo e Regras de Valuation

## Objetivo do motor

O motor calcula uma estimativa gerencial de valor para venda ou locação usando:

- área considerada;
- referência de valor por m²;
- comparáveis de mercado;
- fatores de ajuste;
- score de confiança;
- margem de faixa.

## Métodos disponíveis

### 1. Regra simples por m²

Código:

```text
simple_m2
```

Fórmula:

```text
Valor m² selecionado = valor m² da referência
```

Uso recomendado:

- início de implantação;
- poucos comparáveis cadastrados;
- regiões com tabela de referência confiável.

### 2. Comparáveis ponderados

Código:

```text
comparables
```

Fórmula:

```text
Valor m² selecionado = média ponderada dos comparáveis
```

Cada comparável recebe pontuação conforme similaridade.

Critérios de similaridade:

- mesma cidade;
- mesmo bairro;
- mesmo tipo de uso;
- mesmo padrão;
- mesma conservação;
- área parecida;
- negócio interno fechado;
- peso manual.

### 3. Híbrido

Código:

```text
hybrid
```

Fórmula atual:

```text
Valor m² selecionado = referência m² × 55% + comparáveis × 45%
```

Se só existir uma das bases, o sistema usa a base disponível.

Uso recomendado:

- operação enterprise;
- combinação de base interna com pesquisa externa;
- equilíbrio entre referência estável e realidade de mercado.

## Seleção da melhor referência m²

O sistema procura referências compatíveis com:

- empresa atual ou referência global;
- finalidade: venda ou locação;
- valor m² positivo;
- data válida;
- cidade;
- bairro;
- tipo de uso;
- padrão;
- confiança.

Pontuação simplificada:

| Critério | Peso |
|---|---:|
| Mesma cidade | +40 |
| Mesmo bairro | +35 |
| Mesmo tipo de uso | +15 |
| Mesmo padrão | +15 |
| Confiança da referência | até +10 |

## Seleção dos comparáveis

O sistema busca comparáveis ativos com:

- mesma finalidade;
- área maior que zero;
- valor m² positivo;
- mesma empresa ou comparável global.

Depois calcula uma pontuação e seleciona até 12 melhores comparáveis.

Pontuação simplificada:

| Critério | Peso |
|---|---:|
| Mesma cidade | +30 |
| Mesmo bairro | +35 |
| Mesmo tipo de uso | +15 |
| Mesmo padrão | +10 |
| Mesma conservação | +5 |
| Área até 15% de diferença | +15 |
| Área até 30% de diferença | +8 |
| Área até 50% de diferença | +3 |
| Área muito diferente | -10 |
| Negócio interno fechado | +10 |
| Peso manual | multiplica a pontuação |

## Aplicação dos fatores

Após selecionar o valor m² base, o motor aplica multiplicadores:

```text
Valor m² ajustado = valor m² selecionado
                  × fator localização
                  × fator padrão
                  × fator conservação
                  × fator liquidez
                  × fator vacância
```

Depois calcula:

```text
Valor sugerido = valor m² ajustado × área considerada
```

## Faixa de valor

O sistema calcula uma margem com base na confiança.

| Confiança | Margem |
|---:|---:|
| >= 85% | 8% |
| >= 70% | 12% |
| >= 55% | 18% |
| < 55% | 28% |

Exemplo:

```text
Valor sugerido: R$ 25.000
Confiança: 72%
Margem: 12%
Faixa: R$ 22.000 a R$ 28.000
```

## Score de confiança

A confiança considera:

- existência de referência m²;
- confiança da referência;
- quantidade de comparáveis;
- quantidade de negócios internos fechados;
- confiabilidade das fontes;
- cidade preenchida;
- bairro preenchido;
- área preenchida;
- padrão preenchido;
- conservação preenchida.

## Memória de cálculo

Cada execução grava em `calculation_notes`:

- método utilizado;
- área considerada;
- referência usada;
- quantidade de comparáveis;
- valor m² selecionado;
- fatores aplicados;
- valor m² ajustado;
- valor sugerido;
- faixa inferior/superior;
- confiança;
- margem.

## Validações

O sistema não permite:

- área menor ou igual a zero;
- fator menor ou igual a zero;
- valor m² de referência menor ou igual a zero;
- comparável com área menor ou igual a zero;
- comparável com valor total menor ou igual a zero;
- confiança fora de 0 a 100.

## Melhorias futuras no cálculo

Ver também o roadmap, mas os próximos passos naturais são:

- normalização por distância geográfica;
- geocodificação;
- tratamento de outliers;
- pesos configuráveis por empresa;
- regressão hedônica;
- aprendizado com contratos fechados;
- atualização automática por índices;
- cálculo separado entre preço anunciado e preço realizado.
