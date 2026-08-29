from odoo import api, fields, models, _


class PropertyLead(models.Model):
    _name = "property.lead"
    _description = "Interesse em Imóvel"
    _inherit = ["mail.thread"]
    _order = "create_date desc"
    _rec_name = "name"

    # ==================== Contato ====================
    name = fields.Char("Nome", required=True, tracking=True, help="Nome principal do cadastro exibido no sistema.")
    email = fields.Char("E-mail", required=True, tracking=True)
    phone = fields.Char("Telefone", tracking=True, help="Telefone principal para contato.")
    stakeholder_profile_id = fields.Many2one("property.stakeholder.profile", string="Perfil Central", ondelete="set null")

    partner_id = fields.Many2one("res.partner", string="Contato Relacionado", tracking=True, help="Contato mestre criado ou vinculado automaticamente para este lead.")

    # ==================== Imóvel ====================
    asset_id = fields.Many2one(
        "property.asset", string="Imóvel",
        required=True, ondelete="cascade", tracking=True
    )
    interest_type = fields.Selection([
        ("rent", "Locação"),
        ("buy", "Compra"),
        ("both", "Locação ou Compra"),
    ], string="Interesse", default="rent", tracking=True)

    message = fields.Text("Mensagem", help="Mensagem livre enviada pelo interessado sobre o imóvel.")
    source_channel = fields.Selection([
        ("website_public", "Site Público"),
        ("website_portal", "Site com Login"),
        ("website_broker", "Área Restrita de Corretor"),
        ("internal", "Interno"),
    ], string="Origem", default="website_public", tracking=True)
    submitter_user_id = fields.Many2one("res.users", string="Usuário Solicitante", tracking=True)
    access_profile = fields.Char("Perfil de Acesso", tracking=True, help="Perfil de acesso do usuário no momento do envio: público, portal, corretor etc.")

    # ==================== Corretor ====================
    broker_id = fields.Many2one(
        "res.partner", string="Corretor Responsável",
        tracking=True,
        domain=[("category_id.name", "ilike", "Corretor")],
    )

    # ==================== Status ====================
    status = fields.Selection([
        ("new", "Novo"),
        ("contacted", "Contatado"),
        ("qualified", "Qualificado"),
        ("lost", "Perdido"),
    ], default="new", tracking=True, required=True)

    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, index=True
    )

    def _lead_partner_category(self):
        return self.env.ref("property_core.res_partner_category_property_prospect", raise_if_not_found=False)

    def _ensure_profile(self):
        """Cria o perfil central correto para lead/prospect sem disparar recursão.

        A versão anterior usava stakeholder_type_broker e `rec.user_id`, mas
        o model property.lead possui `submitter_user_id`. Também atribuía
        campos diretamente durante o fluxo de sincronização, o que podia
        reentrar no write em alguns cenários.
        """
        stype = self.env.ref("property_core.stakeholder_type_prospect", raise_if_not_found=False)
        for rec in self:
            if not rec.partner_id or not stype or rec.stakeholder_profile_id:
                continue

            profile = self.env["property.stakeholder.profile"].search([
                ("partner_id", "=", rec.partner_id.id),
                ("stakeholder_type_id", "=", stype.id),
            ], limit=1)

            if not profile:
                vals = {
                    "partner_id": rec.partner_id.id,
                    "stakeholder_type_id": stype.id,
                    "company_id": rec.company_id.id or rec.env.company.id,
                }
                if "user_id" in self.env["property.stakeholder.profile"]._fields and rec.submitter_user_id:
                    vals["user_id"] = rec.submitter_user_id.id
                profile = self.env["property.stakeholder.profile"].create(vals)

            rec.with_context(skip_property_lead_partner_sync=True).write({
                "stakeholder_profile_id": profile.id,
            })

    def _sync_partner(self):
        """Sincroniza o contato mestre do lead sem loop recursivo.

        O erro `maximum recursion depth exceeded` acontecia porque a versão
        anterior fazia `rec.partner_id = partner` mesmo quando o parceiro já
        era o mesmo. Essa atribuição chama `write()`, que chamava
        `_sync_partner()` novamente.
        """
        cat = self._lead_partner_category()
        Partner = self.env["res.partner"].sudo()

        for rec in self:
            vals = {"name": rec.name, "email": rec.email, "phone": rec.phone}
            vals = {key: value for key, value in vals.items() if value}

            partner = rec.partner_id
            if not partner and rec.email:
                partner = Partner.search([("email", "=", rec.email)], limit=1)

            if partner:
                partner.write(vals)
                if cat and cat not in partner.category_id:
                    partner.write({"category_id": [(4, cat.id)]})
            else:
                if cat:
                    vals["category_id"] = [(6, 0, [cat.id])]
                partner = Partner.create(vals)

            if partner and rec.partner_id.id != partner.id:
                rec.with_context(skip_property_lead_partner_sync=True).write({
                    "partner_id": partner.id,
                })

    # ==================== Actions ====================

    def action_set_contacted(self):
        self.ensure_one()
        self.status = "contacted"
        self.message_post(body=_("Lead marcado como Contatado."))

    def action_set_qualified(self):
        self.ensure_one()
        self.status = "qualified"
        self.message_post(body=_("Lead qualificado."))

    def action_set_lost(self):
        self.ensure_one()
        self.status = "lost"
        self.message_post(body=_("Lead perdido."))

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        if not self.env.context.get("skip_property_lead_partner_sync"):
            recs._sync_partner()
            recs._ensure_profile()
        return recs

    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get("skip_property_lead_partner_sync"):
            return res
        if {"name", "email", "phone", "partner_id"}.intersection(vals.keys()):
            self._sync_partner()
            self._ensure_profile()
        return res
