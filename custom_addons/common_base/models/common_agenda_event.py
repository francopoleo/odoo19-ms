# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CommonAgendaEvent(models.Model):
    """Operational agenda separated from Odoo's native meeting calendar.

    Odoo's calendar.event is intentionally a meeting/appointment object. The
    enterprise operational agenda uses this dedicated model so inspections,
    maintenance, document deadlines and governance follow-ups do not appear as
    generic "Reuniões" in the standard Calendar app.
    """

    _name = "common.agenda.event"
    _description = "Agenda Geral"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "start desc, id desc"

    name = fields.Char("Assunto", required=True, tracking=True)
    active = fields.Boolean(default=True)

    agenda_module = fields.Selection(
        [
            ("property", "Imóveis"),
            ("governance", "Governança"),
            ("document", "Documentos"),
            ("financial", "Financeiro"),
            ("other", "Outros"),
        ],
        string="Módulo de Origem",
        index=True,
        required=True,
        default="other",
        tracking=True,
    )
    agenda_type = fields.Selection(
        [
            ("inspection", "Vistoria"),
            ("maintenance", "Manutenção"),
            ("governance_case", "Caso de Governança"),
            ("governance_response_deadline", "Prazo de Resposta"),
            ("governance_resolution_deadline", "Prazo de Resolução"),
            ("governance_followup", "Follow-up de Governança"),
            ("governance_pending", "Pendência de Governança"),
            ("governance_meeting", "Compromisso de Governança"),
            ("document", "Documento"),
            ("dossier", "Dossiê"),
            ("contract", "Contrato"),
            ("rent", "Parcela / Aluguel"),
            ("rent_adjustment", "Reajuste"),
            ("contract_amendment", "Aditivo Contratual"),
            ("payment_proof", "Comprovante de Pagamento"),
            ("operational", "Operacional"),
            ("other", "Outros"),
        ],
        string="Tipo de Agenda",
        index=True,
        required=True,
        default="operational",
        tracking=True,
    )
    state = fields.Selection(
        [
            ("draft", "Rascunho"),
            ("scheduled", "Agendado"),
            ("done", "Concluído"),
            ("cancelled", "Cancelado"),
        ],
        string="Situação",
        default="scheduled",
        required=True,
        tracking=True,
    )

    start = fields.Datetime("Início", required=True, tracking=True)
    stop = fields.Datetime("Fim", required=True, tracking=True)
    duration_hours = fields.Float("Duração (h)", compute="_compute_duration_hours", store=True)
    all_day = fields.Boolean("Dia inteiro")
    location = fields.Char("Local")
    description = fields.Html("Descrição / Observações")

    user_id = fields.Many2one(
        "res.users",
        string="Responsável Principal",
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
    )
    responsible_user_ids = fields.Many2many(
        "res.users",
        "common_agenda_event_responsible_rel",
        "event_id",
        "user_id",
        string="Responsáveis / Equipe",
        tracking=True,
    )
    partner_ids = fields.Many2many(
        "res.partner",
        "common_agenda_event_partner_rel",
        "event_id",
        "partner_id",
        string="Participantes / Contatos",
    )

    visibility = fields.Selection(
        [
            ("restricted", "Somente responsáveis/participantes"),
            ("custom", "Responsáveis + usuários adicionais"),
            ("internal", "Todos os usuários internos"),
        ],
        string="Quem pode visualizar",
        default="restricted",
        required=True,
        tracking=True,
    )
    visible_user_ids = fields.Many2many(
        "res.users",
        "common_agenda_event_visible_user_rel",
        "event_id",
        "user_id",
        string="Usuários adicionais com acesso",
    )

    source_model = fields.Char("Modelo de Origem", index=True, copy=False)
    source_res_id = fields.Integer("ID de Origem", index=True, copy=False)
    source_key = fields.Char(
        "Chave de Origem",
        index=True,
        copy=False,
        help="Identificador técnico do marco dentro do registro de origem. Ex.: response_deadline, resolution_deadline, followup.",
    )
    source_name = fields.Char("Registro de Origem", copy=False)
    source_ref = fields.Reference(
        selection="_selection_source_ref",
        string="Registro Vinculado",
        compute="_compute_source_ref",
    )
    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.company)

    color = fields.Integer("Cor", compute="_compute_color", store=True)

    @api.depends("start", "stop")
    def _compute_duration_hours(self):
        for rec in self:
            if rec.start and rec.stop:
                rec.duration_hours = max((rec.stop - rec.start).total_seconds() / 3600.0, 0.0)
            else:
                rec.duration_hours = 0.0

    @api.depends("agenda_module", "agenda_type")
    def _compute_color(self):
        module_color = {
            "property": 2,
            "governance": 4,
            "document": 6,
            "financial": 9,
            "other": 0,
        }
        type_color = {
            "inspection": 10,
            "maintenance": 3,
            "governance_response_deadline": 1,
            "governance_resolution_deadline": 4,
            "governance_followup": 8,
            "governance_pending": 1,
            "governance_meeting": 7,
            "document": 6,
            "dossier": 5,
            "rent": 9,
        }
        for rec in self:
            rec.color = type_color.get(rec.agenda_type) or module_color.get(rec.agenda_module, 0)

    @api.model
    def _selection_source_ref(self):
        return [(model, model) for model in self.env]

    def _compute_source_ref(self):
        for rec in self:
            rec.source_ref = False
            if rec.source_model and rec.source_res_id and rec.source_model in self.env:
                target = self.env[rec.source_model].browse(rec.source_res_id).exists()
                if target:
                    rec.source_ref = "%s,%s" % (rec.source_model, rec.source_res_id)

    @api.model
    def _agenda_user_is_manager(self):
        return (
            self.env.su
            or self.env.user.has_group("base.group_system")
            or self.env.user.has_group("common_base.group_common_agenda_manager")
        )

    @api.model
    def _default_access_domain(self):
        if self._agenda_user_is_manager():
            return []
        uid = self.env.user.id
        return [
            "|",
                ("visibility", "=", "internal"),
                "|",
                    ("user_id", "=", uid),
                    "|",
                        ("create_uid", "=", uid),
                        "|",
                            ("responsible_user_ids", "in", [uid]),
                            ("visible_user_ids", "in", [uid]),
        ]

    def action_open_source(self):
        self.ensure_one()
        if not self.source_model or not self.source_res_id:
            raise UserError(_("Este item da agenda não possui registro de origem."))
        if self.source_model not in self.env:
            raise UserError(_("O modelo de origem %s não está disponível.") % self.source_model)
        record = self.env[self.source_model].browse(self.source_res_id).exists()
        if not record:
            raise UserError(_("O registro de origem não existe mais."))
        return {
            "type": "ir.actions.act_window",
            "name": record.display_name,
            "res_model": self.source_model,
            "res_id": record.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_mark_done(self):
        self.write({"state": "done"})
        return True

    def action_cancel(self):
        self.write({"state": "cancelled"})
        return True

    def action_archive(self):
        """Cancel and archive without physically deleting the agenda history."""
        self.write({"state": "cancelled", "active": False})
        return True

    def action_set_scheduled(self):
        self.write({"state": "scheduled", "active": True})
        return True

    def unlink(self):
        """Allow hard delete only to Agenda Geral/System administrators.

        Operational users should cancel/archive agenda items to preserve an
        audit trail. This method gives a clear message when a user tries to
        delete from a place where ACLs allow it in the future.
        """
        if not self._agenda_user_is_manager():
            raise UserError(_("Somente Administradores da Agenda Geral podem excluir definitivamente. Use Cancelar/Arquivar para remover o item da agenda mantendo o histórico."))
        return super().unlink()


    @api.model
    def cleanup_legacy_agenda_rules(self):
        """Disable record rules left by older test versions.

        Previous builds temporarily added rules on mail.activity/calendar.event
        using fields such as agenda_is_erp and agenda_type. The final design uses
        common.agenda.event, so those rules must be disabled before the webclient
        queries mail.activity/calendar.event.
        """
        Rule = self.env["ir.rule"].sudo()
        legacy_rules = Rule.search([
            "|", "|",
            ("domain_force", "ilike", "agenda_is_erp"),
            ("domain_force", "ilike", "agenda_type"),
            ("name", "ilike", "atividades ERP"),
        ])
        legacy_rules = legacy_rules.filtered(
            lambda r: r.model_id.model in ("mail.activity", "calendar.event")
        )
        if legacy_rules:
            legacy_rules.write({"active": False, "domain_force": "[(1, '=', 1)]"})
        return True

    @api.model
    def backfill_from_old_calendar_events(self):
        """Best-effort migration from earlier versions that created calendar.event.

        It uses raw SQL because the new version intentionally does not depend on
        custom ORM fields on calendar.event. This keeps normal Calendar clean
        while preserving existing operational dates when those columns still
        exist in the database from a previous test version.
        """
        cr = self.env.cr
        cr.execute("""
            SELECT column_name
              FROM information_schema.columns
             WHERE table_name = 'calendar_event'
               AND column_name IN (
                   'agenda_module','agenda_type','agenda_source_model',
                   'agenda_source_res_id','agenda_source_name','agenda_visibility'
               )
        """)
        cols = {row[0] for row in cr.fetchall()}
        required = {'agenda_module', 'agenda_type', 'agenda_source_model', 'agenda_source_res_id'}
        if not required.issubset(cols):
            return True
        cr.execute("""
            SELECT id, name, start, stop, user_id, location, description,
                   agenda_module, agenda_type, agenda_source_model,
                   agenda_source_res_id, agenda_source_name,
                   COALESCE(agenda_visibility, 'restricted')
              FROM calendar_event
             WHERE agenda_type IS NOT NULL
        """)
        for row in cr.fetchall():
            (
                old_id, name, start, stop, user_id, location, description,
                module, agenda_type, source_model, source_res_id, source_name,
                visibility,
            ) = row
            existing = self.sudo().search([
                ("source_model", "=", source_model),
                ("source_res_id", "=", source_res_id),
                ("agenda_type", "=", agenda_type),
            ], limit=1)
            vals = {
                "name": name or source_name or _("Agenda Geral"),
                "start": start,
                "stop": stop or start,
                "user_id": user_id or self.env.user.id,
                "location": location,
                "description": description,
                "agenda_module": module or "other",
                "agenda_type": agenda_type or "operational",
                "source_model": source_model,
                "source_res_id": source_res_id,
                "source_name": source_name,
                "visibility": visibility or "restricted",
            }
            if start and (existing or vals.get("stop")):
                if existing:
                    existing.write(vals)
                else:
                    self.sudo().create(vals)
        return True
