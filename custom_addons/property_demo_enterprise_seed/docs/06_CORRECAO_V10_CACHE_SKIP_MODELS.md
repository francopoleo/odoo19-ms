# Correção v10 — cache de models opcionais sem atributo no recordset

## Problema

A versão anterior tentava executar:

```python
self._demo_optional_skip_models = set()
```

Em Odoo 19, recordsets/model records não aceitam atributos arbitrários fora dos campos definidos.
Isso gerava:

```text
AttributeError: 'property.demo.generator' object has no attribute '_demo_optional_skip_models'
```

## Correção

O cache de models opcionais ignorados agora fica em uma variável de módulo, isolada por banco e cursor:

```python
_OPTIONAL_SKIP_MODELS_BY_CURSOR[(dbname, id(cursor))]
```

Assim o wizard pode pular models/tabelas opcionais quebradas sem tentar gravar atributos temporários no recordset.
