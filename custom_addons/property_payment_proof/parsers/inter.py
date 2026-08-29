# -*- coding: utf-8 -*-
from .base import BaseParser, parser_registry


@parser_registry.register
class InterParser(BaseParser):
    """Banco Inter."""
    name = "Banco Inter"
    slug = "inter"
    priority = 90
    institution = "Banco Inter"

    DETECT_KEYWORDS = ["banco inter", "bancointer", "inter.co"]

    PAYER_NAME_PATTERNS = [
        r"(?:pagador|quem\s+enviou|remetente|de)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]

    RECEIVER_NAME_PATTERNS = [
        r"(?:recebedor|quem\s+recebeu|favorecido|para)[:\s\-]+([^\n\r]{3,80})",
    ]

    TRANSACTION_ID_PATTERNS = [
        r"(?:id\s+da\s+transa[cç][aã]o|end[- ]?to[- ]?end|e2e)[:\s\-]+([A-Z0-9\.\-_/]{8,})",
        r"\b(E[0-9A-Z]{20,})\b",
    ]