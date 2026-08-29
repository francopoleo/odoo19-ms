from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CommonTag(models.Model):
    _name = "common.tag"
    _description = "Tag Genérica"
    _order = "sequence, name"
    _rec_name = "name"

    name = fields.Char(string="Nome", required=True, translate=True)
    sequence = fields.Integer(string="Ordem", default=10)
    color = fields.Integer(string="Cor", default=0)
    active = fields.Boolean(string="Ativo", default=True)

    company_id = fields.Many2one(
        'res.company',
        string="Empresa",
        index=True,
        help="Deixe em branco para tags globais (visíveis em todas as empresas)",
    )

    category = fields.Selection([
        ("general", "Geral"),
        ("governance", "Governança"),
        ("property", "Imóveis"),
        ("contract", "Contratos"),
        ("financial", "Financeiro"),
        ("maintenance", "Manutenção"),
    ], string="Categoria", default="general")

    description = fields.Text(string="Descrição", translate=True)
    usage_count = fields.Integer(string="Quantidade de Usos", compute="_compute_usage_count")

    @api.depends("name")
    def _compute_usage_count(self):
        for tag in self:
            tag.usage_count = 0

    @api.constrains("name", "category", "company_id")
    def _check_unique_name(self):
        for tag in self:
            existing = self.search([
                ("name", "=", tag.name),
                ("category", "=", tag.category),
                ("company_id", "=", tag.company_id.id if tag.company_id else False),
                ("id", "!=", tag.id),
            ])
            if existing:
                raise ValidationError(
                    _("Já existe uma tag '%s' na categoria '%s' para esta empresa!") %
                    (tag.name, dict(self._fields["category"].selection).get(tag.category))
                )

    def action_toggle_active(self):
        for tag in self:
            tag.active = not tag.active