# -*- coding: utf-8 -*-
from .base import BaseParser, parser_registry


@parser_registry.register
class CaixaParser(BaseParser):
    """Caixa Econômica Federal (PIX, TED, CAIXA Tem)."""
    name = "Caixa Econômica Federal"
    slug = "caixa"
    priority = 90
    institution = "Caixa Econômica Federal"

    DETECT_KEYWORDS = ["caixa econômica", "caixa economica", "cef", "caixa tem", "caixatem"]

    PAYER_NAME_PATTERNS = [
        r"(?:origem|pagador|remetente|ordenante)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+do\s+pagador[\s\S]{0,200}?nome[:\s]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]

    RECEIVER_NAME_PATTERNS = [
        r"(?:destino|recebedor|favorecido|benefici[aá]rio)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+do\s+(?:recebedor|favorecido)[\s\S]{0,200}?nome[:\s]+([^\n\r]{3,80})",
    ]

    TRANSACTION_ID_PATTERNS = [
        r"(?:autentica[cç][aã]o|autenticação|comprovante\s+n[º°]?)[:\s\-]+([0-9A-Z\.\-_/]{6,})",
        r"(?:end[- ]?to[- ]?end|e2e)[:\s\-]+([A-Z0-9\.\-_/]{8,})",
        r"\b(E[0-9A-Z]{20,})\b",
    ]