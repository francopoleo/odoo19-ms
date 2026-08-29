# -*- coding: utf-8 -*-


def post_init_hook(env):
    env["property.contract.ocr.template"].sudo().action_install_default_templates()
