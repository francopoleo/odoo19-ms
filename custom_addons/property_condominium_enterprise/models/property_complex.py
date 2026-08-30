from odoo import _, fields, models


class PropertyComplex(models.Model):
    _inherit = "property.complex"

    complex_mode = fields.Selection(
        [
            ("property", "Imóvel"),
            ("condominium", "Condomínio"),
            ("mall", "Shopping / Centro Comercial"),
            ("mixed", "Uso Misto"),
        ],
        string="Modo de Operação",
        default="property",
        tracking=True,
    )
    condo_active = fields.Boolean("Condomínio Ativo", default=False, tracking=True)
    condo_manager_id = fields.Many2one(
        "res.partner",
        string="Administrador do Condomínio",
        tracking=True,
        help="Administrador principal responsável pelo complexo.",
    )
    condo_rent_day = fields.Integer(
        "Dia de Vencimento",
        default=10,
        help="Dia padrão usado para cobranças e boletos do condomínio.",
    )
    condo_advance_days = fields.Integer(
        "Dias de Antecedência",
        default=10,
        help="Quantidade de dias antes do vencimento para gerar a cobrança mensal.",
    )
    condo_fee_amount = fields.Monetary(
        "Taxa Padrão do Condomínio",
        currency_field="currency_id",
        tracking=True,
    )
    common_area_budget = fields.Monetary(
        "Orçamento das Áreas Comuns",
        currency_field="currency_id",
        tracking=True,
    )
    common_area_rateio_key = fields.Selection(
        [
            ("equal", "Igual"),
            ("fractional", "Fração Ideal"),
            ("gla", "Por ABL"),
            ("custom", "Personalizado"),
        ],
        string="Regra de Rateio",
        default="fractional",
        tracking=True,
    )
    charge_model = fields.Selection(
        [("manual", "Manual"), ("automatic", "Automático")],
        string="Modelo de Cobrança",
        default="automatic",
        tracking=True,
    )
    cnab_profile_id = fields.Many2one(
        "property.condominium.cnab.profile",
        string="Perfil CNAB",
        tracking=True,
        help="Perfil bancário usado para gerar remessa e ler retorno.",
    )

    def action_generate_condominium_charges(self):
        self.ensure_one()
        self.env["property.condominium.charge"].action_generate_monthly_charges()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Condomínio"),
                "message": _("As cobranças mensais foram geradas."),
                "type": "success",
            },
        }
