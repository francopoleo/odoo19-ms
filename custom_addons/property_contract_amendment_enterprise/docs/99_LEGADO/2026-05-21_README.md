# Documentação — Contratos e Aditivos Imobiliários Empresarial

Este diretório documenta o módulo `property_contract_amendment_enterprise` para Odoo 19 Community.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `MANUAL_USUARIO.md` | Explicação funcional completa para usuários operacionais, gestores, financeiro e jurídico. |
| `FLUXO_ADITIVOS.md` | Fluxo ponta a ponta de criação, aprovação, assinatura e aplicação de aditivos. |
| `OPCOES_COMPLETAS.md` | Lista completa dos tipos, status, motivos, motivos financeiros, tipos de documento e opções do módulo. |
| `INSTALACAO_E_OPERACAO.md` | Instalação, atualização, permissões, menus e rotina operacional. |
| `MODELO_TECNICO.md` | Modelos Odoo, campos principais e integrações internas. |

## Objetivo do módulo

O módulo trata aditivos contratuais como eventos formais, auditáveis e versionados dentro do app **Imóveis**. Ele permite registrar o motivo da mudança, classificar impactos, controlar aprovações, armazenar documentos, criar novas regras financeiras, registrar ajustes retroativos e manter histórico das condições aplicadas ao contrato.


## Seleção controlada na aba Alterações

A aba **Alterações** usa o campo **Campo do Contrato** em formato de seleção controlada.
O usuário operacional não precisa digitar campo técnico nem rótulo. Ao escolher uma opção, o módulo preenche automaticamente:

- categoria da alteração;
- campo técnico interno;
- rótulo amigável;
- tipo de valor;
- valor anterior do contrato.

Essa regra evita erros de digitação e garante que o botão **Aplicar ao Contrato** altere apenas campos previstos pelo módulo.


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
