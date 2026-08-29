# Document Core — Perfis, Filtros e Governança Operacional

## Objetivo da melhoria

Esta versão separa claramente a operação diária de documentos da configuração documental.

A operação pode cadastrar documentos, anexar arquivos, informar datas, origem, protocolo, responsável e localização física já existente. A configuração de categorias, tipos documentais, regras de acesso, publicação e validação fica restrita ao perfil gestor.

## Perfis

### Documentos - Operacional

Perfil para usuários que fazem o cadastramento e manutenção básica dos documentos.

Permissões:

- criar documentos;
- editar documentos;
- anexar arquivos;
- consultar categorias documentais;
- consultar tipos documentais;
- consultar localizações físicas;
- consultar documentos respeitando a regra multiempresa;
- não excluir documentos;
- não criar categorias;
- não criar tipos documentais;
- não criar localizações físicas;
- não alterar regras de acesso, publicação, sensibilidade ou validação formal.

### Documentos - Gestor

Perfil para usuários responsáveis pela governança documental.

Permissões:

- todas as permissões do operacional;
- criar, editar e excluir documentos;
- criar e editar categorias documentais;
- criar e editar tipos documentais;
- criar e editar localizações físicas;
- alterar nível de acesso, publicação, sensibilidade e validação;
- acessar menus de configuração.

### Administrador do Sistema

O grupo técnico `base.group_system` herda automaticamente `Documentos - Gestor`.

## Filtros prontos em Documentos

Foram adicionados filtros operacionais para:

- Vigentes;
- Rascunhos;
- Arquivados;
- Válidos;
- A vencer;
- Vencidos;
- Sem vencimento;
- Exigem validação;
- Pendentes de validação;
- Validados;
- Revisão próxima;
- Revisão atrasada;
- Sensíveis;
- Publicados no site;
- Com original físico.

## Agrupamentos prontos em Documentos

Foram adicionados agrupamentos por:

- Categoria;
- Tipo;
- Situação;
- Estado;
- Responsável;
- Origem;
- Nível de acesso;
- Empresa;
- Mês de vencimento.

A ação principal de documentos abre agrupada por categoria por padrão.

## Filtros prontos em Tipos de Documento

Foram adicionados filtros para:

- Ativos;
- Inativos;
- Exigem emissão;
- Exigem vencimento;
- Exigem revisão;
- Exigem validação;
- Exigem original físico;
- Sensíveis;
- Publicáveis no site.

## Agrupamentos prontos em Tipos de Documento

Foram adicionados agrupamentos por:

- Categoria;
- Aplicável a;
- Acesso padrão;
- Validação;
- Vencimento.

## Filtros prontos em Categorias

Foram adicionados filtros para:

- Ativas;
- Inativas;
- Publicáveis no site.

## Agrupamentos prontos em Categorias

Foram adicionados agrupamentos por:

- Acesso padrão;
- Publicação no site.

## Filtros prontos em Localizações Físicas

Foram adicionados filtros para:

- Ativas;
- Inativas.

## Agrupamentos prontos em Localizações Físicas

Foram adicionados agrupamentos por:

- Empresa;
- Unidade;
- Responsável.

## Regras anti-cadastro indevido

Para reduzir nomes errados e valores duplicados:

- campos Many2one operacionais foram configurados com `no_create` e `no_create_edit`;
- o perfil operacional não tem permissão de criação em categorias, tipos e localizações;
- campos sensíveis de governança foram ocultados para operacional;
- o backend bloqueia alteração manual de campos de acesso, publicação, sensibilidade e validação por usuários que não sejam gestores.

## Campos bloqueados para o perfil operacional

- Nível de acesso;
- Grupos internos autorizados;
- Publicação no site;
- Visibilidade no site;
- Permitir download;
- Documento sensível;
- Validado por;
- Data da validação.

Esses campos devem ser governados pelo tipo documental ou pelo gestor documental.
