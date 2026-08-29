# Instalação e Operação

## 1. Dependências

O módulo depende de:

- `base`;
- `mail`;
- `account`;
- `analytic`;
- `property_core`.

## 2. Instalação local

```bash
cd /Users/franco/Dev/odoo/odoo19-ms
rm -rf custom_addons/property_contract_amendment_enterprise
unzip ~/Downloads/property_contract_amendment_enterprise_pt_br_docs_1_3_0.zip -d custom_addons/
./odoo-bin -d ms -u property_contract_amendment_enterprise --stop-after-init
```

Depois inicie o Odoo normalmente.

## 3. Instalação em Docker

```bash
docker compose exec web odoo -d ms -u property_contract_amendment_enterprise --stop-after-init
```

Se o serviço Odoo usa outro comando, adapte o nome do container e o nome da base.

## 4. Verificações após atualização

Confirme a versão:

```bash
grep -n "version" custom_addons/property_contract_amendment_enterprise/__manifest__.py
```

Resultado esperado:

```python
'19.0.1.3.0'
```

Confirme que a herança problemática do formulário principal do contrato não está sendo carregada:

```bash
find custom_addons/property_contract_amendment_enterprise -name "contract_views.xml"
```

Nesta versão segura, esse arquivo não deve existir.

## 5. Permissões

O módulo cria os grupos:

| Grupo | Função |
| --- | --- |
| Aditivos Contratuais / Usuário | Operação diária de aditivos, documentos, valores, obrigações e opções. |
| Aditivos Contratuais / Gestor | Configurações, motivos e tipos de documento. |
| Contratos / Jurídico | Revisão jurídica e aprovação jurídica. |
| Contratos / Financeiro | Revisão financeira e ajustes. |
| Contratos / Administrador | Administração plena do módulo. |

A versão atual adiciona o grupo de usuário de aditivos ao grupo interno do Odoo (`base.group_user`) para facilitar a visualização do menu operacional.

## 6. Se o menu não aparecer

Verifique:

1. Se o módulo atualizou sem erro.
2. Se o usuário é usuário interno.
3. Se a página foi recarregada com limpeza de cache: `Cmd + Shift + R`.
4. Se não existe módulo duplicado em outro `addons_path`:

```bash
find /Users/franco/Dev/odoo/odoo19-ms -path "*property_contract_amendment_enterprise/__manifest__.py" -print
```

## 7. Observação sobre integração com o contrato

Esta versão mantém o módulo seguro para instalação e não injeta uma aba automática no formulário principal de `property.contract`. A operação deve ser feita pelos menus de **Aditivos Contratuais**. Depois que o `property_core` estiver estabilizado, é possível reativar uma view herdada para exibir abas de aditivos diretamente dentro do contrato.
