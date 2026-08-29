# -*- coding: utf-8 -*-
from .base import BaseParser, parser_registry


@parser_registry.register
class NubankParser(BaseParser):
    """
    Comprovante Nubank / Nu Pagamentos.

    Formato típico:
        Nubank
        Comprovante de Pix
        Valor  R$ 1.500,00
        Para
        KATIA MANUELA DA SILVA
        CPF: ***.123.456-**
        Instituição: Nubank
        De
        RAFAEL DE MATTOS SABATO
        CPF: ***.368.878-**
        Conta: Nubank
        ID da transação: E...
    """
    name = "Nubank"
    slug = "nubank"
    priority = 100
    institution = "Nubank"

    DETECT_KEYWORDS = ["nubank", "nu pagamentos", "nu.com.br"]

    PAYER_NAME_PATTERNS = [
        # Nubank coloca "De\n[NOME]" para o pagador
        r"(?:^|\n)\s*de\s*[\r\n]+\s*([A-ZÁÉÍÓÚÃÕÂÊÎÔÛÀÈÌÒÙ][^\n\r]{2,79})",
        # Fallback padrões genéricos
        r"(?:pagador|remetente|origem)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]

    RECEIVER_NAME_PATTERNS = [
        # Nubank coloca "Para\n[NOME]" para o recebedor
        r"(?:^|\n)\s*para\s*[\r\n]+\s*([A-ZÁÉÍÓÚÃÕÂÊÎÔÛÀÈÌÒÙ][^\n\r]{2,79})",
        r"(?:recebedor|favorecido|benefici[aá]rio)[:\s\-]+([^\n\r]{3,80})",
    ]

    TRANSACTION_ID_PATTERNS = [
        r"(?:id\s+da\s+transa[cç][aã]o|end[- ]?to[- ]?end|e2e)[:\s\-]+([A-Z0-9\.\-_/]{8,})",
        r"\b(E[0-9A-Z]{20,})\b",
    ]