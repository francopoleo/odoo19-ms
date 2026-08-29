# Manual do Usuário — Document Core

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Visão geral

Gestão documental com documentos, categorias, tipos, validação, revisão, vencimento, localização, segurança e agenda documental.

## 2. Quem usa

- Operador documental
- Gestor documental
- Administrador funcional

## 3. Conceitos importantes

| Conceito | Explicação prática |
|---|---|
| Registro principal | Objeto central trabalhado no módulo, como documento, imóvel, caso, dossiê ou comprovante. |
| Atividade | Tarefa individual com responsável e prazo, criada pelo chatter. |
| Pendência Operacional | Atividade genérica para cobrança interna simples. |
| Agenda Geral | Agenda operacional separada do calendário nativo do Odoo para marcos críticos. |
| Ajuda contextual | Painel lateral aberto pelo botão Ajuda; mostra artigos curtos e opções reais da tela. |
| Opções dinâmicas | Categorias, tipos, filtros e campos que a Central lê diretamente do Odoo. |

## 4. Como usar a ajuda contextual

1. Abra a tela do módulo.
2. Clique em **Ajuda** no topo do Odoo.
3. Leia primeiro os **Artigos deste contexto**.
4. Consulte a seção **Campos, opções e filtros desta tela** para ver opções reais cadastradas.
5. Use **Abrir tela completa** apenas se precisar administrar ou editar o artigo.

> Os artigos explicam o fluxo e os exemplos; as opções reais aparecem dinamicamente. Se uma categoria nova for cadastrada no Odoo, ela aparece na ajuda sem alterar manualmente o texto.

## Fluxos operacionais ricos


### Fluxo 1: Criar documento

**Objetivo:** Cadastrar documento, anexar arquivo principal, escolher categoria/tipo, vincular ao contexto correto e salvar.


#### Quando usar

Use este fluxo quando o usuário precisar executar **criar documento** de forma rastreável, com responsável definido e histórico preservado.


#### Passo a passo recomendado

1. Acesse o menu principal do módulo.
2. Crie ou abra o registro operacional correto.
3. Preencha responsável principal, empresa e vínculos de negócio antes de avançar.
4. Preencha campos obrigatórios e revise mensagens de validação.
5. Quando houver tarefa individual, use **Agendar atividade**.
6. Quando houver marco crítico, compromisso ou prazo formal, use **Agenda Geral**.
7. Anexe documentos ou mídias no campo próprio do fluxo, evitando anexos soltos no chatter.
8. Salve e valide o resultado nos menus de acompanhamento.


#### Exemplo prático

| Campo | Exemplo |
|---|---|
| Documento | Certidão Negativa |
| Categoria | Jurídica/Fiscal conforme configuração |
| Tipo | Definido pelo cadastro de tipos documentais |
| Vencimento | 30/06 |
| Responsável | Juliana |

**Resultado esperado:** o documento fica rastreável, pode gerar atividade de revisão e, se for marco crítico, aparece na Agenda Geral. As opções reais de categoria/tipo são exibidas dinamicamente no drawer de ajuda.


#### Boas práticas

- Não duplique informações em outro módulo quando houver vínculo próprio.
- Não use Agenda Geral para toda tarefa pequena; use atividades para lembretes individuais.
- Prefira cancelar/arquivar registros com histórico em vez de excluir.
- Use títulos claros e consistentes.
- Revise a ajuda contextual depois de qualquer alteração de tela, campo ou fluxo.


### Fluxo 2: Validar documento

**Objetivo:** Conferir arquivo, metadados, validade e responsável antes de marcar como validado.


#### Quando usar

Use este fluxo quando o usuário precisar executar **validar documento** de forma rastreável, com responsável definido e histórico preservado.


#### Passo a passo recomendado

1. Acesse o menu principal do módulo.
2. Crie ou abra o registro operacional correto.
3. Preencha responsável principal, empresa e vínculos de negócio antes de avançar.
4. Preencha campos obrigatórios e revise mensagens de validação.
5. Quando houver tarefa individual, use **Agendar atividade**.
6. Quando houver marco crítico, compromisso ou prazo formal, use **Agenda Geral**.
7. Anexe documentos ou mídias no campo próprio do fluxo, evitando anexos soltos no chatter.
8. Salve e valide o resultado nos menus de acompanhamento.


#### Exemplo prático

| Campo | Exemplo |
|---|---|
| Documento | Certidão Negativa |
| Categoria | Jurídica/Fiscal conforme configuração |
| Tipo | Definido pelo cadastro de tipos documentais |
| Vencimento | 30/06 |
| Responsável | Juliana |

**Resultado esperado:** o documento fica rastreável, pode gerar atividade de revisão e, se for marco crítico, aparece na Agenda Geral. As opções reais de categoria/tipo são exibidas dinamicamente no drawer de ajuda.


#### Boas práticas

- Não duplique informações em outro módulo quando houver vínculo próprio.
- Não use Agenda Geral para toda tarefa pequena; use atividades para lembretes individuais.
- Prefira cancelar/arquivar registros com histórico em vez de excluir.
- Use títulos claros e consistentes.
- Revise a ajuda contextual depois de qualquer alteração de tela, campo ou fluxo.


### Fluxo 3: Controlar vencimento

**Objetivo:** Registrar validade e acompanhar atividades ou marcos relevantes na Agenda Geral.


#### Quando usar

Use este fluxo quando o usuário precisar executar **controlar vencimento** de forma rastreável, com responsável definido e histórico preservado.


#### Passo a passo recomendado

1. Acesse o menu principal do módulo.
2. Crie ou abra o registro operacional correto.
3. Preencha responsável principal, empresa e vínculos de negócio antes de avançar.
4. Preencha campos obrigatórios e revise mensagens de validação.
5. Quando houver tarefa individual, use **Agendar atividade**.
6. Quando houver marco crítico, compromisso ou prazo formal, use **Agenda Geral**.
7. Anexe documentos ou mídias no campo próprio do fluxo, evitando anexos soltos no chatter.
8. Salve e valide o resultado nos menus de acompanhamento.


#### Exemplo prático

| Campo | Exemplo |
|---|---|
| Documento | Certidão Negativa |
| Categoria | Jurídica/Fiscal conforme configuração |
| Tipo | Definido pelo cadastro de tipos documentais |
| Vencimento | 30/06 |
| Responsável | Juliana |

**Resultado esperado:** o documento fica rastreável, pode gerar atividade de revisão e, se for marco crítico, aparece na Agenda Geral. As opções reais de categoria/tipo são exibidas dinamicamente no drawer de ajuda.


#### Boas práticas

- Não duplique informações em outro módulo quando houver vínculo próprio.
- Não use Agenda Geral para toda tarefa pequena; use atividades para lembretes individuais.
- Prefira cancelar/arquivar registros com histórico em vez de excluir.
- Use títulos claros e consistentes.
- Revise a ajuda contextual depois de qualquer alteração de tela, campo ou fluxo.


## 5. Boas práticas gerais

- Preencha responsáveis antes de criar atividades ou agenda.
- Use o campo próprio do módulo para anexos, documentos e mídias.
- Evite anexos soltos no chatter quando houver modelo/documento específico.
- Use nomes objetivos: `Vistoria - Sala Comercial 301`, `Prazo de Resposta - Caso X`, `Vencimento - Certidão Negativa`.
- Consulte o botão **Ajuda** para confirmar campos obrigatórios, filtros e categorias reais.

## 6. Erros comuns

| Erro | Causa provável | Como resolver |
|---|---|---|
| Opção citada no treinamento não existe | A configuração do cliente é diferente | Consulte a seção dinâmica do drawer; não dependa de lista fixa no manual. |
| Agenda não aparece | Faltou data, responsável ou sincronização | Preencha responsável/data e use ação de sincronização quando disponível. |
| Atividade no tipo errado | Usuário escolheu atividade de outro fluxo | Use tipos específicos do módulo ou Pendência Operacional. |
| Duplicidade de informação | Criou novo registro em vez de atualizar o vínculo existente | Atualize o registro original ou use vínculo/dossiê correto. |
| Usuário vê informação demais | Visibilidade, responsável ou regra de acesso incorreta | Revisar permissões, equipe e visibilidade do registro/agenda. |
