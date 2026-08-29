# Sistema de Mídias e Fotos

Guia completo para usar o sistema unificado de mídias na plataforma.

## 📋 Índice Rápido

| Local | O que vai | Categoria | Propósito |
|-------|----------|-----------|----------|
| **Imóvel** → Galeria do Imóvel | Fotos | Galeria, Marketing | Website + Portal |
| **Vistoria** → Arquivos | Documentos, Fotos | Inspection | Documentar a vistoria |
| **Manutenção** → Orçamentos | PDFs, Notas Fiscais | Maintenance | Comprovantes de serviço |
| **Manutenção** → Evidências | Fotos Antes/Depois | Before, After | Evidência visual do trabalho |
| **Documento** → Mídias | Scans, Fotos | Document_support, Evidence | Apoio ao documento |

---

## 🏠 IMÓVEL → Galeria do Imóvel

**Donde vão**: Fotos exibidas no website e portal de proprietários/inquilinos

**Categorias permitidas**:
- **Galeria** - Fotos principais do imóvel
  - Fachada, sala de estar, cozinha, quartos, banheiros, jardim, garagem
  - São as fotos que aparecem no site quando alguém acessa o imóvel

- **Marketing** - Materiais comerciais
  - Fotos profissionais, brochuras, renders, materiais de divulgação

**Como adicionar**:
1. Abrir imóvel
2. Ir para aba "Galeria do Imóvel"
3. Clicar "📸 Adicionar Fotos"
4. Selecionar imagens no wizard
5. Escolher: Galeria ou Marketing
6. Confirmar

**Dica importante**:
- Marque UMA foto como **Capa** (★) - ela será exibida em destaque no site
- Fotos com `visibility_level = "public"` + `website_published = true` aparecem no site
- Fotos com `visibility_level = "portal"` aparecem apenas para proprietários logados

---

## 🔍 VISTORIA → Arquivos da Vistoria

**Donde vão**: Documentação da vistoria realizada

**O que colocar**:
- Fotos da vistoria (estado do imóvel)
- Relatório de vistoria (PDF)
- Documentos relacionados à inspeção
- Evidências fotográficas

**Como adicionar**:
1. Abrir vistoria
2. Ir para aba "Arquivos da Vistoria"
3. Clicar "📎 Adicionar Arquivos"
4. Selecionar fotos/documentos
5. Categoria: `Vistoria` (automático)
6. Confirmar

**Nota**: A visibilidade é automática (restrito ao imóvel/contract)

---

## 🔧 MANUTENÇÃO → Orçamentos + Evidências

### Aba 1: Orçamentos

**O que colocar**:
- Orçamento em PDF
- Nota Fiscal
- Recibo de pagamento
- Comprovante de serviço

**Como adicionar**:
1. Abrir manutenção
2. Ir para aba "Orçamentos"
3. Clicar "📄 Adicionar Orçamento"
4. Selecionar arquivo PDF
5. Categoria: `Maintenance` (automático)
6. Confirmar

### Aba 2: Evidências Fotográficas

**O que colocar**:
- Foto ANTES do trabalho
- Foto DEPOIS do trabalho
- Evidência visual do resultado

**Categorias obrigatórias**:
- **Antes** - Estado antes da manutenção
- **Depois** - Estado após a manutenção

**Como adicionar**:
1. Abrir manutenção
2. Ir para aba "Evidências Fotográficas"
3. Clicar "📸 Adicionar Fotos"
4. Selecionar fotos before/after
5. No wizard: escolher "Antes" ou "Depois"
6. Confirmar

**Dica**: Tire sempre fotos before+after para documentar o trabalho realizado

---

## 📄 DOCUMENTO → Mídias / Evidências

**Donde vão**: Suporte visual ao documento

**Exemplos**:
- Scan de contrato assinado (evidência)
- Foto de matrícula original
- Screenshot de e-mail importante
- Foto de documento validado

**Como adicionar**:
1. Abrir documento
2. Ir para aba "Mídias / Evidências"
3. Clicar "📸 Adicionar Evidência"
4. Selecionar foto/arquivo
5. Categoria: Document_support ou Evidence
6. Confirmar

---

## 🎯 Resumo de Categorias

```
┌─ Galeria do Imóvel
│  ├─ "Galeria" - Fotos do imóvel para site
│  └─ "Marketing" - Materiais comerciais
│
├─ Vistoria
│  └─ "Vistoria" - Fotos e docs da inspeção
│
├─ Manutenção
│  ├─ "Maintenance" - Orçamentos, notas fiscais
│  ├─ "Antes" - Fotos before
│  └─ "Depois" - Fotos after
│
└─ Documento
   ├─ "Document_support" - Apoio ao documento
   └─ "Evidence" - Evidência fotográfica
```

---

## 🔒 Visibilidade e Publicação

### Níveis de Visibilidade

- **Interno** - Apenas equipe (padrão)
- **Restrito Interno** - Usuários específicos
- **Corretores Autorizados** - Corretores cadastrados
- **Portal** - Proprietário/inquilino logado
- **Público** - Qualquer pessoa no site

### Publicar no Site

Marque `website_published = true` para exibir em:
- Listagem de imóveis
- Ficha do imóvel
- Galeria visual

**Regra**: Precisa ter `visibility_level = public` AND `website_published = true`

---

## 📊 Ver Todas as Mídias

Menu → Mídias e Fotos:
- Visualiza TODAS as mídias do sistema
- Filtro por categoria
- Filtro por imóvel
- Kanban visual com miniaturas

---

## ✅ Checklist de Upload

Ao adicionar fotos via bulk:

- [ ] Arquivo está em formato correto (JPG, PNG, PDF)?
- [ ] Nome da foto é descritivo? (ex: "Sala_principal_2026.jpg")
- [ ] Escolheu a categoria correta?
- [ ] Visibilidade está correta (interno/portal/público)?
- [ ] Marcou como "Capa" se for a principal?
- [ ] Publicar no site está marcado se for para website?

---

## 🆘 Dúvidas Frequentes

**P: Onde aparecem as fotos que coloquei?**
R: Na galeria do imóvel no website/portal (se estiverem com visibility_level=public/portal + website_published=true)

**P: Posso colocar foto de vistoria na galeria do site?**
R: Não recomendado. Use "Galeria do Imóvel" para fotos profissionais. Fotos de vistoria ficam em "Arquivos da Vistoria"

**P: Como mudo a foto de capa do imóvel?**
R: Na galeria do imóvel, marque outra foto com ★ Capa. Automático desmarcar a anterior

**P: Preciso manter histórico de fotos antigas?**
R: Sim, o sistema mantém todas as fotos. Use `active=false` para "arquivar" sem deletar

---

## 📝 Notas Técnicas

- `file_size`: Calculado automaticamente ao fazer upload
- `date_taken`: Preenchido com data atual, pode ser alterado
- `image_512`: Miniatura automática (256x256 para galeria do site)
- Múltiplas fotos por vez via wizard bulk
- Suporta: JPG, PNG, PDF, GIF, WEBP


## Ajuste de fluxo

- Fotos e documentos usam o mesmo modelo `property.media`.
- Em Vistoria e Manutenção, a aba operacional é única: **Mídias da Vistoria** ou **Mídias da Manutenção**.
- O tipo de conteúdo (`Foto / Imagem` ou `Arquivo / Documento`) é detectado automaticamente no upload em lote.
- **Galeria do Imóvel** é uma finalidade/filtro, não um menu operacional separado. O cadastro principal da galeria deve ser feito pela aba do imóvel.
