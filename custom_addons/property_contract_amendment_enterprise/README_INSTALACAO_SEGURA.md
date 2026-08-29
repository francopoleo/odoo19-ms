# Instalação segura — Contratos e Aditivos Imobiliários Empresarial

Esta versão mantém o módulo seguro para instalar/atualizar, sem carregar herança direta no formulário principal de `property.contract`.

## Por quê?

A view herdada do formulário principal do contrato depende da estrutura exata do módulo `property_core`. Como o seu ambiente já apresentou erro de validação de campos durante a instalação, esta versão evita mexer diretamente no formulário base do contrato e entrega a operação pelos menus próprios de **Aditivos Contratuais**.

## O que instala

- modelos de aditivos;
- motivos de aditivos;
- motivos financeiros;
- tipos de documentos;
- tabela de valores;
- plano de cobrança;
- ajustes financeiros;
- documentos contratuais;
- aprovações;
- obrigações;
- opções contratuais;
- histórico de termos;
- versões consolidadas;
- menus dentro de **Imóveis**;
- documentação na pasta `docs/`.

## O que não faz nesta versão segura

- Não injeta aba automática no formulário principal de `property.contract`.
- Não cria wizard de geração automática de minuta.
- Não envia assinatura eletrônica de forma automática.
- Não gera faturas automaticamente; deixa a estrutura pronta para integração com cobrança.

## Comando recomendado

```bash
cd /Users/franco/Dev/odoo/odoo19-ms
rm -rf custom_addons/property_contract_amendment_enterprise
unzip ~/Downloads/property_contract_amendment_enterprise_pt_br_docs_1_3_0.zip -d custom_addons/
./odoo-bin -d ms -u property_contract_amendment_enterprise --stop-after-init
```

Depois reinicie o Odoo normalmente.

## Verificações

```bash
grep -n "version" custom_addons/property_contract_amendment_enterprise/__manifest__.py
```

Resultado esperado:

```python
'version': '19.0.1.3.0'
```

```bash
find custom_addons/property_contract_amendment_enterprise -name "contract_views.xml"
```

Nesta versão, o comando não deve retornar arquivo.
