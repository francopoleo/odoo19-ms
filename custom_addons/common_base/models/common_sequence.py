from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CommonSequence(models.Model):
    """
    Configuração de sequências numéricas para o ERP.
    Cada empresa tem suas próprias sequências independentes.
    """
    _name = "common.sequence"
    _description = "Sequência Numérica"
    _order = "code"

    name = fields.Char(string="Nome", required=True, translate=True)
    code = fields.Char(string="Código", required=True, help="Código único da sequência por empresa")

    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )

    # Configuração da sequência
    prefix = fields.Char(string="Prefixo", help="Ex: PROP/%(year)s/")
    suffix = fields.Char(string="Sufixo")
    padding = fields.Integer(string="Número de Dígitos", default=5, help="Quantidade de dígitos (ex: 5 = 00001)")
    start_number = fields.Integer(string="Número Inicial", default=1)

    # Próximo número
    next_number = fields.Integer(string="Próximo Número", default=1, readonly=True)

    # Campos de controle
    active = fields.Boolean(string="Ativo", default=True)

    _code_company_unique = models.Constraint(
        'UNIQUE(code, company_id)',
        'Já existe uma sequência com este código para esta empresa.',
    )

    def _get_next_number(self):
        """Retorna o próximo número e incrementa"""
        self.ensure_one()
        number = self.next_number
        self.next_number += 1
        return number

    def _format_number(self, number):
        """Formata o número com padding e prefixo/sufixo"""
        import datetime

        self.ensure_one()
        padded = str(number).zfill(self.padding)
        formatted = padded

        if self.prefix:
            formatted = self.prefix + formatted
        if self.suffix:
            formatted = formatted + self.suffix

        today = datetime.date.today()
        formatted = formatted.replace("%(year)s", str(today.year))
        formatted = formatted.replace("%(month)s", str(today.month).zfill(2))
        formatted = formatted.replace("%(day)s", str(today.day).zfill(2))

        return formatted

    def get_next(self):
        """Obtém o próximo valor formatado da sequência"""
        self.ensure_one()
        number = self._get_next_number()
        return self._format_number(number)

    @api.model
    def next_by_code(self, code):
        """Obtém o próximo valor para um código de sequência da empresa atual.

        Se não existir sequência para a empresa atual, copia automaticamente
        a configuração de outra empresa (ex: empresa principal) e cria uma nova.
        """
        company = self.env.company
        sequence = self.search([
            ("code", "=", code),
            ("active", "=", True),
            ("company_id", "=", company.id),
        ], limit=1)
        if not sequence:
            # Busca template em qualquer empresa
            template = self.search([
                ("code", "=", code),
                ("active", "=", True),
            ], limit=1)
            if not template:
                return False
            sequence = self.sudo().create({
                "name": template.name,
                "code": template.code,
                "company_id": company.id,
                "prefix": template.prefix,
                "suffix": template.suffix,
                "padding": template.padding,
                "start_number": template.start_number,
                "next_number": template.start_number,
            })
        return sequence.get_next()