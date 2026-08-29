from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GovernanceCaseParticipant(models.Model):
    _name = "governance.case.participant"
    _description = "Participante do Caso de Governança"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    case_id = fields.Many2one("governance.case", string="Caso", required=True, ondelete="cascade", index=True)
    company_id = fields.Many2one(related="case_id.company_id", store=True, readonly=True, index=True)
    partner_id = fields.Many2one("res.partner", string="Contato", required=True, ondelete="restrict")
    role = fields.Selection([
        ("claimant", "Reclamante"),
        ("notified", "Notificado"),
        ("owner", "Proprietário"),
        ("tenant", "Locatário"),
        ("buyer", "Comprador"),
        ("seller", "Vendedor"),
        ("broker", "Corretor"),
        ("legal_counsel", "Advogado"),
        ("proxy", "Procurador"),
        ("counterparty", "Parte Contrária"),
        ("public_body", "Órgão Público"),
        ("registry_office", "Cartório"),
        ("syndic", "Síndico"),
        ("administrator", "Administradora"),
        ("witness", "Testemunha"),
        ("internal_owner", "Responsável Interno"),
        ("other", "Outro"),
    ], string="Papel", required=True, default="other")
    is_primary = fields.Boolean(string="Contato Principal")
    note = fields.Char(string="Observação")
    email = fields.Char(string="E-mail", compute="_compute_contact_channels", readonly=True)
    phone = fields.Char(string="Telefone", compute="_compute_contact_channels", readonly=True)
    mobile = fields.Char(string="Celular", compute="_compute_contact_channels", readonly=True)


    @api.depends("partner_id")
    def _compute_contact_channels(self):
        for rec in self:
            partner = rec.partner_id
            rec.email = partner.email or False
            rec.phone = partner.phone or False
            rec.mobile = partner._fields.get("mobile") and partner.mobile or False

    @api.constrains("case_id", "partner_id", "role")
    def _check_unique_participant_role(self):
        for rec in self:
            if not rec.case_id or not rec.partner_id or not rec.role:
                continue
            duplicate = self.search([
                ("id", "!=", rec.id),
                ("case_id", "=", rec.case_id.id),
                ("partner_id", "=", rec.partner_id.id),
                ("role", "=", rec.role),
            ], limit=1)
            if duplicate:
                raise ValidationError(_("Já existe este participante com o mesmo papel neste caso."))

    @api.constrains("case_id", "is_primary")
    def _check_single_primary(self):
        for rec in self.filtered("is_primary"):
            others = rec.case_id.participant_ids.filtered(lambda p: p.id != rec.id and p.is_primary)
            if others:
                raise ValidationError(_("Só pode existir um contato principal por caso."))

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._normalize_primary_flag()
        records.mapped("case_id")._sync_partner_ids_from_participants()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._normalize_primary_flag()
        self.mapped("case_id")._sync_partner_ids_from_participants()
        return res

    def unlink(self):
        cases = self.mapped("case_id")
        res = super().unlink()
        cases._sync_partner_ids_from_participants()
        return res

    def _normalize_primary_flag(self):
        for rec in self.filtered("is_primary"):
            others = rec.case_id.participant_ids.filtered(lambda p: p.id != rec.id and p.is_primary)
            if others:
                others.with_context(skip_participant_partner_sync=True).write({"is_primary": False})

    @api.onchange("is_primary")
    def _onchange_is_primary(self):
        if self.is_primary and self.case_id:
            others = self.case_id.participant_ids.filtered(lambda p: p != self and p.is_primary)
            others.is_primary = False
