# 06 — Segurança, Multiempresa e Auditoria

## Grupos de acesso

O módulo cria dois grupos:

### Usuário de Valuation

Grupo:

```text
property_valuation_engine.group_property_valuation_user
```

Permite operar o módulo, consultar registros e criar estimativas.

### Gestor de Valuation

Grupo:

```text
property_valuation_engine.group_property_valuation_manager
```

Herda o grupo de usuário e permite gerenciar configurações como:

- fontes;
- fatores;
- algoritmos;
- referências;
- cadastros de mercado.

## Segurança por modelo

O arquivo `security/ir.model.access.csv` define permissões para:

- `property.valuation.source`;
- `property.valuation.factor`;
- `property.price.m2.reference`;
- `property.market.comparable`;
- `property.valuation.algorithm`;
- `property.valuation.run`.

## Regras multiempresa

O módulo usa `company_id` nos principais modelos.

Regra aplicada:

```text
Registros sem empresa definida ou da empresa atual podem ser acessados.
```

Domínio padrão usado nas regras:

```python
['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]
```

## Quando usar registros globais

Um registro com `company_id` vazio pode ser usado como referência global.

Exemplos:

- fator padrão `high = 1.15`;
- algoritmo híbrido padrão;
- fonte genérica `Pesquisa Manual`.

## Quando usar registros por empresa

Use `company_id` preenchido quando o dado é específico de uma empresa.

Exemplos:

- tabela de valor m² negociada por uma empresa;
- comparáveis internos sigilosos;
- fontes com contratos específicos;
- parâmetros aprovados por diretoria.

## Auditoria da estimativa

Cada estimativa gera registro próprio em `property.valuation.run`.

O registro guarda:

- data;
- método;
- imóvel;
- área;
- valor m² base;
- comparáveis;
- fontes;
- fatores;
- valor calculado;
- valor aprovado;
- usuário aprovador;
- data de aprovação;
- memória de cálculo.

## Recomendações enterprise

1. Nunca apagar estimativas aprovadas.
2. Preferir arquivar registros antigos com `active = False`.
3. Usar `review_notes` para justificar ajustes manuais.
4. Separar usuário operacional de gestor aprovador.
5. Não permitir edição livre de fatores em produção sem aprovação.
6. Criar rotina mensal de revisão das referências m².
7. Guardar fonte e data de toda informação externa.

## Controle sugerido de responsabilidades

| Responsável | Atividade |
|---|---|
| Comercial | Cadastra comparáveis e pesquisas |
| Gestão patrimonial | Revisa padrão, área e liquidez |
| Financeiro | Valida impactos de aluguel/venda |
| Jurídico/Governança | Valida uso documental e riscos |
| Diretoria/Gestor | Aprova valor final |
| TI | Mantém integrações e permissões |
