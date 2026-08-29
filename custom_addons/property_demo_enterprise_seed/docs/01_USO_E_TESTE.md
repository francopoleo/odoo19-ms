# Guia rápido de uso e teste

## Cenários que devem aparecer

Após gerar 60 contratos, você deve encontrar:

- contratos `DEMO-IMOB` ativos;
- contratos encerrados com parcelas históricas pagas;
- contratos inadimplentes com parcelas atrasadas;
- contratos a vencer para testar alertas;
- parcelas futuras em aberto;
- parcelas parcialmente pagas;
- comprovantes `DEMO-IMOB-E2E-*` no estado conciliado;
- dossiês de contrato com documentos completos e pendentes;
- casos de governança associados a imóveis e contratos.

## Filtros recomendados

Use o termo `DEMO-IMOB` nas listas de:

- Contratos;
- Parcelas;
- Comprovantes de pagamento;
- Dossiês;
- Documentos;
- Casos de governança;
- Vistorias;
- Manutenções;
- Aditivos;
- Valuation.

## Regerar massa

Abra **Imóveis > Dados de Teste**, marque **Apagar massa DEMO-IMOB antes de gerar** e execute novamente.

## Checklist técnico

- O módulo deve estar instalado apenas em ambiente de teste.
- Os módulos base de imóveis, documentos, dossiês, governança, comprovantes e valuation devem estar instalados.
- Caso a base não tenha imóveis suficientes, o gerador cria imóveis fallback com prefixo `DEMO-IMOB`.
- Caso existam imóveis reais de teste, o gerador usa estes imóveis antes de criar fallback.
