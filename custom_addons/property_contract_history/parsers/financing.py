# -*- coding: utf-8 -*-
"""Financing/mortgage contract parser."""
from .base import BaseContractParser, parser_registry


@parser_registry.register
class FinancingContractParser(BaseContractParser):
    name = "Contrato de Financiamento/Hipoteca"
    slug = "financing"
    priority = 80
    contract_type = "financing"

    DETECT_KEYWORDS = [
        "contrato de financiamento",
        "financiamento imobiliário",
        "hipoteca",
        "crédito imobiliário",
        "financing agreement",
        "mortgage",
        "mutuante",
        "mutuário",
    ]

    # Financing-specific patterns
    TOTAL_VALUE_PATTERNS = [
        r"(?:valor\s+do\s+financiamento|valor\s+financiado|valor\s+mutuado)[:\s]+(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})",
        r"(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s+(?:de\s+financiamento|financiados|mutuados))",
    ]

    MONTHLY_AMOUNT_PATTERNS = [
        r"(?:prestação|valor\s+da\s+prestação|parcela|mensalidade)[:\s]+(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})",
        r"(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s+(?:de\s+prestação|mensal|mensalidade))",
    ]

    START_DATE_PATTERNS = [
        r"(?:data\s+da\s+primeira\s+prestação|início\s+do\s+financiamento)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:a\s+partir\s+de)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    END_DATE_PATTERNS = [
        r"(?:data\s+do\s+último\s+pagamento|término\s+do\s+financiamento)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:vencimento\s+final)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    PARTY1_NAME_PATTERNS = [
        r"(?:mutuante|instituição\s+financeira|banco|credor)[:\s]+([^\n\r]{3,120})",
    ]

    PARTY2_NAME_PATTERNS = [
        r"(?:mutuário|devedor|tomador|senhor|sr\.?|senhora|sra\.?)[:\s]+([^\n\r]{3,120})",
    ]
