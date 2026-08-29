# Guia de Implementação — Central de Ajuda

## 1. Escopo

Implantar e validar o módulo `common_help_center` em ambiente Odoo 19.

## 2. Ordem recomendada

1. Validar dependências.
2. Fazer backup.
3. Copiar módulo para `custom_addons`.
4. Atualizar lista de apps.
5. Instalar/atualizar módulo.
6. Rodar testes.
7. Importar documentação na Central de Ajuda.
8. Validar ajuda contextual e mapa de contextos.

## 3. Comandos

```bash
./odoo-bin -d ms -u common_help_center --stop-after-init
```

## 4. Critérios de aceite

| Critério | Aceito quando |
| --- | --- |
| Instalação | Módulo carrega sem traceback. |
| Menus | Menus aparecem para usuários corretos. |
| Fluxos | Fluxos principais salvam e criam atividades/agendas conforme regra. |
| Ajuda | Drawer exibe contexto e artigos corretos. |
| Docs | Central importa `docs/*.md` sem duplicidade. |

## 5. Rollback

1. Restaurar ZIP anterior do módulo.
2. Rodar update do módulo.
3. Se necessário, restaurar backup do banco.
4. Limpar assets se houve alteração JS/SCSS.
