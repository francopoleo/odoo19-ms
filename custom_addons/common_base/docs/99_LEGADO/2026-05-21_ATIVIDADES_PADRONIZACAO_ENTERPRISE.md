# Padronização Enterprise de Atividades e Agenda Geral

## Regra principal

- `mail.activity` é usado para tarefas, prazos, lembretes e cobranças internas.
- `common.agenda.event` é usado para compromissos operacionais exibidos na Agenda Geral.
- `calendar.event` do Odoo fica reservado para reuniões pessoais/nativas do Odoo.

## Tipos de atividade

Os tipos específicos de módulo são mantidos, mas ficam restritos ao seu respectivo model por `res_model`:

- Documentos: `document.document`
- Governança: `governance.case` e `governance.case.pending`
- Imóveis: `property.inspection`, `property.maintenance`, `property.contract`, `property.rent`, etc.

Com isso, o popup nativo **Agendar atividade** não mistura atividades de documentos dentro de imóveis, nem atividades de governança fora de governança.

## Uso recomendado

- Para prazo simples: usar **Agendar atividade** no chatter.
- Para compromisso operacional: usar a aba **Agenda e Atividades** e o botão **Sincronizar Agenda Completa**.
- Para consulta central: usar o aplicativo **Agenda Geral**.

## Ajuste de nomenclatura: Pendência Operacional

O tipo de atividade comum anteriormente chamado **Prazo Operacional** passa a se chamar **Pendência Operacional**.

A finalidade é evitar confusão com a **Agenda Geral**. Este tipo deve ser usado apenas para lembretes, cobranças internas e tarefas com vencimento, sem horário real de execução.

Use assim:

- **Pendência Operacional**: cobrança/tarefa interna com vencimento.
- **Agenda Geral**: compromisso operacional com data/hora, responsável, visibilidade e calendário próprio.
- **Reunião**: reunião nativa do Odoo/calendário padrão.
- **Vencimento/Validação/Revisão de Documento**: apenas em documentos.
- **Follow-up/Acompanhar Resposta de Governança**: apenas em governança.

A padronização por módulo deve impedir que atividades específicas de Documento apareçam em Imóveis e que atividades específicas de Governança apareçam fora de Governança.

