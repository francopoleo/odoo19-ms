# Fluxo de Criação e Aplicação de Aditivos

## 1. Preparação

Antes de criar o aditivo, confirme:

- contrato correto;
- partes envolvidas;
- motivo da alteração;
- data de assinatura;
- data de efeito;
- se haverá efeito retroativo;
- se haverá impacto financeiro;
- se haverá alteração de prazo, partes, imóvel, garantia, obrigações ou documentos.

## 2. Criar o aditivo

Acesse:

```text
Imóveis > Aditivos Contratuais > Todos os Aditivos
```

Crie um novo registro e preencha:

| Campo | Como usar |
| --- | --- |
| Nome | Pode ser automático, como `Aditivo 01`, ou descritivo. |
| Contrato | Contrato original que será alterado. |
| Número do Aditivo | Sequencial por contrato. O módulo tenta preencher automaticamente. |
| Tipo de Aditivo | Classificação principal da alteração. |
| Motivo | Catálogo detalhado com motivos padronizados. |
| Escopo | Financeiro, prazo, partes, imóvel/área, cláusula específica ou consolidação ampla. |
| Efeito Econômico | Neutro, acréscimo/a mais, desconto/a menos ou misto. |
| Risco | Baixo, médio, alto ou crítico. |
| Forma de Assinatura | Manual, digital, eletrônica, cartório ou sem assinatura. |
| Data de Efeito | Data a partir da qual a alteração passa a valer. |

## 3. Classificar impactos

O módulo marca alguns impactos automaticamente conforme o tipo do aditivo, mas o usuário pode ajustar conforme a realidade do contrato.

Use os campos de impacto para indicar se o aditivo exige:

- atualização financeira;
- recálculo de cobrança;
- ajuste contábil;
- atualização de partes;
- atualização de prazo;
- atualização de garantia;
- atualização de imóvel ou área.

## 4. Registrar resumo e base jurídica

Na aba **Resumo**, preencha:

- **Resumo do Aditivo:** descrição executiva da mudança.
- **Base Legal/Contratual:** cláusula, negociação, evento, acordo ou fundamento.
- **Cláusulas Afetadas:** cláusulas alteradas ou incluídas.
- **Cláusulas Mantidas:** texto ou observação de que as demais cláusulas permanecem inalteradas.

## 5. Registrar alterações de campos

Na aba **Alterações**, cadastre mudanças que devem ser aplicadas diretamente no cadastro do contrato.

O campo principal agora é **Campo do Contrato**, uma seleção controlada. O usuário não digita mais o campo técnico nem o rótulo. Ao selecionar uma opção, o sistema preenche automaticamente:

- **Categoria da Alteração**;
- **Campo Técnico** interno;
- **Rótulo do Campo**;
- **Tipo de Valor**;
- **Valor Anterior** com base no contrato escolhido.

### Opções disponíveis em Campo do Contrato

| Opção visível | Campo técnico automático | Tipo de valor | Quando usar |
| --- | --- | --- | --- |
| Aluguel base atual | `current_base_rent` | Número | Aumento, redução ou alteração permanente do aluguel-base vigente. |
| Aluguel original | `original_monthly_rent` | Número | Correção ou registro do aluguel original histórico. |
| Início vigente | `current_start_date` | Data | Alteração da data inicial vigente. |
| Fim vigente | `current_end_date` | Data | Prorrogação, redução ou encerramento do prazo. |
| Desconto até | `current_discount_until` | Data | Data final de um desconto temporário. |
| Dia de vencimento vigente | `current_payment_day` | Número | Mudança do dia de vencimento. |
| Índice de reajuste vigente | `current_adjustment_index` | Texto | Mudança para IPCA, IGP-M, INCC, fixo ou sem reajuste. |
| Locatário atual | `current_partner_id` | Contato | Troca, cessão ou substituição de locatário. |
| Locatário original | `original_partner_id` | Contato | Correção do histórico do locatário original. |
| Garantia vigente | `current_guarantee_type` | Texto | Alteração de caução, fiador, seguro-fiança ou outra garantia. |
| Finalidade vigente | `current_purpose` | Texto | Mudança de finalidade de uso do imóvel. |
| Foro vigente | `current_jurisdiction` | Texto | Alteração de foro, comarca ou jurisdição contratual. |
| Status jurídico | `legal_status` | Texto | Atualização controlada do status jurídico do contrato. |
| Status operacional | `operational_status` | Texto | Atualização controlada do status operacional do contrato. |
| Termos consolidados | `consolidated_terms_html` | Texto | Consolidação textual de cláusulas alteradas. |
| Emitido por | `issuer` | Texto | Identificação do emissor do instrumento/documento. |

### Como preencher uma linha

1. Clique em **Adicionar uma linha**.
2. Escolha **Campo do Contrato**.
3. Confira o **Tipo de Valor** e o **Valor Anterior** preenchidos automaticamente.
4. Preencha apenas o campo de novo valor correspondente:
   - **Novo Valor (Número)** para número/valor monetário;
   - **Novo Valor (Data)** para datas;
   - **Novo Contato** para locatário/parceiro;
   - **Novo Valor (Texto)** para texto/código.
5. Informe a **Data de Efeito**.

A aplicação do aditivo grava histórico em **Histórico de Termos**.

## 6. Registrar impacto financeiro

### 6.1 Quando usar Tabela de Valores

Use a aba **Impacto Financeiro > Tabela de Valores** para criar a nova regra de cobrança.

Exemplo de aumento permanente:

1. Tipo de cobrança: `Aluguel-base`.
2. Tipo de valor: `Fixo`.
3. Valor: novo aluguel.
4. Data inicial: início da vigência do novo valor.
5. Recorrente: sim.
6. Status: rascunho até aprovação/aplicação.

Exemplo de desconto temporário:

1. Tipo de cobrança: `Desconto`.
2. Valor: valor do desconto.
3. Data inicial e final: período do desconto.
4. Temporário: sim.
5. Recorrente: sim, se for mensal.

### 6.2 Quando usar Ajustes Financeiros

Use **Ajustes Financeiros** para correções retroativas ou diferenças pontuais.

Exemplo de cobrança a menor:

1. Tipo de ajuste: `Débito por cobrança a menor`.
2. Valor: diferença a cobrar.
3. Período de referência: mês/competência da diferença.
4. Forma de aplicação: próxima fatura, fatura separada ou lançamento manual.

Exemplo de cobrança a maior:

1. Tipo de ajuste: `Crédito por cobrança a maior`.
2. Valor: diferença a devolver/compensar.
3. Forma de aplicação: próxima fatura ou nota de crédito.

## 7. Anexar documentos

Na aba **Documentos**, anexe:

- minuta do aditivo;
- versão final assinada;
- certificado de assinatura;
- notificações;
- documentos de aprovação;
- registros em cartório, se houver;
- documentos de encerramento, quando aplicável.

## 8. Registrar aprovações

Na aba **Aprovações**, registre aprovações necessárias:

- jurídica;
- financeira;
- comercial;
- diretoria;
- risco/conformidade;
- operacional;
- partes externas.

O status pode ser pendente, aprovado, rejeitado ou dispensado.

## 9. Enviar para assinatura

Depois de aprovado:

1. Clique em **Enviar Assinatura**.
2. Atualize documentos e informações de assinatura.
3. Quando finalizado, clique em **Marcar Assinado**.
4. Confira a data de assinatura e o documento final.

## 10. Aplicar ao contrato

Quando estiver aprovado/assinado:

1. Clique em **Pronto para Aplicar**.
2. Clique em **Aplicar ao Contrato**.

Ao aplicar, o módulo:

- aplica alterações de campos no contrato;
- ativa linhas de tabela de valores em rascunho;
- marca efeito retroativo quando a data de efeito é anterior à data atual;
- cria histórico de termos alterados;
- cria versão consolidada do contrato;
- marca o aditivo como aplicado;
- atualiza o status jurídico do contrato para `Aditado`.

## 11. Cancelamento

Use **Cancelar** quando o aditivo não seguirá adiante. Aditivos aplicados não devem ser cancelados sem procedimento administrativo de reversão ou novo aditivo.


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
