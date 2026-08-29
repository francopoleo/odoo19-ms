# -*- coding: utf-8 -*-
"""
Base infrastructure for payment proof parsers.

HOW TO ADD A NEW BANK:
1. Create a file in this directory (e.g. sicredi.py)
2. Subclass BaseParser and decorate with @parser_registry.register
3. Set DETECT_KEYWORDS and override field patterns as needed
4. Import the new file in __init__.py

The registry tries parsers in descending priority order.
The generic parser (priority=0) always matches as fallback.
"""
import re
from datetime import date


# ─────────────────────────── helpers ────────────────────────────────────────

def first_match(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text or "", flags=re.I | re.M)
        if match:
            return (match.group(1) or "").strip()
    return ""


def parse_br_amount(text):
    candidates = re.findall(
        r"(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})", text or "", flags=re.I
    )
    values = []
    for c in candidates:
        try:
            values.append(float(c.replace(".", "").replace(",", ".")))
        except Exception:
            pass
    return max(values) if values else 0.0


def parse_br_date(text):
    matches = re.findall(r"\b(\d{2})[/-](\d{2})[/-](\d{4})\b", text or "")
    for dd, mm, yyyy in matches:
        try:
            return date(int(yyyy), int(mm), int(dd))
        except Exception:
            continue
    return False


# ──────────────────────────── base class ─────────────────────────────────────

class BaseParser:
    """
    Abstract base for payment proof parsers.

    Override DETECT_KEYWORDS and/or DETECT_PATTERN to control detection.
    Override *_PATTERNS lists to customise field extraction for a specific bank.
    """

    name = "Base"
    slug = "base"
    priority = 0        # Higher = tried first. Generic fallback = 0 (always matches).
    institution = ""    # Human-readable bank name set on successful detection

    # ── detection ────────────────────────────────────────────────────────────
    DETECT_KEYWORDS: list[str] = []   # any of these in lowercased text
    DETECT_PATTERN: str | None = None # optional extra regex

    # ── field patterns (first match wins) ────────────────────────────────────
    PAYER_NAME_PATTERNS: list[str] = [
        r"(?:pagador|quem\s+pagou|origem|remetente)[:\s\-]+([^\n\r]{3,80})",
        r"(?:nome\s+do\s+pagador)[:\s\-]+([^\n\r]{3,80})",
        # "Dados de quem FEZ/PAGOU a transação" → "Nome:" na próxima linha
        # O verbo obrigatório evita bater em "dados de quem recebeu"
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
        r"(?:pagador|remetente)\s*[\r\n]+\s*nome[:\s]+([^\n\r]{3,80})",
    ]

    RECEIVER_NAME_PATTERNS: list[str] = [
        r"(?:recebedor|favorecido|destino|para|benefici[aá]rio)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:recebeu|recebe)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]

    PAYER_VAT_PATTERNS: list[str] = [
        # ── Contexto da seção do pagador (máxima precisão) ───────────────
        # "Dados de quem fez/pagou" → CPF/CNPJ (completo ou mascarado)
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?(?:cpf|cnpj)[^0-9\*]{0,5}([\*\d]{3}\.[\*\d]{3}\.[\*\d]{3}-[\*\d]{2})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?(?:cpf|cnpj)[^0-9]{0,10}(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})",
        # "Dados do pagador" → CPF/CNPJ
        r"dados\s+do\s+pagador[\s\S]{0,200}?(?:cpf|cnpj)[^0-9\*]{0,5}([\*\d]{3}\.[\*\d]{3}\.[\*\d]{3}-[\*\d]{2})",
        r"dados\s+do\s+pagador[\s\S]{0,200}?(?:cpf|cnpj)[^0-9]{0,10}(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})",
        # "Pagador" como título de seção (linha própria) → CPF/CNPJ nas próximas linhas
        r"(?:^|\n)pagador\s*[\r\n][\s\S]{0,200}?(?:cpf|cnpj)[^0-9\*]{0,5}([\*\d]{3}\.[\*\d]{3}\.[\*\d]{3}-[\*\d]{2})",
        r"(?:^|\n)pagador\s*[\r\n][\s\S]{0,200}?(?:cpf|cnpj)[^0-9]{0,10}(\d{3}\.?\d{3}\.?\d{3}-?\d{2})",
        # ── Fallback genérico (sem contexto — último recurso) ────────────
        # Mascarado
        r"(?:cpf|cnpj)[^0-9\*]{0,5}([\*\d]{3}\.[\*\d]{3}\.[\*\d]{3}-[\*\d]{2})",
        r"(?:cpf|cnpj)[^0-9\*]{0,5}([\*\d]{2}\.[\*\d]{3}\.[\*\d]{3}/[\*\d]{4}-[\*\d]{2})",
        # Completo
        r"(?:cpf|cnpj)[^0-9]{0,10}(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})",
    ]

    # Chave PIX — telefone, email, CPF/CNPJ como chave, chave aleatória
    PIX_KEY_PATTERNS: list[str] = [
        r"chave\s*(?:pix)?[:\s]*(\+?55[\s\-]?\(?\d{2}\)?[\s\-]?\d{4,5}[\s\-]?\d{4})",  # telefone
        r"chave\s*(?:pix)?[:\s]*([\w\.\+\-]+@[\w\.\-]+\.[a-z]{2,6})",                   # e-mail
        r"chave\s*(?:pix)?[:\s]*([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",  # UUID
        r"chave\s*(?:pix)?[:\s]*([0-9a-zA-Z]{32,})",                                      # chave aleatória
        r"(?:chave|key)\s*pix[:\s]+([^\n\r]{5,80})",                                      # fallback genérico
    ]

    TRANSACTION_ID_PATTERNS: list[str] = [
        r"(?:end[- ]?to[- ]?end|e2e|id\s+da\s+transa[cç][aã]o|id\s+transa[cç][aã]o|autentica[cç][aã]o|nsu)[:\s\-]+([A-Z0-9\.\-_/]{8,})",
        r"\b(E[0-9A-Z]{20,})\b",
    ]

    BANK_NAME_PATTERNS: list[str] = [
        r"(?:institui[cç][aã]o|banco)[:\s\-]+([^\n\r]{3,60})",
    ]

    # Data de débito — diferente da data da transação em alguns bancos
    DEBIT_DATE_PATTERNS: list[str] = [
        r"data\s+de\s+d[eé]bito[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"d[eé]bito\s+em[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"data\s+do\s+d[eé]bito[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    # ── public API ────────────────────────────────────────────────────────────

    def detect(self, text: str) -> bool:
        lowered = text.lower()
        if self.DETECT_KEYWORDS and any(k in lowered for k in self.DETECT_KEYWORDS):
            return True
        if self.DETECT_PATTERN and re.search(self.DETECT_PATTERN, text, re.I):
            return True
        return False

    def parse(self, text: str) -> dict:
        debit_date_raw = first_match(self.DEBIT_DATE_PATTERNS, text)
        debit_date = parse_br_date(debit_date_raw) if debit_date_raw else False
        return {
            "parser": self.slug,
            "parser_name": self.name,
            "payment_method": self._detect_method(text),
            "payment_date": parse_br_date(text),
            "debit_date": debit_date,
            "amount": parse_br_amount(text),
            "payer_name": first_match(self.PAYER_NAME_PATTERNS, text),
            "payer_vat": first_match(self.PAYER_VAT_PATTERNS, text),
            "pix_key": first_match(self.PIX_KEY_PATTERNS, text),
            "receiver_name": first_match(self.RECEIVER_NAME_PATTERNS, text),
            "transaction_id": first_match(self.TRANSACTION_ID_PATTERNS, text),
            "bank_name": self.institution or first_match(self.BANK_NAME_PATTERNS, text),
        }

    # ── internal ──────────────────────────────────────────────────────────────

    def _detect_method(self, text):
        lowered = text.lower()
        if "pix" in lowered or "end-to-end" in lowered or "e2e" in lowered:
            return "pix"
        if "boleto" in lowered:
            return "boleto"
        if "ted" in lowered or "doc" in lowered or "transfer" in lowered:
            return "transfer"
        if "depósito" in lowered or "deposito" in lowered:
            return "deposit"
        return "other"


# ──────────────────────────── registry ───────────────────────────────────────

class _ParserRegistry:
    """
    Singleton registry.  Use the module-level `parser_registry` instance.

    Usage:
        @parser_registry.register
        class MyBankParser(BaseParser):
            ...
    """

    def __init__(self):
        self._parsers: list[type[BaseParser]] = []

    def register(self, parser_class: type[BaseParser]) -> type[BaseParser]:
        """Decorator — registers a parser class and keeps list sorted by priority."""
        self._parsers.append(parser_class)
        self._parsers.sort(key=lambda p: p.priority, reverse=True)
        return parser_class

    def find(self, text: str) -> BaseParser:
        """Returns the highest-priority parser whose detect() returns True."""
        for cls in self._parsers:
            instance = cls()
            if instance.detect(text):
                return instance
        return BaseParser()  # Should never reach here if GenericParser is registered

    def all_parsers(self) -> list[type[BaseParser]]:
        return list(self._parsers)


parser_registry = _ParserRegistry()