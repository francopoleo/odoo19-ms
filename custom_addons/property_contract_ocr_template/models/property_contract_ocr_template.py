# -*- coding: utf-8 -*-
import json
import re
from datetime import date, datetime

from odoo import _, api, fields, models


PT_MONTHS = {
    "janeiro": 1, "jan": 1,
    "fevereiro": 2, "fev": 2,
    "marco": 3, "março": 3, "mar": 3,
    "abril": 4, "abr": 4,
    "maio": 5, "mai": 5,
    "junho": 6, "jun": 6,
    "julho": 7, "jul": 7,
    "agosto": 8, "ago": 8,
    "setembro": 9, "set": 9,
    "outubro": 10, "out": 10,
    "novembro": 11, "nov": 11,
    "dezembro": 12, "dez": 12,
}



def _prepare_ocr_text_for_regex(text):
    """Normalize OCR text just enough to make regex templates less brittle.

    It preserves words and punctuation but collapses whitespace, normalizes
    smart quotes/dashes and fixes common OCR variants in real scanned leases.
    """
    text = text or ""
    replacements = {
        "–": "-", "—": "-", "−": "-",
        "“": '"', "”": '"', "„": '"',
        "’": "'", "‘": "'",
        "º": "º", "°": "º",
        " R$ ": " R$ ",
        " RS ": " R$ ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Join hyphenated line-break artifacts and collapse long whitespace.
    text = re.sub(r"-\s*\n\s*", "", text)
    text = re.sub(r"[\t\r\f\v]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    # Keep a spaced copy: regex with \s+ becomes much easier against OCR.
    return text


class PropertyContractOcrTemplate(models.Model):
    _name = "property.contract.ocr.template"
    _description = "Template OCR de Contrato Imobiliário"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one("res.company", string="Empresa")
    document_kind = fields.Selection(
        [
            ("contract", "Contrato"),
            ("amendment", "Aditivo"),
            ("termination", "Distrato/Rescisão"),
            ("signature_certificate", "Certificado de Assinatura"),
            ("unknown", "Desconhecido"),
        ],
        string="Tipo de Documento",
        default="contract",
        required=True,
        tracking=True,
        help="Define a família do documento para o pipeline decidir se cria contrato, aditivo, distrato ou apenas certificado.",
    )
    min_auto_detect_score = fields.Integer(
        string="Pontuação mínima",
        default=30,
        help="Pontuação mínima para aceitar a autodetecção. Regex soma 50 pontos; cada palavra-chave soma 10 pontos.",
    )
    contract_type = fields.Selection(
        [
            ("rental", "Aluguel/Locação"),
            ("sale", "Venda"),
            ("financing", "Financiamento/Hipoteca"),
            ("comodato", "Comodato"),
            ("other", "Outro"),
        ],
        string="Tipo padrão",
        default="rental",
        required=True,
        help="Tipo preenchido no contrato quando este template for usado.",
    )
    extraction_mode = fields.Selection(
        [
            ("auto", "Automático: PDF texto + OCR se necessário"),
            ("pypdf", "Somente texto pesquisável do PDF"),
            ("ocr", "Forçar OCR de PDF/imagem"),
        ],
        default="auto",
        required=True,
        help="Automático tenta primeiro texto pesquisável. Se não houver texto, renderiza o PDF/imagem e aplica OCR.",
    )
    page_limit = fields.Integer(
        default=8,
        help="Quantidade máxima de páginas processadas no OCR. Contratos longos podem ser lentos; use 6 a 12 páginas para teste.",
    )
    auto_detect_pattern = fields.Char(
        string="Regex de autodetecção",
        help="Regex usada para identificar se este template serve para o documento. Ex.: LOCADORA|LOCATÁRIO|QUADRO RESUMO.",
    )
    auto_detect_keywords = fields.Text(
        string="Palavras-chave de autodetecção",
        help="Uma por linha. Se alguma aparecer no texto OCR, o template pode ser escolhido automaticamente.",
    )
    description = fields.Html(
        string="Orientação",
        help="Explique ao usuário quando usar este template e quais campos ele procura.",
    )
    line_ids = fields.One2many(
        "property.contract.ocr.template.line",
        "template_id",
        string="Campos a procurar",
        copy=True,
    )

    def _get_field_name_label_map(self):
        return dict(self.env["property.contract.history.line"]._fields["field_type"].selection)

    def _get_candidate_templates(self, company=False):
        domain = [("active", "=", True)]
        if company:
            domain.append(("company_id", "in", [False, company.id]))
        return self.search(domain)

    def _score_template_against_text(self, template, text):
        """Score every active template instead of returning the first match.

        Contracts from the same landlord can share many words. A score makes
        autodetection safer for enterprise use because a BRF layout, a quadro
        resumo layout and a newer clause-only layout can coexist.
        """
        score = 0
        text = text or ""
        lowered = text.lower()
        if template.auto_detect_pattern:
            try:
                if re.search(template.auto_detect_pattern, text, flags=re.I | re.M | re.S):
                    score += 50
            except re.error:
                score -= 20
        keywords = [x.strip().lower() for x in (template.auto_detect_keywords or "").splitlines() if x.strip()]
        for keyword in keywords:
            if keyword and keyword in lowered:
                score += 10
        return score

    def _auto_detect_from_text(self, text, company=False):
        best_template = False
        best_score = 0
        for template in self._get_candidate_templates(company=company):
            score = self._score_template_against_text(template, text)
            if score > best_score:
                best_score = score
                best_template = template
        if best_template and best_score >= (best_template.min_auto_detect_score or 30):
            return best_template
        return False


    @api.model
    def action_install_default_templates(self):
        """Create/update robust default templates.

        This method is called by XML data on install/update, unlike post_init
        hooks which only run on first installation. It deliberately updates the
        default template because OCR regexes are meant to evolve with real PDFs.
        """
        Field = self.env["ir.model.fields"].sudo()
        Line = self.env["property.contract.ocr.template.line"].sudo()

        def field(name):
            return Field.search([("model", "=", "property.contract.history"), ("name", "=", name)], limit=1)

        template = self.sudo().search([("name", "=", "Contrato de Locação Não Residencial - Quadro Resumo")], limit=1)
        values = {
            "name": "Contrato de Locação Não Residencial - Quadro Resumo",
            "sequence": 10,
            "contract_type": "rental",
            "extraction_mode": "auto",
            "page_limit": 14,
            "auto_detect_pattern": r"QUADRO\s+RESUMO|CONTRATO\s+DE\s+LOCA[ÇC][ÃA]O\s+DE\s+IM[ÓO]VEL|INSTRUMENTO\s+PARTICULAR\s+DE\s+LOCA[ÇC][ÃA]O|LOCADORA|LOCAT[ÁA]RIA?",
            "auto_detect_keywords": "locadora\nlocatário\nlocatária\nquadro resumo\ncontrato de locação\ninstrumento particular de locação",
            "description": "Template padrão robusto para contratos de locação não residencial. Cobre dois layouts: (1) quadro resumo com seções A/B/C/F; (2) contrato corrido por cláusulas com Locadora/Locatária.",
        }
        if template:
            template.write(values)
        else:
            template = self.sudo().create(values)

        rows = [
            # sequence, field_name, value_type, mode, regex, fixed, required, notes, confidence, section
            (10, "contract_type", "selection", "fixed", False, "rental", True, "Tipo fixo para contrato de locação.", 100, "full"),
            (20, "party1_name", "char", "regex", r"A\s*[-–]?\s*LOCADORA[\s\S]{0,260}?([A-Z0-9 &.,ÇÁÉÍÓÚÂÊÔÃÕ\-]+(?:LTDA|EIRELI|S/?S)(?:\.)?)\s*,", False, True, "Nome da locadora no Quadro Resumo.", 95, "landlord"),
            (21, "party1_name", "char", "regex", r"([A-Z0-9][A-Z0-9\s.,&ÇÁÉÍÓÚÂÊÔÃÕ\-]+(?:LTDA|EIRELI|S/?S)(?:\.)?)\s*,[\s\S]{0,350}?doravante\s+denominada\s+[\"']?LOCADORA", False, True, "Nome da locadora em contrato corrido.", 88, "landlord"),
            (30, "party1_vat", "char", "regex", r"A\s*[-–]?\s*LOCADORA[\s\S]{0,750}?CNPJ\s*/?\s*MF\s+sob\s+(?:o\s+)?n[ºo]?\s*([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}/?[0-9]{4}-?[0-9]{2})", False, False, "CNPJ da locadora.", 95, "landlord"),
            (40, "party2_name", "char", "regex", r"B\s*[-–]?\s*LOCAT[ÁA]RI[OA]S?:?[\s\S]{0,260}?([A-Z0-9][A-Z0-9\s.,&ÇÁÉÍÓÚÂÊÔÃÕ\-]+(?:LTDA|EIRELI|S/?S)(?:\.)?)\s*,", False, True, "Nome da locatária pessoa jurídica no quadro resumo.", 95, "tenant"),
            (41, "party2_name", "char", "regex", r"B\s*[-–]?\s*LOCAT[ÁA]RI[OA]S?:?[\s\S]{0,240}?([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ\s.]{5,80}?),\s*brasileir", False, True, "Nome do locatário pessoa física no quadro resumo.", 92, "tenant"),
            (42, "party2_name", "char", "regex", r"B\s*[-–]?\s*LOCAT[ÁA]RI[OA]S?:?[\s\S]{0,420}?([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ\s.]{5,80}?)\s*,[\s\S]{0,180}?CPF\s*/?\s*MF", False, True, "Nome de locatário antes de CPF/MF.", 86, "tenant"),
            (50, "party2_vat", "char", "regex", r"B\s*[-–]?\s*LOCAT[ÁA]RI[OA]S?:?[\s\S]{0,900}?CNPJ\s*/?\s*MF\s+sob\s+(?:o\s+)?n[ºo]?\s*([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}/?[0-9]{4}-?[0-9]{2})", False, False, "CNPJ da locatária.", 95, "tenant"),
            (51, "party2_vat", "char", "regex", r"B\s*[-–]?\s*LOCAT[ÁA]RI[OA]S?:?[\s\S]{0,950}?CPF\s*/?\s*MF\s+sob\s+(?:o\s+)?n[ºo]?\s*([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2})", False, False, "CPF do locatário. Aceita CPFMF/CPF/MF.", 92, "tenant"),
            (60, "property_description", "text", "regex", r"C\s*[-–]?\s*IM[ÓO]VEL:?[\s\S]{0,30}?([\s\S]{20,900}?)(?=\n\s*D\s*[-–]?\s*DESTINA|D\s*[-–]?\s*DESTINA)", False, True, "Descrição completa do imóvel no quadro resumo.", 94, "asset"),
            (61, "property_description", "text", "regex", r"OBJETO\s+DA\s+LOCA[ÇC][ÃA]O:?[\s\S]{0,80}?([\s\S]{20,900}?)(?=\n\s*3\.|\n\s*PRAZO|\n\s*B\s*[-–])", False, False, "Descrição em layout BRF/contrato corrido.", 86, "asset"),
            (70, "address", "char", "regex", r"localizad[ao]\s+na\s+([^\.\n;]{15,220})", False, True, "Endereço iniciado por localizado/localizada na.", 88, "asset"),
            (71, "address", "char", "regex", r"na\s+(Alameda|Avenida|Rua)\s+([^\.\n;]{8,220})", False, False, "Endereço alternativo por logradouro.", 78, "asset"),
            (72, "zip_code", "char", "regex", r"CEP\s*([0-9]{5}-?[0-9]{3})", False, False, "CEP quando constar no contrato.", 90, "asset"),
            (73, "city", "char", "regex", r"\b(Santana\s+de\s+Parna[ií]ba|Barueri|Osasco|São\s+Paulo)\s*/\s*SP\b", False, False, "Cidade pelo padrão Cidade/SP.", 85, "asset"),
            (80, "monthly_amount", "monetary", "regex", r"F\s*[-–]?\s*ALUGUEL\s+INICIAL:?[\s\S]{0,220}?R\$\s*([0-9.]+,[0-9]{2})", False, True, "Valor do aluguel inicial no quadro resumo.", 97, "rent"),
            (81, "monthly_amount", "monetary", "regex", r"(?:aluguel|alugueres|pre[çc]o)[\s\S]{0,160}?R\$\s*([0-9.]+,[0-9]{2})", False, True, "Valor do aluguel em cláusula de preço.", 87, "rent"),
            (82, "monthly_amount", "monetary", "regex", r"valor\s+(?:mensal|mínimo\s+garantido)[\s\S]{0,120}?R\$?\s*([0-9.]+,[0-9]{2})", False, False, "Valor mensal/mínimo garantido em layouts diferentes.", 84, "rent"),
            (90, "start_date", "date", "regex", r"iniciando-se\s+em\s+(\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4})", False, True, "Data inicial por 'iniciando-se em'.", 98, "term"),
            (91, "start_date", "date", "regex", r"(?:se\s+iniciando\s+em|iniciar\s+em|in[ií]cio\s+em|com\s+in[ií]cio\s+em)\s+(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})", False, True, "Data inicial numérica em contrato corrido.", 94, "term"),
            (92, "start_date", "date", "regex", r"(?:se\s+iniciando\s+em|iniciar\s+em|in[ií]cio\s+em|com\s+in[ií]cio\s+em)\s+(\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4})", False, True, "Data inicial textual em variação de cláusula.", 92, "term"),
            (100, "end_date", "date", "regex", r"(?:a\s+terminar\s+em|terminar\s+em|t[ée]rmino\s+(?:previsto\s+)?(?:para|em))\s+(\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4})", False, True, "Data final textual.", 98, "term"),
            (101, "end_date", "date", "regex", r"(?:a\s+terminar\s+em|terminar\s+em|t[ée]rmino\s+(?:previsto\s+)?(?:para|em))\s+(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})", False, True, "Data final numérica.", 94, "term"),
            (110, "sign_date", "date", "regex", r"(?:Santana\s+de\s+Parna[ií]ba|Barueri|São\s+Paulo),\s*(\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4})", False, False, "Data de assinatura textual.", 90, "forum"),
            (111, "sign_date", "date", "regex", r"(?:assinado|firmado)[\s\S]{0,80}?em\s+(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})", False, False, "Data de assinatura em certificados/rodapé.", 78, "forum"),
        ]

        existing = {line.sequence: line for line in template.line_ids}
        for sequence, field_name, value_type, value_mode, pattern, fixed, required, notes, confidence, section_key in rows:
            field_rec = field(field_name)
            if not field_rec:
                continue
            vals = {
                "template_id": template.id,
                "sequence": sequence,
                "field_id": field_rec.id,
                "value_type": value_type,
                "value_mode": value_mode,
                "pattern": pattern or False,
                "required": required,
                "notes": notes,
                "dotall": True,
                "confidence": confidence,
                "section_key": section_key,
            }
            if value_mode == "fixed":
                vals["fixed_value_selection"] = fixed
            if sequence in existing:
                existing.pop(sequence).write(vals)
            else:
                Line.create(vals)
        for leftover in existing.values():
            leftover.unlink()
        return True

    def extract_payload(self, text):
        self.ensure_one()
        regex_text = _prepare_ocr_text_for_regex(text or "")
        values = {
            "template": self.name,
            "template_id": self.id,
            "document_kind": self.document_kind,
            "contract_type": self.contract_type,
        }
        lines = []
        candidates = {}
        for line in self.line_ids.sorted(lambda x: (x.sequence, x.id)):
            value, raw_value, confidence, matched = line.extract_value(regex_text)
            if matched and value not in (False, None, ""):
                candidates.setdefault(line.field_name, []).append({
                    "value": value, "raw": raw_value, "confidence": confidence, "line": line,
                })
            lines.append({
                "field_name": line.field_name,
                "field_label": line.field_label,
                "raw_value": raw_value or "",
                "parsed_value": value if value not in (False, None) else "",
                "field_type": line.value_type,
                "confidence": confidence,
                "required": line.required,
                "matched": matched,
                "notes": line.notes or "",
                "pattern": line.pattern or "",
                "value_mode": line.value_mode,
            })
        for field_name, items in candidates.items():
            # Best candidate wins. If equal confidence, earlier sequence wins.
            best = sorted(items, key=lambda x: (x["confidence"], -x["line"].sequence), reverse=True)[0]
            values[field_name] = best["value"]
        return values, lines


class PropertyContractOcrTemplateLine(models.Model):
    _name = "property.contract.ocr.template.line"
    _description = "Linha do Template OCR de Contrato"
    _order = "template_id, sequence, id"

    template_id = fields.Many2one(
        "property.contract.ocr.template", required=True, ondelete="cascade"
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Descrição", help="Nome interno da regra, opcional.")
    field_id = fields.Many2one(
        "ir.model.fields",
        string="Campo do Contrato",
        required=True,
        ondelete="cascade",
        domain=[
            ("model", "=", "property.contract.history"),
            ("name", "in", [
                "contract_type", "party1_name", "party1_vat", "party2_name", "party2_vat",
                "sign_date", "start_date", "end_date", "renewal_date",
                "monthly_amount", "total_value", "deposit_value",
                "address", "address_complement", "neighborhood", "city", "zip_code",
                "property_description",
            ]),
        ],
        help="Campo que receberá o valor extraído.",
    )
    field_name = fields.Char(related="field_id.name", store=True, readonly=True)
    field_label = fields.Char(related="field_id.field_description", readonly=True)
    field_ttype = fields.Selection(related="field_id.ttype", readonly=True)
    value_type = fields.Selection(
        [
            ("char", "Texto"),
            ("text", "Texto longo"),
            ("date", "Data"),
            ("float", "Número/Valor"),
            ("monetary", "Valor monetário"),
            ("selection", "Seleção"),
        ],
        default="char",
        required=True,
        help="Como converter o texto encontrado antes de preencher o campo.",
    )
    value_mode = fields.Selection(
        [("regex", "Procurar por regex"), ("fixed", "Valor fixo")],
        default="regex",
        required=True,
    )
    pattern = fields.Text(
        string="Regex / Padrão",
        help="Regex usada para localizar o campo no texto OCR. Se usar grupo de captura, o primeiro grupo será usado.",
    )
    dotall = fields.Boolean(
        default=True,
        string="Permitir quebra de linha",
        help="Ativa regex DOTALL para o ponto e padrões atravessarem linhas. Útil em PDFs/OCR.",
    )
    required = fields.Boolean(
        string="Obrigatório",
        help="Marca o campo como essencial. Se não encontrar, aparecerá no log de pendências do template.",
    )
    confidence = fields.Float(default=85.0, help="Confiança padrão quando a regra encontrar valor.")
    fixed_value_char = fields.Char("Valor fixo texto")
    fixed_value_float = fields.Float("Valor fixo numérico")
    fixed_value_date = fields.Date("Valor fixo data")
    fixed_value_selection = fields.Char("Valor fixo seleção")
    decimal_separator = fields.Selection(
        [("comma", "Vírgula decimal"), ("dot", "Ponto decimal")], default="comma"
    )
    thousand_separator = fields.Selection(
        [("dot", "Ponto de milhar"), ("comma", "Vírgula de milhar"), ("space", "Espaço"), ("none", "Nenhum")],
        default="dot",
    )
    section_key = fields.Selection(
        [
            ("full", "Texto completo"),
            ("landlord", "A - Locadora"),
            ("tenant", "B - Locatária/Locatários"),
            ("asset", "C / Objeto - Imóvel"),
            ("purpose", "D / Finalidade - Destinação"),
            ("term", "Prazo / Vigência"),
            ("rent", "Aluguel / Preço"),
            ("adjustment", "Reajuste"),
            ("guarantee", "Garantia"),
            ("forum", "Foro / Local e Data"),
        ],
        default="full",
        string="Bloco preferencial",
        help="Ajuda operacional para organizar regras. A extração continua usando o texto completo para não perder contratos fora do padrão.",
    )
    notes = fields.Text("Ajuda / Observação", help="Explique o que esta regra procura no documento.")

    @api.onchange("field_id")
    def _onchange_field_id(self):
        for line in self:
            if line.field_id.ttype in ("date", "datetime"):
                line.value_type = "date"
            elif line.field_id.ttype in ("float", "monetary"):
                line.value_type = "monetary"
            elif line.field_id.ttype == "text":
                line.value_type = "text"
            elif line.field_id.ttype == "selection":
                line.value_type = "selection"
            else:
                line.value_type = "char"

    def _extract_raw_regex(self, text):
        self.ensure_one()
        if not self.pattern:
            return False, False
        flags = re.I | re.M
        if self.dotall:
            flags |= re.S
        try:
            matches = list(re.finditer(self.pattern, text or "", flags=flags))
        except re.error as exc:
            return f"ERRO REGEX: {exc}", False
        if not matches:
            return False, False
        match = matches[0]
        if match.groups():
            groups = [g for g in match.groups() if g]
            raw = " ".join(groups).strip() if groups else ""
        else:
            raw = match.group(0).strip()
        return raw, True

    def _fixed_value(self):
        self.ensure_one()
        if self.value_type in ("float", "monetary"):
            return self.fixed_value_float
        if self.value_type == "date":
            return self.fixed_value_date
        if self.value_type == "selection":
            return self.fixed_value_selection
        return self.fixed_value_char

    def extract_value(self, text):
        self.ensure_one()
        if self.value_mode == "fixed":
            value = self._fixed_value()
            return value, value, 100.0, bool(value not in (False, None, ""))
        raw, matched = self._extract_raw_regex(text)
        if not matched:
            return False, raw, 0.0, False
        value = self._convert_value(raw)
        return value, raw, self.confidence, True

    def _convert_value(self, raw):
        self.ensure_one()
        raw = (raw or "").strip()
        raw = re.sub(r"(?i)CPFMF", "CPF/MF", raw)
        raw = re.sub(r"(?i)CNPJMF", "CNPJ/MF", raw)
        if self.value_type == "date":
            return self._parse_date(raw)
        if self.value_type in ("float", "monetary"):
            return self._parse_amount(raw)
        if self.value_type == "selection":
            return raw.strip().lower()
        return re.sub(r"\s+", " ", raw).strip()

    def _parse_amount(self, raw):
        value = re.sub(r"[^0-9,.-]", "", raw or "")
        if self.thousand_separator == "dot":
            value = value.replace(".", "")
        elif self.thousand_separator == "comma":
            value = value.replace(",", "")
        elif self.thousand_separator == "space":
            value = value.replace(" ", "")
        if self.decimal_separator == "comma":
            value = value.replace(",", ".")
        try:
            return float(value)
        except Exception:
            return 0.0

    def _parse_date(self, raw):
        raw = re.sub(r"\s+", " ", (raw or "").strip().lower())
        m = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", raw)
        if m:
            dd, mm, yy = m.groups()
            yy = int(yy) + 2000 if len(yy) == 2 else int(yy)
            try:
                return date(yy, int(mm), int(dd))
            except Exception:
                return False
        m = re.search(r"(\d{1,2})\s+de\s+([a-zç]+)\s+de\s+(\d{4})", raw)
        if not m:
            m = re.search(r"(\d{1,2})\s+([a-zç]+)\s+(\d{4})", raw)
        if m:
            dd, month_name, yy = m.groups()
            mm = PT_MONTHS.get(month_name)
            if mm:
                try:
                    return date(int(yy), mm, int(dd))
                except Exception:
                    return False
        return False
