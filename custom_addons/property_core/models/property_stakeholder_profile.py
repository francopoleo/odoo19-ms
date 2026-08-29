from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PropertyStakeholderProfile(models.Model):
    _name = "property.stakeholder.profile"
    _description = "Perfil Imobiliário do Contato"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "partner_id, stakeholder_type_id"
    _rec_name = "display_name"

    display_name = fields.Char(compute="_compute_display_name", store=True)
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner", string="Contato Mestre", required=True, ondelete="restrict", tracking=True, help="Contato mestre do Odoo que representa esta pessoa ou empresa.")
    stakeholder_type_id = fields.Many2one("property.stakeholder.type", string="Perfil / Papel Imobiliário", required=True, ondelete="restrict", tracking=True, help="Define o papel funcional deste contato no contexto imobiliário, como proprietário, locatário, corretor, comprador ou investidor.")
    role_status = fields.Selection([
        ("draft", "Rascunho"),
        ("active", "Ativo"),
        ("inactive", "Inativo"),
        ("blocked", "Bloqueado"),
    ], string="Status", default="active", required=True, tracking=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True, index=True)
    start_date = fields.Date("Início")
    end_date = fields.Date("Fim")
    user_id = fields.Many2one("res.users", string="Usuário Relacionado", help="Usuário interno associado a este perfil, quando houver. Útil para corretores, responsáveis comerciais e operação interna.")
    brokerage_profile_id = fields.Many2one("property.stakeholder.profile", string="Imobiliária Vinculada", domain="[('stakeholder_type_id.code', '=', 'brokerage')]", help="Use este campo quando o perfil estiver ligado a uma imobiliária já cadastrada como perfil imobiliário do tipo Imobiliária.")
    registration_number = fields.Char("Registro Profissional / Empresarial", help="Número de CRECI, registro empresarial ou outro identificador profissional relacionado ao papel deste perfil.")
    notes = fields.Text("Orientações e Observações", help="Use este campo para registrar instruções operacionais, contexto do relacionamento e observações internas sobre este perfil.")

    @api.depends("partner_id", "stakeholder_type_id")
    def _compute_display_name(self):
        for rec in self:
            parts = [rec.partner_id.name or ""]
            if rec.stakeholder_type_id.name:
                parts.append(rec.stakeholder_type_id.name)
            rec.display_name = " • ".join([p for p in parts if p])

    @api.constrains("partner_id", "stakeholder_type_id")
    def _check_unique_partner_type(self):
        for rec in self:
            duplicate = self.search([
                ("id", "!=", rec.id),
                ("partner_id", "=", rec.partner_id.id),
                ("stakeholder_type_id", "=", rec.stakeholder_type_id.id),
            ], limit=1)
            if duplicate:
                raise ValidationError("O contato já possui este tipo de perfil imobiliário.")

    @api.constrains("end_date", "start_date")
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(_("A data final não pode ser menor que a data inicial."))

    def _sync_partner_tag(self):
        for rec in self:
            tag = rec.stakeholder_type_id.default_partner_tag_id
            if rec.partner_id and tag and tag not in rec.partner_id.category_id:
                rec.partner_id.category_id = [(4, tag.id)]

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        recs._sync_partner_tag()
        return recs

    def write(self, vals):
        res = super().write(vals)
        if {"stakeholder_type_id", "partner_id"} & set(vals.keys()):
            self._sync_partner_tag()
        return res

    def action_open_partner(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "view_mode": "form",
            "res_id": self.partner_id.id,
        }
