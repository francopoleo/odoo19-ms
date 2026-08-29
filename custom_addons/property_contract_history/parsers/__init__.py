# -*- coding: utf-8 -*-
"""
Parser infrastructure for contract history extraction.
Follows the same pattern as property_payment_proof.
"""
from .base import BaseContractParser, parser_registry
from . import generic, rental, sale, financing, others

__all__ = ["BaseContractParser", "parser_registry"]
