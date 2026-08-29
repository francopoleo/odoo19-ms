# Property Core — Odoo 19

## Visão Geral

Módulo central de gestão imobiliária do ERP. Controla todo o ciclo de vida dos ativos imobiliários: do cadastro do imóvel até a geração de repasses para proprietários.

---

## Modelos Principais

### `property.asset` — Imóvel

Representa o ativo imobiliário.

| Campo-chave | Descrição |
|---|---|
| Nome / Referência | Identificação do imóvel |
| Tipo | Residencial / Comercial / Terreno / Industrial / Uso Misto |
| Status | Disponível / Alugado / À Venda / Em Negociação / Em Manutenção / Inativo |
| Matrícula / IPTU | Dados legais |
| Endereço completo | Localização |
| Proprietário | Vinculado a `property.owner` |
| Valor de Aluguel | Valor base para contratos |

Smart buttons disponíveis:

- Contratos vinculados
- Documentos
- Inspeções
- Manutenções
- Casos de Governança

---

### `property.contract` — Contrato de Locação

Representa o contrato de locação vinculado a um imóvel.

| Campo-chave | Descrição |
|---|---|
| Tipo | Residencial / Comercial / Comodato / Arrendamento |
| Imóvel | Vinculado a `property.asset` |
| Locatário | Vinculado a `res.partner` |
| Datas | Início e fim do contrato |
| Valor Mensal | Aluguel base |
| Status | Rascunho / Ativo / Vencendo / Renovando / Inadimplente / Vencido / Encerrado |

Smart buttons disponíveis:

- Parcelas abertas / total
- Casos de Governança

---

### `property.owner` — Proprietário

Cadastro de proprietários com controle de repasse.

### `property.rent` — Parcela

Parcelas geradas a partir do contrato. Controla vencimentos, pagamentos e inadimplência.

### `property.owner.repasse` — Repasse ao Proprietário

Consolidação dos valores a repassar ao proprietário após deduções (comissão, manutenção, etc.).

### `property.broker` / `property.broker.assignment` — Corretor e Mandato

Cadastro de corretores e seus mandatos de venda/locação vinculados a imóveis.

### `property.inspection` — Vistoria

Registro de vistorias de entrada e saída.

### `property.maintenance` — Manutenção

Ordens de manutenção vinculadas ao imóvel.

### `document.document` — Documento

Documentos vinculados ao imóvel (matrícula, IPTU, laudos, etc.).

### `property.acquisition` — Aquisição

Registro de processos de aquisição de imóveis.

### `property.lead` — Lead Imobiliário

Oportunidades de locação e venda vindas do site.

---

## Integração com Governança

Todos os imóveis e contratos possuem integração direta com o módulo **Governance**:

- Smart button mostra a contagem de casos de governança vinculados
- Clique abre a lista filtrada de casos daquele imóvel/contrato
- Novos casos criados pelo smart button já vêm pré-vinculados

Casos de governança podem ser vinculados a:

- Imóveis (`asset_ids`)
- Contratos (`contract_ids`)
- Mandatos em disputa (`assignment_ids`)

---

## Integração com Contabilidade

Via módulo `base_accounting_kit`:

- Geração de lançamentos contábeis para parcelas
- Integração com plano de contas
- Relatórios financeiros por imóvel

---

## Portal do Proprietário

Proprietários têm acesso via portal web a:

- Seus imóveis
- Contratos ativos
- Histórico de repasses

---

## Fluxo Principal

```
Imóvel cadastrado
    └── Mandato de locação (corretor)
    └── Contrato ativado
            └── Parcelas geradas mensalmente
            └── Pagamentos registrados
            └── Repasse ao proprietário calculado
            └── E-mail de repasse enviado com PDF
```

---

## Dependências

- `mail` — chatter e atividades
- `governance` — casos de governança
- `portal` — acesso do proprietário
- `website` — leads do site
- `account` — integração contábil
- `common_base` — mixin, sequências e configurações compartilhadas

---

## Status do Módulo

- Cadastro completo de imóveis
- Contratos com workflow
- Geração de parcelas
- Controle de inadimplência
- Proprietários com repasse
- Corretores e mandatos
- Vistorias e manutenções
- Documentos por imóvel
- Aquisições
- Leads do website
- Portal do proprietário
- Integração com governança (smart buttons bidirecionais)
- Relatórios: contrato, extrato do proprietário, repasse, portfólio, inadimplência, rentabilidade