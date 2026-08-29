# Agenda Geral — Segurança e Visibilidade

## Objetivo

A Agenda Geral controla dois objetos do Odoo:

- `calendar.event`: compromisso real no calendário;
- `mail.activity`: atividade interna/prazo/follow-up.

O objetivo da camada de segurança é impedir que todos os usuários internos vejam todos os compromissos operacionais.

## Regras de visualização

Cada registro com agenda possui o campo **Quem pode visualizar**:

- **Somente responsáveis/participantes**: visível para organizador, responsável principal, equipe, participantes internos e criador.
- **Responsáveis + usuários adicionais**: além dos usuários acima, também mostra para os usuários informados em **Usuários adicionais com acesso**.
- **Todos os usuários internos**: qualquer usuário interno pode visualizar.

Usuários do grupo **Administrador da Agenda Geral** e administradores técnicos podem auditar todos os eventos e atividades da Agenda Geral.

## Onde configurar

Em cada fluxo operacional:

- Vistoria
- Manutenção
- Governança
- Pendência
- Documento
- Dossiê
- Contrato
- Parcela/Aluguel
- Aditivo
- Comprovante

abra a aba **Agenda e Atividades** e ajuste:

- Responsável Principal;
- Responsáveis / Equipe;
- Participantes;
- Quem pode visualizar;
- Usuários adicionais com acesso.

Depois clique em **Sincronizar Agenda Completa**.

## Regras técnicas

Os eventos da Agenda Geral recebem metadados técnicos:

- `agenda_module`
- `agenda_type`
- `agenda_visibility`
- `agenda_responsible_user_ids`
- `agenda_visible_user_ids`
- `agenda_source_model`
- `agenda_source_res_id`

As atividades recebem metadados equivalentes:

- `agenda_is_erp`
- `agenda_module`
- `agenda_type`
- `agenda_visibility`
- `agenda_visible_user_ids`
- `agenda_source_model`
- `agenda_source_res_id`

## Backfill

Durante a atualização do módulo, o arquivo `common_agenda_security_data.xml` executa funções de backfill para preencher metadados de eventos e atividades já existentes.


## Ajuste de compatibilidade Odoo 18/19

A Agenda Geral não cria mais campos armazenados diretamente em `mail.activity`.
As atividades seguem o comportamento nativo do Odoo: são atribuídas ao usuário responsável e aparecem para ele.
A visibilidade avançada por responsáveis, participantes e usuários adicionais fica concentrada nos eventos de `calendar.event`, evitando erros de `UndefinedColumn` no webclient/mail durante atualizações.
