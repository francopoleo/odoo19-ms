# Modelo Técnico

## 1. Modelos principais

| Modelo | Descrição |
| --- | --- |
| `property.contract.amendment` | Registro principal do aditivo contratual. |
| `property.contract.amendment.change` | Linhas de alteração de campos do contrato. |
| `property.contract.version` | Versões consolidadas/snapshots do contrato após aplicação. |
| `property.contract.term.history` | Histórico auditável de termos alterados. |
| `property.contract.rent.schedule` | Tabela de valores e regras de cobrança recorrentes ou futuras. |
| `property.contract.billing.plan` | Plano de cobrança por período. |
| `property.contract.billing.line` | Linhas detalhadas do plano de cobrança. |
| `property.contract.financial.adjustment` | Ajustes financeiros pontuais ou retroativos. |
| `property.contract.document` | Documentos contratuais e de assinatura. |
| `property.contract.approval` | Aprovações internas. |
| `property.contract.obligation` | Obrigações contratuais. |
| `property.contract.option` | Opções contratuais. |
| `property.contract.amendment.reason` | Motivos padronizados de aditivo. |
| `property.contract.financial.reason` | Motivos financeiros padronizados. |
| `property.contract.document.type` | Tipos de documentos. |

## 2. Extensão de `property.contract`

O módulo adiciona campos de compatibilidade e consolidação ao contrato:

- empresa e moeda;
- emissor;
- locatário original e atual;
- aluguel original, aluguel-base atual, aluguel efetivo atual, desconto atual e acréscimos atuais;
- início e fim vigentes;
- garantia vigente;
- índice vigente;
- dia de vencimento vigente;
- finalidade vigente;
- foro vigente;
- status jurídico e operacional;
- relações com aditivos, versões, tabela de valores, plano de cobrança, ajustes, documentos, obrigações, opções e histórico.

## 3. Aplicação do aditivo

O método `action_apply` executa:

1. validação para impedir reaplicação;
2. validação do status permitido;
3. aplicação das linhas de alteração no contrato;
4. ativação das linhas financeiras em rascunho;
5. criação de versão consolidada;
6. registro de usuário/data de aplicação;
7. atualização do status jurídico do contrato para `Aditado`.

## 4. Regras financeiras

A tabela de valores calcula o aluguel efetivo atual a partir de:

```text
aluguel efetivo = aluguel-base - descontos + acréscimos
```

Os ajustes financeiros não substituem a tabela de valores. Eles servem para corrigir diferenças pontuais, retroativas ou acordos.

## 5. Pontos de evolução recomendados

- Reativar uma aba de aditivos dentro do formulário do contrato após estabilizar a view base de `property_core`.
- Criar geração automática de minuta do aditivo a partir de templates.
- Criar integração com provedor de assinatura eletrônica.
- Criar geração automática do plano de cobrança a partir da tabela de valores.
- Criar assistente/wizard para aditivos financeiros com validação de período e simulação de impacto.
- Criar permissões mais granulares para operador somente leitura, jurídico, financeiro e gestor.


## Seleção controlada de campos contratuais

O modelo `property.contract.amendment.change` possui o campo `field_key`, uma seleção controlada baseada na constante `CONTROLLED_CONTRACT_FIELD_OPTIONS`.

Quando `field_key` é preenchido, o módulo sincroniza automaticamente:

- `field_name`: nome técnico aplicado no `contract.write()`;
- `field_label`: rótulo amigável gravado no histórico;
- `value_type`: tipo de valor esperado;
- `change_category`: categoria funcional da alteração.

A sincronização ocorre em `create()`, `write()` e `onchange`, evitando que integrações, importações ou edição em lista gravem metadados inconsistentes.


## Controle enterprise de parcelas afetadas

A partir da versão 19.0.1.5.0, o módulo possui controle de parcelas afetadas por aditivos. O fluxo financeiro completo está documentado em `docs/PARCELAS_AFETADAS.md`.

Resumo do fluxo:

1. cadastrar o aditivo;
2. informar as alterações contratuais e a tabela de valores;
3. registrar ajustes financeiros retroativos, quando existirem;
4. clicar em **Simular Parcelas**;
5. revisar a aba **Parcelas Afetadas**;
6. clicar em **Aplicar Parcelas** ou aplicar o aditivo completo;
7. consultar cada parcela em **Plano de Cobrança > Ajustes por Aditivo**.

As parcelas pagas ou faturadas não são sobrescritas. O sistema gera parcela complementar ou crédito para preservar a auditoria.
