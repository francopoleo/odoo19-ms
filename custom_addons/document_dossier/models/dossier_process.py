# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DossierProcess(models.Model):
    _name = "dossier.process"
    _description = "Definição de Tipo de Processo/Fluxo para Dossiês"
    _order = "sequence asc, name asc"

    name = fields.Char(string="Nome do Processo", required=True, translate=True)
    description = fields.Text(string="Descrição", translate=True)

    # Domain association: governance, property_core, etc.
    domain = fields.Selection(
        selection=[
            ("governance", "Governança"),
            ("property", "Imóvel"),
            ("hr", "Recursos Humanos"),
            ("generic", "Genérico/Outro"),
        ],
        string="Domínio",
        required=True,
        default="generic",
    )

    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(default=True)

    # Many2Many relationship with document templates
    template_ids = fields.Many2many(
        comodel_name="document.dossier.template",
        relation="dossier_process_template_rel",
        column1="process_id",
        column2="template_id",
        string="Templates de Documentos",
    )

    # Computed: how many templates are in this process
    template_count = fields.Integer(
        string="Qtd. Templates",
        compute="_compute_template_count",
        store=True,
    )

    # Computed: how many dossiés use this process
    dossier_count = fields.Integer(
        string="Qtd. Dossiês",
        compute="_compute_dossier_count",
        store=True,
    )

    @api.depends("template_ids")
    def _compute_template_count(self):
        for record in self:
            record.template_count = len(record.template_ids)

    @api.depends("dossier_count")
    def _compute_dossier_count(self):
        DossierModel = self.env["dossier.dossier"]
        for record in self:
            record.dossier_count = DossierModel.search_count([("process_id", "=", record.id)])

    # ── View Actions ──────────────────────────────────────────────────
    def action_view_dossiérs(self):
        """Open all dossiérs using this process"""
        return {
            "type": "ir.actions.act_window",
            "name": _("Dossiérs using %s") % self.name,
            "res_model": "dossier.dossier",
            "view_mode": "kanban,list,form",
            "domain": [("process_id", "=", self.id)],
        }
