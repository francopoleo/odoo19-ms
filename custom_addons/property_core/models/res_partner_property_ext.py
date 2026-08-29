from odoo import api, fields, models


class ResPartnerPropertyExt(models.Model):
    _inherit = "res.partner"

    # ==================== CAMPOS GERAIS ====================
    mobile = fields.Char(
        string="Celular / WhatsApp",
        help="Celular ou WhatsApp para contato rápido.",
    )

    # ==================== CAMPOS PROPRIETÁRIO ====================
    cpf_cnpj = fields.Char(
        string="CPF / CNPJ",
        help="Documento fiscal para identificação e obrigações contratuais/fiscais.",
    )

    bank_name = fields.Char(
        string="Banco",
        help="Banco para repasses e pagamentos.",
    )

    bank_agency = fields.Char(
        string="Agência",
        help="Agência bancária.",
    )

    bank_account = fields.Char(
        string="Conta Bancária",
        help="Número da conta bancária.",
    )

    # ==================== CAMPOS CORRETOR ====================
    creci = fields.Char(
        string="CRECI",
        help="Número de registro no CRECI.",
    )

    commission_rate = fields.Float(
        string="Comissão Padrão (%)",
        digits=(5, 2),
        default=6.0,
        help="Percentual padrão de comissão.",
    )

    # ==================== CAMPOS COMPRADOR / VENDEDOR ====================
    budget_min = fields.Monetary(
        string="Orçamento Mínimo",
        help="Orçamento mínimo para compra.",
        currency_field="currency_id",
    )

    budget_max = fields.Monetary(
        string="Orçamento Máximo",
        help="Orçamento máximo para compra.",
        currency_field="currency_id",
    )

    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
    )

    # ==================== CAMPOS INVESTIDOR ====================
    investment_profile = fields.Selection(
        [
            ("income", "Renda"),
            ("growth", "Valorização"),
            ("mixed", "Misto"),
        ],
        string="Perfil de Investimento",
        default="mixed",
        help="Perfil de investimento preferido.",
    )

    # ==================== CAMPOS COMPUTADOS ====================
    property_contact_count = fields.Integer(
        string="Relacionamentos Imobiliários",
        compute="_compute_property_contact_count",
        help="Número de relacionamentos imobiliários (proprietário, corretor, etc).",
    )

    has_property_roles = fields.Boolean(
        string="Tem Papéis Imobiliários",
        compute="_compute_has_property_roles",
        search="_search_has_property_roles",
        help="Se o contato tem algum papel imobiliário (proprietário, corretor, etc).",
    )

    property_role_ids = fields.Many2many(
        "res.partner.category",
        compute="_compute_property_role_ids",
        help="Papéis imobiliários deste contato.",
    )

    # Role indicator fields for view visibility
    has_role_broker = fields.Boolean(
        compute="_compute_has_role_broker",
        help="Tem papel de Corretor",
    )
    has_role_owner = fields.Boolean(
        compute="_compute_has_role_owner",
        help="Tem papel de Proprietário",
    )
    has_role_buyer = fields.Boolean(
        compute="_compute_has_role_buyer",
        help="Tem papel de Comprador",
    )
    has_role_seller = fields.Boolean(
        compute="_compute_has_role_seller",
        help="Tem papel de Vendedor",
    )
    has_role_investor = fields.Boolean(
        compute="_compute_has_role_investor",
        help="Tem papel de Investidor",
    )

    def _compute_property_contact_count(self):
        property_categories = self.env["res.partner.category"].search(
            [
                ("name", "in", [
                    "Proprietário", "Corretor", "Inquilino",
                    "Comprador", "Vendedor", "Investidor",
                    "Corretora", "Construtora"
                ])
            ]
        )
        for partner in self:
            cats = partner.category_ids if hasattr(partner, 'category_ids') else self.env["res.partner.category"]
            partner.property_contact_count = len(cats & property_categories) if cats else 0

    def _compute_has_property_roles(self):
        property_categories = self.env["res.partner.category"].search(
            [
                ("name", "in", [
                    "Proprietário", "Corretor", "Inquilino",
                    "Comprador", "Vendedor", "Investidor",
                    "Corretora", "Construtora"
                ])
            ]
        )
        for partner in self:
            cats = partner.category_ids if hasattr(partner, 'category_ids') else self.env["res.partner.category"]
            partner.has_property_roles = bool(cats & property_categories) if cats else False

    def _compute_property_role_ids(self):
        property_categories = self.env["res.partner.category"].search(
            [
                ("name", "in", [
                    "Proprietário", "Corretor", "Inquilino",
                    "Comprador", "Vendedor", "Investidor",
                    "Corretora", "Construtora"
                ])
            ]
        )
        for partner in self:
            if hasattr(partner, 'category_ids') and partner.category_ids:
                partner.property_role_ids = partner.category_ids & property_categories
            else:
                partner.property_role_ids = self.env["res.partner.category"]

    def _compute_has_role_broker(self):
        broker_cat = self.env["res.partner.category"].search([("name", "=", "Corretor")], limit=1)
        for partner in self:
            cats = partner.category_ids if hasattr(partner, 'category_ids') else self.env["res.partner.category"]
            partner.has_role_broker = broker_cat in cats if broker_cat and cats else False

    def _compute_has_role_owner(self):
        owner_cat = self.env["res.partner.category"].search([("name", "=", "Proprietário")], limit=1)
        for partner in self:
            cats = partner.category_ids if hasattr(partner, 'category_ids') else self.env["res.partner.category"]
            partner.has_role_owner = owner_cat in cats if owner_cat and cats else False

    def _compute_has_role_buyer(self):
        buyer_cat = self.env["res.partner.category"].search([("name", "=", "Comprador")], limit=1)
        for partner in self:
            cats = partner.category_ids if hasattr(partner, 'category_ids') else self.env["res.partner.category"]
            partner.has_role_buyer = buyer_cat in cats if buyer_cat and cats else False

    def _compute_has_role_seller(self):
        seller_cat = self.env["res.partner.category"].search([("name", "=", "Vendedor")], limit=1)
        for partner in self:
            cats = partner.category_ids if hasattr(partner, 'category_ids') else self.env["res.partner.category"]
            partner.has_role_seller = seller_cat in cats if seller_cat and cats else False

    def _compute_has_role_investor(self):
        investor_cat = self.env["res.partner.category"].search([("name", "=", "Investidor")], limit=1)
        for partner in self:
            cats = partner.category_ids if hasattr(partner, 'category_ids') else self.env["res.partner.category"]
            partner.has_role_investor = investor_cat in cats if investor_cat and cats else False

    @staticmethod
    def _search_has_property_roles(operator, value):
        property_categories = models.Model.env["res.partner.category"].search(
            [
                ("name", "in", [
                    "Proprietário", "Corretor", "Inquilino",
                    "Comprador", "Vendedor", "Investidor",
                    "Corretora", "Construtora"
                ])
            ]
        )
        if operator == "=" and value:
            return [("category_ids", "in", property_categories.ids)]
        elif operator == "!=" and not value:
            return [("category_ids", "in", property_categories.ids)]
        else:
            return [("category_ids", "not in", property_categories.ids)]
