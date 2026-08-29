# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DossierAssignWizard(models.TransientModel):
    _name = "dossier.assign.wizard"
    _description = "Atribuir Dossiê ao Registro"

    target_model = fields.Char("Modelo", required=True, readonly=True)
    target_id = fields.Integer("ID do Registro", required=True, readonly=True)
    target_name = fields.Char("Registro", readonly=True)

    mode = fields.Selection(
        [("create", "Criar novo dossiê"), ("select", "Selecionar dossiê existente")],
        string="Operação",
        required=True,
        default="create",
    )
    dossier_id = fields.Many2one("dossier.dossier", string="Dossiê Existente")
    process_id = fields.Many2one("dossier.process", string="Tipo de Processo")
    template_id = fields.Many2one("document.dossier.template", string="Template Específico")
    name = fields.Char("Nome do Dossiê")
    description = fields.Text("Descrição")
    responsible_id = fields.Many2one("res.users", string="Responsável", default=lambda self: self.env.user)

    include_existing_documents = fields.Boolean(
        "Incluir documentos já vinculados ao registro",
        default=True,
        help="Inclui documentos individuais já cadastrados no contexto do imóvel, contrato ou caso.",
    )
    include_related_documents = fields.Boolean(
        "Incluir documentos de registros relacionados",
        default=False,
        help="Ex.: no contrato, também considerar documentos do imóvel; no imóvel, considerar documentos dos contratos; na governança, considerar imóveis/contratos relacionados.",
    )
    create_template_documents = fields.Boolean(
        "Criar documentos esperados pelo template",
        default=True,
    )
    create_only_missing = fields.Boolean(
        "Criar somente itens faltantes",
        default=True,
    )

    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        target_model = vals.get("target_model") or self.env.context.get("default_target_model") or self.env.context.get("active_model")
        target_id = vals.get("target_id") or self.env.context.get("default_target_id") or self.env.context.get("active_id")
        if target_model and target_id:
            try:
                TargetModel = self.env[target_model]
            except KeyError:
                TargetModel = False
            target = TargetModel and TargetModel.browse(target_id).exists()
            if target:
                vals.setdefault("target_model", target_model)
                vals.setdefault("target_id", target.id)
                vals.setdefault("target_name", target.display_name)
                vals.setdefault("name", self._default_dossier_name(target_model, target))
                vals.setdefault("description", self._default_description(target_model, target))
                vals.setdefault("process_id", self._default_process_id(target_model, target))
                vals.setdefault("responsible_id", self._default_responsible_id(target))
        return vals

    @api.model
    def _default_dossier_name(self, target_model, target):
        if target_model == "property.asset":
            return _("Dossiê do Imóvel - %s") % target.display_name
        if target_model == "property.contract":
            return _("Dossiê do Contrato - %s") % target.display_name
        if target_model == "governance.case":
            return _("Dossiê de Governança - %s") % target.display_name
        return _("Dossiê - %s") % target.display_name

    @api.model
    def _default_description(self, target_model, target):
        if target_model == "property.asset":
            return _("Dossiê documental vinculado ao imóvel %s.") % target.display_name
        if target_model == "property.contract":
            asset = getattr(target, "asset_id", False)
            if asset:
                return _("Dossiê documental vinculado ao contrato %s e ao imóvel %s.") % (target.display_name, asset.display_name)
            return _("Dossiê documental vinculado ao contrato %s.") % target.display_name
        if target_model == "governance.case":
            return getattr(target, "description", False) or _("Dossiê documental vinculado ao caso de governança %s.") % target.display_name
        return False

    @api.model
    def _default_process_id(self, target_model, target):
        xmlid = self.env.context.get("default_process_xmlid")
        if xmlid:
            process = self.env.ref(xmlid, raise_if_not_found=False)
            if process:
                return process.id
        if target_model == "property.contract":
            process = self.env.ref("document_dossier.process_property_lease", raise_if_not_found=False)
        elif target_model == "property.asset":
            process = self.env.ref("document_dossier.process_property_lease", raise_if_not_found=False)
        elif target_model == "governance.case":
            process = self.env.ref("document_dossier.process_governance_audit", raise_if_not_found=False)
        else:
            process = self.env.ref("document_dossier.process_generic_default", raise_if_not_found=False)
        return process.id if process else False

    @api.model
    def _default_responsible_id(self, target):
        if "responsible_id" in target._fields and target.responsible_id:
            return target.responsible_id.id
        return self.env.user.id

    @api.onchange("process_id")
    def _onchange_process_id(self):
        if self.process_id and self.process_id.template_ids and not self.template_id:
            self.template_id = self.process_id.template_ids[:1]

    def _get_target_record(self):
        self.ensure_one()
        if not self.target_model or not self.target_id:
            raise ValidationError(_("Registro de origem inválido para atribuir dossiê."))
        try:
            TargetModel = self.env[self.target_model]
        except KeyError:
            raise ValidationError(_("Modelo de origem inválido para atribuir dossiê."))
        record = TargetModel.browse(self.target_id).exists()
        if not record:
            raise ValidationError(_("O registro de origem não existe mais."))
        return record

    def _create_or_select_dossier(self):
        self.ensure_one()
        target = self._get_target_record()
        if self.mode == "select":
            if not self.dossier_id:
                raise ValidationError(_("Selecione o dossiê existente."))
            dossier = self.dossier_id
            dossier.write({
                "target_model": self.target_model,
                "target_res_id": self.target_id,
                "target_name": self.target_name or target.display_name,
            })
            return dossier

        if not self.process_id:
            raise ValidationError(_("Informe o tipo de processo do dossiê."))
        if not (self.name or "").strip():
            raise ValidationError(_("Informe o nome do dossiê."))

        return self.env["dossier.dossier"].create({
            "name": self.name.strip(),
            "description": self.description,
            "process_id": self.process_id.id,
            "responsible_id": self.responsible_id.id if self.responsible_id else False,
            "target_model": self.target_model,
            "target_res_id": self.target_id,
            "target_name": self.target_name or target.display_name,
        })

    def _link_dossier_to_target(self, dossier):
        self.ensure_one()
        target = self._get_target_record()
        if self.target_model in ("property.contract", "governance.case") and "dossier_id" in target._fields:
            target.write({"dossier_id": dossier.id})
        elif self.target_model == "property.asset" and "dossier_ids" in target._fields:
            target.write({"dossier_ids": [(4, dossier.id)]})
        return target

    def action_assign_dossier(self):
        self.ensure_one()
        dossier = self._create_or_select_dossier()
        self._link_dossier_to_target(dossier)

        if self.include_existing_documents:
            dossier._link_existing_documents_from_target(include_related=self.include_related_documents)

        if self.create_template_documents:
            templates = self.template_id if self.template_id else dossier.process_id.template_ids
            dossier.apply_templates(templates=templates, create_only_missing=self.create_only_missing)

        return {
            "type": "ir.actions.act_window",
            "name": dossier.name,
            "res_model": "dossier.dossier",
            "res_id": dossier.id,
            "view_mode": "form",
            "target": "current",
        }
