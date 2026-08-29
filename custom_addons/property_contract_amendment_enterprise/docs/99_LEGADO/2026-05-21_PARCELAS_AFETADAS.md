# Parcelas afetadas por aditivos

Este módulo trata alterações financeiras por aditivo de forma auditável. O objetivo é impedir que uma mudança contratual altere valores de parcelas sem rastreabilidade.

## Conceito central

Quando um aditivo altera aluguel, desconto, acréscimo, carência, crédito, multa, diferença retroativa ou qualquer valor recorrente, o sistema gera registros em **Parcelas Afetadas**.

Cada registro mostra:

- contrato;
- aditivo responsável;
- parcela original;
- período de competência;
- vencimento;
- status da parcela;
- tipo de impacto;
- regra de aplicação;
- valor original;
- novo valor;
- diferença;
- se é retroativo;
- parcela complementar ou crédito gerado, quando aplicável.

## Onde visualizar

### No aditivo

Acesse:

**Imóveis > Aditivos Contratuais > Todos os Aditivos > Aditivo > Parcelas Afetadas**

Nessa aba aparecem todas as parcelas que serão ou foram impactadas pelo aditivo.

### Na parcela

Acesse:

**Imóveis > Aditivos Contratuais > Plano de Cobrança > Parcela > Ajustes por Aditivo**

A parcela mostra os aditivos que alteraram seu valor, o valor original e a diferença aplicada.

### No menu geral

Acesse:

**Imóveis > Aditivos Contratuais > Parcelas Afetadas**

Essa visão consolida todos os impactos financeiros de todos os aditivos.

## Botões do aditivo

### Simular Parcelas

Gera a lista de parcelas afetadas com base nas linhas da **Tabela de Valores** e dos **Ajustes Financeiros** do aditivo.

A simulação não altera a cobrança ainda. Ela apenas mostra o impacto previsto.

### Aplicar Parcelas

Aplica as diferenças simuladas nas parcelas conforme a regra de aplicação.

### Reverter Parcelas

Reverte impactos financeiros aplicados quando tecnicamente possível. Quando o impacto gerou parcela complementar, a parcela complementar é cancelada.

## Regras de aplicação

### Parcela futura ou calculada

Quando a parcela está em **Rascunho** ou **Calculado**, o sistema pode recalcular a própria parcela.

Exemplo:

- valor original: R$ 10.000,00;
- novo aluguel por aditivo: R$ 12.000,00;
- diferença: R$ 2.000,00.

A parcela passa a mostrar:

- Valor Original Antes dos Aditivos: R$ 10.000,00;
- Valor Após Aditivos: R$ 12.000,00;
- Diferença por Aditivos: R$ 2.000,00;
- Alterada por Aditivo: sim.

### Parcela aprovada em aberto

Quando a parcela está **Aprovada**, o sistema pode atualizar a parcela, mas mantendo histórico.

A alteração fica registrada em **Ajustes por Aditivo**.

### Parcela faturada

Quando a parcela está **Faturada**, o sistema não sobrescreve o valor principal. Ele gera uma parcela complementar ou crédito, conforme a diferença.

- diferença positiva: gera parcela complementar;
- diferença negativa: gera crédito.

### Parcela paga

Parcela paga não deve ser alterada. O sistema gera:

- parcela complementar, se houver valor a receber;
- crédito, se houver valor a devolver/descontar.

### Parcela cancelada ou substituída

Não é alterada. O impacto fica ignorado.

## Exemplos

### Aumento de aluguel

Aditivo altera aluguel de R$ 10.000,00 para R$ 12.000,00 a partir de 01/06/2026.

Na Tabela de Valores:

- Tipo de cobrança: Aluguel-base;
- Valor: R$ 12.000,00;
- Data inicial: 01/06/2026;
- Recorrente: sim.

Ao clicar em **Simular Parcelas**, as parcelas futuras dentro do período recebem diferença de R$ 2.000,00.

### Desconto temporário

Aditivo concede desconto de R$ 2.000,00 entre 01/06/2026 e 31/08/2026.

Na Tabela de Valores:

- Tipo de cobrança: Desconto;
- Valor: R$ 2.000,00;
- Data inicial: 01/06/2026;
- Data final: 31/08/2026;
- Temporário: sim.

As parcelas do período recebem diferença negativa de R$ 2.000,00.

### Cobrança retroativa

Aditivo aprovado em junho, com efeito desde abril, gera diferença de R$ 4.000,00.

Em Ajustes Financeiros:

- Tipo: Débito retroativo;
- Valor: R$ 4.000,00;
- Período de referência: abril a maio;
- Forma de aplicação: Próxima fatura ou Fatura separada.

Se as parcelas de abril e maio já estiverem pagas ou faturadas, o sistema gera parcela complementar.

### Crédito retroativo

Aditivo reduz valores já cobrados.

Em Ajustes Financeiros:

- Tipo: Crédito retroativo;
- Valor: R$ 3.000,00;
- Forma de aplicação: Nota de crédito ou próxima fatura.

O sistema cria crédito ou reduz a próxima parcela em aberto, conforme a regra.

## Campos novos na parcela

O plano de cobrança recebeu os seguintes campos:

- **Alterada por Aditivo**;
- **Valor Original Antes dos Aditivos**;
- **Diferença por Aditivos**;
- **Valor Após Aditivos**;
- **Data de Efeito do Aditivo**;
- **Aditivo Aplicado em**;
- **Ajustes por Aditivo**.

## Campos novos no aditivo

O aditivo recebeu:

- **Parcelas Afetadas**;
- **Quantidade de Parcelas Afetadas**;
- **Diferença Total nas Parcelas**;
- **Possui Parcelas Pendentes**.

## Observação importante

Este módulo não altera parcela paga diretamente. Essa é uma decisão de governança e auditoria: parcela paga é documento financeiro histórico. A diferença deve virar crédito ou cobrança complementar.
