# Implementação Completa — Sistema de Mídias e Galeria

**Status**: ✅ FASE 1 + FASE 2 CONCLUÍDAS
**Data**: 2026-05-19
**Versão**: v1.0.0

---

## 📋 Checklist de Implementação

### FASE 1 — Consolidação do Modelo ✅

- ✅ **1.1** Constraint `is_cover` única por asset
  - Arquivo: `property_core/models/property_media.py`
  - Método: `_check_is_cover_unique()`
  - Testa: Apenas 1 foto com `is_cover=True` por imóvel

- ✅ **1.2** Stat button "Mídias" em Manutenção
  - Arquivo: `property_core/models/property_maintenance.py` (line 178)
  - Método: `action_view_media()`
  - Arquivo: `property_core/views/property_maintenance_views.xml` (lines 57-66)

- ✅ **1.3** Stat button invisível quando vazio
  - Arquivo: `property_core/views/property_asset_views.xml`
  - Atributo: `invisible="media_count == 0"`

- ✅ **1.4** View Kanban de `property.media`
  - Arquivo: `property_core/views/property_media_views.xml`
  - Kanban com thumbnails `image_512` visíveis
  - Action mode: `view_mode="kanban,list,form"`

- ✅ **1.5** Aba de Mídias em Documento
  - Arquivo: Herdada em `property_core/views/property_document_views.xml`
  - Exibe media_ids com kanban inline

---

### FASE 2 — Wizard de Upload em Lote ✅

- ✅ **2.1** Modelo TransientModel
  - Arquivo: `property_core/wizard/property_media_bulk_wizard.py`
  - Modelos: `PropertyMediaBulkWizard` + `PropertyMediaBulkWizardLine`

- ✅ **2.2** Campos do Wizard
  - Contextos: asset_id, inspection_id, maintenance_id, document_id
  - Settings: media_role, visibility_level, website_published, allow_download
  - Upload: image_ids (Many2many ir.attachment com widget many2many_binary)

- ✅ **2.3** Fluxo de 3 Passos
  - Step 1: Seleção de contexto + configurações
  - Step 2: Upload de múltiplos arquivos
  - Step 3: Confirmação com revisão

- ✅ **2.4** Métodos de Ação
  - `action_next_step()` — validação e progressão
  - `action_previous_step()` — volta ao passo anterior
  - `action_create_media()` — criação final com `ir.actions.act_window_close`

- ✅ **2.5** View do Wizard
  - Arquivo: `property_core/wizard/property_media_bulk_wizard_views.xml`
  - 3 divs com `invisible="step != 'step_name'"`
  - Footer com botões de navegação e confirmação

- ✅ **2.6** Integração nos Forms
  - Arquivo: `property_core/views/property_asset_views.xml`
  - Arquivo: `property_core/views/property_inspection_views.xml` (2026-05-19)
  - Arquivo: `property_core/views/property_maintenance_views.xml` (2026-05-19)
  - Botão: `action_open_bulk_media_wizard` em cada contexto

---

### REFATORAÇÃO — Vistoria (2026-05-19) ✅

**Antes**: "Fotos / Arquivos" genérico + 2 abas no notebook
**Depois**: Dois tabs separados com kanban visual

- ✅ **Aba 1: "Relatório da Vistoria"**
  - Domain: `[('inspection_id', '=', id), ('file_data', '!=', False), ('image_1920', '=', False)]`
  - Display: Kanban com ícone PDF (fa-file-pdf-o, 48px, #dc3545)
  - Campos: name, file_name, file_size (bytes)
  - Form simplificado: name, file_name, file_size, description

- ✅ **Aba 2: "Fotos da Vistoria"**
  - Domain: `[('inspection_id', '=', id), ('image_1920', '!=', False)]`
  - Display: Kanban com thumbnails `/web/image/property.media/{id}/image_512`
  - Campos: thumbnail, name, location_note
  - Form com dual image (Preview 256x256 + Ampliada 512x512)

- ✅ **Melhorias**:
  - Removido generic "Fotos / Arquivos" group com attachment_ids
  - Buttons persistentes (não esconde quando media_count > 0)
  - Alert boxes com explicação clara
  - Ícones com title attributes (Odoo 19 compliance)

---

### REFATORAÇÃO — Manutenção (2026-05-19) ✅

**Status**: Alinhado com padrão Vistoria

- ✅ **Aba 1: "Orçamentos"**
  - Domain: `[('maintenance_id', '=', id), ('file_data', '!=', False), ('image_1920', '=', False)]`
  - Display: Kanban com ícone PDF
  - Campos: name, file_name, file_size
  - Form: name, file_name, file_size, description

- ✅ **Aba 2: "Evidências Fotográficas"**
  - Domain: `[('maintenance_id', '=', id), ('image_1920', '!=', False)]`
  - Display: Kanban com thumbnails + badge (ANTES/DEPOIS)
  - Campos: thumbnail, name, media_role (badge), location_note
  - Form com dual image + description

- ✅ **Melhorias**:
  - Removido generic "Fotos / Orçamentos" group
  - Buttons persistentes
  - Alert boxes alinhadas
  - Badges de media_role para distinguir before/after

---

### ASSET — Galeria do Imóvel ✅

**Status**: Já bem-estruturada e mantida

- ✅ **Page: "Galeria do Imóvel"**
  - Domain: `[('media_role', 'in', ('gallery', 'marketing'))]`
  - Display: Kanban com thumbnails + badges (Capa ★, Publicada)
  - Campos: name, media_role, is_cover, website_published
  - Form: informações + imagem ampliada + detalhes

- ✅ **Alert Box**:
  - Explica as duas categorias permitidas (Galeria, Marketing)
  - Mostra como marcar como capa (★)

---

## 🔍 Verificação de Código

### Modelos (Models) ✅

**property_media.py**:
- ✅ Campos: media_role, visibility_level, website_published, is_cover, image_1920, image_512, file_data, file_name, file_mimetype, file_size
- ✅ Computed: `_compute_file_meta()` — calcula file_mimetype e file_size de ambos file_data e image_1920
- ✅ Constraint: `_check_is_cover_unique()` — garante única capa por asset
- ✅ Context fields: asset_id, inspection_id, maintenance_id, document_id (para multi-context)

**property_asset.py**:
- ✅ Métodos: `action_view_media()`, `action_open_bulk_media_wizard()`

**property_inspection.py**:
- ✅ Métodos: `action_open_bulk_media_wizard()`

**property_maintenance.py**:
- ✅ Métodos: `action_view_media()`, `action_open_bulk_media_wizard()`

**property_media_bulk_wizard.py** (novo):
- ✅ `PropertyMediaBulkWizard` TransientModel
- ✅ `PropertyMediaBulkWizardLine` TransientModel para edição de detalhes
- ✅ Método: `action_next_step()` — navegação com validação
- ✅ Método: `action_previous_step()` — volta
- ✅ Método: `action_create_media()` — criação com `ir.actions.act_window_close`

### Views (XML) ✅

**property_asset_views.xml**:
- ✅ Page "Galeria do Imóvel" com kanban + alert box
- ✅ Button "📸 Adicionar Fotos" → `action_open_bulk_media_wizard`
- ✅ Kanban com campos: image_512, name, media_role, is_cover, website_published
- ✅ Badges: ★ Capa (warning), Publicada (success)

**property_inspection_views.xml** (refatorado 2026-05-19):
- ✅ Aba 1: "Relatório da Vistoria"
  - Domain filters: file_data ≠ False, image_1920 = False
  - Kanban PDF cards
  - Button "📄 Adicionar Documento"
- ✅ Aba 2: "Fotos da Vistoria"
  - Domain filters: image_1920 ≠ False
  - Kanban image cards com location_note
  - Button "📸 Adicionar Fotos"

**property_maintenance_views.xml** (refatorado 2026-05-19):
- ✅ Aba 1: "Orçamentos"
  - Domain filters: file_data ≠ False, image_1920 = False
  - Kanban PDF cards
  - Button "📄 Adicionar Orçamento"
- ✅ Aba 2: "Evidências Fotográficas"
  - Domain filters: image_1920 ≠ False
  - Kanban image cards com before/after badges
  - Button "📸 Adicionar Fotos"

**property_media_bulk_wizard_views.xml** (novo):
- ✅ Form com 3 steps visíveis via `invisible="step != 'step_name'"`
- ✅ Step 1: Context selection + settings
- ✅ Step 2: Upload via many2many_binary
- ✅ Step 3: Confirmation review (readonly fields)
- ✅ Footer: Anterior (invisible on step 1), Próximo (invisible on step 3), Confirmar (visible on step 3), Cancelar

**property_media_views.xml**:
- ✅ Kanban view com image_512 thumbnails
- ✅ List view com colunas essenciais
- ✅ Form view completo
- ✅ Action: `view_mode="kanban,list,form"`

### Manifest ✅

**property_core/__manifest__.py**:
- ✅ "views/property_asset_views.xml"
- ✅ "views/property_media_views.xml"
- ✅ "views/property_inspection_views.xml"
- ✅ "views/property_maintenance_views.xml"
- ✅ "wizard/property_media_bulk_wizard_views.xml"
- ✅ "docs/MEDIA_SYSTEM.md"

---

## 🧪 Testes End-to-End (Recomendado)

### Teste 1: Upload de Fotos no Asset
```
1. Abrir imóvel
2. Aba "Galeria do Imóvel"
3. Clicar "📸 Adicionar Fotos"
4. Selecionar 3 imagens (JPG/PNG)
5. Wizard Step 1: Asset selecionado, role=gallery
6. Wizard Step 2: Selecionar arquivos via drag-drop
7. Wizard Step 3: Revisar e confirmar
8. Verificar fotos aparecem no kanban
9. Marcar uma como capa (is_cover)
10. Tentar marcar outra como capa → verificar erro de constraint
```

### Teste 2: Upload de Documentos em Vistoria
```
1. Abrir vistoria
2. Aba "Relatório da Vistoria"
3. Clicar "📄 Adicionar Documento"
4. Wizard Step 1: Inspection selecionada, role=inspection
5. Wizard Step 2: Upload PDF/Word
6. Confirmar
7. Verificar documento aparece em kanban (ícone PDF)
8. Verificar file_name, file_size preenchidos
```

### Teste 3: Upload de Fotos em Vistoria
```
1. Abrir vistoria
2. Aba "Fotos da Vistoria"
3. Clicar "📸 Adicionar Fotos"
4. Selecionar múltiplas imagens
5. Confirmar
6. Verificar thumbnails aparecem em kanban
7. Clicar em uma para editar: adicionar caption, location_note
8. Salvar e verificar badges/labels
```

### Teste 4: Upload em Manutenção (Orçamentos)
```
1. Abrir manutenção
2. Aba "Orçamentos"
3. Clicar "📄 Adicionar Orçamento"
4. Upload PDF de orçamento
5. Confirmar
6. Verificar documento em kanban com file_size
```

### Teste 5: Upload em Manutenção (Evidências)
```
1. Abrir manutenção
2. Aba "Evidências Fotográficas"
3. Clicar "📸 Adicionar Fotos"
4. Selecionar 2 fotos
5. Confirmar
6. Editar primeira foto: media_role="before" (antes)
7. Editar segunda foto: media_role="after" (depois)
8. Verificar badges ANTES/DEPOIS aparecem no kanban
```

### Teste 6: Domain Filtering
```
1. Asset com 5 fotos gallery + 2 PDFs de contrato
2. Aba "Galeria do Imóvel": verificar aparecem apenas as 5 fotos (não os PDFs)
3. Vistoria com 3 documentos + 4 fotos
4. Aba "Relatório": verificar aparecem apenas os 3 documentos
5. Aba "Fotos": verificar aparecem apenas as 4 fotos
```

### Teste 7: Metadados (file_name, file_size, file_mimetype)
```
1. Upload via wizard: "minha_foto_2026.jpg" + "orcamento.pdf"
2. Verificar no form após criar:
   - file_name = nome original do arquivo
   - file_size = tamanho em bytes (não 0)
   - file_mimetype = image/jpeg ou application/pdf
3. Verificar no kanban: tamanho exibido em bytes
```

### Teste 8: Restrições de Visibilidade
```
1. Criar foto com visibility_level="internal"
2. Marcar website_published=true
3. Acessar `/imoveis/<id>` (site público)
4. Verificar que foto NÃO aparece (precisa visibility_level=public)
5. Mudar para visibility_level="public"
6. Recarregar site → foto deve aparecer
```

---

## 📁 Arquivos Modificados/Criados

### Novos Arquivos
- ✅ `property_core/wizard/property_media_bulk_wizard.py` (233 linhas)
- ✅ `property_core/wizard/property_media_bulk_wizard_views.xml` (104 linhas)
- ✅ `property_core/docs/MEDIA_SYSTEM.md` (216 linhas)
- ✅ `property_core/docs/IMPLEMENTATION_CHECKLIST.md` (este arquivo)

### Arquivos Modificados
- ✅ `property_core/models/property_media.py` (+constraint is_cover)
- ✅ `property_core/models/property_asset.py` (+action_view_media, +action_open_bulk_media_wizard)
- ✅ `property_core/models/property_inspection.py` (+action_open_bulk_media_wizard)
- ✅ `property_core/models/property_maintenance.py` (+action_view_media, +action_open_bulk_media_wizard)
- ✅ `property_core/views/property_asset_views.xml` (refactored media section)
- ✅ `property_core/views/property_inspection_views.xml` (refactored 2026-05-19)
- ✅ `property_core/views/property_maintenance_views.xml` (refactored 2026-05-19)
- ✅ `property_core/views/property_media_views.xml` (kanban view added)
- ✅ `property_core/__manifest__.py` (added wizard files)
- ✅ `property_core/wizard/__init__.py` (import property_media_bulk_wizard)

---

## 🚀 Próximas Fases (Futuro)

### FASE 3 — Website Público: Carrossel + Galeria
- Implementar Bootstrap Carousel com media.media filtrado por visibility_level=public
- Template de detalhe de imóvel com galeria visual
- Fallback para image_1920 do asset se sem mídias

### FASE 4 — Portal Proprietário: Galeria com Filtros
- Tabelas de categorias (Galeria, Vistoria, Manutenção, Marketing)
- Lightbox simples (modal Bootstrap)
- Foto de capa nas listagens

### FASE 5 — document_core: Mídias Associadas
- Aba "Mídias / Evidências" em documento.documento
- Kanban inline com media_ids filtrados

---

## 📝 Notas Técnicas

- **File Storage**: Usa campos Binary (`file_data` para documentos, `image_1920` para fotos)
- **Thumbnails**: `image_512` auto-computado do `image_1920`
- **File Metadata**: Calculado via `_compute_file_meta()` não-storado (sob demanda)
- **Constraints**: `_check_is_cover_unique()` garante uma única capa por imóvel
- **Multi-Context**: `asset_id`, `inspection_id`, `maintenance_id`, `document_id` — media pode estar vinculado a qualquer contexto
- **Domain Filtering**: Separação visual via domain na view (file_data vs image_1920)
- **Kanban Visual**: Ícones (PDF) vs Thumbnails (imagens)
- **Acessibilidade**: Todos FA icons com `title` attribute (Odoo 19 compliance)

---

**Status**: Pronto para testes end-to-end. Todas as componentes em lugar.
