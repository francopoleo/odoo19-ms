from odoo import api, fields, models


class CommonMixin(models.AbstractModel):
    """
    Mixin com campos e métodos comuns para todos os modelos do ERP.
    Use: _inherit = ['common.mixin']
    """
    _name = "common.mixin"
    _description = "Mixin com campos comuns"

    # ========== CAMPOS DE ATIVIDADE ==========
    active = fields.Boolean(
        string="Ativo",
        default=True,
        help="Desative para arquivar o registro sem excluí-lo"
    )

    # ========== CAMPOS DE EMPRESA ==========
    _check_company_auto = True

    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        default=lambda self: self.env.company,
        required=True,
        index=True,
        help="Empresa à qual este registro pertence"
    )

    # ========== CAMPOS DE CLASSIFICAÇÃO ==========
    tag_ids = fields.Many2many(
        "common.tag",
        string="Tags",
        help="Tags para classificação e busca"
    )

    # ========== CAMPOS DE AUDITORIA (já existem no Odoo, mas reforçamos) ==========
    # create_uid, create_date, write_uid, write_date já são automáticos

    # ========== MÉTODOS DE UTILIDADE ==========
    @api.model
    def _get_default_company(self):
        """Retorna a empresa padrão do usuário atual"""
        return self.env.company

    def action_archive(self):
        """Arquiva o registro"""
        self.active = False

    def action_unarchive(self):
        """Desarquiva o registro"""
        self.active = True

    def action_open_attachments(self):
        """Abre os anexos do registro"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Anexos",
            "res_model": "ir.attachment",
            "view_mode": "tree,form",
            "domain": [("res_model", "=", self._name), ("res_id", "=", self.id)],
            "context": {"default_res_model": self._name, "default_res_id": self.id},
        }