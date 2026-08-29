# Agenda e Atividades Enterprise

Esta camada padroniza agenda e atividades entre os módulos principais do sistema.

## Conceito

- **Atividade**: cobrança interna, prazo, pendência ou follow-up. Deve aparecer no chatter e na fila de atividades do usuário.
- **Calendário**: compromisso real com data e hora, como vistoria, visita técnica, reunião de governança, revisão presencial ou conferência documental.

## Campos comuns

Os modelos habilitados passam a ter:

- Responsável Principal
- Responsáveis / Equipe
- Participantes Externos
- Prazo da Atividade
- Início Agendado
- Fim Agendado
- Duração Prevista
- Local do Compromisso
- Notas de Agenda
- Evento no Calendário

## Modelos cobertos

### Property Core

- Vistorias
- Manutenções
- Contratos
- Parcelas de aluguel
- Reajustes de aluguel

### Governance

- Casos de governança
- Pendências de governança
- Comunicações do tipo reunião

### Document Core / Dossiês

- Documentos
- Dossiês

### Auxiliares

- Aditivos contratuais
- Comprovantes de pagamento

## Regras de uso

Use **Criar/Atualizar Atividades** quando o objetivo for cobrar uma ação interna até uma data.

Use **Sincronizar Calendário** quando existir compromisso com data/hora real.

Vistorias e manutenções sincronizam automaticamente atividades e calendário ao usar o botão **Agendar**, desde que exista data agendada.
