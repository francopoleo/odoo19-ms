# -*- coding: utf-8 -*-
"""
Base infrastructure for contract history parsers.
Reuses patterns from property_payment_proof.

HOW TO ADD A NEW CONTRACT TYPE:
1. Create a file in this directory (e.g., lease_extension.py)
2. Subclass BaseContractParser and decorate with @parser_registry.register
3. Set DETECT_KEYWORDS and override field patterns as needed
4. Import the new file in __init__.py

The registry tries parsers in descending priority order.
The generic parser (priority=0) always matches as fallback.
"""
import re
from datetime import date


# ─────────────────────────── helpers ────────────────────────────────────────

def first_match(patterns, text):
    """Return first regex match from patterns list."""
    for pattern in patterns:
        match = re.search(pattern, text or "", flags=re.I | re.M)
        if match:
            return (match.group(1) or "").strip()
    return ""


def parse_br_amount(text):
    """Extract Brazilian currency amounts (R$ 1.234,56 → 1234.56)."""
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
    """Extract Brazilian dates (DD/MM/YYYY or DD-MM-YYYY)."""
    matches = re.findall(r"\b(\d{2})[/-](\d{2})[/-](\d{4})\b", text or "")
    for dd, mm, yyyy in matches:
        try:
            return date(int(yyyy), int(mm), int(dd))
        except Exception:
            continue
    return False


def normalize_text(value):
    """Normalize text for comparison."""
    value = (value or "").strip().lower()
    value = re.sub(r"[\W_]+", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def normalize_doc(value):
    """Normalize document (CPF/CNPJ) to digits only."""
    return re.sub(r"\D+", "", value or "")


# ──────────────────────────── base class ─────────────────────────────────────

class BaseContractParser:
    """
    Abstract base for contract history parsers.

    Override DETECT_KEYWORDS and/or DETECT_PATTERN to control detection.
    Override *_PATTERNS lists to customize field extraction for a specific contract type.
    """

    name = "Contrato Base"
    slug = "base_contract"
    priority = 0  # Higher = tried first. Generic fallback = 0 (always matches).
    contract_type = "other"  # Selection value: rental, sale, financing, comodato, other
    institution = ""  # Human-readable bank/institution name

    # ── detection ────────────────────────────────────────────────────────────
    DETECT_KEYWORDS: list = []  # any of these in lowercased text
    DETECT_PATTERN: str | None = None  # optional extra regex

    # ── field patterns (first match wins) ────────────────────────────────────
    PARTY1_NAME_PATTERNS: list = [
        r"(?:senhor|sr\.?|senhora|sra\.?|pessoa\s+física|pessoa\s+jurídica)[:\s\-]+([^\n\r]{3,120})",
        r"(?:locador|proprietário|vendedor|credor|institui[çc][aã]o\s+financeira)[:\s\-]+([^\n\r]{3,120})",
        r"(?:lado\s+(?:esquerdo|esquerdo|primeiro))[:\s\-]+([^\n\r]{3,120})",
    ]

    PARTY1_VAT_PATTERNS: list = [
        r"(?:cpf|cnpj)\s*(?:do\s+)?(?:locador|proprietário|vendedor|credor)[^0-9]{0,10}(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})",
        r"(?:locador|proprietário|vendedor)[^\n\r]{0,200}?(?:cpf|cnpj)[^0-9]{0,10}(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})",
    ]

    PARTY2_NAME_PATTERNS: list = [
        r"(?:locatário|inquilino|comprador|devedor|tomador)[:\s\-]+([^\n\r]{3,120})",
        r"(?:lado\s+(?:direito|direito|segundo))[:\s\-]+([^\n\r]{3,120})",
    ]

    PARTY2_VAT_PATTERNS: list = [
        r"(?:cpf|cnpj)\s*(?:do\s+)?(?:locatário|inquilino|comprador|devedor|tomador)[^0-9]{0,10}(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})",
        r"(?:locatário|inquilino|comprador|devedor)[^\n\r]{0,200}?(?:cpf|cnpj)[^0-9]{0,10}(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})",
    ]

    SIGN_DATE_PATTERNS: list = [
        r"(?:assinado|celebrado|datado)\s+(?:em\s+)?(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:nesta\s+data|neste\s+ato)[,:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:data)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    START_DATE_PATTERNS: list = [
        r"(?:a\s+partir\s+de|início|começo|vigência)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:data\s+de\s+início)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    END_DATE_PATTERNS: list = [
        r"(?:até|término|final|vencimento|expiração)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:data\s+de\s+término)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    MONTHLY_AMOUNT_PATTERNS: list = [
        r"(?:aluguel|mensalidade|prestação|parcela|valor\s+mensal)[:\s]+(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})",
        r"(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s+(?:mensai|mensal|por\s+mês))",
    ]

    TOTAL_VALUE_PATTERNS: list = [
        r"(?:preço|valor\s+total|valor\s+da\s+(?:venda|compra|operação))[:\s]+(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})",
        r"(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s+(?:total|à\s+vista|à\s+prazo))",
    ]

    DEPOSIT_PATTERNS: list = [
        r"(?:depósito|caução|garantia)[:\s]+(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})",
        r"(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s+(?:de\s+depósito|de\s+caução))",
    ]

    PROPERTY_ADDRESS_PATTERNS: list = [
        r"(?:localiza[dç]o|endereço|imóvel|propriedade)[:\s]+([^\n\r]{10,120})",
        r"(?:rua|avenida|av\.?|travessa|praça|alameda|estrada)[.,\s]+([^\n\r]{5,100})",
    ]

    NEIGHBORHOOD_PATTERNS: list = [
        r"(?:bairro)[:\s]+([^\n\r]{3,80})",
    ]

    CITY_PATTERNS: list = [
        r"(?:cidade|município)[:\s]+([^\n\r]{3,80})",
        r"(?:em\s+)?([A-Z][a-zá-ú\s]+)\s*,\s*(?:SP|RJ|MG|BA|RS|PR|SC|GO|DF|ES|PE|CE|PA|PB|MA|RN|AL|MT|MS|RO|AC|AP|AM|TO)",
    ]

    ZIP_CODE_PATTERNS: list = [
        r"(?:cep|código\s+postal)[:\s]+(\d{5}-\d{3}|\d{8})",
    ]

    PROPERTY_DESC_PATTERNS: list = [
        r"(?:descrição|característica|especificação)[:\s]+([^\n\r]{10,300})",
    ]

    # ── public API ────────────────────────────────────────────────────────────

    def detect(self, text: str) -> bool:
        """Return True if this parser should handle the text."""
        lowered = text.lower()
        if self.DETECT_KEYWORDS and any(k in lowered for k in self.DETECT_KEYWORDS):
            return True
        if self.DETECT_PATTERN and re.search(self.DETECT_PATTERN, text, re.I):
            return True
        return False

    def parse(self, text: str) -> dict:
        """Extract structured data from contract text."""
        return {
            "parser": self.slug,
            "parser_name": self.name,
            "contract_type": self.contract_type,
            "party1_name": first_match(self.PARTY1_NAME_PATTERNS, text),
            "party1_vat": first_match(self.PARTY1_VAT_PATTERNS, text),
            "party2_name": first_match(self.PARTY2_NAME_PATTERNS, text),
            "party2_vat": first_match(self.PARTY2_VAT_PATTERNS, text),
            "sign_date": self._parse_date(first_match(self.SIGN_DATE_PATTERNS, text)),
            "start_date": self._parse_date(first_match(self.START_DATE_PATTERNS, text)),
            "end_date": self._parse_date(first_match(self.END_DATE_PATTERNS, text)),
            "monthly_amount": parse_br_amount(first_match(self.MONTHLY_AMOUNT_PATTERNS, text)),
            "total_value": parse_br_amount(first_match(self.TOTAL_VALUE_PATTERNS, text)),
            "deposit_value": parse_br_amount(first_match(self.DEPOSIT_PATTERNS, text)),
            "address": first_match(self.PROPERTY_ADDRESS_PATTERNS, text),
            "neighborhood": first_match(self.NEIGHBORHOOD_PATTERNS, text),
            "city": first_match(self.CITY_PATTERNS, text),
            "zip_code": first_match(self.ZIP_CODE_PATTERNS, text),
            "property_description": first_match(self.PROPERTY_DESC_PATTERNS, text),
        }

    # ── internal ──────────────────────────────────────────────────────────────

    def _parse_date(self, date_str):
        """Parse date string to date object."""
        return parse_br_date(date_str) if date_str else False


# ──────────────────────────── registry ───────────────────────────────────────

class _ParserRegistry:
    """
    Singleton registry for contract parsers.

    Usage:
        @parser_registry.register
        class RentalContractParser(BaseContractParser):
            ...
    """

    def __init__(self):
        self._parsers: list[type[BaseContractParser]] = []

    def register(self, parser_class: type[BaseContractParser]) -> type[BaseContractParser]:
        """Decorator — registers a parser class and keeps list sorted by priority."""
        self._parsers.append(parser_class)
        self._parsers.sort(key=lambda p: p.priority, reverse=True)
        return parser_class

    def find(self, text: str) -> BaseContractParser:
        """Returns the highest-priority parser whose detect() returns True."""
        for cls in self._parsers:
            instance = cls()
            if instance.detect(text):
                return instance
        return BaseContractParser()  # Fallback (should never reach if generic is registered)

    def all_parsers(self) -> list[type[BaseContractParser]]:
        return list(self._parsers)


parser_registry = _ParserRegistry()
