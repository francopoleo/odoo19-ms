# -*- coding: utf-8 -*-
"""Sales contract parser."""
from .base import BaseContractParser, parser_registry


@parser_registry.register
class SalesContractParser(BaseContractParser):
    name = "Contrato de Venda"
    slug = "sale"
    priority = 90
    contract_type = "sale"

    DETECT_KEYWORDS = [
        "contrato de venda",
        "contrato de compra e venda",
        "promessa de venda",
        "promissória de venda",
        "sales agreement",
        "purchase agreement",
        "comprador",
        "vendedor",
    ]

    # Sales-specific patterns
    TOTAL_VALUE_PATTERNS = [
        r"(?:preço|preço\s+total|valor\s+total|valor\s+da\s+venda|preço\s+de\s+venda)[:\s]+(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})",
        r"(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s+(?:preço|valor|total))",
    ]

    PARTY1_NAME_PATTERNS = [
        r"(?:vendedor|alienante|senhor|sr\.?|senhora|sra\.?)[:\s]+([^\n\r]{3,120})",
    ]

    PARTY2_NAME_PATTERNS = [
        r"(?:comprador|adquirente|senhor|sr\.?|senhora|sra\.?)[:\s]+([^\n\r]{3,120})",
    ]

    SIGN_DATE_PATTERNS = [
        r"(?:assinado|celebrado|datado)\s+(?:em\s+)?(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:nesta\s+data|neste\s+ato)[,:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    START_DATE_PATTERNS = [
        r"(?:data\s+de\s+vigência|data\s+de\s+início)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]
