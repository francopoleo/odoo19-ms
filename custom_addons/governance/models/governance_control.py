from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GovernanceControl(models.Model):
    _name = "governance.control"
    _description = "Controle de Governança"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "next_test_date, id"

    name = fields.Char(string="Controle", required=True, tracking=True)
    reference = fields.Char(string="Referência", readonly=True, copy=False, default="Novo")
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company, tracking=True)
    owner_id = fields.Many2one("res.users", string="Dono do controle", required=True, default=lambda self: self.env.user, tracking=True)
    control_type = fields.Selection([
        ("preventive", "Preventivo"), ("detective", "Detectivo"), ("corrective", "Corretivo"),
    ], string="Tipo", required=True, default="preventive", tracking=True)
    frequency = fields.Selection([
        ("event", "Por evento"), ("monthly", "Mensal"), ("quarterly", "Trimestral"),
        ("semiannual", "Semestral"), ("annual", "Anual"),
    ], string="Frequência", required=True, default="annual", tracking=True)
    state = fields.Selection([
        ("draft", "Em desenho"), ("active", "Ativo"), ("deficient", "Com deficiência"),
        ("inactive", "Inativo"),
    ], string="Situação", default="draft", required=True, tracking=True)
    description = fields.Html(string="Objetivo e procedimento", required=True)
    test_method = fields.Html(string="Como testar")
    last_test_date = fields.Date(string="Último teste", tracking=True)
    next_test_date = fields.Date(string="Próximo teste", tracking=True)
    last_test_result = fields.Selection([
        ("effective", "Eficaz"), ("partially_effective", "Parcialmente eficaz"),
        ("ineffective", "Ineficaz"), ("not_tested", "Não testado"),
    ], string="Resultado do último teste", default="not_tested", tracking=True)
    risk_ids = fields.Many2many("governance.case.risk", string="Riscos cobertos")
    case_ids = fields.Many2many("governance.case", string="Casos relacionados")

    @api.constrains("last_test_date", "next_test_date")
    def _check_test_dates(self):
        for record in self:
            if record.last_test_date and record.next_test_date and record.next_test_date < record.last_test_date:
                raise ValidationError(_("O próximo teste não pode ser anterior ao último teste."))

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["common.sequence"].sudo()
        for vals in vals_list:
            if vals.get("reference", "Novo") == "Novo":
                vals["reference"] = sequence.next_by_code("governance.control") or "CTL-NOVA"
        return super().create(vals_list)

    def action_activate(self):
        self.write({"state": "active"})
        return True

    def action_mark_deficient(self):
        self.write({"state": "deficient"})
        return True

    def action_deactivate(self):
        self.write({"state": "inactive"})
        return True
