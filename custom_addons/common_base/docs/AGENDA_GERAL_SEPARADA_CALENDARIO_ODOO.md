# Agenda Geral separada do Calendário nativo do Odoo

No Odoo 18/19, o model `calendar.event` representa compromissos pessoais e reuniões. Por isso a interface padrão mostra conceitos como participantes e reunião.

A Agenda Geral operacional deste pacote usa o model próprio `common.agenda.event`.

## Regra de uso

- **mail.activity**: tarefa, cobrança, prazo e lembrete interno.
- **common.agenda.event**: agenda operacional do ERP imobiliário, governança e documentos.
- **calendar.event**: calendário pessoal/reuniões nativas do Odoo. Não é usado automaticamente pela Agenda Geral.

## Benefícios

- Vistorias e manutenções não aparecem como “Reuniões”.
- Governança e documentos ficam na Agenda Geral com filtros próprios.
- A visualização por usuário fica controlada por responsáveis, participantes e usuários adicionais.
- O app Calendário padrão do Odoo continua limpo para reuniões pessoais.
