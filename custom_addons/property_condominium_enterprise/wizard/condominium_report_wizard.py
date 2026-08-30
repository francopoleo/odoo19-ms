from odoo import fields, models, _


class CondominiumReportWizard(models.TransientModel):
    _name = "property.condominium.report.wizard"
    _description = "Resumo do Condomínio"

    complex_id = fields.Many2one("property.complex", string="Condomínio")
    date_from = fields.Date(string="Data Inicial")
    date_to = fields.Date(string="Data Final")
    report_type = fields.Selection(
        [
            ("overdue", "Inadimplência"),
            ("expenses", "Despesas"),
            ("monthly", "Resumo Mensal"),
            ("financial", "Resumo Financeiro"),
            ("financial_by_complex", "Aging por Condomínio"),
        ],
        default="overdue",
        required=True,
        string="Tipo de Resumo",
    )

    def _domain_base(self, date_field="due_date"):
        self.ensure_one()
        domain = []
        if self.complex_id:
            domain.append(("complex_id", "=", self.complex_id.id))
        if self.date_from:
            domain.append((date_field, ">=", self.date_from))
        if self.date_to:
            domain.append((date_field, "<=", self.date_to))
        return domain

    def action_open_report(self):
        self.ensure_one()
        if self.report_type == "expenses":
            return {
                "type": "ir.actions.act_window",
                "name": _("Despesas do Condomínio"),
                "res_model": "property.condominium.expense",
                "view_mode": "list,form",
                "domain": self._domain_base(date_field="expense_date"),
                "target": "current",
            }
        if self.report_type == "monthly":
            lines = self.env["property.condominium.report.line"].search([("wizard_id", "=", self.id)])
            lines.unlink()
            expense_domain = []
            charge_domain = []
            if self.complex_id:
                expense_domain.append(("complex_id", "=", self.complex_id.id))
                charge_domain.append(("complex_id", "=", self.complex_id.id))
            if self.date_from:
                expense_domain.append(("expense_date", ">=", self.date_from))
                charge_domain.append(("due_date", ">=", self.date_from))
            if self.date_to:
                expense_domain.append(("expense_date", "<=", self.date_to))
                charge_domain.append(("due_date", "<=", self.date_to))

            expense_summary = {}
            for expense in self.env["property.condominium.expense"].search(expense_domain):
                key = expense.category or "other"
                row = expense_summary.setdefault(key, {"name": expense.category, "count": 0, "amount": 0.0})
                row["count"] += 1
                row["amount"] += expense.amount or 0.0

            charge_summary = {
                "open": {"name": _("Cobranças em Aberto"), "count": 0, "amount": 0.0},
                "paid": {"name": _("Cobranças Pagas"), "count": 0, "amount": 0.0},
                "overdue": {"name": _("Cobranças Vencidas"), "count": 0, "amount": 0.0},
            }
            for charge in self.env["property.condominium.charge"].search(charge_domain):
                bucket = charge.state if charge.state in charge_summary else "open"
                charge_summary[bucket]["count"] += 1
                charge_summary[bucket]["amount"] += charge.amount_total or 0.0

            for key, values in expense_summary.items():
                self.env["property.condominium.report.line"].create({
                    "wizard_id": self.id,
                    "bucket_code": f"expense_{key}",
                    "line_type": "expense",
                    "name": values["name"] or _("Outros"),
                    "charge_count": values["count"],
                    "amount_total": values["amount"],
                })
            for key, values in charge_summary.items():
                self.env["property.condominium.report.line"].create({
                    "wizard_id": self.id,
                    "bucket_code": f"charge_{key}",
                    "line_type": "charge",
                    "name": values["name"],
                    "charge_count": values["count"],
                    "amount_total": values["amount"],
                })
            return {
                "type": "ir.actions.act_window",
                "name": _("Resumo Mensal do Condomínio"),
                "res_model": "property.condominium.report.line",
                "view_mode": "list,form",
                "domain": [("wizard_id", "=", self.id)],
                "target": "current",
            }
        if self.report_type == "financial":
            lines = self.env["property.condominium.report.line"].search([("wizard_id", "=", self.id)])
            lines.unlink()
            charges = self.env["property.condominium.charge"].search(self._domain_base() + [("state", "in", ["open", "overdue"])])
            today = fields.Date.context_today(self)
            buckets = [
                ("current", _("Vencendo"), 0, 0),
                ("bucket_0_30", _("0 a 30 dias"), 0, 30),
                ("bucket_31_60", _("31 a 60 dias"), 31, 60),
                ("bucket_61_90", _("61 a 90 dias"), 61, 90),
                ("bucket_90_plus", _("Acima de 90 dias"), 91, 99999),
            ]
            summary = {code: {"label": label, "count": 0, "amount": 0.0} for code, label, _, _ in buckets}
            for charge in charges:
                overdue_days = max((today - charge.due_date).days, 0) if charge.due_date else 0
                amount = charge.amount_total or 0.0
                if overdue_days <= 0:
                    bucket = "current"
                elif overdue_days <= 30:
                    bucket = "bucket_0_30"
                elif overdue_days <= 60:
                    bucket = "bucket_31_60"
                elif overdue_days <= 90:
                    bucket = "bucket_61_90"
                else:
                    bucket = "bucket_90_plus"
                summary[bucket]["count"] += 1
                summary[bucket]["amount"] += amount
            for code, values in summary.items():
                self.env["property.condominium.report.line"].create({
                    "wizard_id": self.id,
                    "bucket_code": code,
                    "name": values["label"],
                    "charge_count": values["count"],
                    "amount_total": values["amount"],
                })
            return {
                "type": "ir.actions.act_window",
                "name": _("Resumo de Inadimplência"),
                "res_model": "property.condominium.report.line",
                "view_mode": "list,form",
                "domain": [("wizard_id", "=", self.id)],
                "target": "current",
            }
        if self.report_type == "financial_by_complex":
            lines = self.env["property.condominium.report.line"].search([("wizard_id", "=", self.id)])
            lines.unlink()
            complex_domain = self._domain_base() + [("state", "in", ["open", "overdue"])]
            today = fields.Date.context_today(self)
            summary = {}
            for charge in self.env["property.condominium.charge"].search(complex_domain):
                complex_name = charge.complex_id.display_name or charge.complex_id.name
                complex_bucket = summary.setdefault(complex_name, {
                    "complex_id": charge.complex_id.id,
                    "current": {"count": 0, "amount": 0.0},
                    "bucket_0_30": {"count": 0, "amount": 0.0},
                    "bucket_31_60": {"count": 0, "amount": 0.0},
                    "bucket_61_90": {"count": 0, "amount": 0.0},
                    "bucket_90_plus": {"count": 0, "amount": 0.0},
                })
                overdue_days = max((today - charge.due_date).days, 0) if charge.due_date else 0
                if overdue_days <= 0:
                    bucket = "current"
                elif overdue_days <= 30:
                    bucket = "bucket_0_30"
                elif overdue_days <= 60:
                    bucket = "bucket_31_60"
                elif overdue_days <= 90:
                    bucket = "bucket_61_90"
                else:
                    bucket = "bucket_90_plus"
                complex_bucket[bucket]["count"] += 1
                complex_bucket[bucket]["amount"] += charge.amount_total or 0.0
            for complex_name, values in summary.items():
                for bucket_code, bucket_values in values.items():
                    if bucket_code == "complex_id":
                        continue
                    bucket_labels = {
                        "current": _("Vencendo"),
                        "bucket_0_30": _("0 a 30 dias"),
                        "bucket_31_60": _("31 a 60 dias"),
                        "bucket_61_90": _("61 a 90 dias"),
                        "bucket_90_plus": _("Acima de 90 dias"),
                    }
                    label = bucket_labels.get(bucket_code, bucket_code.replace("_", " "))
                    self.env["property.condominium.report.line"].create({
                        "wizard_id": self.id,
                        "bucket_code": f"{values['complex_id']}_{bucket_code}",
                        "line_type": "charge",
                        "complex_id": values["complex_id"],
                        "name": f"{complex_name} - {label}",
                        "charge_count": bucket_values["count"],
                        "amount_total": bucket_values["amount"],
                    })
            return {
                "type": "ir.actions.act_window",
                "name": _("Aging por Condomínio"),
                "res_model": "property.condominium.report.line",
                "view_mode": "list,form",
                "domain": [("wizard_id", "=", self.id)],
                "target": "current",
            }
        domain = self._domain_base() + [("state", "in", ["open", "overdue"])]
        return {
            "type": "ir.actions.act_window",
            "name": _("Inadimplência do Condomínio"),
            "res_model": "property.condominium.charge",
            "view_mode": "list,form",
            "domain": domain,
            "target": "current",
        }


class CondominiumReportLine(models.TransientModel):
    _name = "property.condominium.report.line"
    _description = "Linha do Resumo do Condomínio"

    wizard_id = fields.Many2one("property.condominium.report.wizard", required=True, ondelete="cascade")
    bucket_code = fields.Char(readonly=True)
    line_type = fields.Selection([("charge", "Cobrança"), ("expense", "Despesa")], readonly=True)
    complex_id = fields.Many2one("property.complex", string="Condomínio", readonly=True)
    name = fields.Char(readonly=True)
    charge_count = fields.Integer(string="Qtd. Cobranças", readonly=True)
    amount_total = fields.Monetary(string="Valor Total", currency_field="currency_id", readonly=True)
    currency_id = fields.Many2one(related="wizard_id.complex_id.currency_id", store=True, readonly=True)
