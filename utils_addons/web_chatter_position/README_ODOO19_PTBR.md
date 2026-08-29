# Chatter Position — Odoo 19

Este pacote foi ajustado para Odoo 19 a partir do módulo `web_chatter_position`.

## O que faz

Adiciona uma preferência no usuário para escolher a posição do Chatter:

- **Responsive / Responsivo**: comportamento padrão do Odoo.
- **Bottom / Inferior**: força o Chatter abaixo do formulário.
- **Sided / Lateral**: mantém o Chatter lateral quando houver espaço.

## Instalação manual

Este módulo foi configurado para instalação manual:

```python
"installable": True
"auto_install": False
"application": False
```

Por ser um módulo técnico de interface, ele não cria menu próprio.
Depois de copiar a pasta para `custom_addons`, atualize a lista de aplicativos e procure por:

```text
Chatter Position
```

Se o filtro **Apps** estiver ativo, remova o filtro para visualizar módulos técnicos.

## Após instalar

Acesse:

```text
Preferências do usuário → Chatter Position
```

Depois altere para `Responsive`, `Bottom` ou `Sided`.

## Limpeza de cache recomendada

Como o módulo altera assets web, após atualizar ou instalar execute:

```bash
./odoo-bin -d sua_base -u web_chatter_position --stop-after-init
```

Em seguida reinicie o Odoo e atualize o navegador com limpeza de cache.


## Ajuste v2
- Corrigida a posição do campo `chatter_position` na tela de preferências do usuário.
- Adicionado rótulo explícito do campo.
