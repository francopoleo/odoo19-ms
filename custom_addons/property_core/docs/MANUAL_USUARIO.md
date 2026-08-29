# Manual do Usuário — Sistema de Gestão Imobiliária
### Silva Empreendimentos | Property Core v19.0.2.3.0

---

## Índice

1. [Visão Geral do Sistema](#1-visão-geral-do-sistema)
2. [Dashboard](#2-dashboard)
3. [Portfólio de Imóveis](#3-portfólio-de-imóveis)
4. [Proprietários](#4-proprietários)
5. [Contratos de Locação](#5-contratos-de-locação)
6. [Parcelas de Aluguel](#6-parcelas-de-aluguel)
7. [Corretores e Mandatos](#7-corretores-e-mandatos)
8. [Comissões](#8-comissões)
9. [Manutenções](#9-manutenções)
10. [Vistorias](#10-vistorias)
11. [Documentos](#11-documentos)
12. [Pipeline de Aquisição](#12-pipeline-de-aquisição)
13. [Leads](#13-leads)
14. [Relatórios](#14-relatórios)
15. [Portal do Proprietário](#15-portal-do-proprietário)
16. [Integração Contábil](#16-integração-contábil)

---

## 1. Visão Geral do Sistema

O **Property Core** é um sistema completo de gestão imobiliária integrado ao Odoo 19. Ele cobre todo o ciclo de vida de imóveis: desde a captação e aquisição, passando pela locação e gestão operacional, até o fechamento financeiro com o proprietário.

### Fluxo Principal

```
CAPTAÇÃO          LOCAÇÃO              OPERAÇÃO           FINANCEIRO
─────────────     ──────────────────   ─────────────────  ──────────────
Lead/Oportunidade → Mandato Corretor → Manutenções        Parcelas
        ↓                 ↓            Vistorias       →  Pagamentos
  Aquisição        Contrato Ativo      Documentos      →  Lançamento Contábil
        ↓                 ↓                               Comissões
   Novo Imóvel     Parcelas Mensais                    →  Extrato Proprietário
```

### Perfis de Usuário

| Perfil | Responsabilidades |
|---|---|
| **Gestor** | Dashboard, relatórios, configurações, visão estratégica |
| **Operacional** | Contratos, parcelas, manutenções, vistorias |
| **Corretor** | Leads, mandatos, acompanhamento de comissões |
| **Proprietário** | Acesso ao portal para ver imóveis e extratos |

---

## 2. Dashboard

**Acesso**: Imóveis → Dashboard

O dashboard é a tela inicial com todos os KPIs do portfólio. Os valores são calculados em tempo real.

### Seções do Dashboard

#### ALERTAS (topo — itens que precisam atenção imediata)

| Indicador | Descrição | Ação recomendada |
|---|---|---|
| Contratos a vencer (30d) | Contratos que vencem nos próximos 30 dias | Contatar locatário para renovação |
| Parcelas atrasadas | Total de parcelas com status Atrasado | Acionar régua de cobrança |
| Emergências abertas | Manutenções de emergência não resolvidas | Despachar equipe técnica |
| Documentos vencidos | Documentos com validade expirada | Solicitar renovação |
| Mandatos a vencer (7d) | Mandatos de corretor expirando em 7 dias | Renovar ou encerrar |

> **Dica**: Clique em qualquer card de alerta para ir direto à lista filtrada.

#### Portfólio de Imóveis

Mostra o total de imóveis por status:
- **Total**: todos os imóveis cadastrados
- **Alugados**: com contrato ativo
- **Disponíveis**: prontos para locação
- **Manutenção**: imóveis em reforma/manutenção
- **À Venda**: imóveis disponíveis para venda

#### Contratos

- **Ativos**: contratos em vigor
- **A Vencer**: dentro do prazo de alerta (padrão: 60 dias)
- **Em Renovação**: em processo de renovação
- **Inadimplentes**: com parcelas vencidas ≥ 30 dias

#### Financeiro

| KPI | Significado |
|---|---|
| Receita Mensal | Soma dos aluguéis de todos os contratos ativos |
| Recebido no Mês | Total efetivamente pago no mês corrente |
| Em Aberto | Total de parcelas abertas/parciais |
| Atrasado | Total de parcelas com status Atrasado |
| % Inadimplência | (Parcelas atrasadas / Total em aberto) × 100 |

#### Corretores & Proprietários

- **Proprietários**: total de proprietários ativos
- **Corretores Ativos**: corretores com status ativo
- **Mandatos Ativos**: mandatos em vigor
- **Comissões Pendentes**: valor total aguardando pagamento

---

## 3. Portfólio de Imóveis

**Acesso**: Imóveis → Portfólio → Imóveis

### 3.1 Cadastro de Imóvel

Campos obrigatórios:
- **Nome**: identificação do imóvel (ex: `Apartamento Centro 101`)
- **Tipo**: Apartamento, Casa, Comercial, Terreno, etc.

Campos importantes:
- **Proprietário**: vínculo com `property.owner`
- **Valor de Locação**: aluguel sugerido (pré-preenche o contrato)
- **Valor de Mercado**: usado no cálculo do yield% no relatório de rentabilidade
- **Status**: Disponível, Alugado, Manutenção, À Venda, Inativo

### 3.2 Custos Fixos do Imóvel

Preencha para que o cálculo de rentabilidade seja preciso:
- **IPTU Anual**: imposto predial
- **Foro Anual**: taxa de aforamento (imóveis foreiros)
- **Condomínio Mensal**: taxa condominial

O campo **Custo Anual Total** é calculado automaticamente:
```
Custo Anual = IPTU + Foro + (Condomínio × 12)
```

### 3.3 Status do Imóvel

| Status | Descrição | Quando ocorre |
|---|---|---|
| `Disponível` | Pronto para locação | Padrão inicial / após encerrar contrato |
| `Alugado` | Com contrato ativo | Automaticamente ao ativar contrato |
| `Manutenção` | Em reforma | Manual |
| `À Venda` | Disponível para venda | Manual |
| `Inativo` | Não disponível | Manual |

> **Automação**: Ao ativar um contrato, o imóvel vai para `Alugado`. Ao encerrar o contrato, volta para `Disponível` (se não houver outros contratos ativos).

---

## 4. Proprietários

**Acesso**: Imóveis → Proprietários

### 4.1 Cadastro

Campos principais:
- **Nome** + **CPF/CNPJ**
- **Contato / Acesso Portal**: parceiro Odoo vinculado (para acesso ao portal)
- **Dados bancários**: Banco, Agência, Conta, **Chave PIX**

### 4.2 Indicadores Financeiros (calculados automaticamente)

| Campo | Fórmula |
|---|---|
| Total de Imóveis | Contagem de imóveis vinculados |
| Contratos Ativos | Contratos ativos nos imóveis do proprietário |
| Receita Mensal Bruta | Soma dos aluguéis dos contratos ativos |
| Custos Anuais | Soma dos custos anuais de todos os imóveis |
| **Resultado Mensal Líquido** | Receita Mensal − (Custos Anuais ÷ 12) |

### 4.3 Extrato Mensal

1. Abra o proprietário
2. Clique em **Gerar Extrato**
3. Informe o período (De/Até)
4. Clique em **Imprimir Extrato**

O PDF inclui: aluguéis recebidos, comissões pagas, custos de manutenção, custos fixos pro-rata, **resultado líquido**.

---

## 5. Contratos de Locação

**Acesso**: Imóveis → Contratos → Contratos

### 5.1 Ciclo de Vida do Contrato

```
Rascunho → Ativo → A Vencer → Em Renovação → Encerrado
                ↘ Atrasado/Vencido
                ↘ Inadimplente
```

| Status | Descrição |
|---|---|
| `Rascunho` | Em elaboração, ainda não gerou parcelas |
| `Ativo` | Vigente, parcelas geradas |
| `A Vencer` | Dentro do período de alerta (padrão: 60 dias antes do vencimento) |
| `Em Renovação` | Processo de renovação iniciado |
| `Atrasado/Vencido` | Data fim ultrapassada |
| `Inadimplente` | Parcela em atraso ≥ 30 dias |
| `Encerrado` | Finalizado |

### 5.2 Criação e Ativação

**Criar contrato**:
1. Preencha: Tipo, Imóvel, Locatário, Datas, Aluguel Mensal
2. (Opcional) Vincule Corretor e Mandato
3. (Opcional) Configure Reajuste (IPCA, IGP-M, percentual fixo)
4. Salve como **Rascunho**

**Ativar contrato** (botão "Ativar Contrato"):
- Gera todas as parcelas mensais automaticamente
- Muda status do imóvel para `Alugado`
- Se houver corretor vinculado, cria comissão de locação automaticamente

### 5.3 Reajuste de Aluguel

- **Índice**: IPCA, IGP-M, INCC ou Percentual Fixo
- **Período**: a cada N meses (padrão: 12)
- O sistema calcula a **próxima data de reajuste** automaticamente

Para aplicar um reajuste, use o smart button **Reajustes** e crie um novo registro.

### 5.4 Configuração Contábil por Contrato

Na seção **Contabilidade** do contrato:
- **Diário Contábil**: sobrepõe o padrão da empresa para este contrato
- **Conta de Receita**: conta específica para as receitas deste contrato

Se vazio, usa o padrão configurado em **Configurações → Contabilidade → Imóveis**.

---

## 6. Parcelas de Aluguel

**Acesso**: Imóveis → Contratos → Parcelas de Aluguel

### 6.1 Ciclo de Vida da Parcela

```
Rascunho → Em Aberto → Parcialmente Pago → Pago
                    ↘ Atrasado
                    ↘ Cancelado
```

### 6.2 Registrar Pagamento

1. Abra a parcela (status `Em Aberto` ou `Atrasado`)
2. Preencha:
   - **Valor Pago**: valor recebido
   - **Data de Pagamento**: data do recebimento
   - **Forma de Pagamento**: PIX, Transferência, Boleto, Dinheiro, Cheque
3. Clique em **Registrar Pagamento**

**Pagamento total** (valor pago ≥ valor a pagar):
- Status → `Pago`
- Lançamento contábil gerado automaticamente

**Pagamento parcial** (valor pago < valor a pagar):
- Status → `Parcialmente Pago`
- Sem lançamento contábil (aguarda pagamento total)

### 6.3 Ajustes da Parcela

Antes de registrar o pagamento, é possível ajustar:
- **Desconto**: reduz o valor a pagar
- **Multa**: aumenta o valor a pagar (para atrasos)
- **Juros**: acréscimo por atraso

### 6.4 Régua de Inadimplência (automática)

O cron diário verifica parcelas vencidas e aplica:

| Prazo | Ação |
|---|---|
| D+1 | Nota interna no chatter |
| D+5 | E-mail enviado ao locatário |
| D+15 | Atividade urgente criada para o responsável |
| D+30 | Contrato marcado como `Inadimplente` |

---

## 7. Corretores e Mandatos

### 7.1 Cadastro de Corretor

**Acesso**: Imóveis → Corretores → Corretores

Campos principais:
- **Nome**, **CRECI**, **E-mail**, **Telefone**
- **Taxa de Comissão (%)**: usada para calcular comissões automaticamente
- **Status**: Ativo/Inativo

### 7.2 Mandato de Corretor

**Acesso**: Imóveis → Corretores → Mandatos

O mandato formaliza a exclusividade de um corretor para um imóvel.

**Campos importantes**:
- **Imóvel** + **Corretor**
- **Tipo**: Locação, Venda, ou Ambos
- **Exclusividade**: se marcado, impede outro mandato ativo do mesmo tipo para o mesmo imóvel
- **Datas**: início e fim do mandato

**Regra de exclusividade**:
> Se tentar criar um mandato exclusivo para um imóvel que já tem mandato exclusivo ativo do mesmo tipo (com datas sobrepostas), o sistema bloqueia com erro de validação.

**Status do mandato** (calculado automaticamente):
| Status | Condição |
|---|---|
| `Ativo` | Dentro do período, não convertido |
| `Expirado` | Após a data fim |
| `Convertido` | Gerou um contrato |
| `Cancelado` | Cancelado manualmente |

### 7.3 Vincular Mandato ao Contrato

No contrato, selecione o **Mandato**. O corretor é preenchido automaticamente.

Ao **ativar o contrato**, o mandato é automaticamente marcado como `Convertido`.

---

## 8. Comissões

**Acesso**: Imóveis → Corretores → Comissões

### 8.1 Criação Automática

Comissões são criadas automaticamente em dois momentos:

| Evento | Tipo | Cálculo |
|---|---|---|
| Ativar contrato com corretor | Locação | Taxa% × Valor Total do Contrato |
| Fechar aquisição com corretor | Venda | Taxa% × Valor de Compra |

### 8.2 Status da Comissão

| Status | Descrição |
|---|---|
| `Pendente` | Aguardando pagamento |
| `Pago` | Comissão paga |
| `Cancelado` | Cancelada manualmente |

### 8.3 Registrar Pagamento

1. Abra a comissão
2. Informe a **Data de Pagamento**
3. Clique em **Marcar como Pago**

> O dashboard atualiza automaticamente os contadores de comissões pendentes.

---

## 9. Manutenções

**Acesso**: Imóveis → Operações → Manutenções

### 9.1 Tipos de Manutenção

| Tipo | Descrição |
|---|---|
| `Preventiva` | Manutenção programada |
| `Corretiva` | Reparo de defeito |
| `Emergência` | Situação urgente |
| `Reforma` | Obra de melhoria |

> **Alerta**: Manutenções do tipo `Emergência` aparecem destacadas no Dashboard → ALERTAS.

### 9.2 Fluxo de Estados

```
Aberto → Aprovado → Em Execução → Concluído
       ↘ Cancelado
```

### 9.3 Campos de Custo

- **Custo Estimado**: orçamento inicial
- **Custo Real**: valor final após conclusão

Os custos de manutenção são incluídos no **Extrato do Proprietário**.

---

## 10. Vistorias

**Acesso**: Imóveis → Operações → Vistorias

### 10.1 Tipos de Vistoria

| Tipo | Quando realizar |
|---|---|
| `Entrada` | No início do contrato |
| `Saída` | No encerramento do contrato |
| `Periódica` | Vistorias de rotina durante o contrato |
| `Especial` | Situações específicas |

### 10.2 Fluxo de Estados

```
Agendada → Confirmada → Concluída
         ↘ Cancelada
```

### 10.3 Checklist (campo Observações)

Use as observações para registrar o estado dos cômodos, equipamentos e eventuais divergências.

---

## 11. Documentos

**Acesso**: Imóveis → Operações → Documentos

### 11.1 Controle de Validade

O sistema monitora automaticamente documentos com validade:

| Status | Condição |
|---|---|
| `Válido` | Dentro da validade |
| `A Vencer` | Dentro dos próximos 30 dias |
| `Vencido` | Validade ultrapassada |

> O cron diário atualiza os status automaticamente.
> Dashboard → ALERTAS mostra **Documentos Vencidos** em tempo real.

### 11.2 Tipos de Documento

Exemplos: Contrato Assinado, Laudo de Vistoria, IPTU, Habite-se, RGI, Seguro, Procuração.

---

## 12. Pipeline de Aquisição

**Acesso**: Imóveis → Pipeline → Aquisições

### 12.1 Estágios do Pipeline

```
Prospecção → Análise → Negociação → Due Diligence → Fechamento → Fechado
           ↘ Cancelado
```

### 12.2 Fechar Negócio

Ao clicar em **Fechar Negócio**:
1. Estágio → `Fechado`
2. Um novo **imóvel** é criado automaticamente no portfólio
3. Uma **comissão de venda** é criada para o corretor vinculado

### 12.3 Campos Financeiros

- **Valor de Oferta**: proposta feita
- **Valor de Compra**: valor final negociado
- **Custo de Aquisição**: despesas adicionais (ITBI, cartório, etc.)

---

## 13. Leads

**Acesso**: Imóveis → Pipeline → Leads

Leads são oportunidades de negócio ainda não qualificadas. Podem ser:
- Imóveis para captação (tornar-se proprietário)
- Interessados em alugar (tornar-se locatário)
- Parceiros corretores

Vincule o **Corretor** responsável pelo atendimento do lead.

---

## 14. Relatórios

### 14.1 Como Gerar Relatórios

Todos os relatórios são gerados pelo menu **Imprimir** dentro das listas ou formulários.

| Relatório | Onde Gerar | Modelo |
|---|---|---|
| Contrato de Locação | Contrato → Imprimir | `property.contract` |
| Extrato do Proprietário | Proprietário → Gerar Extrato | `property.owner` |
| Carteira de Imóveis | Imóveis (lista) → Imprimir → Carteira | `property.asset` |
| Inadimplência | Contratos (lista) → Imprimir → Inadimplência | `property.contract` |
| Rentabilidade | Imóveis (lista) → Imprimir → Rentabilidade | `property.asset` |

### 14.2 Relatório de Carteira de Imóveis

**O que mostra**:
- Resumo de status (totais por categoria)
- Tabela com: Referência, Nome, Tipo, Cidade, Proprietário, Área, Aluguel Atual, Custo Anual, Status
- Totais de aluguel e custo no rodapé

### 14.3 Relatório de Inadimplência

**O que mostra**:
- KPIs no topo: quantidade de contratos inadimplentes, total em aberto, inadimplentes vs atrasados
- Tabela ordenada por valor em aberto (maior primeiro)
- Campos: Contrato, Imóvel, Locatário, Vencimento, Parcelas Atrasadas, Valor em Aberto, Status

> **Dica**: Filtre por status `Inadimplente` ou `Atrasado` antes de gerar o relatório para resultados mais focados.

### 14.4 Relatório de Rentabilidade

**O que mostra**:
- Por imóvel: Valor de Mercado, Aluguel/mês, Custo/mês, Líquido/mês, **Yield Anual**
- Yield colorido: 🟢 Verde ≥ 6% | 🟠 Laranja 4–6% | 🔴 Vermelho < 4%
- Totais no rodapé

**Fórmula do Yield**:
```
Yield Anual (%) = (Aluguel Mensal × 12) / Valor de Mercado × 100
```

---

## 15. Portal do Proprietário

### 15.1 Acesso

URL: `http://seu-odoo/my/properties`

O proprietário faz login com o usuário do portal vinculado ao registro `property.owner`.

### 15.2 O que o Proprietário Vê

**Página inicial** (`/my/properties`):
- Cards de KPIs: total de imóveis, alugados, receita mensal, pendências
- Lista de imóveis com foto, status e badge colorido

**Detalhe do imóvel** (`/my/properties/{id}`):
- Dados completos do imóvel
- Tabela de contratos ativos com valores e datas

### 15.3 Configurar Acesso

1. Crie o proprietário em **Imóveis → Proprietários**
2. Vincule um `res.partner` no campo **Contato / Acesso Portal**
3. No parceiro: **Ação → Conceder Acesso ao Portal**
4. O proprietário recebe e-mail com credenciais de acesso

---

## 16. Integração Contábil

### 16.1 Como Funciona

Ao registrar o **pagamento total** de uma parcela, o sistema cria automaticamente um **lançamento contábil** (`account.move`) no Odoo:

```
DÉBITO  │ Conta do Diário (Banco/Caixa)     │ R$ valor_pago
CRÉDITO │ Conta de Receita de Aluguéis      │ R$ valor_pago
```

O lançamento é postado (validado) automaticamente.

### 16.2 Ver o Lançamento

Na parcela paga: clique no smart button **Lançamento Contábil**.

Você verá o `account.move` com:
- **Tipo**: Lançamento Contábil (entry)
- **Status**: Lançado
- **Data**: data do pagamento
- **Referência**: número da parcela
- **Linhas**: débito na conta do diário + crédito na conta de receita

### 16.3 Estorno ao Cancelar

Se cancelar uma parcela que já foi paga:
- O `account.move` é automaticamente cancelado (revertido)
- Garante que a contabilidade permaneça consistente

### 16.4 Sem Configuração (fallback)

Se o diário e a conta de receita não estiverem configurados (nem no contrato nem nas configurações da empresa), o pagamento é registrado normalmente **mas sem gerar lançamento contábil**. Uma nota de aviso é adicionada ao chatter da parcela.

### 16.5 Reconciliação Bancária

Para reconciliar os pagamentos com o extrato bancário:
1. **Contabilidade → Banco e Caixa → Extratos Bancários**
2. Importe o extrato (OFX, XLSX, etc.) via `base_accounting_kit`
3. O sistema sugere reconciliação automática com os lançamentos gerados pelas parcelas

---

## Atalhos e Dicas Rápidas

| Ação | Caminho |
|---|---|
| Ver todas as parcelas atrasadas | Dashboard → card "Parcelas atrasadas" |
| Ver imóveis disponíveis | Dashboard → card "Disponíveis" |
| Gerar comissão manualmente | Imóveis → Corretores → Comissões → Novo |
| Forçar vencimento de contrato | Contrato → botão "Marcar como Atrasado" |
| Ver histórico de um imóvel | Imóvel → chatter (aba Comunicações) |
| Exportar lista para Excel | Qualquer lista → ⚙️ → Exportar |

---

## Glossário

| Termo | Definição |
|---|---|
| **Yield** | Rentabilidade anual do imóvel em % sobre o valor de mercado |
| **Mandato** | Autorização formal do proprietário para o corretor atuar |
| **Exclusividade** | Direito único do corretor de intermediar negócio por período |
| **Régua de Inadimplência** | Sequência automática de ações após vencimento de parcela |
| **Caução** | Depósito de garantia pago pelo locatário |
| **Foro** | Taxa anual de aforamento em imóveis foreiros |
| **Reajuste** | Atualização periódica do valor do aluguel por índice inflacionário |
| **PDC** | Cheque Pré-Datado (Post-Dated Check) |
| **Lançamento Contábil** | Registro de débito/crédito gerado na contabilidade do Odoo |