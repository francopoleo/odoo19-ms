# Property Contract OCR Templates — Atualização Enterprise

## Objetivo

Este módulo adiciona uma camada flexível de OCR por templates para contratos imobiliários no Odoo 19.
Ele foi ajustado para contratos de locação com variações como:

- Quadro Resumo A/B/C/D/E/F/G.
- Contrato corrido por cláusulas.
- Contratos com DocuSign/assinatura eletrônica.
- Contratos escaneados sem texto pesquisável.
- Variações de CPF/MF, CPFMF, CNPJ/MF e CNPJMF.

## Principais melhorias

### 1. Autodetecção por pontuação

Antes, o sistema podia usar o primeiro template que encontrasse. Agora todos os templates ativos são testados e o de maior pontuação é escolhido.

- Regex de autodetecção: +50 pontos.
- Cada palavra-chave encontrada: +10 pontos.
- Pontuação mínima configurável por template.

Isso permite criar templates por família documental sem duplicar regras para cada contrato.

### 2. Tipo de documento

O template agora possui `document_kind`:

- Contrato.
- Aditivo.
- Distrato/Rescisão.
- Certificado de Assinatura.
- Desconhecido.

Esse campo prepara o pipeline para decidir se o OCR alimenta contrato, aditivo, rescisão ou apenas valida assinatura.

### 3. Regras alternativas por campo

Agora o mesmo campo pode ter várias linhas/regras. O sistema coleta candidatos e aplica o valor de maior confiança.

Exemplo: `start_date` pode vir de:

- `iniciando-se em 01 de maio de 2022`
- `se iniciando em 03.06.2024`
- `com início em ...`

### 4. Campos mais flexíveis para os contratos enviados

Foram adicionadas regras alternativas para:

- Locadora.
- CPF/CNPJ da locadora.
- Locatário pessoa física.
- Locatária pessoa jurídica.
- CPF/CNPJ do locatário.
- Descrição do imóvel.
- Endereço.
- CEP.
- Cidade.
- Valor mensal.
- Data inicial.
- Data final.
- Data de assinatura.

### 5. Bloco preferencial da regra

As linhas de template agora têm `section_key`, permitindo organizar regras por blocos:

- Locadora.
- Locatária.
- Imóvel.
- Prazo.
- Aluguel.
- Reajuste.
- Garantia.
- Foro / Local e Data.

A extração ainda usa o texto completo para não perder contratos fora do padrão, mas a organização ajuda manutenção e auditoria.

## Fluxo recomendado

1. Cadastrar contrato histórico.
2. Anexar o PDF no campo Arquivo do Contrato.
3. Usar **Diagnosticar Ambiente OCR** quando for o primeiro teste no servidor.
4. Usar **Testar OCR do Arquivo** para validar se o texto está sendo extraído.
5. Usar **Extrair por Template OCR**.
6. Conferir:
   - campos preenchidos no contrato;
   - linhas de extração;
   - log de extração;
   - obrigatórios não encontrados.

## Instalação / atualização

Copie a pasta `property_contract_ocr_template` para o addons path e atualize:

```bash
./odoo-bin -d ms -u property_contract_ocr_template --stop-after-init
```

No seu ambiente, ajuste o comando conforme o caminho real do `odoo-bin`.

## Dependências recomendadas no ambiente Python

```bash
pip install pypdf PyPDF2 pymupdf pillow pytesseract pdf2image
```

No macOS/Homebrew:

```bash
brew install tesseract tesseract-lang poppler
```

Confirme se existem os idiomas:

```bash
tesseract --list-langs
```

O ideal é aparecer `por` e `eng`.

## Observação importante

OCR nunca deve ser tratado como lançamento automático sem conferência. O fluxo correto é extrair, mostrar evidências, destacar obrigatórios faltantes e deixar o usuário aceitar/corrigir antes de criar parcelas, contatos e vínculos finais.
