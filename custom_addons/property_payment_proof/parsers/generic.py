# -*- coding: utf-8 -*-
from .base import BaseParser, parser_registry


@parser_registry.register
class GenericParser(BaseParser):
    """
    Fallback parser — used when no bank-specific parser is detected.
    Priority 0 means it is always the last to be tried.
    """
    name = "Genérico"
    slug = "generic"
    priority = 0

    def detect(self, text: str) -> bool:
        return True  # always matches as fallback