from odoo import fields, models


class DocumentLocation(models.Model):
    _name = "document.location"
    _description = "Localização Física de Documento"
    _order = "sequence, name"
    _rec_name = "display_name"

    name = fields.Char("Local / Arquivo", required=True)
    code = fields.Char("Código")
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.company, index=True)
    site_name = fields.Char("Unidade / Escritório")
    room = fields.Char("Sala")
    cabinet = fields.Char("Armário")
    shelf = fields.Char("Estante / Prateleira")
    drawer = fields.Char("Gaveta")
    box = fields.Char("Caixa")
    folder = fields.Char("Pasta")
    responsible_id = fields.Many2one("res.users", string="Responsável")
    notes = fields.Text("Observações")
    active = fields.Boolean(default=True)
    display_name = fields.Char(compute="_compute_display_name", store=False)

    def _compute_display_name(self):
        for rec in self:
            parts = [rec.name, rec.site_name, rec.room, rec.cabinet, rec.shelf, rec.box, rec.folder]
            rec.display_name = " / ".join([p for p in parts if p])
