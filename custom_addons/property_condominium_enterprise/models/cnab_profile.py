from odoo import fields, models


class CondominiumCnabProfile(models.Model):
    _name = "property.condominium.cnab.profile"
    _description = "Perfil CNAB do Condomínio"
    _order = "name"

    name = fields.Char(required=True)
    bank_code = fields.Selection(
        [
            ("itau", "Itaú"),
            ("santander", "Santander"),
            ("bradesco", "Bradesco"),
            ("bb", "Banco do Brasil"),
            ("caixa", "Caixa"),
            ("other", "Outro"),
        ],
        default="itau",
        required=True,
    )
    cnab_type = fields.Selection(
        [("240", "CNAB 240"), ("400", "CNAB 400")],
        default="240",
        required=True,
    )
    carteira = fields.Char("Carteira")
    agencia = fields.Char("Agência")
    conta_corrente = fields.Char("Conta Corrente")
    digito_conta = fields.Char("Dígito da Conta")
    convenio = fields.Char("Convênio / Cedente")
    empresa_mae = fields.Char("Empresa / Cedente")
    documento_cedente = fields.Char("CNPJ/CPF do Cedente")
    active = fields.Boolean(default=True)
