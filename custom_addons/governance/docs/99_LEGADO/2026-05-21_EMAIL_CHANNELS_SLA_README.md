# Governance — Canais de E-mail, Tipos de Caso, SLA e Documentos

## O que foi implementado

Esta versão cria o conceito que não existia no módulo original:

- `governance.email.channel` — canal institucional de e-mail;
- vínculo obrigatório do canal com `governance.case.type`;
- tipos permitidos por canal;
- triagem para canais amplos;
- SLA configurável por empresa, tipo de caso e prioridade;
- metadados de e-mail no caso;
- registro de e-mail recebido como `governance.case.communication`;
- registro de e-mail enviado pelo composer do Odoo como comunicação de saída;
- integração documental separada em `governance_documents`, sem depender de `property_core`.

## Arquitetura correta

```text
Canal de E-mail = porta de entrada
Tipo de Caso = regra de negócio
Caso = acompanhamento institucional
Dossiê = checklist/documental
Documento = registro
Anexo = arquivo físico
```

O canal não define SLA, etapas, checklist ou fluxo. Ele apenas direciona o caso para um tipo.

## Onde encontrar no Odoo

Após atualizar o módulo:

- `Governança > Cadastros Operacionais > Canais de E-mail`
- `Governança > Administração > Canais de E-mail`
- `Governança > Administração > Regras de SLA`
- `Governança > Cadastros Operacionais > Tipos de Caso`

O menu de Administração depende do grupo `governance.group_governance_manager`. O menu em Cadastros Operacionais aparece para usuários internos com acesso de leitura.

## Ordem recomendada de atualização

```bash
./odoo-bin -d ms -u governance --stop-after-init
./odoo-bin -d ms -u governance_documents,governance_property,document_dossier_governance --stop-after-init
```

Ou tudo junto:

```bash
./odoo-bin -d ms -u governance,governance_documents,governance_property,document_dossier_governance --stop-after-init
```

## Configuração de e-mail

1. Configure SMTP em Ajustes técnicos do Odoo.
2. Configure Incoming Mail Server/IMAP para a caixa institucional.
3. Configure `mail.catchall.domain` com o domínio correto.
4. Abra cada canal e clique em **Criar/Atualizar Alias**.
5. Teste enviando e-mail para `governance@dominio`, `juridico@dominio`, etc.

## Regras de desenho

- Não usar caixas pessoais como fonte principal de governança.
- Não criar documento solto.
- Não colocar SLA no canal de e-mail.
- Não misturar portal, website e backoffice.
- Reclassificação do caso deve alterar o tipo, não o canal.
