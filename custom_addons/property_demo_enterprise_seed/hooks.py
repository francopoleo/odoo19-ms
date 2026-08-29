# -*- coding: utf-8 -*-
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Gera uma massa inicial somente se o parâmetro estiver habilitado.

    Para gerar automaticamente na instalação, crie antes o parâmetro:
      property_demo_enterprise_seed.auto_generate = 1
    """
    if not isinstance(env, api.Environment):
        env = api.Environment(env, SUPERUSER_ID, {})

    ICP = env["ir.config_parameter"].sudo()
    if ICP.get_param("property_demo_enterprise_seed.auto_generate", "0") not in ("1", "true", "True", True):
        return

    try:
        contract_count = int(ICP.get_param("property_demo_enterprise_seed.contract_count", "60") or 60)
        months_past = int(ICP.get_param("property_demo_enterprise_seed.months_past", "10") or 10)
        months_future = int(ICP.get_param("property_demo_enterprise_seed.months_future", "8") or 8)
        wizard = env["property.demo.generator"].sudo().create({
            "contract_count": contract_count,
            "months_past": months_past,
            "months_future": months_future,
            "clear_previous": False,
        })
        wizard.action_generate()
    except Exception as exc:
        _logger.exception("[DEMO-IMOB] Falha ao gerar massa inicial: %s", exc)
