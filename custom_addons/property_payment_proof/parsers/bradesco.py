# -*- coding: utf-8 -*-
from .base import BaseParser, parser_registry


@parser_registry.register
class BradescoParser(BaseParser):
    """
    Comprovante Bradesco (PIX, TED, DOC, Boleto).

    Formato típico:
        Banco Bradesco S.A.
        Comprovante de Pix
        Dados do Pagador
        Nome: RAFAEL DE MATTOS SABATO
        CPF: ***.368.878-**
        Dados do Recebedor / Favorecido
        Nome: KATIA MANUELA DA SILVA
        NSU: 1234567890
    """
    name = "Bradesco"
    slug = "bradesco"
    priority = 90
    institution = "Bradesco"

    DETECT_KEYWORDS = ["bradesco", "banco bradesco"]

    PAYER_NAME_PATTERNS = [
        r"dados\s+do\s+pagador[\s\S]{0,200}?nome[:\s]+([^\n\r]{3,80})",
        r"pagador\s*[\r\n]+\s*nome[:\s]+([^\n\r]{3,80})",
        r"(?:pagador|remetente)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]

    RECEIVER_NAME_PATTERNS = [
        r"dados\s+do\s+(?:recebedor|favorecido)[\s\S]{0,200}?nome[:\s]+([^\n\r]{3,80})",
        r"(?:recebedor|favorecido|benefici[aá]rio)[:\s\-]+([^\n\r]{3,80})",
    ]

    TRANSACTION_ID_PATTERNS = [
        r"(?:nsu|autentica[cç][aã]o|autenticação)[:\s\-]+([0-9A-Z\.\-_/]{6,})",
        r"(?:end[- ]?to[- ]?end|e2e)[:\s\-]+([A-Z0-9\.\-_/]{8,})",
        r"\b(E[0-9A-Z]{20,})\b",
    ]