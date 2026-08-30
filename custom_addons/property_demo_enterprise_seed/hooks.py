# -*- coding: utf-8 -*-
import logging

from odoo import api, SUPERUSER_ID


_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Gera massa inicial somente quando explicitamente habilitada."""
    if not isinstance(env, api.Environment):
        env = api.Environment(env, SUPERUSER_ID, {})

    parameters = env["ir.config_parameter"].sudo()
    enabled = parameters.get_param(
        "property_demo_enterprise_seed.auto_generate", "0"
    )
    if enabled not in ("1", "true", "True", True):
        return

    try:
        wizard = env["property.demo.generator"].sudo().create({
            "contract_count": int(parameters.get_param(
                "property_demo_enterprise_seed.contract_count", "60"
            ) or 60),
            "months_past": int(parameters.get_param(
                "property_demo_enterprise_seed.months_past", "10"
            ) or 10),
            "months_future": int(parameters.get_param(
                "property_demo_enterprise_seed.months_future", "8"
            ) or 8),
            "clear_previous": False,
        })
        wizard.action_generate()
    except Exception as exc:
        _logger.exception("[DEMO-IMOB] Falha ao gerar massa inicial: %s", exc)
