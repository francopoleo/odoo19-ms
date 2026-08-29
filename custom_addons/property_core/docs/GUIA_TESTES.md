# Guia de Testes — Fluxos Completos

> **Como usar este guia**: cada fluxo é independente e pode ser executado na ordem apresentada.
> Siga cada passo exatamente e verifique os resultados esperados ao final de cada etapa.
> Use o banco de dados de **homologação/teste**, nunca produção.

---

## FLUXO 1 — Configuração Base (executar primeiro)

### Passo 1.1 — Configurar Contabilidade

1. Acesse **Configurações → Contabilidade → Imóveis**
2. Preencha:
   - **Diário**: selecione `Banco` ou `Caixa`
   - **Conta de Receita**: selecione ou crie `3.1.1 - Receita de Aluguéis`
3. Salve

**✅ Resultado esperado**: Campos salvos sem erro.

---

### Passo 1.2 — Criar Proprietário

1. Acesse **Imóveis → Proprietários → Novo**
2. Preencha:
   - **Nome**: `João Silva Proprietário`
   - **CPF/CNPJ**: `123.456.789-00`
   - **E-mail**: `joao@teste.com`
   - **Chave PIX**: `joao@teste.com`
3. Salve

**✅ Resultado esperado**: Registro salvo com referência `PROP-OWN/0001`.

---

### Passo 1.3 — Criar Corretor

1. Acesse **Imóveis → Corretores → Corretores → Novo**
2. Preencha:
   - **Nome**: `Carlos Corretor`
   - **CRECI**: `12345-SP`
   - **Taxa de Comissão**: `5.00`
   - **E-mail**: `carlos@teste.com`
3. Salve

**✅ Resultado esperado**: Registro salvo com referência `COR/0001`.

---

### Passo 1.4 — Criar Imóvel

1. Acesse **Imóveis → Portfólio → Imóveis → Novo**
2. Preencha:
   - **Nome**: `Apartamento Centro 101`
   - **Tipo**: `Apartamento`
   - **Proprietário**: `João Silva Proprietário`
   - **Endereço/Cidade**: `Barueri`
   - **Área Útil**: `75`
   - **Valor de Locação**: `2.500,00`
   - **Valor de Mercado**: `400.000,00`
   - **IPTU Anual**: `1.200,00`
   - **Status**: `Disponível`
3. Salve

**✅ Resultado esperado**:
- Imóvel salvo com referência `IMP/2025/0001`
- Smart button **Proprietário** mostra `João Silva`
- Stats do proprietário atualizam: `asset_count = 1`

---

## FLUXO 2 — Mandato e Contrato de Locação

### Passo 2.1 — Criar Mandato de Corretor

1. Acesse **Imóveis → Corretores → Mandatos → Novo**
2. Preencha:
   - **Imóvel**: `Apartamento Centro 101`
   - **Corretor**: `Carlos Corretor`
   - **Tipo**: `Locação`
   - **Exclusividade**: `✓ Ativado`
   - **Início**: hoje
   - **Fim**: hoje + 90 dias
3. Salve

**✅ Resultado esperado**:
- Mandato salvo com referência `ASN/0001`
- Status calculado: `Ativo`
- Smart button no imóvel mostra `1 Mandato`
- Smart button no corretor mostra `1 Mandato`

---

### Passo 2.2 — Testar Exclusividade (deve falhar)

1. **Imóveis → Corretores → Mandatos → Novo**
2. Preencha:
   - **Imóvel**: `Apartamento Centro 101` (mesmo imóvel)
   - **Corretor**: crie um segundo corretor qualquer
   - **Tipo**: `Locação`
   - **Exclusividade**: `✓ Ativado`
   - Datas sobrepostas com o mandato anterior
3. Tente salvar

**✅ Resultado esperado**: Erro de validação `"Já existe mandato exclusivo ativo para este imóvel"`

---

### Passo 2.3 — Criar Locatário

1. **Contatos → Novo**
2. Preencha:
   - **Nome**: `Maria Locatária`
   - **E-mail**: `maria@locataria.com`
   - **Telefone**: `(11) 99999-9999`
3. Salve

---

### Passo 2.4 — Criar Contrato de Locação

1. **Imóveis → Contratos → Contratos → Novo**
2. Preencha:
   - **Nome**: `Contrato APT-101 Maria`
   - **Tipo**: `Residencial`
   - **Imóvel**: `Apartamento Centro 101`
   - **Locatário**: `Maria Locatária`
   - **Corretor**: `Carlos Corretor`
   - **Mandato**: `ASN/0001`
   - **Início**: primeiro dia do próximo mês
   - **Fim**: início + 12 meses
   - **Aluguel Mensal**: `2.500,00` (deve preencher automaticamente do imóvel)
   - **Caução**: `5.000,00`
   - **Índice de Reajuste**: `IPCA`
   - **Contabilidade → Diário**: deixar vazio (usa padrão)
3. Salve

**✅ Resultado esperado**:
- Contrato salvo como `Rascunho`
- Duração calculada: `12 meses`
- Valor Total calculado: `30.000,00`
- Próximo Reajuste calculado

---

### Passo 2.5 — Ativar Contrato

1. No contrato, clique em **Ativar Contrato**

**✅ Resultado esperado**:
- Status → `Ativo`
- Imóvel status → `Alugado`
- **12 parcelas geradas** automaticamente (verificar aba ou smart button "Parcelas")
- **Comissão criada** automaticamente: `COM/0001` com valor = `5%` de `30.000,00` = `1.500,00`
- Smart button **Comissão** aparece no contrato
- Dashboard atualiza: `contract_active + 1`

---

### Passo 2.6 — Verificar Parcelas

1. No contrato, clique no smart button **Parcelas**
2. Verifique:
   - 12 parcelas criadas
   - Todas com status `Em Aberto`
   - Valor `2.500,00` cada
   - Vencimentos mensais no dia 5

**✅ Resultado esperado**: 12 registros com `status = open`, `amount = 2.500,00`

---

## FLUXO 3 — Pagamento de Aluguel e Contabilidade

### Passo 3.1 — Registrar Pagamento

1. **Imóveis → Contratos → Parcelas de Aluguel**
2. Abra a primeira parcela (mês atual)
3. Preencha:
   - **Valor Pago**: `2.500,00`
   - **Data de Pagamento**: hoje
   - **Forma de Pagamento**: `PIX`
4. Clique em **Registrar Pagamento**

**✅ Resultado esperado**:
- Status → `Pago`
- **Smart button "Lançamento Contábil"** aparece
- Mensagem no chatter: `"Pagamento total registrado: R$ 2.500,00 em DD/MM/AAAA"`

---

### Passo 3.2 — Verificar Lançamento Contábil

1. Clique no smart button **Lançamento Contábil**

**✅ Resultado esperado**:
- `account.move` do tipo `Lançamento Contábil` (entry) com status `Lançado`
- Linha 1 (Débito): Conta do diário (banco/caixa) = `R$ 2.500,00`
- Linha 2 (Crédito): Conta de Receita de Aluguéis = `R$ 2.500,00`
- Data = data do pagamento
- Referência = número da parcela

---

### Passo 3.3 — Testar Cancelamento com Estorno

1. Volte para a parcela paga
2. Clique em **Cancelar**

**✅ Resultado esperado**:
- Status → `Cancelado`
- O `account.move` é revertido (status → `Cancelado`)
- Mensagem no chatter: `"Parcela cancelada em DD/MM/AAAA"`

> **Nota**: Reabra a parcela clicando em **Redefinir** → **Abrir Cobrança** para continuar os testes.

---

### Passo 3.4 — Testar Pagamento Parcial

1. Na parcela em aberto, preencha:
   - **Valor Pago**: `1.000,00` (menos que `2.500,00`)
2. Clique em **Registrar Pagamento**

**✅ Resultado esperado**:
- Status → `Parcialmente Pago`
- **Nenhum lançamento contábil gerado** (só gera no pagamento total)
- Mensagem: `"Pagamento parcial registrado: R$ 1.000,00 de R$ 2.500,00"`

---

## FLUXO 4 — Régua de Inadimplência

### Passo 4.1 — Simular Parcela Vencida

> Para testar sem esperar dias, vamos manipular a data de vencimento via SQL.

1. Anote o ID da parcela que está em aberto
2. Execute no banco:
```sql
UPDATE property_rent
SET due_date = CURRENT_DATE - 2
WHERE id = SEU_ID AND status = 'open';
```
3. Execute o cron manualmente:
   **Configurações → Técnico → Ações Agendadas → "Régua de Inadimplência" → Executar Manualmente**

**✅ Resultado esperado**:
- Status → `Atrasado`
- `days_late` = 2
- `notified_d1 = True`
- Mensagem no chatter: `"⚠️ Parcela vencida há 2 dia(s)"`

---

### Passo 4.2 — Simular D+5

1. Execute no banco:
```sql
UPDATE property_rent SET due_date = CURRENT_DATE - 6 WHERE id = SEU_ID;
UPDATE property_rent SET notified_d5 = false WHERE id = SEU_ID;
```
2. Execute o cron novamente

**✅ Resultado esperado**:
- `notified_d5 = True`
- E-mail enviado ao locatário (se configurado)
- Mensagem no chatter

---

### Passo 4.3 — Simular D+30 (contrato inadimplente)

1. Execute no banco:
```sql
UPDATE property_rent SET due_date = CURRENT_DATE - 31 WHERE id = SEU_ID;
UPDATE property_rent SET notified_d30 = false WHERE id = SEU_ID;
```
2. Execute o cron

**✅ Resultado esperado**:
- `notified_d30 = True`
- Contrato status → `Inadimplente`
- Dashboard: `contract_defaulting + 1`

---

## FLUXO 5 — Manutenção

### Passo 5.1 — Criar Manutenção

1. **Imóveis → Operações → Manutenções → Novo**
2. Preencha:
   - **Imóvel**: `Apartamento Centro 101`
   - **Contrato**: `Contrato APT-101 Maria`
   - **Tipo**: `Corretiva`
   - **Prioridade**: `Alta`
   - **Descrição**: `Vazamento no banheiro`
   - **Data de Abertura**: hoje
   - **Custo Estimado**: `500,00`
3. Salve

**✅ Resultado esperado**: Manutenção criada com status `Aberto`.

---

### Passo 5.2 — Fluxo de Aprovação

1. Clique em **Aprovar** → status: `Aprovado`
2. Clique em **Iniciar Execução** → status: `Em Execução`
3. Preencha **Custo Real**: `450,00`
4. Clique em **Concluir** → status: `Concluído`

**✅ Resultado esperado**:
- `status = done`
- Smart button no contrato: `1 Manutenção`
- Dashboard: `maintenance_open` diminui

---

### Passo 5.3 — Testar Emergência

1. Crie nova manutenção com **Tipo**: `Emergência`
2. Verifique no dashboard: `alert_maintenance_emergency + 1`

---

## FLUXO 6 — Vistoria

### Passo 6.1 — Criar Vistoria de Entrada

1. **Imóveis → Operações → Vistorias → Novo**
2. Preencha:
   - **Imóvel**: `Apartamento Centro 101`
   - **Contrato**: `Contrato APT-101 Maria`
   - **Tipo**: `Entrada`
   - **Data Agendada**: amanhã
   - **Responsável**: seu usuário
3. Salve → status: `Agendada`

**✅ Resultado esperado**: Smart button no contrato: `1 Vistoria`.

---

### Passo 6.2 — Confirmar e Concluir Vistoria

1. Clique em **Confirmar** → status: `Confirmada`
2. Preencha **Observações**: `Imóvel em perfeito estado`
3. Clique em **Concluir** → status: `Concluída`

**✅ Resultado esperado**:
- `status = done`
- Dashboard: `inspection_scheduled` diminui

---

## FLUXO 7 — Documentos

### Passo 7.1 — Anexar Documento

1. **Imóveis → Operações → Documentos → Novo**
2. Preencha:
   - **Imóvel**: `Apartamento Centro 101`
   - **Contrato**: `Contrato APT-101 Maria`
   - **Tipo**: `Contrato Assinado`
   - **Validade**: hoje + 12 meses
3. Anexe um PDF qualquer
4. Salve

**✅ Resultado esperado**: Documento salvo com status `Válido`.

---

### Passo 7.2 — Testar Vencimento

1. Via SQL, coloque a validade no passado:
```sql
UPDATE property_document SET expiry_date = CURRENT_DATE - 1 WHERE id = SEU_ID;
```
2. Execute o cron de verificação de documentos (ou aguarde o cron diário)

**✅ Resultado esperado**:
- Status → `Vencido`
- Dashboard: `alert_documents_expired + 1`

---

## FLUXO 8 — Pipeline de Aquisição

### Passo 8.1 — Criar Lead de Captação

1. **Imóveis → Pipeline → Leads → Novo**
2. Preencha:
   - **Nome**: `Oportunidade Sobrado Alphaville`
   - **Corretor**: `Carlos Corretor`
   - **Contato**: qualquer parceiro
3. Salve

---

### Passo 8.2 — Criar Aquisição

1. **Imóveis → Pipeline → Aquisições → Novo**
2. Preencha:
   - **Imóvel Alvo**: `Sobrado Alphaville`
   - **Corretor**: `Carlos Corretor`
   - **Valor de Oferta**: `850.000,00`
   - **Estágio**: `Prospecção`
3. Avance os estágios: `Prospecção → Análise → Negociação → Fechamento`
4. Clique em **Fechar Negócio**

**✅ Resultado esperado**:
- Novo imóvel criado automaticamente no portfólio
- Comissão de **venda** criada: `COM/0002`
- Dashboard: `acquisition_pipeline` atualiza

---

## FLUXO 9 — Comissão do Corretor

### Passo 9.1 — Verificar Comissão de Locação

1. **Imóveis → Corretores → Comissões**
2. Localize `COM/0001` (criada automaticamente ao ativar o contrato)

**✅ Resultado esperado**:
- Tipo: `Locação`
- Valor: `1.500,00` (5% de R$ 30.000,00)
- Status: `Pendente`
- Corretor: `Carlos Corretor`

---

### Passo 9.2 — Pagar Comissão

1. Abra `COM/0001`
2. Preencha **Data de Pagamento**: hoje
3. Clique em **Marcar como Pago**

**✅ Resultado esperado**:
- Status → `Pago`
- Dashboard: `commission_pending_count - 1`, `commission_pending_total` reduz

---

## FLUXO 10 — Extrato do Proprietário

### Passo 10.1 — Gerar Extrato

1. **Imóveis → Proprietários → João Silva Proprietário**
2. Clique em **Gerar Extrato**
3. Preencha:
   - **Período De**: primeiro dia do mês atual
   - **Período Até**: hoje
4. Clique em **Imprimir Extrato**

**✅ Resultado esperado**:
- PDF gerado com:
  - Dados do proprietário
  - Tabela de aluguéis recebidos
  - Custos do período
  - Resultado líquido

---

### Passo 10.2 — Portal do Proprietário

> **Pré-requisito**: Proprietário deve ter acesso ao portal (ver CONFIGURACAO_INICIAL.md § 7)

1. Acesse `http://localhost:8069/my/properties` com o login do proprietário
2. Verifique:
   - Card "Meus Imóveis" com contador
   - Imóvel `Apartamento Centro 101` aparece
   - KPIs: imóveis alugados, receita, pendências

**✅ Resultado esperado**: Portal carrega sem erro com dados do proprietário.

---

## FLUXO 11 — Relatórios PDF

### Passo 11.1 — Relatório de Carteira

1. **Imóveis → Portfólio → Imóveis** → selecione todos
2. **Imprimir → Carteira de Imóveis**

**✅ Resultado esperado**:
- PDF com resumo: Total/Alugados/Disponíveis/Manutenção/À Venda
- Tabela com todos os imóveis, proprietário, área, aluguel, custo, status

---

### Passo 11.2 — Relatório de Inadimplência

1. **Imóveis → Contratos → Contratos** → selecione todos
2. **Imprimir → Relatório de Inadimplência**

**✅ Resultado esperado**:
- PDF com resumo de contratos inadimplentes
- Tabela ordenada por valor em aberto (maior primeiro)
- Totais no rodapé

> Se nenhum contrato estiver inadimplente, o PDF mostra: "✓ Nenhum contrato inadimplente encontrado."

---

### Passo 11.3 — Relatório de Rentabilidade

1. **Imóveis → Portfólio → Imóveis** → selecione todos
2. **Imprimir → Rentabilidade por Imóvel**

**✅ Resultado esperado**:
- PDF com yield% por imóvel, colorido (verde ≥6%, laranja 4-6%, vermelho <4%)
- Linha de totais no rodapé

---

## FLUXO 12 — Dashboard

### Passo 12.1 — Verificar KPIs

1. Acesse **Imóveis → Dashboard**
2. Verifique cada seção:

| Seção | O que verificar |
|---|---|
| **ALERTAS** | Valores corretos (contratos a vencer, parcelas atrasadas, etc.) |
| **Portfólio** | Total = 1, Alugados = 1 |
| **Contratos** | Ativos = 1 |
| **Financeiro** | Receita Mensal = R$ 2.500,00 |
| **Operações** | Manutenções = 0 (após concluir), Vistorias = 0 |
| **Corretores** | Corretores Ativos = 1, Mandatos = 1 |
| **Pipeline** | Aquisições conforme criadas |

---

### Passo 12.2 — Navegar pelos Cards

1. Clique em cada card e verifique que navega para a lista correta
2. Clique nos alertas e verifique filtros aplicados

**✅ Resultado esperado**: Todos os cards são clicáveis e levam ao modelo correto.

---

## CHECKLIST FINAL DE VERIFICAÇÃO

### Modelos e campos

- [ ] `property.asset` — cria, edita, arquiva
- [ ] `property.owner` — stats calculam corretamente
- [ ] `property.broker` — contadores de mandatos/comissões
- [ ] `property.broker.assignment` — exclusividade funciona
- [ ] `property.contract` — ativação gera parcelas e comissão
- [ ] `property.rent` — pagamento gera `account.move`
- [ ] `property.rent` — cancelamento estorna `account.move`
- [ ] `property.maintenance` — fluxo completo de estados
- [ ] `property.inspection` — fluxo completo de estados
- [ ] `document.document` — upload e controle de validade
- [ ] `property.acquisition` — pipeline e fechamento
- [ ] `property.commission` — pagamento manual

### Automações

- [ ] Cron de contratos vencidos funciona
- [ ] Cron de régua de inadimplência funciona (D+1, D+5, D+15, D+30)
- [ ] Cron de mandatos expirados funciona
- [ ] Cron de comissões pendentes funciona

### Relatórios

- [ ] PDF Contrato de Locação (do contrato)
- [ ] PDF Extrato do Proprietário (do proprietário)
- [ ] PDF Carteira de Imóveis (dos imóveis)
- [ ] PDF Inadimplência (dos contratos)
- [ ] PDF Rentabilidade (dos imóveis)

### Integrações

- [ ] Lançamento contábil gerado no pagamento
- [ ] Estorno ao cancelar parcela paga
- [ ] Portal do proprietário acessível

### Segurança

- [ ] Usuário sem grupo `manager` não vê configurações
- [ ] Usuário `user` pode ver contratos mas não deletar

---

## Dicas de Debug

### Ver log do servidor em tempo real
```bash
tail -f /var/log/odoo/odoo.log | grep -E "ERROR|WARNING|property"
```

### Executar cron manualmente via Python
```python
# No shell do Odoo (Settings → Technical → Shell)
env['property.rent'].action_cron_check_late_rents()
env['property.contract'].action_cron_check_late()
```

### Verificar lançamentos contábeis gerados
```sql
SELECT am.ref, am.date, am.state, aml.account_id, aml.debit, aml.credit
FROM account_move am
JOIN account_move_line aml ON aml.move_id = am.id
WHERE am.narration LIKE '%Recebimento de aluguel%'
ORDER BY am.date DESC;
```

### Resetar status de módulo para reinstalar
```sql
UPDATE ir_module_module SET state = 'uninstalled' WHERE name = 'property_core';
```