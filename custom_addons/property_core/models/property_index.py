from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date
import logging

_logger = logging.getLogger(__name__)

# Mapeamento código → série no SGS/Banco Central do Brasil
BCB_SERIES = {
    "igpm": 189,
    "ipca": 433,
    "inpc": 188,
}


class PropertyIndex(models.Model):
    _name = "property.index"
    _description = "Índice de Reajuste"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char("Nome", required=True)
    code = fields.Selection([
        ("igpm", "IGP-M"),
        ("ipca", "IPCA"),
        ("inpc", "INPC"),
    ], string="Código", required=True)
    bcb_series_code = fields.Integer(
        "Série BCB (SGS)", compute="_compute_bcb_series_code", store=True,
        help="Código da série no Sistema Gerenciador de Séries Temporais do Banco Central"
    )
    value_ids = fields.One2many("property.index.value", "index_id", string="Valores Mensais")
    value_count = fields.Integer("Meses cadastrados", compute="_compute_coverage")
    coverage_from = fields.Char("Cobertura de", compute="_compute_coverage")
    coverage_to = fields.Char("até", compute="_compute_coverage")
    last_sync = fields.Datetime("Última Sincronização", readonly=True)
    months_back = fields.Integer(
        "Meses a buscar", default=24,
        help="Quantidade de meses retroativos a buscar na próxima sincronização com o BCB. "
             "Já existentes não serão duplicados."
    )

    @api.constrains("code")
    def _check_unique_code(self):
        for rec in self:
            if not rec.code:
                continue
            duplicate = self.search([("id", "!=", rec.id), ("code", "=", rec.code)], limit=1)
            if duplicate:
                raise UserError(_("Já existe um índice com este código."))


    @api.depends("code")
    def _compute_bcb_series_code(self):
        for rec in self:
            rec.bcb_series_code = BCB_SERIES.get(rec.code, 0)

    @api.depends("value_ids.year", "value_ids.month")
    def _compute_coverage(self):
        labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                  "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        for rec in self:
            values = rec.value_ids.sorted(lambda v: (v.year, v.month))
            rec.value_count = len(values)
            if values:
                first = values[0]
                last = values[-1]
                rec.coverage_from = "%s/%s" % (labels[first.month - 1], first.year)
                rec.coverage_to = "%s/%s" % (labels[last.month - 1], last.year)
            else:
                rec.coverage_from = "—"
                rec.coverage_to = "—"

    # ==================== Sync BCB ====================

    def _fetch_bcb_data(self, months_back=36):
        """Busca dados do BCB usando endpoint de intervalo de datas (sem limite de registros).

        Usa /dados?dataInicial=...&dataFinal=... em vez de /ultimos/N,
        que tem limite de ~20 registros.
        """
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        import requests

        end = date.today()
        start = date(end.year, end.month, 1) - relativedelta(months=months_back - 1)

        url = (
            "https://api.bcb.gov.br/dados/serie/bcdata.sgs.%s/dados"
            "?dataInicial=%s&dataFinal=%s&formato=json" % (
                self.bcb_series_code,
                start.strftime("%d/%m/%Y"),
                end.strftime("%d/%m/%Y"),
            )
        )
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; OdooERP/19)",
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise UserError(_("Resposta inesperada da API do Banco Central."))
        return data

    def action_sync_from_bcb(self):
        """Busca os últimos 36 meses da API do Banco Central (SGS) e armazena localmente."""
        self.ensure_one()
        self = self.sudo()  # operação de sistema — bypass ACL intencional
        if not self.bcb_series_code:
            raise UserError(_("Este índice não possui código BCB configurado."))

        try:
            data = self._fetch_bcb_data(months_back=self.months_back or 24)
        except Exception as e:
            raise UserError(_("Erro ao acessar a API do Banco Central: %s") % str(e))

        from datetime import datetime
        IndexValue = self.env["property.index.value"].sudo()
        created = 0

        for record in data:
            dt = datetime.strptime(record["data"], "%d/%m/%Y")
            value_pct = float(record["valor"])
            existing = IndexValue.search([
                ("index_id", "=", self.id),
                ("year", "=", dt.year),
                ("month", "=", dt.month),
            ], limit=1)
            if not existing:
                IndexValue.create({
                    "index_id": self.id,
                    "year": dt.year,
                    "month": dt.month,
                    "value_pct": value_pct,
                })
                created += 1

        self.last_sync = fields.Datetime.now()
        self.message_post(body=_(
            "Sincronização BCB concluída: %s novos registros adicionados."
        ) % created)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": _("%s: %s novos registros sincronizados.") % (self.name, created),
                "type": "success",
                "sticky": False,
            },
        }

    # ==================== Cálculo ====================

    def get_accumulated_rate(self, period_start, period_end):
        """Retorna a taxa acumulada composta (%) entre period_start e period_end.

        Fórmula: (1+i1) × (1+i2) × ... - 1  (cada i em decimal)
        Retorna percentual — ex: 6.38 para 6,38%.
        """
        self.ensure_one()
        values = self.env["property.index.value"].search([
            ("index_id", "=", self.id),
        ], order="year, month")

        factor = 1.0
        months_used = 0

        for v in values:
            v_date = date(v.year, v.month, 1)
            if period_start <= v_date <= period_end:
                factor *= (1 + v.value_pct / 100)
                months_used += 1

        if months_used == 0:
            return 0.0, 0

        return (factor - 1) * 100, months_used


class PropertyIndexValue(models.Model):
    _name = "property.index.value"
    _description = "Valor Mensal do Índice"
    _order = "year desc, month desc"

    index_id = fields.Many2one("property.index", required=True, ondelete="cascade")
    year = fields.Integer("Ano", required=True)
    month = fields.Integer("Mês", required=True)
    month_label = fields.Char("Período", compute="_compute_month_label", store=True)
    value_pct = fields.Float(
        "Variação (%)", digits=(6, 4), required=True,
        help="Percentual mensal. Ex: 0.42 = 0,42%. Pode ser negativo (deflação)."
    )

    @api.constrains("index_id", "year", "month")
    def _check_unique_period(self):
        for rec in self:
            if not rec.index_id or not rec.year or not rec.month:
                continue
            duplicate = self.search([
                ("id", "!=", rec.id),
                ("index_id", "=", rec.index_id.id),
                ("year", "=", rec.year),
                ("month", "=", rec.month),
            ], limit=1)
            if duplicate:
                raise UserError(_("Já existe um valor para este índice neste mês/ano."))


    @api.depends("year", "month")
    def _compute_month_label(self):
        labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                  "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        for rec in self:
            if rec.year and rec.month and 1 <= rec.month <= 12:
                rec.month_label = "%s/%s" % (labels[rec.month - 1], rec.year)
            else:
                rec.month_label = ""

    # ==================== Cron ====================

    @api.model
    def action_cron_sync_all_indexes(self):
        """Cron mensal: sincroniza todos os índices BCB cadastrados."""
        indexes = self.env["property.index"].search([("bcb_series_code", ">", 0)])
        for index in indexes:
            try:
                index.action_sync_from_bcb()
            except Exception as e:
                _logger.error("Falha ao sincronizar índice %s: %s", index.name, e)