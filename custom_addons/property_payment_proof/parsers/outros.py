# -*- coding: utf-8 -*-
"""
Parsers para demais instituições: Santander, BTG, Sicoob, Sicredi, C6, PicPay, Mercado Pago.
Adicione novos bancos aqui seguindo o mesmo padrão.
"""
from .base import BaseParser, parser_registry


@parser_registry.register
class SantanderParser(BaseParser):
    name = "Santander"
    slug = "santander"
    priority = 90
    institution = "Santander"
    DETECT_KEYWORDS = ["santander"]
    PAYER_NAME_PATTERNS = [
        r"(?:pagador|remetente|ordenante)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+do\s+pagador[\s\S]{0,200}?nome[:\s]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]
    RECEIVER_NAME_PATTERNS = [
        r"(?:recebedor|favorecido|benefici[aá]rio)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+do\s+(?:recebedor|favorecido)[\s\S]{0,200}?nome[:\s]+([^\n\r]{3,80})",
    ]


@parser_registry.register
class BtgParser(BaseParser):
    name = "BTG Pactual"
    slug = "btg"
    priority = 90
    institution = "BTG Pactual"
    DETECT_KEYWORDS = ["btg pactual", "btgpactual", "banco btg"]
    PAYER_NAME_PATTERNS = [
        r"(?:pagador|remetente)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]


@parser_registry.register
class SicoobParser(BaseParser):
    name = "Sicoob"
    slug = "sicoob"
    priority = 90
    institution = "Sicoob"
    DETECT_KEYWORDS = ["sicoob", "bancoob"]
    PAYER_NAME_PATTERNS = [
        r"(?:pagador|cooperado|remetente)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]


@parser_registry.register
class SicrediParser(BaseParser):
    name = "Sicredi"
    slug = "sicredi"
    priority = 90
    institution = "Sicredi"
    DETECT_KEYWORDS = ["sicredi"]
    PAYER_NAME_PATTERNS = [
        r"(?:pagador|associado|remetente)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]


@parser_registry.register
class C6Parser(BaseParser):
    name = "C6 Bank"
    slug = "c6"
    priority = 90
    institution = "C6 Bank"
    DETECT_KEYWORDS = ["c6 bank", "c6bank"]
    PAYER_NAME_PATTERNS = [
        r"(?:pagador|de|remetente)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]


@parser_registry.register
class PicPayParser(BaseParser):
    name = "PicPay"
    slug = "picpay"
    priority = 90
    institution = "PicPay"
    DETECT_KEYWORDS = ["picpay"]
    PAYER_NAME_PATTERNS = [
        r"(?:pagador|quem\s+pagou|de)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]


@parser_registry.register
class MercadoPagoParser(BaseParser):
    name = "Mercado Pago"
    slug = "mercadopago"
    priority = 90
    institution = "Mercado Pago"
    DETECT_KEYWORDS = ["mercado pago", "mercadopago"]
    PAYER_NAME_PATTERNS = [
        r"(?:pagador|remetente|de)[:\s\-]+([^\n\r]{3,80})",
        r"dados\s+de\s+quem\s+(?:fez|pagou|realizou|enviou|efetuou)[\s\S]{0,300}?nome[:\s]+([^\n\r]{3,80})",
    ]