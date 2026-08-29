# -*- coding: utf-8 -*-
"""Rental/lease contract parser."""
from .base import BaseContractParser, parser_registry


@parser_registry.register
class RentalContractParser(BaseContractParser):
    name = "Contrato de Aluguel/Locação"
    slug = "rental"
    priority = 100  # Highest priority
    contract_type = "rental"

    DETECT_KEYWORDS = [
        "contrato de aluguel",
        "contrato de locação",
        "contrato de locação residencial",
        "lease agreement",
        "rental agreement",
        "locatário",
        "locador",
    ]

    # Rental-specific patterns
    PARTY1_NAME_PATTERNS = [
        r"(?:I\s+–\s+LOCADORA|LOCADORA)[:\s]*\n+([^\n]{3,150})",
        r"(?:locador|proprietário|locadora)[:\s\-]+([^\n\r]{3,120})",
    ]

    PARTY1_VAT_PATTERNS = [
        r"(?:CNPJ|CNPJ/MF)[^0-9]*(\d{2}\.?\d{3}\.?\d{3}/?0001-?\d{2})",
        r"inscritas?\s+no\s+CNPJ[^0-9]*(\d{2}\.?\d{3}\.?\d{3}/?0001-?\d{2})",
    ]

    PARTY2_NAME_PATTERNS = [
        r"(?:II\s+–\s+LOCATÁRIO|LOCATÁRIO)[:\s]*\n+([^\n]{3,150})",
        r"(?:locatário|inquilino|tomador)[:\s\-]+([^\n\r]{3,120})",
    ]

    MONTHLY_AMOUNT_PATTERNS = [
        r"(?:aluguel|mensalidade|valor\s+da\s+locação|aluguel\s+mensal)[:\s]+(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})",
        r"(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s+(?:mensal|por\s+mês|de\s+aluguel|de\s+aluguel\s+mensal))",
    ]

    DEPOSIT_PATTERNS = [
        r"(?:depósito\s+caução|caução|fiança|garantia\s+locatícia|deposito\s+cauçao)[:\s]+(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})",
        r"(?:r\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s+(?:de\s+caução|de\s+depósito|de\s+fiança|cauçao))",
    ]

    START_DATE_PATTERNS = [
        r"(?:início\s+da\s+locação|vigência\s+do\s+contrato|data\s+de\s+início|data\s+do\s+contrato)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:a\s+partir\s+de|aos\s+)(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})",
        r"(?:a\s+partir\s+de)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
    ]

    END_DATE_PATTERNS = [
        r"(?:término\s+da\s+locação|final\s+do\s+contrato|data\s+de\s+término|data\s+do\s+vencimento)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:até\s+)?(\d{2}[/-]\d{2}[/-]\d{4})(?:\s+(?:término|vencimento))",
    ]
