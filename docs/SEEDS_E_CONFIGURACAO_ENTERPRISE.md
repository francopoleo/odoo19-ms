# Seeds e configuração Enterprise

## Objetivo

Deixar um banco novo operacional sem misturar código, configuração de produto,
dados populados e dados de demonstração. O reset deve recriar somente a
estrutura e os dados técnicos mínimos; a configuração empresarial deve entrar
por um seed explícito e os imóveis, contratos, documentos e casos populados
devem entrar por um seed demo separado.

## Diagnóstico da situação atual

A instalação atual carrega dados de negócio diretamente pelos módulos e também
possui dados semelhantes no `property_demo_enterprise_seed`.

| Origem atual | Conteúdo observado | Decisão preliminar |
|---|---|---|
| `property_core/data/property_asset_silva.xml` | 77 imóveis reais/KMS | Migrar para seed de portfólio; não deixar no core |
| `property_core/data/property_taxonomy_data.xml` | 45 classificações/taxonomias | Seed de configuração, após auditoria de uso |
| `property_core/data/property_media_category_data.xml` | 28 categorias de mídia | Seed de configuração |
| `document_core/data/document_seed_data.xml` | 338 registros de tipos/categorias documentais | Dividir em catálogo profissional e demo; remover do core |
| `document_dossier/data/dossier_process_data.xml` | 15 processos de dossiê | Seed de configuração/processos |
| `governance/data/*` | estágios, tipos, catálogo, SLA, canais e atividades | Seed de configuração; manter somente estrutura no módulo |
| `common_base/data/common_config_data.xml` | tags e configuração comum | Revisar e mover cadastros operacionais para configuração |
| `property_contract_amendment_enterprise/data/amendment_reason_data.xml` | cerca de 266 razões financeiras/contratuais | Reduzir para catálogo profissional curado e colocar em configuração |
| `property_demo_enterprise_seed/data/*` | imóveis, documentos, casos, dossiês e processos demo | Manter apenas dados populados e cenários de teste |
| `property_condominium_enterprise/demo/demo.xml` | dados de demonstração de condomínio | Consolidar no seed demo |

Na instalação limpa validada em 30/08/2026, o `property_core` não criou XML IDs
de imóveis e o portfólio KMS ficou no módulo opcional `property_portfolio_seed`.
O instalador padrão também não instala mais o módulo demo.

Nesta primeira etapa, o `enterprise_configuration_seed` usa um carregador de
compatibilidade para ler os arquivos legados nos módulos que definem os
modelos. Isso preserva XML IDs públicos e reduz risco. A etapa seguinte é
física: mover os catálogos para dentro do seed, revisar referências e reduzir
o catálogo de motivos de aditivo/financeiro para uma lista curada.

## Regra de arquitetura

### 1. Módulos funcionais

Devem conter:

- modelos Python, regras de negócio, segurança e views;
- sequências técnicas necessárias ao funcionamento;
- cron jobs técnicos;
- grupos de segurança e dados necessários para referenciar a estrutura;
- poucos registros invariantes, quando o código não puder funcionar sem eles.

Não devem conter imóveis, contratos, documentos de clientes, casos de
governança, contatos reais ou catálogos extensos de operação.

### 2. `enterprise_configuration_seed`

Novo módulo explícito para a configuração operacional padrão:

- tipos de perfil e papéis de stakeholders;
- tags e classificações profissionais;
- tipos de caso e triagem;
- estágios, prioridades e motivos padronizados;
- regras de SLA e atividades;
- canais e modelos de e-mail institucionais;
- categorias e tipos documentais;
- processos e modelos de dossiê;
- modelos de pendências/checklists;
- motivos de aditivo e motivos financeiros selecionados;
- fatores e algoritmos de avaliação padrão;
- categorias de mídia e índices de reajuste;
- configurações padrão de condomínio e cobrança.

Esse módulo deve ser instalável em banco vazio e não deve criar imóveis,
contratos ou pessoas de negócio.

### 3. `property_demo_enterprise_seed`

Deve conter somente massa populada e cenários demonstráveis:

- contatos fictícios;
- imóveis fictícios ou portfólio de demonstração expressamente autorizado;
- complexos, unidades e contratos demo;
- documentos vinculados a pessoas/imóveis demo;
- casos de governança, comunicações e pendências demo;
- dossiês preenchidos;
- pagamentos, comprovantes, avaliações, mídia e históricos demo;
- usuários portal e cenários multi-perfil.

O portfólio KMS real deve ser um seed separado, por exemplo
`property_portfolio_seed`, e não deve ficar misturado com a massa fictícia.

O instalador padrão não instala este módulo. Para obter a massa fictícia,
instale-o explicitamente depois do banco base estar validado.

## Catálogo operacional mínimo recomendado

### Governança e triagem

- Tipos de caso: solicitação, incidente, não conformidade, auditoria,
  regularização, risco, aprovação e disputa.
- Prioridades: baixa, normal, alta e crítica.
- Estágios: triagem, em análise, aguardando informação, em aprovação,
  em execução, resolvido e encerrado.
- Classificação: domínio, subdomínio, origem, impacto, risco e urgência.
- SLA por tipo/prioridade, com atividade de primeiro contato, coleta de
  evidências, revisão e encerramento.

### Perfis e partes interessadas

- proprietário, coproprietário, locatário, fiador, representante legal,
  administrador, corretor, imobiliária, síndico, prestador e auditor.
- relacionamento com vigência, documento de representação e nível de acesso.

### Documentos e dossiês

Categorias mínimas:

- identidade e capacidade;
- titularidade e propriedade;
- contrato e locação;
- fiscal e tributário;
- condomínio;
- financeiro;
- vistoria e manutenção;
- compliance, jurídico e governança;
- mídia e evidências.

Tipos e regras devem ter código estável, descrição, obrigatoriedade por
processo, validade, quem apresenta, quem valida, versão e necessidade de
assinatura. O catálogo não deve inventar dezenas de tipos sem uma regra de
negócio clara.

### Processos de dossiê iniciais

1. **Cadastro e validação do proprietário**
   - CPF/CNPJ, documento de identidade, comprovante de endereço,
     dados bancários, contrato/mandato de administração, representação legal
     quando aplicável e validação de titularidade.
2. **Cadastro e regularização do imóvel**
   - matrícula ou documento equivalente, IPTU, cadastro municipal,
     endereço, área, planta quando aplicável, certidões relevantes,
     condomínio, seguro e evidências de vistoria.
3. **Cadastro e validação do locatário**
   - identificação, comprovantes cadastrais, análise/aprovação,
     garantias e documentos contratuais.
4. **Locação e gestão contratual**
   - contrato assinado, anexos, laudo de vistoria, garantias,
     obrigações, reajustes e encerramento.
5. **Regularização condominial**
   - convenção, regimento, atas, orçamento, rateios, certidões,
     chamados e prestação de contas.
6. **Auditoria e não conformidade**
   - evidência, classificação, responsável, plano de ação, prazo,
     aprovação e encerramento.

## Usuários de teste padrão

O seed deve criar usuários fictícios, ativos e com senha conhecida somente em
ambiente de desenvolvimento:

- administrador técnico;
- operador interno;
- locatário portal;
- proprietário portal;
- governança portal;
- opcionalmente corretor e síndico portal.

O usuário proprietário pode acumular os papéis de proprietário e síndico para
testar multi-perfil, mas isso deve ser explícito no cenário. Nunca usar
contatos reais ou credenciais de produção.

## Plano de execução

### Fase 1 — inventário

- listar todos os XML/CSV carregados por cada manifesto;
- identificar modelo, XML ID, módulo proprietário e dependências;
- localizar duplicidades por nome, código e XML ID;
- separar dados técnicos, configuração, portfólio real e demo;
- validar quais registros são referenciados pelo código.

### Fase 2 — catálogo curado

- revisar categorias, tipos, tags, prioridades, canais e razões;
- eliminar classificações redundantes ou sem uso;
- adotar códigos estáveis e nomes profissionais;
- definir campos de validade, obrigatoriedade, SLA e responsáveis;
- documentar a matriz processo → documentos obrigatórios → validação.

### Fase 3 — extração dos módulos

- retirar imóveis e dados de clientes do `property_core`;
- retirar casos e documentos populados do `document_core` e `governance`;
- mover catálogos operacionais para `enterprise_configuration_seed`;
- separar o portfólio real em seed próprio;
- deixar o demo apenas com dados vinculados ao seu próprio namespace.

### Fase 4 — reset e validação

- resetar banco vazio;
- instalar módulos funcionais;
- instalar configuração enterprise;
- validar que existem tipos, processos e regras, mas zero imóveis,
  contratos, documentos de negócio e casos;
- instalar demo opcionalmente;
- validar usuários, permissões, portal e segregação por parceiro.

## Critérios de aceite

- banco funcional sem seed: estrutura instalada e nenhum dado de negócio;
- configuração enterprise: catálogos e processos prontos para operação;
- demo: massa claramente identificada, reversível e sem duplicar registros;
- nenhum imóvel KMS carregado duas vezes;
- nenhum documento/caso populado fora de um seed autorizado;
- usuários de teste criados somente pelo seed demo/dev;
- cada documento obrigatório possui processo, regra e responsável;
- instalação repetida é idempotente e não cria duplicatas.

## Próxima etapa

Executar a auditoria detalhada por módulo e gerar uma matriz final com:
`arquivo atual`, `modelo`, `quantidade`, `classificação`, `destino`,
`dependências`, `risco de migração` e `critério de remoção`. Só depois dessa
matriz deve ser feita a remoção dos dados dos módulos e a criação do novo seed
de configuração.
