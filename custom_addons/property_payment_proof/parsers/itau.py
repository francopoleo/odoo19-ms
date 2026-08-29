# -*- coding: utf-8 -*-
from .base import BaseParser, parser_registry


@parser_registry.register
class ItauParser(BaseParser):
    """
    Comprovante Itaú Unibanco (PIX, TED, DOC).

    Formato típico:
        ITAÚ UNIBANCO
        COMPROVANTE DE TRANSFERÊNCIA
        Pagador
        Nome: RAFAEL DE MATTOS SABATO
        CPF/CNPJ: ***.368.878-**
        Agência/Conta: 1234/56789-0
        Recebedor
        Nome: KATIA MANUELA DA SILVA
        ...
        Autenticação: 123456789
    """
    name = "Itaú"
    slug = "itau"
    priority = 90
    institution = "Itaú Unibanco"

    DETECT_KEYWORDS = ["itaú", "itau", "itaú unibanco", "iupp"]

    PAYER_NAME_PATTERNS = [
        # Itaú usa seção "Pagador" → "Nome:" na linha seguinte
        r"pagador\s*[\r\n]+\s*nome[:\s]+([^\n\r]{3,80})",
        r"(?:pagador|remetente)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]

    RECEIVER_NAME_PATTERNS = [
        r"recebedor\s*[\r\n]+\s*nome[:\s]+([^\n\r]{3,80})",
        r"(?:recebedor|favorecido|benefici[aá]rio)[:\s\-]+([^\n\r]{3,80})",
    ]

    TRANSACTION_ID_PATTERNS = [
        r"(?:autentica[cç][aã]o|autenticação)[:\s\-]+([0-9A-Z\.\-_/]{6,})",
        r"(?:end[- ]?to[- ]?end|e2e)[:\s\-]+([A-Z0-9\.\-_/]{8,})",
        r"\b(E[0-9A-Z]{20,})\b",
    ]