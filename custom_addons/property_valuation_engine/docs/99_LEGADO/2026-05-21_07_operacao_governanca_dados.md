# 07 — Operação e Governança dos Dados

## Qualidade dos dados

A qualidade da estimativa depende diretamente da qualidade dos dados cadastrados.

Dados críticos:

- área correta;
- bairro padronizado;
- tipo de uso correto;
- padrão realista;
- conservação atualizada;
- referência m² recente;
- comparáveis coerentes;
- fonte confiável.

## Padronização de bairros

Evitar variações como:

```text
Alphaville
Alphaville Industrial
Alphaville - Barueri
Alphavile
```

Recomendação futura:

- criar cadastro de região/bairro;
- usar geolocalização;
- vincular imóveis a microrregiões.

## Diferença entre preço anunciado e preço fechado

Portais geralmente mostram preço pedido, não preço realizado.

O módulo já prevê o campo:

```text
Negócio fechado interno
```

Comparáveis marcados como negócio fechado recebem peso adicional, pois são mais confiáveis.

## Fontes internas são prioritárias

As melhores fontes são:

- contratos fechados;
- propostas aceitas;
- histórico de locação;
- histórico de vacância;
- reajustes praticados;
- valores efetivamente pagos.

## Fontes externas exigem cuidado

Ao usar portais e pesquisas externas:

- registrar URL;
- registrar data da pesquisa;
- registrar se é venda ou locação;
- registrar se é preço anunciado;
- evitar copiar dados pessoais desnecessários;
- respeitar termos de uso da fonte;
- evitar scraping agressivo sem validação jurídica.

## Revisão mensal recomendada

Rotina sugerida:

1. Atualizar referências m² por região.
2. Inativar referências vencidas.
3. Cadastrar novos comparáveis.
4. Revisar fontes com baixa confiabilidade.
5. Rodar estimativa nos imóveis estratégicos.
6. Comparar valor estimado com valor anunciado/contratado.
7. Aprovar novos valores gerenciais.

## Indicadores recomendados

Dashboards futuros podem mostrar:

- valor estimado total da carteira;
- valor de locação potencial;
- imóveis abaixo do mercado;
- imóveis acima do mercado;
- variação mensal de m² por região;
- confiança média das estimativas;
- quantidade de comparáveis por bairro;
- tempo desde a última estimativa;
- diferença entre valor calculado e valor aprovado.

## Política de aprovação

Sugestão:

| Situação | Aprovação recomendada |
|---|---|
| Ajuste até 5% | Gestor comercial |
| Ajuste de 5% a 15% | Diretoria patrimonial |
| Ajuste acima de 15% | Diretoria + justificativa formal |
| Valor usado em venda relevante | Comitê / Governança |
| Valor usado em laudo formal | Profissional habilitado |

## Dados mínimos para uma boa estimativa

Antes de calcular, idealmente preencher:

- área de valuation;
- cidade;
- bairro;
- tipo de uso;
- padrão;
- conservação;
- pelo menos uma referência m²;
- pelo menos três comparáveis recentes.
