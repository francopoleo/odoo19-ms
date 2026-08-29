from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Configurações contábeis para o módulo de imóveis.
    Usa ir.config_parameter para evitar colunas extras em res.company
    (o que causaria erros de coluna inexistente durante o upgrade).
    """
    _inherit = "res.config.settings"

    property_rent_journal_id = fields.Many2one(
        "account.journal",
        string="Diário Padrão de Aluguéis",
        config_parameter="property_core.rent_journal_id",
        help="Diário contábil usado para lançamentos de recebimento de aluguel",
    )
    property_rent_income_account_id = fields.Many2one(
        "account.account",
        string="Conta de Receita de Aluguel",
        config_parameter="property_core.rent_income_account_id",
        help="Conta contábil de receita creditada nos recebimentos de aluguel",
    )
    property_repasse_journal_id = fields.Many2one(
        "account.journal",
        string="Diário de Repasse ao Proprietário",
        config_parameter="property_core.repasse_journal_id",
        help="Diário contábil usado nos pagamentos de repasse ao proprietário (ex: Banco Principal)",
    )
    property_repasse_account_id = fields.Many2one(
        "account.account",
        string="Conta de Repasse (Obrigação)",
        config_parameter="property_core.repasse_account_id",
        domain="[('account_type', 'in', ['liability_current', 'liability_non_current', 'liability_payable'])]",
        help="Conta contábil de passivo debitada ao realizar o repasse ao proprietário",
    )