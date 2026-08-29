# 08 — Roadmap de Melhorias Futuras

## Fase 1 — Consolidação do MVP

Status: base atual.

Melhorias sugeridas:

- encaixar smart buttons adicionais na ficha do imóvel;
- adicionar filtros favoritos por cidade/bairro;
- adicionar kanban de estimativas por status;
- melhorar relatório PDF da estimativa;
- adicionar campo “preço anunciado” versus “preço fechado”;
- adicionar importação CSV/XLSX de comparáveis;
- adicionar wizard para cálculo em lote.

## Fase 2 — Governança e aprovação avançada

Melhorias:

- fluxo de aprovação em múltiplos níveis;
- trilha de auditoria de alteração do valor aprovado;
- bloqueio de edição após aprovação;
- motivo obrigatório para rejeição;
- motivo obrigatório para ajuste manual acima de percentual;
- integração com módulo de governança/auditoria;
- anexos/documentos da pesquisa de mercado.

## Fase 3 — Dados de mercado

Melhorias:

- importador de planilhas de mercado;
- conectores por API;
- cadastro de índice de mercado;
- histórico mensal por região;
- origem separada por tipo: anúncio, contrato, avaliação, índice;
- expiração automática de comparáveis antigos;
- marcação de outliers.

## Fase 4 — Geolocalização

Melhorias:

- latitude/longitude do imóvel;
- cálculo de distância entre comparáveis;
- microrregiões;
- zonas comerciais;
- polos de atratividade;
- proximidade de transporte;
- proximidade de shopping, hospital, escola, centro logístico etc.

## Fase 5 — Estatística avançada

Melhorias:

- remoção automática de outliers;
- mediana ponderada;
- desvio padrão;
- intervalo de confiança estatístico;
- regressão hedônica;
- calibração por região;
- pesos configuráveis por empresa;
- backtesting com contratos reais.

## Fase 6 — Machine Learning

Melhorias:

- treinamento com histórico interno;
- modelo separado para locação e venda;
- score de liquidez;
- previsão de tempo até locar;
- recomendação de preço para reduzir vacância;
- detecção de imóvel subprecificado;
- detecção de imóvel superprecificado;
- aprendizado com propostas perdidas.

## Fase 7 — Integrações comerciais

Melhorias:

- atualizar valor sugerido em propostas;
- integração com pipeline comercial;
- integração com anúncios;
- integração com CRM;
- alertas para imóveis sem atualização há mais de X dias;
- alertas quando mercado variar mais de X%.

## Fase 8 — Relatórios executivos

Relatórios sugeridos:

- estimativa patrimonial da carteira;
- potencial mensal de locação;
- imóveis com maior gap de preço;
- evolução de valor por região;
- comparativo valor aprovado versus mercado;
- ranking de liquidez;
- ativos com risco de vacância.

## Melhorias técnicas recomendadas

- testes unitários do motor de cálculo;
- testes de instalação em base limpa;
- documentação de dados demo;
- migrações versionadas;
- configuração de pesos por parâmetro;
- separação de serviços de cálculo;
- logs técnicos de cálculo;
- compatibilidade com importadores assíncronos.

## Possível integração com IA

A IA pode ajudar em:

- classificação automática de comparáveis;
- resumo de anúncios;
- extração de área/valor de textos externos;
- justificativa textual da estimativa;
- detecção de inconsistência nos dados;
- sugestão de microrregião;
- análise de liquidez.

A IA não deve aprovar valor final sem revisão humana.
