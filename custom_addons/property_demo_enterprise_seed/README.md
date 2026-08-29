# Real Estate Enterprise Demo Seed

Módulo de massa de testes para o ERP imobiliário no Odoo 19.

O objetivo é permitir subir uma base de homologação com muitos dados integrados, sem misturar registros fictícios nos módulos produtivos.

## Melhor abordagem

A melhor forma não é usar importação manual de CSV para este caso. Contratos, parcelas, pagamentos, comprovantes conciliados, dossiês e governança têm muitas relações e regras automáticas. Por isso este módulo usa uma estratégia híbrida:

1. **Cadastros estáveis em Python idempotente** para templates de dossiê, central de ajuda, OCR e categorias de mídia.
2. **Wizard administrativo** para regenerar, limpar e controlar volume.
3. **Uso condicional dos módulos opcionais**: se governança, dossiê, OCR, comprovantes ou valuation não estiverem instalados, o seed pula aquela família sem derrubar o ambiente.
4. **Prefixo único `DEMO-IMOB`** para filtrar e apagar a massa de teste com segurança.

## O que o módulo cria

- Locatários e contatos sintéticos.
- Contratos ativos, a vencer, inadimplentes e encerrados/inativos.
- Parcelas abertas, pagas, parciais e atrasadas.
- Recebimentos confirmados.
- Comprovantes de pagamento já conciliados com parcelas.
- Pagadores autorizados para testar conciliação por terceiros.
- Dossiês de contratos com documentos completos e pendentes.
- Templates de dossiês para locação comercial, locação residencial, regularidade do imóvel, aditivos, cobrança e vistoria.
- Casos de governança vinculados a imóveis e contratos.
- Aditivos contratuais com alteração controlada.
- Vistorias e manutenções.
- Dados de valuation, incluindo fontes, referências por m², comparáveis e execuções.
- Proprietários, compradores, vendedores, investidores e incorporadoras.
- Imobiliárias parceiras e corretores com CRECI.
- Mandatos de corretagem, comissões pendentes/pagas/canceladas e vínculos com contratos.
- Repasses mensais ao proprietário com aluguéis, comissões e manutenções.
- Leads comerciais por imóvel e oportunidades de aquisição.
- Galeria/mídias de imóveis e arquivos técnicos.
- Históricos OCR de contratos e template de extração por regex.
- Tags, agenda geral, comunicação rastreável e registros básicos da Central de Ajuda.

## Instalação

Copie a pasta `property_demo_enterprise_seed` para um caminho presente no `addons_path`.

Depois atualize a lista de apps e instale:

```bash
./odoo-bin -d SUA_BASE -i property_demo_enterprise_seed --stop-after-init
```

Ao instalar, o módulo **não gera automaticamente** por padrão. A geração automática só acontece se o parâmetro `property_demo_enterprise_seed.auto_generate` estiver com valor `1`.

## Uso pelo Odoo

Acesse:

**Imóveis > Dados de Teste**

No wizard é possível informar:

- quantidade de contratos;
- meses anteriores e futuros para parcelas;
- se deve criar comprovantes conciliados;
- se deve criar dossiês;
- se deve criar casos de governança;
- se deve criar aditivos;
- se deve criar vistorias/manutenções;
- se deve criar valuation;
- se deve criar corretores, mandatos e comissões;
- se deve criar proprietários, repasses e extratos;
- se deve criar leads, compradores, vendedores e aquisições;
- se deve criar mídias, fotos e arquivos técnicos;
- se deve criar históricos OCR e templates de extração;
- se deve criar ajuda, tags, agenda e comunicações;
- se deve apagar a massa `DEMO-IMOB` antes de gerar novamente.

## Parâmetros opcionais

Antes da instalação, estes parâmetros podem ser definidos por shell/script ou manualmente em `ir.config_parameter`:

| Parâmetro | Padrão | Função |
|---|---:|---|
| `property_demo_enterprise_seed.auto_generate` | `0` | Use `1` para gerar automaticamente ao instalar. |
| `property_demo_enterprise_seed.contract_count` | `60` | Quantidade inicial de contratos. |
| `property_demo_enterprise_seed.months_past` | `10` | Meses anteriores para gerar parcelas já vencidas. |
| `property_demo_enterprise_seed.months_future` | `8` | Meses futuros para gerar parcelas em aberto. |

## Segurança

Não instale este módulo em produção. Ele cria registros fictícios e deve ficar restrito a ambientes de desenvolvimento, demonstração e homologação.

A limpeza busca registros pelo prefixo `DEMO-IMOB`, mas sempre faça backup antes de reconstruir a massa em uma base compartilhada.
