# Fluxo Enterprise de Dossiês Documentais

## Objetivo

O dossiê passa a ser a camada padrão de organização, checklist e conferência documental para Governança, Imóveis e Contratos.

## Modelo final

- `document.document`: documento único do ERP, com anexos, tipo, categoria, validade, revisão, acesso e pré-visualização.
- `dossier.dossier`: agrupador documental, com processo, responsável, status, documentos e completude.
- `dossier.assign.wizard`: wizard único para criar ou selecionar dossiê e vinculá-lo ao registro de origem.

## Vínculos suportados

- Governança: `governance.case.dossier_id`
- Contrato: `property.contract.dossier_id`
- Imóvel: `property.asset.dossier_ids`
- Documento: `document.document.dossier_ids`

## Regra de convivência

Um documento pode continuar vinculado diretamente ao imóvel, contrato ou caso e também compor um ou mais dossiês. O dossiê não duplica arquivo; ele organiza e controla a completude.

## Botão Atribuir Dossiê

O botão abre o wizard `dossier.assign.wizard`, que permite:

1. Criar novo dossiê ou selecionar existente.
2. Escolher tipo de processo.
3. Aplicar template.
4. Incluir documentos existentes do registro.
5. Opcionalmente incluir documentos de registros relacionados.
6. Criar documentos esperados que ainda não existem.

## Documentos Avulsos

O menu **Documentos Avulsos** agora mostra somente documentos sem vínculo com dossiê:

```python
[("dossier_ids", "=", False)]
```

## Documentos do Dossiê

O menu **Documentos do Dossiê** mostra documentos com pelo menos um dossiê:

```python
[("dossier_ids", "!=", False)]
```

## Compatibilidade Odoo 19

As ações Python que usavam `tree` foram ajustadas para `list`.
