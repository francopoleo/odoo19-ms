import base64

from odoo import fields, models, _
from odoo.exceptions import UserError


class CondominiumReturnWizard(models.TransientModel):
    _name = "property.condominium.return.wizard"
    _description = "Importação de Retorno do Condomínio"

    data_file = fields.Binary("Arquivo de Retorno", required=True)
    filename = fields.Char("Nome do Arquivo")

    def action_import_return(self):
        self.ensure_one()
        if not self.data_file:
            raise UserError(_("Selecione um arquivo de retorno."))
        content = base64.b64decode(self.data_file)
        matched = self.env["property.condominium.cnab.service"].import_return(content)
        return {"type": "ir.actions.act_window_close"}
