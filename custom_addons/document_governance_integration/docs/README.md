# Governance Documents

Integração Community-first entre `governance` e `document_core`.

## Princípio

Documento nunca fica solto. O arquivo físico é `ir.attachment`; o registro `document.document` é o container documental; o `governance.case` é o hub semântico do caso.

## Fluxo

1. Abra o caso de governança.
2. Use **Novo Documento** para criar o documento vinculado.
3. Anexe um ou mais arquivos no documento.
4. Se houver dossiê, use `document_dossier_governance` para controlar checklist e completude.

Este módulo não depende de `property_core` e pode ser usado para casos jurídicos, administrativos, societários, auditoria, compliance e memória institucional.
