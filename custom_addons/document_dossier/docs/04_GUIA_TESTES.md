# Guia de Testes — Document Dossier - Aggregator

> **Regra de documentação viva**  
> Este módulo usa a Central de Ajuda. Os artigos longos ficam na Biblioteca; os artigos curtos e contextuais ficam em `docs/08_AJUDA_CONTEXTUAL.md`. A Central complementa automaticamente o drawer com campos obrigatórios, opções `selection`, categorias cadastradas, tipos relacionados e filtros reais da tela. Por isso, os textos não devem listar manualmente opções que são configuráveis no sistema; devem explicar quando usar, por que usar e mostrar exemplos de decisão.

## 1. Objetivo

Validar os fluxos funcionais, permissões, documentação contextual, atividades e Agenda Geral do módulo.

## 2. Ambiente

- Banco de homologação atualizado.
- Usuário administrador funcional.
- Usuário operacional sem permissões administrativas.
- Central de Ajuda instalada e importada.

## 3. Testes obrigatórios da Central de Ajuda

| Teste | Passos | Resultado esperado |
|---|---|---|
| Abrir drawer | Acessar tela principal e clicar em Ajuda | Drawer abre sem mudar de tela. |
| Contexto correto | Verificar cabeçalho do drawer | Exibe `model / view` coerente com a tela. |
| Artigo contextual | Verificar primeiro artigo | Artigo curto do fluxo aparece antes dos documentos completos. |
| Opções dinâmicas | Verificar seção dinâmica | Campos obrigatórios, selections, categorias/tipos e filtros aparecem quando disponíveis. |
| Mapa de Contextos | Gerar mapa | Telas críticas ficam Documentadas ou apontam pendência clara. |

## 4. Testes funcionais por fluxo

### Teste 1: Criar dossiê

**Pré-condição:** cadastros de apoio criados e usuário com permissão funcional.

**Passos:**
1. Abrir o menu do módulo.
2. Criar ou abrir registro de teste.
3. Preencher responsáveis e vínculos obrigatórios.
4. Executar o fluxo: Criar dossiê.
5. Criar atividade quando houver tarefa individual.
6. Criar/sincronizar Agenda Geral quando houver marco crítico.
7. Abrir o drawer Ajuda e validar o artigo contextual.

**Resultado esperado:**
- Registro salvo sem erro.
- Histórico preservado.
- Atividade criada apenas quando cabível.
- Agenda Geral criada apenas quando for marco relevante.
- Ajuda contextual mostra fluxo e opções dinâmicas reais.

### Teste 2: Aplicar template

**Pré-condição:** cadastros de apoio criados e usuário com permissão funcional.

**Passos:**
1. Abrir o menu do módulo.
2. Criar ou abrir registro de teste.
3. Preencher responsáveis e vínculos obrigatórios.
4. Executar o fluxo: Aplicar template.
5. Criar atividade quando houver tarefa individual.
6. Criar/sincronizar Agenda Geral quando houver marco crítico.
7. Abrir o drawer Ajuda e validar o artigo contextual.

**Resultado esperado:**
- Registro salvo sem erro.
- Histórico preservado.
- Atividade criada apenas quando cabível.
- Agenda Geral criada apenas quando for marco relevante.
- Ajuda contextual mostra fluxo e opções dinâmicas reais.

### Teste 3: Converter documentos avulsos

**Pré-condição:** cadastros de apoio criados e usuário com permissão funcional.

**Passos:**
1. Abrir o menu do módulo.
2. Criar ou abrir registro de teste.
3. Preencher responsáveis e vínculos obrigatórios.
4. Executar o fluxo: Converter documentos avulsos.
5. Criar atividade quando houver tarefa individual.
6. Criar/sincronizar Agenda Geral quando houver marco crítico.
7. Abrir o drawer Ajuda e validar o artigo contextual.

**Resultado esperado:**
- Registro salvo sem erro.
- Histórico preservado.
- Atividade criada apenas quando cabível.
- Agenda Geral criada apenas quando for marco relevante.
- Ajuda contextual mostra fluxo e opções dinâmicas reais.

## 5. Testes de segurança

- [ ] Usuário operacional vê apenas menus permitidos.
- [ ] Administrador funcional vê configurações.
- [ ] Conteúdo técnico da ajuda aparece apenas para público adequado quando configurado.
- [ ] Registros sensíveis respeitam responsáveis, equipe e grupos.

## 6. Testes de regressão

- [ ] Atualizar módulo com `-u` não duplica artigos da Central.
- [ ] Reimportar documentação não duplica artigos com mesmo `code`.
- [ ] Markdown com tabela renderiza corretamente.
- [ ] Arquivo `08_AJUDA_CONTEXTUAL.md` sem bloco válido não quebra importação.
