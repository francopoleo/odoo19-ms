from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date


class PropertyInspection(models.Model):
    _name = "property.inspection"
    _description = "Vistoria de Imóvel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc"
    _rec_name = "name"

    # ==================== Identificação ====================
    name = fields.Char("Título", compute="_compute_name", store=True)
    reference = fields.Char("Referência", readonly=True, copy=False, default="New")

    inspection_type = fields.Selection([
        ("entry", "Entrada"),
        ("exit", "Saída"),
        ("periodic", "Periódica"),
        ("emergency", "Emergência"),
    ], string="Tipo de Vistoria", required=True, default="periodic", tracking=True)

    # ==================== Vínculos ====================
    asset_id = fields.Many2one(
        "property.asset", string="Imóvel",
        required=True, ondelete="cascade", tracking=True
    )
    contract_id = fields.Many2one(
        "property.contract", string="Contrato",
        ondelete="set null", tracking=True
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        store=True,
        index=True,
    )

    # ==================== Datas ====================
    scheduled_date = fields.Date("Data Agendada", tracking=True)
    date = fields.Date("Data de Realização", tracking=True)

    # ==================== Responsáveis ====================
    inspector_id = fields.Many2one(
        "res.partner", string="Vistoriador", tracking=True
    )
    present_ids = fields.Many2many(
        "res.partner",
        relation="property_inspection_present_rel",
        column1="inspection_id",
        column2="partner_id",
        string="Presentes",
    )

    # ==================== Resultado ====================
    overall_condition = fields.Selection([
        ("excellent", "Excelente"),
        ("good", "Bom"),
        ("fair", "Regular"),
        ("poor", "Ruim"),
    ], string="Condição Geral", tracking=True)

    report = fields.Html(
        "Laudo", help="Descrição detalhada das condições encontradas"
    )
    observations = fields.Text("Observações Gerais")

    # ==================== Arquivos ====================
    attachment_ids = fields.Many2many(
        "ir.attachment",
        relation="property_inspection_attachment_rel",
        column1="inspection_id",
        column2="attachment_id",
        string="Fotos / Arquivos",
    )
    attachment_count = fields.Integer(
        "Arquivos", compute="_compute_attachment_count"
    )

    media_ids = fields.One2many(
        "property.media",
        "inspection_id",
        string="Mídias",
    )
    media_count = fields.Integer(
        "Qtd. Mídias", compute="_compute_media_count"
    )

    # ==================== Status ====================
    status = fields.Selection([
        ("draft", "Rascunho"),
        ("scheduled", "Agendada"),
        ("done", "Concluída"),
        ("cancelled", "Cancelada"),
    ], default="draft", tracking=True, required=True)

    # ==================== Computed ====================

    @api.depends("inspection_type", "asset_id", "scheduled_date", "date")
    def _compute_name(self):
        type_labels = {
            "entry": "Entrada",
            "exit": "Saída",
            "periodic": "Periódica",
            "emergency": "Emergência",
        }
        for insp in self:
            ref_date = insp.date or insp.scheduled_date
            label = type_labels.get(insp.inspection_type, "Vistoria")
            if ref_date:
                insp.name = "Vistoria %s – %s (%s)" % (
                    label, insp.asset_id.name or "", ref_date.strftime("%m/%Y")
                )
            else:
                insp.name = "Vistoria %s – %s" % (label, insp.asset_id.name or "")

    @api.depends("attachment_ids")
    def _compute_attachment_count(self):
        for insp in self:
            insp.attachment_count = len(insp.attachment_ids)

    @api.depends("media_ids")
    def _compute_media_count(self):
        for insp in self:
            insp.media_count = len(insp.media_ids)

    # ==================== Actions ====================

    def action_schedule(self):
        self.ensure_one()
        if self.status != "draft":
            raise UserError(_("Apenas vistorias em Rascunho podem ser agendadas."))
        if not self.scheduled_date:
            raise UserError(_("Informe a data agendada antes de confirmar."))
        self.status = "scheduled"
        self.message_post(body=_("Vistoria agendada para %s.") % self.scheduled_date)

    def action_done(self):
        self.ensure_one()
        if self.status not in ("draft", "scheduled"):
            raise UserError(_("Esta vistoria não pode ser concluída."))
        if not self.date:
            self.date = date.today()
        self.status = "done"
        self.message_post(body=_("Vistoria concluída em %s.") % self.date)

    def action_cancel(self):
        self.ensure_one()
        self.status = "cancelled"
        self.message_post(body=_("Vistoria cancelada."))

    def action_reset_draft(self):
        self.ensure_one()
        self.status = "draft"


    def action_view_media(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Mídias"),
            "res_model": "property.media",
            "view_mode": "list,form",
            "domain": [("inspection_id", "=", self.id)],
            "context": {
                "default_inspection_id": self.id,
                "default_asset_id": self.asset_id.id,
                "default_purpose": "inspection",
                "default_context_selection": "inspection",
                "default_upload_kind": self.env.context.get("default_upload_kind", "auto"),
            },
        }

    def action_open_bulk_media_wizard(self):
        """Open bulk media upload wizard for this inspection."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Adicionar Múltiplas Mídias"),
            "res_model": "property.media.bulk.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_inspection_id": self.id,
                "default_asset_id": self.asset_id.id,
                "default_context_selection": "inspection",
                "default_purpose": "inspection",
                "default_upload_kind": self.env.context.get("default_upload_kind", "auto"),
            },
        }

    # ==================== ORM ====================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["common.sequence"].sudo().next_by_code("property.inspection") or "New"
                )
        return super().create(vals_list)