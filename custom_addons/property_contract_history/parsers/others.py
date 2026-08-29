# -*- coding: utf-8 -*-
"""Other contract types parser (comodato, arrendamento, etc.)."""
from .base import BaseContractParser, parser_registry


@parser_registry.register
class ComodatoContractParser(BaseContractParser):
    name = "Contrato de Comodato"
    slug = "comodato"
    priority = 50
    contract_type = "comodato"

    DETECT_KEYWORDS = [
        "contrato de comodato",
        "comodato",
        "empréstimo gratuito",
        "comodante",
        "comodatário",
    ]

    PARTY1_NAME_PATTERNS = [
        r"(?:comodante|proprietário)[:\s]+([^\n\r]{3,120})",
    ]

    PARTY2_NAME_PATTERNS = [
        r"(?:comodatário|tomador|senhor|sr\.?|senhora|sra\.?)[:\s]+([^\n\r]{3,120})",
    ]

    START_DATE_PATTERNS = [
        r"(?:data\s+de\s+entrega|vigência|a\s+partir\s+de)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    END_DATE_PATTERNS = [
        r"(?:data\s+de\s+devolução|término)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]
