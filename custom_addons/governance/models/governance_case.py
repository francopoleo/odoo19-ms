from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, timedelta


class GovernanceCase(models.Model):
    _name = "governance.case"
    _description = "Caso de Governança"
    _inherit = ["mail.thread", "mail.activity.mixin", "common.mixin"]
    _order = "create_date desc"
    _rec_name = "name"

    name = fields.Char(string="Assunto", required=True, tracking=True)
    reference = fields.Char(string="Referência", default="New", readonly=True, copy=False)
    description = fields.Html(string="Descrição", tracking=True)

    origin_date = fields.Date(string="Data de Origem", default=fields.Date.today, tracking=True)
    response_deadline = fields.Date(string="Prazo para Resposta", compute="_compute_response_deadline", store=True)
    response_date = fields.Date(string="Data de Resposta", tracking=True)

    stage_id = fields.Many2one(
        "governance.stage", string="Etapa", tracking=True,
        group_expand="_read_group_stage_ids",
        default=lambda self: self.env.ref("governance.stage_planned", raise_if_not_found=False),
    )
    status = fields.Selection(related="stage_id.status", string="Status", store=True)

    tag_ids = fields.Many2many(
        "common.tag", string="Tags",
        domain=[("category", "=", "governance")],
        context={"default_category": "governance"},
    )

    case_type_id = fields.Many2one(
        "governance.case.type", string="Tipo", tracking=True,
        default=lambda self: self.env["governance.case.type"].search([("name", "=", "Operacional")], limit=1),
    )

    case_type_color = fields.Integer(string="Cor do Tipo", compute="_compute_type_stage_colors", store=True)
    stage_color = fields.Integer(string="Cor da Etapa", compute="_compute_type_stage_colors", store=True)

    priority = fields.Selection([
        ("0", "Baixo"),
        ("1", "Médio"),
        ("2", "Alto"),
        ("3", "Crítico"),
    ], string="Prioridade", default="1", tracking=True)

    type_sla_days = fields.Integer(string="SLA do Tipo", compute="_compute_type_settings", store=True)
    require_primary_participant = fields.Boolean(string="Exige Contato Principal", compute="_compute_type_settings", store=True)
    auto_followup_days = fields.Integer(string="Follow-up Automático (dias)", compute="_compute_type_settings", store=True)
    auto_create_followup_activity = fields.Boolean(string="Criar Atividade Automática", compute="_compute_type_settings", store=True)

    sla_days = fields.Integer(string="SLA (dias)", compute="_compute_sla_days", store=True)
    resolution_deadline = fields.Date(string="Prazo de Resolução", compute="_compute_resolution_deadline", store=True)

    responsible_id = fields.Many2one("res.users", string="Responsável", tracking=True)
    partner_ids = fields.Many2many("res.partner", string="Envolvidos")
    participant_ids = fields.One2many("governance.case.participant", "case_id", string="Participantes")
    communication_ids = fields.One2many("governance.case.communication", "case_id", string="Comunicações")
    pending_ids = fields.One2many("governance.case.pending", "case_id", string="Pendências")
    response_ids = fields.One2many("governance.case.response", "case_id", string="Respostas")
    participant_count = fields.Integer(string="Qtd Participantes", compute="_compute_participant_count")
    communication_count = fields.Integer(string="Qtd Comunicações", compute="_compute_operational_counts")
    pending_count = fields.Integer(string="Qtd Pendências", compute="_compute_operational_counts")
    pending_open_count = fields.Integer(string="Pendências Abertas", compute="_compute_operational_counts")
    case_volume = fields.Integer(string="Casos", default=1, readonly=True)
    response_count = fields.Integer(string="Qtd Respostas", compute="_compute_operational_counts")
    checklist_generated = fields.Boolean(string="Checklist Gerado", default=False, copy=False)
    checklist_progress = fields.Float(string="Progresso do Checklist (%)", compute="_compute_checklist_progress", store=True)
    primary_partner_id = fields.Many2one("res.partner", string="Contato Principal", compute="_compute_primary_partner", store=True)

    email_sent_date = fields.Date(string="E-mail Enviado em", tracking=True)
    last_followup_date = fields.Date(string="Último Follow-up")

    days_without_response = fields.Integer(string="Dias sem Resposta", compute="_compute_days_without_response", aggregator="avg")
    is_overdue = fields.Boolean(string="Atrasado", compute="_compute_is_overdue", store=True)
    followup_count = fields.Integer(string="Qtd Follow-ups", default=0)
    followup_activity_count = fields.Integer(string="Qtd Atividades", compute="_compute_followup_activity_count")
    has_open_pendings = fields.Boolean(string="Possui Pendências Abertas", compute="_compute_queue_fields", store=True)
    requires_response_attention = fields.Boolean(string="Exige Atenção de Resposta", compute="_compute_queue_fields", store=True)
    next_action_date = fields.Date(string="Próxima Data de Ação", compute="_compute_queue_fields", store=True)
    work_queue_status = fields.Selection([
        ("ok", "Em Dia"),
        ("attention", "Atenção"),
        ("urgent", "Urgente"),
    ], string="Fila de Trabalho", compute="_compute_queue_fields", store=True)
    response_state = fields.Selection([
        ("no_request", "Sem Solicitação"),
        ("pending", "Aguardando Resposta"),
        ("received", "Resposta Recebida"),
        ("overdue", "Resposta Atrasada"),
    ], string="Situação da Resposta", compute="_compute_operational_status", store=True)
    last_communication_datetime = fields.Datetime(string="Última Comunicação", compute="_compute_operational_status", store=True)
    next_pending_due_date = fields.Date(string="Próxima Pendência", compute="_compute_operational_status", store=True)
    open_required_pending_count = fields.Integer(string="Pendências Obrigatórias Abertas", compute="_compute_operational_status", store=True)
    overdue_pending_count = fields.Integer(string="Pendências Atrasadas", compute="_compute_operational_status", store=True)
    pending_due_7d_count = fields.Integer(string="Pendências Próx. 7 Dias", compute="_compute_operational_status", store=True)
    response_request_open_count = fields.Integer(string="Solicitações sem Resposta", compute="_compute_operational_status", store=True)
    aging_bucket = fields.Selection([
        ("0_7", "0-7 dias"),
        ("8_15", "8-15 dias"),
        ("16_30", "16-30 dias"),
        ("31_plus", "31+ dias"),
    ], string="Faixa de Antiguidade", compute="_compute_executive_kpis", store=True)
    sla_status = fields.Selection([
        ("on_track", "Dentro do Prazo"),
        ("due_soon", "Próximo do Prazo"),
        ("overdue", "Atrasado"),
        ("closed", "Encerrado"),
    ], string="Status SLA", compute="_compute_executive_kpis", store=True)

    @api.depends("case_type_id.color", "stage_id.color")
    def _compute_type_stage_colors(self):
        for case in self:
            case.case_type_color = case.case_type_id.color if case.case_type_id else 0
            case.stage_color = case.stage_id.color if case.stage_id else 0

    @api.depends(
        "case_type_id.sla_days",
        "case_type_id.require_primary_participant",
        "case_type_id.auto_followup_days",
        "case_type_id.auto_create_followup_activity",
    )
    def _compute_type_settings(self):
        for case in self:
            case.type_sla_days = case.case_type_id.sla_days or 0
            case.require_primary_participant = bool(case.case_type_id.require_primary_participant)
            case.auto_followup_days = case.case_type_id.auto_followup_days or 0
            case.auto_create_followup_activity = bool(case.case_type_id.auto_create_followup_activity)

    @api.depends("priority", "case_type_id", "case_type_id.default_priority", "case_type_id.sla_days")
    def _compute_sla_days(self):
        sla_map = {"0": 30, "1": 15, "2": 7, "3": 3}
        for case in self:
            if case.case_type_id and case.case_type_id.sla_days:
                case.sla_days = case.case_type_id.sla_days
            else:
                effective_priority = case.priority or case.case_type_id.default_priority or "1"
                case.sla_days = sla_map.get(effective_priority, 15)

    @api.depends("origin_date", "sla_days")
    def _compute_resolution_deadline(self):
        for case in self:
            case.resolution_deadline = case.origin_date + timedelta(days=case.sla_days) if case.origin_date else False

    @api.depends("response_deadline", "response_date", "stage_id.status")
    def _compute_is_overdue(self):
        for case in self:
            case.is_overdue = bool(
                case.response_deadline
                and case.response_deadline < date.today()
                and not case.response_date
                and case.stage_id
                and case.stage_id.status != "closed"
            )

    @api.depends("response_date", "origin_date")
    def _compute_days_without_response(self):
        for case in self:
            if case.response_date:
                case.days_without_response = 0
            elif case.origin_date:
                case.days_without_response = (date.today() - case.origin_date).days
            else:
                case.days_without_response = 0

    @api.depends("origin_date")
    def _compute_response_deadline(self):
        config = self.env["common.config"].get_config()
        for case in self:
            case.response_deadline = case.origin_date + timedelta(days=config.governance_silence_days) if case.origin_date else False

    @api.depends("participant_ids")
    def _compute_participant_count(self):
        for case in self:
            case.participant_count = len(case.participant_ids)

    @api.depends("communication_ids", "pending_ids", "pending_ids.state", "response_ids")
    def _compute_operational_counts(self):
        for case in self:
            case.communication_count = len(case.communication_ids)
            case.pending_count = len(case.pending_ids)
            case.pending_open_count = len(case.pending_ids.filtered(lambda p: p.state == "open"))
            case.response_count = len(case.response_ids)

    @api.depends("pending_ids", "pending_ids.state", "pending_ids.required")
    def _compute_checklist_progress(self):
        for case in self:
            required_pendings = case.pending_ids.filtered(lambda p: p.required)
            if not required_pendings:
                case.checklist_progress = 100.0 if case.checklist_generated else 0.0
                continue
            done_count = len(required_pendings.filtered(lambda p: p.state == "done"))
            case.checklist_progress = (done_count / len(required_pendings)) * 100.0

    @api.depends("participant_ids.partner_id", "participant_ids.is_primary", "partner_ids")
    def _compute_primary_partner(self):
        for case in self:
            primary = case.participant_ids.filtered(lambda p: p.is_primary)[:1]
            case.primary_partner_id = primary.partner_id if primary else case.partner_ids[:1]

    @api.depends(
        "is_overdue",
        "response_deadline",
        "response_date",
        "pending_ids",
        "pending_ids.state",
        "pending_ids.due_date",
        "communication_ids",
        "communication_ids.requires_response",
        "communication_ids.response_received",
    )
    def _compute_queue_fields(self):
        today = fields.Date.today()
        for case in self:
            open_pendings = case.pending_ids.filtered(lambda p: p.state == "open")
            pending_dates = [d for d in open_pendings.mapped("due_date") if d]
            response_dates = []
            if case.response_deadline and not case.response_date and case.stage_id.status in ["sent", "waiting", "partial", "no_response"]:
                response_dates.append(case.response_deadline)
            next_dates = pending_dates + response_dates
            next_action = min(next_dates) if next_dates else False

            requires_response_attention = any(
                comm.requires_response and not comm.response_received
                for comm in case.communication_ids
            ) and not bool(case.response_date)

            has_open_pendings = bool(open_pendings)
            urgent = bool(case.is_overdue) or any(d < today for d in pending_dates)
            attention = False
            if not urgent:
                if requires_response_attention or has_open_pendings:
                    attention = True
                elif next_action and next_action <= (today + timedelta(days=2)):
                    attention = True

            case.has_open_pendings = has_open_pendings
            case.requires_response_attention = requires_response_attention
            case.next_action_date = next_action
            case.work_queue_status = "urgent" if urgent else "attention" if attention else "ok"

    @api.depends(
        "communication_ids.communication_datetime",
        "communication_ids.requires_response",
        "communication_ids.response_received",
        "pending_ids.state",
        "pending_ids.required",
        "pending_ids.due_date",
        "communication_ids.requires_response",
        "communication_ids.response_received",
        "response_date",
        "response_deadline",
        "stage_id.status",
        "is_overdue",
    )
    def _compute_operational_status(self):
        today = fields.Date.today()
        for case in self:
            communications = case.communication_ids.filtered(lambda c: c.communication_datetime)
            if communications:
                case.last_communication_datetime = max(communications.mapped("communication_datetime"))
            else:
                case.last_communication_datetime = False

            required_open = case.pending_ids.filtered(lambda p: p.state == "open" and p.required)
            case.open_required_pending_count = len(required_open)
            case.overdue_pending_count = len(required_open.filtered(lambda p: p.is_overdue))
            case.pending_due_7d_count = len(required_open.filtered(lambda p: p.due_date and today <= p.due_date <= (today + timedelta(days=7))))

            pending_dates = [d for d in case.pending_ids.filtered(lambda p: p.state == "open").mapped("due_date") if d]
            case.next_pending_due_date = min(pending_dates) if pending_dates else False

            open_response_comms = case.communication_ids.filtered(lambda c: c.requires_response and not c.response_received)
            case.response_request_open_count = len(open_response_comms)
            requires_response = bool(open_response_comms)
            if case.response_date:
                case.response_state = "received"
            elif requires_response:
                if case.is_overdue or (case.response_deadline and case.response_deadline < today):
                    case.response_state = "overdue"
                else:
                    case.response_state = "pending"
            else:
                case.response_state = "no_request"

    @api.depends("days_without_response", "resolution_deadline", "stage_id.status", "is_overdue")
    def _compute_executive_kpis(self):
        today = fields.Date.today()
        for case in self:
            days = case.days_without_response or 0
            if days <= 7:
                case.aging_bucket = "0_7"
            elif days <= 15:
                case.aging_bucket = "8_15"
            elif days <= 30:
                case.aging_bucket = "16_30"
            else:
                case.aging_bucket = "31_plus"

            if case.stage_id and case.stage_id.status in ["done", "closed"]:
                case.sla_status = "closed"
            elif case.is_overdue:
                case.sla_status = "overdue"
            elif case.resolution_deadline and case.resolution_deadline <= (today + timedelta(days=2)):
                case.sla_status = "due_soon"
            else:
                case.sla_status = "on_track"

    def _compute_followup_activity_count(self):
        activity_model = self.env["mail.activity"]
        for case in self:
            case.followup_activity_count = activity_model.search_count([
                ("res_model", "=", self._name),
                ("res_id", "=", case.id),
            ])

    @api.onchange("case_type_id")
    def _onchange_case_type_id_apply_defaults(self):
        for case in self:
            if case.case_type_id and not case._origin.id:
                case.priority = case.case_type_id.default_priority or case.priority

    def _sync_partner_ids_from_participants(self):
        for case in self:
            participant_partner_ids = case.participant_ids.mapped("partner_id").ids
            if participant_partner_ids and set(case.partner_ids.ids) != set(participant_partner_ids):
                super(GovernanceCase, case.with_context(skip_participant_partner_sync=True)).write({
                    "partner_ids": [(6, 0, participant_partner_ids)]
                })

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                seq = self.env["common.sequence"].sudo().next_by_code("governance.case")
                vals["reference"] = seq or "New"
            case_type = False
            if vals.get("case_type_id"):
                case_type = self.env["governance.case.type"].browse(vals["case_type_id"])
            elif not vals.get("priority"):
                case_type = self.env["governance.case.type"].search([("name", "=", "Operacional")], limit=1)
            if case_type and not vals.get("priority"):
                vals["priority"] = case_type.default_priority or "1"
            if case_type and not vals.get("stage_id") and case_type.initial_stage_id:
                vals["stage_id"] = case_type.initial_stage_id.id
        records = super().create(vals_list)
        if not self.env.context.get("skip_participant_partner_sync"):
            records._sync_partner_ids_from_participants()
        records._ensure_required_primary_participant()
        records._create_default_pendings_from_case_type()
        records._create_initial_followup_activity_if_needed()
        return records

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_participant_partner_sync") and "participant_ids" in vals:
            self._sync_partner_ids_from_participants()
        self._ensure_required_primary_participant()
        if any(k in vals for k in ["case_type_id", "responsible_id", "participant_ids", "origin_date"]):
            self._create_default_pendings_from_case_type()
            self._create_initial_followup_activity_if_needed()
        return res

    def _ensure_required_primary_participant(self):
        for case in self.filtered(lambda c: c.require_primary_participant):
            if not case.primary_partner_id and case.participant_ids:
                first = case.participant_ids[:1]
                first.with_context(skip_participant_partner_sync=True).write({"is_primary": True})

    def _create_initial_followup_activity_if_needed(self):
        activity_type = self.env.ref("governance.activity_type_followup", raise_if_not_found=False)
        if not activity_type:
            return
        for case in self.filtered(lambda c: c.auto_create_followup_activity and c.auto_followup_days > 0 and c.responsible_id):
            existing = self.env["mail.activity"].search([
                ("res_model", "=", self._name),
                ("res_id", "=", case.id),
                ("activity_type_id", "=", activity_type.id),
            ], limit=1)
            if existing:
                continue
            deadline = (case.origin_date or fields.Date.today()) + timedelta(days=case.auto_followup_days)
            case.activity_schedule(
                activity_type_id=activity_type.id,
                user_id=case.responsible_id.id,
                date_deadline=deadline,
                summary=_("Follow-up inicial do caso"),
                note=_("Verificar andamento do caso e retorno dos participantes."),
            )

    def _get_stage_by_type_or_default(self, target):
        self.ensure_one()
        mapping = {
            "initial": ("initial_stage_id", "governance.stage_planned"),
            "waiting": ("waiting_stage_id", "governance.stage_waiting"),
            "no_response": ("no_response_stage_id", "governance.stage_no_response"),
            "done": ("done_stage_id", "governance.stage_done"),
            "closed": ("closed_stage_id", "governance.stage_closed"),
        }
        field_name, xmlid = mapping[target]
        stage = self.case_type_id[field_name] if self.case_type_id and field_name in self.case_type_id._fields else False
        if stage:
            return stage
        return self.env.ref(xmlid, raise_if_not_found=False)

    def _apply_stage_transition(self, target, message=None, extra_vals=None):
        self.ensure_one()
        stage = self._get_stage_by_type_or_default(target)
        vals = dict(extra_vals or {})
        if stage:
            vals["stage_id"] = stage.id
        self.write(vals)
        if message:
            self.message_post(body=message)
        return True

    def _create_default_pendings_from_case_type(self):
        pending_model = self.env["governance.case.pending"]
        for case in self.filtered(lambda c: c.case_type_id and c.case_type_id.pending_template_ids):
            existing_names = set(case.pending_ids.mapped("name"))
            to_create = []
            origin = case.origin_date or fields.Date.today()
            for template in case.case_type_id.pending_template_ids.filtered("active"):
                if template.name in existing_names:
                    continue
                due_date = origin + timedelta(days=template.default_deadline_days or 0) if origin else False
                to_create.append({
                    "case_id": case.id,
                    "template_id": template.id,
                    "name": template.name,
                    "description": template.description,
                    "due_date": due_date,
                    "required": bool(template.required),
                    "priority": template.priority or case.priority or "1",
                    "responsible_id": case.responsible_id.id if template.assign_to_responsible and case.responsible_id else False,
                })
            if to_create:
                pending_model.create(to_create)
                case.checklist_generated = True

    def action_generate_default_pendings(self):
        self.ensure_one()
        self._create_default_pendings_from_case_type()
        return self.action_view_pendings()

    def action_view_participants(self):
        self.ensure_one()
        action = self.env.ref("governance.action_governance_case_participant", raise_if_not_found=False)
        if not action:
            return False
        result = action.read()[0]
        result["domain"] = [("case_id", "=", self.id)]
        result["context"] = {"default_case_id": self.id}
        return result


    def action_view_communications(self):
        self.ensure_one()
        action = self.env.ref("governance.action_governance_case_communication", raise_if_not_found=False)
        if not action:
            return False
        result = action.read()[0]
        result["domain"] = [("case_id", "=", self.id)]
        result["context"] = {"default_case_id": self.id, "default_partner_id": self.primary_partner_id.id}
        return result

    def action_view_pendings(self):
        self.ensure_one()
        action = self.env.ref("governance.action_governance_case_pending", raise_if_not_found=False)
        if not action:
            return False
        result = action.read()[0]
        result["domain"] = [("case_id", "=", self.id)]
        result["context"] = {"default_case_id": self.id, "default_responsible_id": self.responsible_id.id}
        return result

    def action_view_required_pendings(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_case_pending")
        action["domain"] = [
            ("case_id", "=", self.id),
            ("required", "=", True),
            ("state", "=", "open"),
        ]
        action["context"] = {
            **self.env.context,
            "default_case_id": self.id,
            "search_default_open": 1,
        }
        return action

    def action_view_response_requests(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_case_communication")
        action["domain"] = [
            ("case_id", "=", self.id),
            ("requires_response", "=", True),
            ("response_received", "=", False),
        ]
        action["context"] = {
            **self.env.context,
            "default_case_id": self.id,
            "search_default_requires_response": 1,
        }
        return action

    def action_view_overdue_pendings(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_case_pending")
        action["domain"] = [
            ("case_id", "=", self.id),
            ("state", "=", "open"),
            ("due_date", "!=", False),
            ("due_date", "<", fields.Date.today()),
        ]
        action["context"] = {
            **self.env.context,
            "default_case_id": self.id,
        }
        return action

    def action_view_pending_due_7d(self):
        self.ensure_one()
        today = fields.Date.today()
        action = self.env["ir.actions.actions"]._for_xml_id("governance.action_governance_case_pending")
        action["domain"] = [
            ("case_id", "=", self.id),
            ("state", "=", "open"),
            ("due_date", "!=", False),
            ("due_date", ">=", today),
            ("due_date", "<=", today + timedelta(days=7)),
        ]
        action["context"] = {
            **self.env.context,
            "default_case_id": self.id,
        }
        return action

    def action_view_responses(self):
        self.ensure_one()
        action = self.env.ref("governance.action_governance_case_response", raise_if_not_found=False)
        if not action:
            return False
        result = action.read()[0]
        result["domain"] = [("case_id", "=", self.id)]
        result["context"] = {"default_case_id": self.id, "default_partner_id": self.primary_partner_id.id, "default_responsible_id": self.responsible_id.id}
        return result

    def action_view_activities(self):
        self.ensure_one()
        return {
            "name": _("Atividades"),
            "type": "ir.actions.act_window",
            "res_model": "mail.activity",
            "view_mode": "list,form",
            "domain": [("res_model", "=", self._name), ("res_id", "=", self.id)],
            "context": {"default_res_model": self._name, "default_res_id": self.id},
        }

    def action_open_next_pending(self):
        self.ensure_one()
        pending = self.pending_ids.filtered(lambda p: p.state == "open").sorted(key=lambda p: (p.due_date or fields.Date.today(), p.id))[:1]
        if pending:
            return {
                "type": "ir.actions.act_window",
                "name": _("Próxima Pendência"),
                "res_model": "governance.case.pending",
                "res_id": pending.id,
                "view_mode": "form",
                "target": "current",
            }
        return self.action_view_pendings()

    def action_new_communication(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Nova Comunicação"),
            "res_model": "governance.case.communication",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_case_id": self.id,
                "default_partner_id": self.primary_partner_id.id,
                "default_responsible_id": self.responsible_id.id or self.env.user.id,
            },
        }


    def action_new_response(self):
        self.ensure_one()
        communication = self.communication_ids.filtered(lambda c: c.requires_response and not c.response_received)[:1]
        participant = communication.participant_id if communication else False
        partner = communication.partner_id if communication else self.primary_partner_id
        return {
            "type": "ir.actions.act_window",
            "name": _("Nova Resposta"),
            "res_model": "governance.case.response",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_case_id": self.id,
                "default_communication_id": communication.id if communication else False,
                "default_participant_id": participant.id if participant else False,
                "default_partner_id": partner.id if partner else False,
                "default_responsible_id": self.responsible_id.id or self.env.user.id,
            },
        }

    def action_new_pending(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Nova Pendência"),
            "res_model": "governance.case.pending",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_case_id": self.id,
                "default_responsible_id": self.responsible_id.id or self.env.user.id,
                "default_partner_id": self.primary_partner_id.id,
            },
        }

    @api.constrains("origin_date", "response_date")
    def _check_dates(self):
        for case in self:
            if case.response_date and case.origin_date and case.response_date < case.origin_date:
                raise ValidationError(_("A data de resposta não pode ser anterior à data de origem."))

    @api.constrains("require_primary_participant", "participant_ids", "primary_partner_id")
    def _check_primary_participant_required(self):
        for case in self:
            if case.require_primary_participant and case.participant_ids and not case.primary_partner_id:
                raise ValidationError(_("Este tipo de caso exige um contato principal definido."))

    @api.constrains("case_type_id", "stage_id")
    def _check_stage_allowed_by_case_type(self):
        for case in self:
            if case.case_type_id and case.case_type_id.allowed_stage_ids and case.stage_id and case.stage_id not in case.case_type_id.allowed_stage_ids:
                raise ValidationError(_("A etapa selecionada não é permitida para este tipo de caso."))

    @api.model
    def action_cron_check_overdue(self):
        config = self.env["common.config"].get_config()
        overdue = self.search([
            ("stage_id.status", "in", ["sent", "waiting"]),
            ("response_deadline", "<", date.today()),
            ("response_date", "=", False),
        ])
        template = self.env.ref("governance.mail_template_governance_overdue", raise_if_not_found=False)
        for case in overdue:
            case.action_set_no_response()
            if template and config.enable_email_notifications and case.partner_ids:
                template.send_mail(case.id, force_send=True, email_values={"partner_ids": [(4, pid) for pid in case.partner_ids.ids]})

    @api.model
    def action_cron_schedule_followups(self):
        activity_type = self.env.ref("governance.activity_type_followup", raise_if_not_found=False)
        if not activity_type:
            return
        today = fields.Date.today()
        cases = self.search([
            ("auto_create_followup_activity", "=", True),
            ("auto_followup_days", ">", 0),
            ("responsible_id", "!=", False),
            ("stage_id.status", "in", ["planned", "sent", "waiting", "partial"]),
        ])
        for case in cases:
            target_date = (case.origin_date or today) + timedelta(days=case.auto_followup_days)
            if target_date > today:
                continue
            existing = self.env["mail.activity"].search([
                ("res_model", "=", self._name),
                ("res_id", "=", case.id),
                ("activity_type_id", "=", activity_type.id),
                ("date_deadline", "=", target_date),
            ], limit=1)
            if not existing:
                case.activity_schedule(
                    activity_type_id=activity_type.id,
                    user_id=case.responsible_id.id,
                    date_deadline=target_date,
                    summary=_("Follow-up automático"),
                    note=_("Criado automaticamente conforme configuração do tipo de caso."),
                )

    @api.model
    def action_cron_schedule_operational_alerts(self):
        response_activity = self.env.ref("governance.activity_type_response_overdue", raise_if_not_found=False)
        pending_activity = self.env.ref("governance.activity_type_required_pending", raise_if_not_found=False)
        today = fields.Date.today()
        cases = self.search([("stage_id.status", "not in", ["done", "closed"])])
        for case in cases:
            if case.responsible_id and response_activity and case.response_state == "overdue":
                existing = self.env["mail.activity"].search([
                    ("res_model", "=", self._name),
                    ("res_id", "=", case.id),
                    ("activity_type_id", "=", response_activity.id),
                    ("date_deadline", "=", today),
                ], limit=1)
                if not existing:
                    case.activity_schedule(
                        activity_type_id=response_activity.id,
                        user_id=case.responsible_id.id,
                        date_deadline=today,
                        summary=_("Resposta em atraso"),
                        note=_("O caso exige atenção: há resposta em atraso."),
                    )
            if case.responsible_id and pending_activity and case.open_required_pending_count and case.next_pending_due_date and case.next_pending_due_date <= today:
                existing = self.env["mail.activity"].search([
                    ("res_model", "=", self._name),
                    ("res_id", "=", case.id),
                    ("activity_type_id", "=", pending_activity.id),
                    ("date_deadline", "=", today),
                ], limit=1)
                if not existing:
                    case.activity_schedule(
                        activity_type_id=pending_activity.id,
                        user_id=case.responsible_id.id,
                        date_deadline=today,
                        summary=_("Pendência obrigatória vencida"),
                        note=_("O caso possui pendência obrigatória aberta com prazo vencido."),
                    )


    def action_send_followup_email(self):
        self.ensure_one()
        if not self.partner_ids and self.participant_ids:
            self._sync_partner_ids_from_participants()
        if not self.partner_ids:
            raise UserError(_("Nenhum envolvido cadastrado no caso."))
        template = self.env.ref("governance.mail_template_governance_followup", raise_if_not_found=False)
        if not template:
            raise UserError(_("Template de follow-up não encontrado."))
        template.send_mail(self.id, force_send=True, email_values={"partner_ids": [(4, pid) for pid in self.partner_ids.ids]})
        self.last_followup_date = fields.Date.today()
        self.followup_count += 1

    def _validate_transition_requirements(self, target_status):
        self.ensure_one()
        case_type = self.case_type_id
        if not case_type:
            return True
        if target_status in ("done", "closed") and case_type.require_response_before_done:
            has_response = bool(self.response_date or self.response_ids or self.status == "no_response")
            if not has_response:
                raise UserError(_("Este tipo de caso exige resposta registrada (ou ausência de resposta) antes da conclusão/encerramento."))
        if target_status in ("done", "closed") and case_type.require_required_pendings_done:
            required_open = self.pending_ids.filtered(lambda p: p.required and p.state != "done")
            if required_open:
                raise UserError(_("Existem pendências obrigatórias em aberto: %s") % ", ".join(required_open.mapped("name")[:5]))
        if target_status == "closed" and case_type.require_no_open_pendings_to_close:
            open_pendings = self.pending_ids.filtered(lambda p: p.state == "open")
            if open_pendings:
                raise UserError(_("Não é possível encerrar com pendências abertas."))
        return True

    def action_log_first_contact(self):
        """Abre o formulário de nova comunicação como primeiro contato do caso."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Registrar Contato"),
            "res_model": "governance.case.communication",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_case_id": self.id,
                "default_partner_id": self.primary_partner_id.id,
                "default_responsible_id": self.responsible_id.id or self.env.user.id,
                "default_requires_response": True,
            },
        }

    def action_set_waiting(self):
        self.ensure_one()
        return self._apply_stage_transition("waiting", _("Aguardando resposta formal desde %s") % date.today())

    def action_set_no_response(self):
        self.ensure_one()
        return self._apply_stage_transition("no_response", _("Registrado sem resposta em %s") % date.today())

    def action_set_done(self):
        self.ensure_one()
        self._validate_transition_requirements("done")
        return self._apply_stage_transition("done", _("Caso concluído em %s") % date.today())

    def action_send_email(self):
        self.ensure_one()
        template = self.env.ref("governance.mail_template_governance_notification", raise_if_not_found=False)
        ctx = {
            "default_model": self._name,
            "default_res_ids": [self.id],
            "default_use_template": bool(template),
            "default_template_id": template.id if template else False,
            "default_composition_mode": "comment",
            "default_partner_ids": (self.partner_ids or self.participant_ids.mapped("partner_id")).ids,
            "mark_governance_sent": True,
        }
        return {
            "type": "ir.actions.act_window",
            "res_model": "mail.compose.message",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }

    def action_register_response(self):
        self.ensure_one()
        partial_stage = self.env.ref("governance.stage_partial", raise_if_not_found=False)
        vals = {"response_date": fields.Date.today()}
        if partial_stage:
            vals["stage_id"] = partial_stage.id
        self.write(vals)
        activity_type = self.env.ref("governance.activity_type_response_check", raise_if_not_found=False)
        if activity_type and self.responsible_id:
            self.activity_schedule(
                activity_type_id=activity_type.id,
                user_id=self.responsible_id.id,
                date_deadline=fields.Date.today() + timedelta(days=1),
                summary=_("Validar resposta recebida"),
            )

    def action_register_no_response(self):
        self.ensure_one()
        pending_vals = {
            "case_id": self.id,
            "name": _("Analisar ausência de resposta"),
            "responsible_id": self.responsible_id.id or self.env.user.id,
            "due_date": fields.Date.today(),
            "priority": self.priority or "1",
            "description": _("Pendência criada automaticamente por ausência de resposta no caso."),
        }
        self.env["governance.case.pending"].create(pending_vals)
        self.action_set_no_response()
        return True

    def action_close(self):
        self.ensure_one()
        self._validate_transition_requirements("closed")
        return self._apply_stage_transition("closed", _("Caso encerrado em %s") % date.today())

    @api.model
    def action_open_work_queue(self):
        action = self.env.ref("governance.action_governance_work_queue", raise_if_not_found=False)
        return action.read()[0] if action else False

    @api.model
    def action_open_my_queue(self):
        action = self.env.ref("governance.action_governance_my_work_queue", raise_if_not_found=False)
        return action.read()[0] if action else False

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env["governance.stage"].search([])

    def message_post(self, **kwargs):
        """Injeta identidade institucional se o canal forçar."""
        channel = self.email_channel_id if hasattr(self, 'email_channel_id') else None
        if channel and channel.force_institutional_identity:
            if channel.institutional_email_from and 'email_from' not in kwargs:
                kwargs['email_from'] = channel.institutional_email_from
            reply_to = channel.institutional_reply_to or channel.institutional_email_from
            if reply_to and 'reply_to' not in kwargs:
                kwargs['reply_to'] = reply_to
        return super().message_post(**kwargs)
