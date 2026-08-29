# Guia de Testes — Central de Ajuda

## 1. Objetivo

Validar instalação, segurança, fluxos funcionais, Agenda Geral, atividades e ajuda contextual do módulo `common_help_center`.

## 2. Massa de dados mínima

| Item | Exemplo |
| --- | --- |
| Usuário operacional | João Operacional |
| Gestor/admin | Ana Gestora |
| Empresa | Empresa padrão |
| Registro base | Registro principal do módulo |

## 3. Testes funcionais

| Teste | Passos | Resultado esperado |
| --- | --- | --- |
| Criar registro em Central de Ajuda | Abrir menu principal, clicar em Novo, preencher campos obrigatórios e salvar. | Registro salvo sem erro. |
| Criar atividade | No chatter, usar Agendar atividade com Pendência Operacional. | Atividade atribuída ao responsável correto. |
| Criar marco na Agenda Geral | Preencher responsável e prazo/horário, sincronizar agenda quando o fluxo existir. | Item aparece na Agenda Geral e não no calendário nativo como reunião. |
| Ajuda contextual | Abrir tela principal e clicar em Ajuda. | Drawer mostra artigos do contexto primeiro. |
| Importação dos docs | Executar Importar Documentação na Central de Ajuda. | Artigos atualizados sem duplicidade. |



## 4. Testes técnicos por model

| Model | Teste recomendado |
| --- | --- |
| help.article | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.category | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.checklist.template | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.checklist.item | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.checklist.progress | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.context | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.context.candidate | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.doc.source | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.feedback | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.learning.path | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.learning.step | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.metric | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.suggestion.rule | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.tag | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |
| help.tip | Criar, editar, validar campos obrigatórios, testar permissões e abrir ajuda contextual. |



## 5. Testes de segurança

- [ ] Usuário operacional vê apenas menus permitidos.
- [ ] Usuário sem grupo não acessa registros protegidos.
- [ ] Administrador funcional consegue configurar dados mestres.
- [ ] Multiempresa respeita isolamento quando aplicável.

## 6. Testes de regressão

- [ ] Atualização do módulo não remove documentos antigos.
- [ ] Importação de documentação não duplica artigos por `code`.
- [ ] Tabelas Markdown renderizam como tabela no frontend da Central de Ajuda.
- [ ] Drawer de ajuda não quebra a tela atual.
