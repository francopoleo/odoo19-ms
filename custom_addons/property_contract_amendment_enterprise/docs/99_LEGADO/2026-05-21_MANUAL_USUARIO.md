# Manual do Usuário — Contratos e Aditivos Imobiliários Empresarial

## 1. Visão geral

O módulo **Contratos e Aditivos Imobiliários Empresarial** complementa o módulo `property_core` para administrar alterações contratuais após a criação de um contrato imobiliário. Ele foi desenhado para contratos de locação, contratos comerciais, contratos não residenciais, operações com encargos, descontos, cobranças adicionais, reajustes, prazos, garantias, documentos, obrigações e aprovações.

No Odoo, o contrato original permanece como o registro principal. Cada aditivo é um evento controlado que explica o que mudou, por qual motivo, quando passa a valer, quem aprovou, quais documentos foram assinados e quais efeitos financeiros ou operacionais precisam ser aplicados.

## 2. O que o módulo faz

O módulo cobre as seguintes áreas:

- **Aditivos contratuais:** registro principal da alteração contratual.
- **Motivos de aditivo:** catálogo de motivos jurídicos, comerciais, financeiros, operacionais e de encerramento.
- **Tabela de valores:** regras vigentes ou futuras de aluguel, descontos, acréscimos, encargos e carências.
- **Plano de cobrança:** visão de períodos, vencimentos, valores base, descontos, acréscimos e total.
- **Ajustes financeiros:** correções pontuais ou retroativas, como crédito, débito, cobrança a maior, cobrança a menor, perdão de multa e acordo.
- **Documentos contratuais:** contrato original, aditivos, certificado de assinatura, notificações, registros e documentos de encerramento.
- **Aprovações:** fluxo interno por tipo de aprovação, aprovador, grupo responsável e status.
- **Obrigações:** compromissos derivados do contrato ou do aditivo, como seguros, licenças, garantias, vistorias e manutenções.
- **Opções contratuais:** direitos e janelas contratuais, como renovação, preferência de compra, expansão, saída e uso exclusivo.
- **Histórico de termos:** memória do que foi alterado, valor anterior, novo valor, data de efeito e responsável.
- **Versões consolidadas:** snapshot/registro consolidado das condições do contrato após aplicação do aditivo.

## 3. Menus

O módulo cria os menus dentro do app **Imóveis**:

```text
Imóveis
└── Aditivos Contratuais
    ├── Todos os Aditivos
    ├── Tabela de Valores
    ├── Plano de Cobrança
    ├── Ajustes Financeiros
    ├── Documentos Contratuais
    ├── Obrigações
    ├── Opções Contratuais
    └── Configuração de Aditivos
        ├── Motivos de Aditivo
        ├── Motivos Financeiros
        └── Tipos de Documento
```

A área **Configuração de Aditivos** deve ser usada somente por gestor ou administrador, para evitar criação livre de categorias, motivos e tipos duplicados.

## 4. Conceito central

Um aditivo deve responder a sete perguntas:

1. **Qual contrato será alterado?**
2. **Qual é o tipo de aditivo?**
3. **Qual é o motivo da alteração?**
4. **Qual é a data de efeito?**
5. **A alteração tem impacto financeiro, jurídico, operacional, comercial ou de partes?**
6. **Quais valores, prazos, documentos ou obrigações mudam?**
7. **Quem aprovou, assinou e aplicou a alteração?**

## 5. Como tratar valores a mais e a menos

O módulo separa mudanças financeiras em duas camadas:

### 5.1 Tabela de Valores

Use quando a mudança passa a fazer parte da regra futura ou vigente do contrato.

Exemplos:

- aumento do aluguel-base;
- redução permanente do aluguel;
- desconto temporário;
- carência;
- aluguel escalonado;
- acréscimo recorrente;
- alteração de IPTU, condomínio, seguro, fundo de marketing ou despesas comuns;
- mudança de índice de reajuste ou condição de cobrança.

### 5.2 Ajustes Financeiros

Use quando a mudança corrige um período já cobrado, uma diferença pontual ou um acordo específico.

Exemplos:

- crédito retroativo;
- débito retroativo;
- cobrança a maior;
- cobrança a menor;
- perdão de multa;
- perdão de juros;
- crédito de acordo;
- débito de acordo;
- fatura separada;
- nota de crédito.

## 6. Papéis recomendados

| Papel | Uso esperado |
| --- | --- |
| Operacional | Cadastrar aditivos, documentos, obrigações e opções. |
| Jurídico | Revisar cláusulas, base legal, risco, assinatura e documentos. |
| Financeiro | Validar tabela de valores, plano de cobrança e ajustes financeiros. |
| Gestor | Aprovar aditivos, motivos e configurações. |
| Administrador | Excluir registros quando necessário e manter permissões. |

## 7. Boas práticas

- Não edite diretamente o contrato quando a mudança exige rastreabilidade; crie um aditivo.
- Use **Motivo de Aditivo** para padronizar classificação e relatórios.
- Use **Tabela de Valores** para regra recorrente ou futura.
- Use **Ajustes Financeiros** para diferença pontual ou retroativa.
- Preencha **Resumo Antes**, **Resumo Depois**, **Base Legal/Contratual** e **Cláusulas Afetadas** em aditivos relevantes.
- Não aplique aditivo antes de aprovação ou assinatura, salvo fluxo interno autorizado.
- Mantenha o documento final e o certificado de assinatura anexados.


## Aba Alterações com seleção controlada

Na criação do aditivo, a aba **Alterações** deve ser usada quando o aditivo modifica um dado estrutural do contrato.

O usuário deve preencher primeiro o campo **Campo do Contrato**. As opções são controladas pelo sistema para evitar digitação incorreta. Depois da seleção, o sistema preenche automaticamente a categoria, o campo técnico, o rótulo, o tipo de valor e o valor anterior.

### Exemplos rápidos

| Objetivo | Campo do Contrato | Campo novo a preencher | Exemplo |
| --- | --- | --- | --- |
| Aumentar aluguel | Aluguel base atual | Novo Valor (Número) | 12000 |
| Prorrogar contrato | Fim vigente | Novo Valor (Data) | 31/12/2027 |
| Trocar locatário | Locatário atual | Novo Contato | Novo locatário |
| Alterar garantia | Garantia vigente | Novo Valor (Texto) | Seguro-fiança |
| Alterar vencimento | Dia de vencimento vigente | Novo Valor (Número) | 10 |
| Alterar índice | Índice de reajuste vigente | Novo Valor (Texto) | ipca |

Não use a aba Alterações para detalhar parcelas, créditos, débitos ou composições financeiras complexas. Para isso, use também **Impacto Financeiro**, **Tabela de Valores** e **Ajustes Financeiros**.


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
