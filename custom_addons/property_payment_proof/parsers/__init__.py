# -*- coding: utf-8 -*-
"""
Parser registry for payment proof extraction.

To add a new bank/institution:
  1. Create a new .py file in this directory
  2. Subclass BaseParser, decorate with @parser_registry.register
  3. Import it below

The registry automatically sorts parsers by priority (highest first).
GenericParser (priority=0) always matches as the final fallback.
"""
from .base import parser_registry, BaseParser  # noqa: F401

# ── Import all parsers so they self-register ──────────────────────────────────
from . import generic   # priority  0  – always matches (fallback)
from . import nubank    # priority 100
from . import itau      # priority  90
from . import bradesco  # priority  90
from . import caixa     # priority  90
from . import inter     # priority  90
from . import outros    # priority  90  – Santander, BTG, Sicoob, Sicredi, C6, PicPay, Mercado Pago