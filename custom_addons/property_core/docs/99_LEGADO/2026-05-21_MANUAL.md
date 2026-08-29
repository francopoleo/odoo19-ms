# Manual do Usuário — Property Core

---

## Cadastro de Imóvel

**Menu:** Imóveis → Imóveis → Criar

### Campos obrigatórios

| Campo | Exemplo |
|---|---|
| Nome do Imóvel | Apartamento 42 — Ed. Solar |
| Tipo | Residencial |
| Status | Disponível |

### Dados recomendados

- Endereço completo (para contratos e relatórios)
- Matrícula (número no cartório de registro de imóveis)
- Número do IPTU
- Proprietário vinculado
- Valor de aluguel base

### Status do Imóvel

| Status | Quando usar |
|---|---|
| Disponível | Pronto para locação ou venda |
| Alugado | Com contrato ativo |
| À Venda | Em processo de venda |
| Em Negociação | Proposta em andamento |
| Em Manutenção | Indisponível por manutenção |
| Inativo | Fora de operação |

---

## Cadastro de Contrato

**Menu:** Imóveis → Contratos → Criar

### Campos obrigatórios

| Campo | Exemplo |
|---|---|
| Nome do Contrato | Locação Apto 42 — João Silva |
| Tipo de Contrato | Residencial |
| Imóvel | Apartamento 42 — Ed. Solar |
| Locatário | João Silva |
| Data de Início | 01/04/2026 |
| Data de Término | 31/03/2027 |
| Valor Mensal | R$ 2.500,00 |

### Ativando o Contrato

Após preencher todos os campos, clique em **Ativar Contrato**.

O sistema irá:
- mudar o status do imóvel para "Alugado"
- liberar o botão **Gerar Parcelas**

### Gerando Parcelas

Clique em **Gerar Parcelas** para criar todas as parcelas mensais do período do contrato.

As parcelas ficam disponíveis em **Imóveis → Parcelas**.

---

## Registrando Pagamentos

**Menu:** Imóveis → Parcelas

1. Abra a parcela desejada
2. Clique em **Registrar Pagamento**
3. Informe a data e o valor recebido

---

## Repasse ao Proprietário

**Menu:** Imóveis → Proprietários → [Proprietário] → Repasses

O repasse consolida o que deve ser transferido ao proprietário:

- Receita do período (parcelas pagas)
- Deduções (comissão, manutenção, taxas)
- Valor líquido a transferir

Ao marcar o repasse como **Pago**, o sistema envia automaticamente o e-mail com o comprovante em PDF.

---

## Governança vinculada a Imóveis e Contratos

Em qualquer imóvel ou contrato, o botão **Governança** mostra os casos vinculados.

### Como criar um caso a partir do imóvel

1. Abra o imóvel
2. Clique no smart button **Governança**
3. Clique em **Criar**
4. O caso já vem vinculado ao imóvel

### Quando criar um caso de governança

| Situação | Tipo recomendado |
|---|---|
| Documentação faltante (matrícula, escritura) | Documental |
| Locatário inadimplente | Financeiro |
| Notificação judicial recebida | Jurídico |
| Vistoria não realizada | Operacional |
| Reclamação de inquilino ou vizinho | Reclamação |
| Imóvel sem regularização ambiental | Compliance |

---

## Vistoria

**Menu:** Imóveis → Imóvel → aba Vistorias

Registre vistorias de:
- Entrada (início do contrato)
- Saída (término do contrato)
- Periódica

---

## Manutenção

**Menu:** Imóveis → Imóvel → aba Manutenções

Registre ordens de manutenção com:
- Tipo (preventiva / corretiva)
- Responsável
- Custo
- Status

---

## Documentos do Imóvel

**Menu:** Imóveis → Imóvel → aba Documentos

Vincule documentos ao imóvel:
- Matrícula
- Escritura
- IPTU
- Laudos
- Certidões

---

## Corretores e Mandatos

**Menu:** Imóveis → Corretores

Cadastre corretores e vincule **Mandatos** (exclusivos ou não) para venda ou locação de imóveis específicos.

---

## Inadimplência

Contratos em atraso mudam automaticamente para status **Inadimplente** via cron diário.

Para acompanhar:
- **Menu:** Imóveis → Contratos → filtrar por "Inadimplente"

Ação recomendada: criar um caso de governança do tipo **Financeiro** com prioridade **Alto**.

---

## Exemplo Completo — Novo Imóvel para Locação

1. **Criar Imóvel** — nome, endereço, tipo Residencial, status Disponível
2. **Vincular Proprietário** — selecionar o dono do imóvel
3. **Criar Mandato** — vincular corretor responsável pela locação
4. **Contrato encontrado** — criar Contrato, vincular imóvel e locatário, ativar
5. **Gerar Parcelas** — clicar em Gerar Parcelas
6. **Registrar Pagamentos** — mensalmente, conforme recebimento
7. **Gerar Repasse** — consolidar e transferir ao proprietário

---

## Regras Importantes

- Todo contrato deve estar vinculado a um imóvel
- Todo imóvel com contrato ativo deve ter status "Alugado"
- Parcelas só são geradas após ativação do contrato
- Documentos sempre vinculados ao imóvel (nunca soltos)
- Qualquer pendência relevante deve ter um caso de governança