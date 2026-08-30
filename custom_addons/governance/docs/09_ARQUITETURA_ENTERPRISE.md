# Governance Enterprise — Arquitetura e Processo

## Objetivo

O Governance é o hub de controle de situações que exigem responsabilidade, prazo,
evidência e decisão. O caso é o contexto; ele não substitui o registro do imóvel,
contrato, documento ou contato que originou o trabalho.

## Vocabulário oficial

| Objeto | Uso |
|---|---|
| Caso | Situação, exceção, incidente, risco ou demanda que precisa ser governada. |
| Obrigação | Algo que uma pessoa, empresa ou equipe deve fornecer ou executar. |
| Comunicação | Evento de contato: e-mail, ligação, reunião, ofício ou mensagem. |
| Resposta formal | Manifestação recebida que precisa ser analisada e classificada. |
| Atividade | Tarefa atribuída a um usuário. |
| Decisão | Ato fundamentado de aprovar, rejeitar, aceitar exceção ou encerrar. |
| Risco | Possibilidade de impacto que precisa ser avaliada e tratada. |
| Controle | Verificação repetível que reduz a probabilidade ou o impacto de um risco. |
| Evidência | Documento ou registro que prova o fato ou o cumprimento. |

## Regra de relacionamento

```text
Caso → Obrigações → Comunicações → Respostas → Decisões → Ações → Evidências
```

Riscos são relacionados a controles; controles têm dono, frequência de teste,
resultado e próxima revisão.

Uma comunicação não é uma resposta automaticamente. Uma resposta não encerra
uma obrigação automaticamente. Uma obrigação só pode ser encerrada quando houver
resultado, evidência ou justificativa registrada.

## Processo padrão

```text
Receber → Triar → Classificar → Atribuir → Executar → Aguardar terceiro
→ Analisar resposta → Decidir → Tratar pendências → Encerrar → Revisar indicadores
```

## Regras de encerramento

- Não encerrar caso com obrigação obrigatória aberta.
- Não aceitar risco alto sem decisão fundamentada.
- Não considerar e-mail recebido como resposta sem relacioná-lo a uma obrigação.
- Não concluir todas as obrigações em massa a partir de uma resposta.
- Toda rejeição, exceção ou encerramento sem resposta exige justificativa.
- Documentos relevantes devem estar no Documents/Dossier, não somente no chatter.

## Integrações

- `document_core`: documento e evidência.
- `document_dossier`: checklist e completude documental.
- `property_core`: imóvel, contrato, mandato e proprietário.
- `common_base`: agenda, atividades e comunicação.
- `common_help_center`: playbooks e ajuda contextual.
- `mail`: chatter, aliases e histórico de mensagens.
- `sign`: documentos formais e certificado de conclusão.

## Exemplo imobiliário

```text
Caso: regularização documental do imóvel Edifício Alameda, sala 302
  └─ Obrigação: proprietário enviar certidão atualizada até 20/09
      └─ Comunicação: solicitação enviada por e-mail em 10/09
          └─ Resposta formal: certidão recebida em 18/09
              └─ Decisão: documento aprovado pelo jurídico
                  └─ Evidência: certidão vinculada ao dossiê
```

## Indicadores mínimos

- casos por etapa, tipo, empresa e responsável;
- obrigações abertas, próximas do vencimento e atrasadas;
- tempo até primeira resposta e resolução;
- SLA cumprido e violado;
- decisões aguardando aprovação;
- riscos altos sem tratamento;
- documentos obrigatórios ausentes ou vencidos;
- casos encerrados sem resposta ou sem evidência.
