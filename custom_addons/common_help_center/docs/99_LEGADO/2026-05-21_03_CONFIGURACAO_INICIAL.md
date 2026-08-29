# Configuração Inicial - Central de Ajuda

## 1. Instalação

Instale o módulo `common_help_center` normalmente pelo Odoo ou via comando:

```bash
./odoo-bin -d ms -i common_help_center --stop-after-init
```

## 2. Primeira importação

Após instalar:

1. Abra **Central de Ajuda > Configuração > Importar Documentação**.
2. Execute com as três opções marcadas:
   - Varrer módulos instalados
   - Importar fontes ativas
   - Gerar mapa de contextos

## 3. Categorias

As categorias devem representar áreas funcionais, não tipos de documento.

Correto:

```text
Documentos
Imóveis
Governança
Agenda Geral
Central de Ajuda
```

Evitar:

```text
Manual do Usuário
Documentação Técnica
```

O tipo do documento já é controlado pelo campo `article_type`.

## 4. Política de reimportação

Use por padrão:

```text
Preservar edições feitas no Odoo
```

Use `Sobrescrever sempre pelo Markdown` somente quando a documentação versionada for a fonte única.

## 5. Checklist inicial

- [ ] Instalar o módulo.
- [ ] Rodar importação de documentação.
- [ ] Gerar Mapa de Contextos.
- [ ] Revisar contextos sem artigo.
- [ ] Criar/ajustar `08_AJUDA_CONTEXTUAL.md` nos módulos principais.
- [ ] Testar botão Ajuda em Documentos, Imóveis e Governança.
- [ ] Validar permissões para usuário comum e administrador.
