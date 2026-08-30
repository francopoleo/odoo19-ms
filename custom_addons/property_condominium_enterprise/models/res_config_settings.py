from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    property_condominium_journal_id = fields.Many2one(
        "account.journal",
        string="Diário do Condomínio",
        config_parameter="property_condominium.journal_id",
        help="Diário padrão usado para faturas e baixas do condomínio.",
    )
    property_condominium_income_account_id = fields.Many2one(
        "account.account",
        string="Conta de Receita do Condomínio",
        config_parameter="property_condominium.income_account_id",
        domain="[('account_type','in',['income','income_other'])]",
        help="Conta de receita usada nas cobranças do condomínio.",
    )
