# -*- coding: utf-8 -*-
import logging
from email.utils import parseaddr

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class GovernanceEmailChannel(models.Model):
    _name = "governance.email.channel"
    _description = "Canal de E-mail de Governança"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(string="Nome", required=True, tracking=True)
    sequence = fields.Integer(string="Sequência", default=10)
    active = fields.Boolean(string="Ativo", default=True, tracking=True)

    company_id = fields.Many2one(
        "res.company",
        string="Empresa",
        default=lambda self: self.env.company,
        required=True,
        index=True,
        tracking=True,
        help="Empresa dona da caixa/canal. Em multiempresa, prefira um canal por empresa quando o processo for segregado.",
    )

    alias_name = fields.Char(
        string="Alias / Caixa",
        required=True,
        tracking=True,
        help="Informe somente a parte antes do @. Ex.: governance, juridico, documental.",
    )
    alias_id = fields.Many2one("mail.alias", string="Alias Técnico", readonly=True, copy=False)
    alias_email = fields.Char(string="E-mail Esperado", compute="_compute_alias_email", readonly=True)

    case_type_id = fields.Many2one(
        "governance.case.type",
        string="Tipo de Caso Padrão",
        required=True,
        tracking=True,
        help="Tipo aplicado aos casos criados por este canal quando a classificação automática estiver ativa.",
    )
    allowed_case_type_ids = fields.Many2many(
        "governance.case.type",
        "governance_email_channel_case_type_rel",
        "channel_id",
        "case_type_id",
        string="Tipos de Caso Permitidos",
        help="Se preenchido, casos originados neste canal só poderão usar estes tipos. Deixe vazio para permitir todos.",
    )
    auto_assign_type = fields.Boolean(
        string="Aplicar Tipo Automaticamente",
        default=True,
        tracking=True,
        help="Quando marcado, o e-mail novo recebe o tipo padrão do canal.",
    )
    requires_triage = fields.Boolean(
        string="Exige Triagem",
        default=False,
        tracking=True,
        help="Use em caixas gerais, como governance@, para indicar que o caso precisa ser classificado antes do fluxo definitivo.",
    )

    priority = fields.Selection(
        [("0", "Baixo"), ("1", "Médio"), ("2", "Alto"), ("3", "Crítico")],
        string="Prioridade de Entrada",
        default="1",
        tracking=True,
        help="Prioridade inicial sugerida para e-mails recebidos por este canal. O SLA continua vindo do tipo/regra do caso.",
    )
    responsible_id = fields.Many2one(
        "res.users",
        string="Responsável de Triagem",
        tracking=True,
        help="Responsável inicial pela triagem. Regras permanentes devem ficar no Tipo de Caso.",
    )

    create_case_from_email = fields.Boolean(string="Criar caso para e-mail novo", default=True, tracking=True)
    update_existing_case = fields.Boolean(string="Atualizar caso existente por resposta", default=True, tracking=True)
    auto_add_sender_as_participant = fields.Boolean(string="Adicionar remetente como participante", default=True, tracking=True)
    require_response_by_default = fields.Boolean(string="Entrada exige resposta por padrão", default=True, tracking=True)
    notes = fields.Html(string="Instruções do Canal")

    # Identidade Institucional de Saída
    institutional_email_from = fields.Char(
        string="Remetente Institucional",
        tracking=True,
        help="Remetente usado em e-mails de saída deste canal. Ex.: 'Governança XPTO <governance@xpto.com.br>'.",
    )
    institutional_reply_to = fields.Char(
        string="Responder Para Institucional",
        tracking=True,
        help="Endereço reply-to em e-mails de saída. Deixe vazio para usar o Remetente Institucional.",
    )
    force_institutional_identity = fields.Boolean(
        string="Forçar Identidade Institucional",
        default=False,
        tracking=True,
        help="Se marcado, e-mails de saída de casos deste canal usarão sempre o Remetente e Reply-To institucionais.",
    )
    domain_alias = fields.Char(
        string="Domínio de Alias Customizado",
        tracking=True,
        help="Domínio customizado para este canal. Ex.: 'governance.xpto.com.br'. Deixe vazio para usar o domínio global (mail.catchall.domain).",
    )
    auto_import_attachments = fields.Boolean(
        string="Importar Anexos Automaticamente",
        default=True,
        tracking=True,
        help="Quando marcado, anexos de e-mails recebidos serão automaticamente importados como documentos de governança.",
    )

    _alias_name_company_unique = models.Constraint(
        'UNIQUE(alias_name, company_id)',
        'Já existe um canal com este alias para esta empresa.',
    )

    @api.depends("alias_name", "domain_alias")
    def _compute_alias_email(self):
        global_domain = self.env["ir.config_parameter"].sudo().get_param("mail.catchall.domain")
        for rec in self:
            domain = rec.domain_alias or global_domain
            rec.alias_email = "%s@%s" % (rec.alias_name, domain) if rec.alias_name and domain else (rec.alias_name or False)

    @api.constrains("alias_name")
    def _check_alias_name(self):
        for rec in self:
            if rec.alias_name and "@" in rec.alias_name:
                raise ValidationError(_("Informe somente a parte antes do @ no alias."))

    @api.constrains("case_type_id", "allowed_case_type_ids")
    def _check_default_type_allowed(self):
        for rec in self:
            if rec.case_type_id and rec.allowed_case_type_ids and rec.case_type_id not in rec.allowed_case_type_ids:
                raise ValidationError(_("O Tipo de Caso Padrão precisa estar entre os Tipos de Caso Permitidos do canal."))

    @api.constrains("company_id", "case_type_id", "allowed_case_type_ids", "responsible_id")
    def _check_company_consistency(self):
        for rec in self:
            company = rec.company_id
            if not company:
                continue
            case_types = rec.case_type_id | rec.allowed_case_type_ids
            # governance.case.type ganhou company_id opcional nesta implementação.
            invalid_types = case_types.filtered(lambda t: "company_id" in t._fields and t.company_id and t.company_id != company)
            if invalid_types:
                raise ValidationError(_("Os tipos de caso do canal precisam ser globais ou pertencer à mesma empresa do canal."))
            if rec.responsible_id and rec.responsible_id.company_ids and company not in rec.responsible_id.company_ids:
                raise ValidationError(_("O responsável de triagem precisa ter acesso à empresa do canal."))

    @api.model_create_multi
    def create(self, vals_list):
        """Criar canal e seu alias técnico automaticamente."""
        records = super().create(vals_list)
        # Criar alias para cada canal novo
        for rec in records.filtered(lambda r: r.active and not r.alias_id):
            try:
                rec.action_create_or_update_alias()
            except Exception as e:
                _logger.warning(f"Falha ao criar alias para canal {rec.name}: {e}")
        return records

    def write(self, vals):
        """Atualizar alias técnico se nome ou status mudar."""
        result = super().write(vals)
        # Atualizar/criar alias se o canal foi ativado ou nome mudou
        if any(k in vals for k in ['alias_name', 'active']):
            for rec in self.filtered(lambda r: r.active):
                try:
                    rec.action_create_or_update_alias()
                except Exception as e:
                    _logger.warning(f"Falha ao atualizar alias para canal {rec.name}: {e}")
        return result

    def _prepare_case_defaults(self):
        """Valores iniciais para caso criado pelo canal.

        O canal é só porta de entrada. Fluxo, SLA, checklist e etapas continuam
        pertencendo ao governance.case.type.
        """
        self.ensure_one()
        vals = {
            "message_origin": "email",
            "email_channel_id": self.id,
            "requires_triage": self.requires_triage,
        }
        if self.company_id:
            vals["company_id"] = self.company_id.id
        if self.auto_assign_type and self.case_type_id:
            vals["case_type_id"] = self.case_type_id.id
        if self.priority:
            vals["priority"] = self.priority
        if self.responsible_id:
            vals["responsible_id"] = self.responsible_id.id
        return vals

    def _get_alias_defaults(self):
        self.ensure_one()
        return self._prepare_case_defaults()

    def action_create_or_update_alias(self):
        Alias = self.env["mail.alias"].sudo()
        model = self.env["ir.model"]._get("governance.case")
        for rec in self:
            vals = {
                "alias_name": rec.alias_name,
                "alias_model_id": model.id,
                "alias_defaults": repr(rec._get_alias_defaults()),
            }
            if "alias_contact" in Alias._fields:
                vals["alias_contact"] = "everyone"
            if "alias_user_id" in Alias._fields and rec.responsible_id:
                vals["alias_user_id"] = rec.responsible_id.id
            if rec.alias_id:
                rec.alias_id.write(vals)
            else:
                rec.alias_id = Alias.create(vals).id
        return True

    def action_open_alias(self):
        self.ensure_one()
        if not self.alias_id:
            raise UserError(_("Crie o alias técnico antes de abrir."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Alias Técnico"),
            "res_model": "mail.alias",
            "view_mode": "form",
            "res_id": self.alias_id.id,
            "target": "current",
        }

    def action_open_case_type(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Tipo de Caso"),
            "res_model": "governance.case.type",
            "view_mode": "form",
            "res_id": self.case_type_id.id,
            "target": "current",
        }

    def action_open_cases(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Casos do Canal — %s") % self.name,
            "res_model": "governance.case",
            "view_mode": "list,kanban,form",
            "domain": [("email_channel_id", "=", self.id)],
            "context": {
                "default_email_channel_id": self.id,
                "default_case_type_id": self.case_type_id.id,
                "default_priority": self.priority,
                "default_company_id": self.company_id.id,
                "default_responsible_id": self.responsible_id.id,
                "default_requires_triage": self.requires_triage,
            },
        }

    @api.model
    def _find_by_message_recipients(self, msg_dict):
        recipients = ",".join([
            msg_dict.get("to") or "",
            msg_dict.get("cc") or "",
            msg_dict.get("email_to") or "",
        ])
        aliases = []
        for part in recipients.split(","):
            _name, email = parseaddr(part.strip())
            if email and "@" in email:
                aliases.append(email.lower().split("@")[0])
        if not aliases:
            return self.browse()
        return self.search([("active", "=", True), ("alias_name", "in", aliases)], limit=1)
