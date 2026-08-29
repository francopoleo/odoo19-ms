# -*- coding: utf-8 -*-
"""Generic contract parser — fallback for unknown contract types."""
from .base import BaseContractParser, parser_registry


@parser_registry.register
class GenericContractParser(BaseContractParser):
    name = "Contrato Genérico"
    slug = "generic"
    priority = 0  # Lowest priority — always matches as fallback
    contract_type = "other"
    DETECT_KEYWORDS = ["contrato"]  # Matches any document with "contrato"
