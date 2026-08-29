from odoo import api, fields, models


class PropertyDashboard(models.TransientModel):
    """Painel de KPIs do portfólio imobiliário.
    TransientModel: lido via form view, sem persistência de dados.
    """
    _name = "property.dashboard"
    _description = "Dashboard de Imóveis"

    name = fields.Char(default="Dashboard de Imóveis")

    # ==================== Portfólio ====================
    asset_total = fields.Integer("Total de Imóveis", compute="_compute_all")
    asset_available = fields.Integer("Disponíveis", compute="_compute_all")
    asset_rented = fields.Integer("Alugados", compute="_compute_all")
    asset_maintenance = fields.Integer("Em Manutenção", compute="_compute_all")
    asset_for_sale = fields.Integer("À Venda", compute="_compute_all")

    # ==================== Contratos ====================
    contract_active = fields.Integer("Contratos Ativos", compute="_compute_all")
    contract_expiring = fields.Integer("A Vencer", compute="_compute_all")
    contract_renewing = fields.Integer("Em Renovação", compute="_compute_all")
    contract_defaulting = fields.Integer("Inadimplentes", compute="_compute_all")

    # ==================== Financeiro ====================
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id
    )
    monthly_revenue = fields.Monetary(
        "Receita Mensal (contratos ativos)",
        currency_field="currency_id", compute="_compute_all"
    )
    rent_open_total = fields.Monetary(
        "Parcelas em Aberto (R$)",
        currency_field="currency_id", compute="_compute_all"
    )
    rent_late_total = fields.Monetary(
        "Parcelas Atrasadas (R$)",
        currency_field="currency_id", compute="_compute_all"
    )
    rent_received_month = fields.Monetary(
        "Recebido no Mês (R$)",
        currency_field="currency_id", compute="_compute_all"
    )

    # ==================== Inadimplência ====================
    default_rate = fields.Float(
        "Taxa de Inadimplência (%)", digits=(5, 2), compute="_compute_all"
    )
    late_rent_count = fields.Integer("Qtd. Parcelas Atrasadas", compute="_compute_all")

    # ==================== Operações ====================
    maintenance_open = fields.Integer("Manutenções Abertas", compute="_compute_all")
    maintenance_emergency = fields.Integer("Emergências", compute="_compute_all")
    inspection_scheduled = fields.Integer("Vistorias Agendadas", compute="_compute_all")

    # ==================== Pipeline ====================
    acquisition_pipeline = fields.Integer("Aquisições em Aberto", compute="_compute_all")
    acquisition_closing = fields.Integer("Em Fechamento", compute="_compute_all")

    # ==================== Corretores & Proprietários ====================
    broker_active = fields.Integer("Corretores Ativos", compute="_compute_all")
    owner_count = fields.Integer("Proprietários", compute="_compute_all")
    commission_pending_count = fields.Integer("Comissões A Pagar", compute="_compute_all")
    commission_pending_total = fields.Monetary(
        "Total Comissões Pendentes", currency_field="currency_id", compute="_compute_all"
    )
    assignment_active = fields.Integer("Mandatos Ativos", compute="_compute_all")

    # ==================== Alertas ====================
    alert_contracts_expiring_30 = fields.Integer(
        "Contratos a Vencer em 30 dias", compute="_compute_all"
    )
    alert_late_rents = fields.Integer("Parcelas Atrasadas", compute="_compute_all")
    alert_maintenance_emergency = fields.Integer(
        "Manutenções de Emergência", compute="_compute_all"
    )
    alert_assignment_expiring_7 = fields.Integer(
        "Mandatos Expirando em 7 dias", compute="_compute_all"
    )

    # ==================== Taxas & Indicadores ====================
    occupancy_rate = fields.Float(
        "Taxa de Ocupação (%)", digits=(5, 1), compute="_compute_all"
    )
    collection_rate = fields.Float(
        "Taxa de Cobrança no Mês (%)", digits=(5, 1), compute="_compute_all"
    )
    revenue_growth = fields.Float(
        "Crescimento vs Mês Ant. (%)", digits=(5, 1), compute="_compute_all"
    )
    repasse_pending_count = fields.Integer("Repasses Pendentes", compute="_compute_all")
    repasse_pending_total = fields.Monetary(
        "Repasses a Pagar", currency_field="currency_id", compute="_compute_all"
    )

    # ==================== Ociosidade ====================
    idle_count = fields.Integer("Imóveis Ociosos", compute="_compute_all")
    idle_potential_monthly = fields.Monetary(
        "Receita Potencial Perdida/Mês", currency_field="currency_id", compute="_compute_all"
    )
    idle_potential_annual = fields.Monetary(
        "Receita Potencial Perdida/Ano", currency_field="currency_id", compute="_compute_all"
    )
    idle_costs_monthly = fields.Monetary(
        "Custo Direto Mensal (IPTU+Cond.)", currency_field="currency_id", compute="_compute_all"
    )
    idle_deterioration_monthly = fields.Monetary(
        "Deterioração Estimada/Mês (1% a.a.)", currency_field="currency_id", compute="_compute_all"
    )
    idle_total_burden_monthly = fields.Monetary(
        "Custo Total Mensal de Ociosidade", currency_field="currency_id", compute="_compute_all"
    )
    idle_days_avg = fields.Integer("Média de Dias Ociosos", compute="_compute_all")
    idle_over_90_days = fields.Integer("Ociosos > 90 dias", compute="_compute_all")
    idle_over_180_days = fields.Integer("Ociosos > 180 dias (crítico)", compute="_compute_all")
    idle_aging_risk = fields.Integer(
        "Arquitetura > 20 anos (risco conformidade)", compute="_compute_all"
    )
    idle_standard_risk = fields.Integer(
        "Padrão Inadequado p/ Empresas", compute="_compute_all"
    )
    idle_never_rented = fields.Integer("Nunca Foram Alugados", compute="_compute_all")
    idle_yield_loss_pct = fields.Float(
        "Yield Perdido (% do Portfólio)", digits=(5, 1), compute="_compute_all"
    )

    # ==================== Gráficos HTML ====================
    chart_received_html = fields.Html(
        "Gráfico Recebimentos 6 Meses", compute="_compute_charts", sanitize=False
    )
    chart_portfolio_html = fields.Html(
        "Distribuição da Carteira", compute="_compute_charts", sanitize=False
    )
    growth_html = fields.Html(
        "Indicador de Crescimento", compute="_compute_charts", sanitize=False
    )
    chart_vacancy_html = fields.Html(
        "Análise de Ociosidade", compute="_compute_charts", sanitize=False
    )

    # ==================== Computed ====================

    def _compute_all(self):
        from datetime import date
        today = date.today()
        Asset = self.env["property.asset"]
        Contract = self.env["property.contract"]
        Rent = self.env["property.rent"]
        Maint = self.env["property.maintenance"]
        Insp = self.env["property.inspection"]
        Acq = self.env["property.acquisition"]

        for dash in self:
            # --- Portfólio ---
            dash.asset_total = Asset.search_count([])
            dash.asset_available = Asset.search_count([("status", "=", "available")])
            dash.asset_rented = Asset.search_count([("status", "=", "rented")])
            dash.asset_maintenance = Asset.search_count([("status", "=", "maintenance")])
            dash.asset_for_sale = Asset.search_count([("status", "=", "for_sale")])

            # --- Contratos ---
            dash.contract_active = Contract.search_count([("status", "=", "active")])
            dash.contract_expiring = Contract.search_count([("status", "=", "expiring")])
            dash.contract_renewing = Contract.search_count([("status", "=", "renewing")])
            dash.contract_defaulting = Contract.search_count([("status", "=", "defaulting")])

            # --- Receita mensal ---
            active_contracts = Contract.search([("status", "in", ["active", "expiring", "renewing"])])
            dash.monthly_revenue = sum(active_contracts.mapped("monthly_rent"))

            # --- Parcelas ---
            open_rents = Rent.search([("status", "in", ["open", "partial"])])
            late_rents = Rent.search([("status", "=", "late")])
            dash.rent_open_total = sum(open_rents.mapped("amount_due"))
            dash.rent_late_total = sum(late_rents.mapped("amount_due"))
            dash.late_rent_count = len(late_rents)

            # Recebido no mês corrente
            month_start = today.replace(day=1)
            paid_month = Rent.search([
                ("status", "=", "paid"),
                ("payment_date", ">=", month_start),
                ("payment_date", "<=", today),
            ])
            dash.rent_received_month = sum(paid_month.mapped("amount_paid"))

            # Taxa de inadimplência
            total_open = len(open_rents) + len(late_rents)
            dash.default_rate = (
                len(late_rents) / total_open * 100 if total_open else 0.0
            )

            # --- Operações ---
            dash.maintenance_open = Maint.search_count([
                ("status", "not in", ["done", "cancelled"])
            ])
            dash.maintenance_emergency = Maint.search_count([
                ("maintenance_type", "=", "emergency"),
                ("status", "not in", ["done", "cancelled"]),
            ])
            dash.inspection_scheduled = Insp.search_count([("status", "=", "scheduled")])

            # --- Pipeline ---
            dash.acquisition_pipeline = Acq.search_count([
                ("stage", "not in", ["closed", "cancelled"])
            ])
            dash.acquisition_closing = Acq.search_count([("stage", "=", "closing")])

            # --- Corretores & Proprietários ---
            Partner = self.env["res.partner"]
            Comm = self.env["property.commission"]
            Asn = self.env["property.broker.assignment"]

            dash.broker_active = Partner.search_count([
                ("active", "=", True),
                ("category_id.name", "ilike", "Corretor"),
            ])
            dash.owner_count = Partner.search_count([
                ("active", "=", True),
                ("category_id.name", "ilike", "Proprietário"),
            ])
            pending_comms = Comm.search([("status", "=", "pending")])
            dash.commission_pending_count = len(pending_comms)
            dash.commission_pending_total = sum(pending_comms.mapped("commission_value"))
            dash.assignment_active = Asn.search_count([("status", "=", "active")])

            # --- Alertas ---
            from datetime import timedelta
            in_30 = today + timedelta(days=30)
            in_7 = today + timedelta(days=7)

            dash.alert_contracts_expiring_30 = Contract.search_count([
                ("status", "in", ["active", "expiring"]),
                ("end_date", "<=", in_30),
                ("end_date", ">=", today),
            ])
            dash.alert_late_rents = len(late_rents)
            dash.alert_maintenance_emergency = Maint.search_count([
                ("maintenance_type", "=", "emergency"),
                ("status", "not in", ["done", "cancelled"]),
            ])
            dash.alert_assignment_expiring_7 = Asn.search_count([
                ("status", "=", "active"),
                ("end_date", "<=", in_7),
                ("end_date", ">=", today),
            ])

            # --- Taxas ---
            dash.occupancy_rate = (
                dash.asset_rented / dash.asset_total * 100
            ) if dash.asset_total else 0.0
            dash.collection_rate = (
                dash.rent_received_month / dash.monthly_revenue * 100
            ) if dash.monthly_revenue else 0.0

            # Revenue growth vs previous month
            prev_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
            prev_end = today.replace(day=1) - timedelta(days=1)
            paid_prev = Rent.search([
                ("status", "=", "paid"),
                ("payment_date", ">=", prev_start),
                ("payment_date", "<=", prev_end),
            ])
            prev_total = sum(paid_prev.mapped("amount_paid"))
            curr_recv = dash.rent_received_month
            if prev_total:
                dash.revenue_growth = (curr_recv - prev_total) / prev_total * 100
            else:
                dash.revenue_growth = 100.0 if curr_recv else 0.0

            # --- Repasses pendentes ---
            Repasse = self.env["property.owner.repasse"]
            pending_repasses = Repasse.search([("state", "in", ["draft", "confirmed"])])
            dash.repasse_pending_count = len(pending_repasses)
            dash.repasse_pending_total = sum(pending_repasses.mapped("net_amount"))

            # --- Ociosidade ---
            idle_statuses = ["available", "maintenance"]
            idle_assets = Asset.search([("status", "in", idle_statuses)])
            dash.idle_count = len(idle_assets)

            # Receita potencial perdida: usa rental_value de cada imóvel ocioso
            pot_monthly = sum(a.rental_value or 0.0 for a in idle_assets)
            dash.idle_potential_monthly = pot_monthly
            dash.idle_potential_annual = pot_monthly * 12.0

            # Custo direto mensal: IPTU/12 + condomínio
            direct_cost_monthly = sum(
                (a.iptu_annual or 0.0) / 12.0 + (a.condominium_monthly or 0.0)
                for a in idle_assets
            )
            dash.idle_costs_monthly = direct_cost_monthly

            # Deterioração patrimonial estimada: 1% a.a. do valor do imóvel / 12
            deterioration_monthly = sum(
                (a.asset_value or 0.0) * 0.01 / 12.0
                for a in idle_assets
            )
            dash.idle_deterioration_monthly = deterioration_monthly
            dash.idle_total_burden_monthly = direct_cost_monthly + deterioration_monthly

            # Yield perdido = potencial / receita total do portfólio
            total_rev = dash.monthly_revenue + pot_monthly
            dash.idle_yield_loss_pct = (
                pot_monthly / total_rev * 100.0
            ) if total_rev else 0.0

            # Análise por dias de ociosidade
            idle_days_list = []
            idle_over_90 = 0
            idle_over_180 = 0
            idle_never = 0
            for asset in idle_assets:
                last_contract = Contract.search(
                    [("asset_id", "=", asset.id), ("status", "=", "closed")],
                    order="end_date desc", limit=1,
                )
                if last_contract and last_contract.end_date:
                    idle_d = (today - last_contract.end_date).days
                    idle_days_list.append(max(idle_d, 0))
                    if idle_d > 180:
                        idle_over_180 += 1
                    if idle_d > 90:
                        idle_over_90 += 1
                else:
                    idle_never += 1
                    idle_days_list.append(0)
            dash.idle_days_avg = (
                int(sum(idle_days_list) / len(idle_days_list))
                if idle_days_list else 0
            )
            dash.idle_over_90_days = idle_over_90
            dash.idle_over_180_days = idle_over_180
            dash.idle_never_rented = idle_never

            # Riscos arquitetônicos e de conformidade
            current_year = today.year
            aging_risk = 0
            standard_risk = 0
            for asset in idle_assets:
                if asset.construction_year and (current_year - asset.construction_year) > 20:
                    aging_risk += 1
                # Padrão simples + tipo comercial = risco de não conformidade corporativa
                if (
                    asset.construction_standard == "simple"
                    and asset.asset_type in ("commercial", "mixed", "industrial")
                ):
                    standard_risk += 1
            dash.idle_aging_risk = aging_risk
            dash.idle_standard_risk = standard_risk

    def _compute_charts(self):
        import calendar
        from datetime import date, timedelta  # noqa: F811
        today = date.today()
        Rent = self.env["property.rent"]
        cur_sym = self.env.company.currency_id.symbol or "R$"

        for dash in self:
            # ---- 6-month received bar chart (SVG) ----
            months_data = []
            for i in range(5, -1, -1):
                year, month = today.year, today.month - i
                while month <= 0:
                    month += 12
                    year -= 1
                m_start = date(year, month, 1)
                m_end = date(year, month, calendar.monthrange(year, month)[1])
                paid = Rent.search([
                    ("status", "=", "paid"),
                    ("payment_date", ">=", m_start),
                    ("payment_date", "<=", m_end),
                ])
                amount = sum(paid.mapped("amount_paid"))
                months_data.append((m_start.strftime("%b/%y"), amount))

            max_val = max(v for _, v in months_data) or 1
            ch, bw, gap = 90, 44, 14
            vb_w = 6 * bw + 5 * gap
            bars_svg = ""
            for i, (label, value) in enumerate(months_data):
                x = i * (bw + gap)
                bar_h = max(int(value / max_val * ch), 2 if value else 0)
                y = ch - bar_h
                color = "#0d6efd" if i == 5 else "#aac8fd"
                bars_svg += (
                    f'<rect x="{x}" y="{y}" width="{bw}" height="{bar_h}" '
                    f'fill="{color}" rx="3"/>'
                    f'<text x="{x + bw // 2}" y="{ch + 16}" text-anchor="middle" '
                    f'font-size="9.5" fill="#6c757d">{label}</text>'
                )
                if value >= 1000:
                    short = f"{value / 1000:.0f}k"
                elif value > 0:
                    short = f"{value:.0f}"
                else:
                    short = ""
                if short:
                    val_y = max(y - 5, 9)
                    bars_svg += (
                        f'<text x="{x + bw // 2}" y="{val_y}" text-anchor="middle" '
                        f'font-size="8.5" fill="{color}" font-weight="bold">{short}</text>'
                    )

            dash.chart_received_html = (
                f'<div style="padding:4px 0;">'
                f'<div style="font-size:10px;font-weight:700;color:#6c757d;'
                f'text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">'
                f'Recebimentos — Últimos 6 Meses</div>'
                f'<svg viewBox="0 0 {vb_w} {ch + 24}" '
                f'style="width:100%;max-width:500px;display:block;">'
                f'{bars_svg}</svg></div>'
            )

            # ---- Portfolio stacked bar ----
            total = dash.asset_total or 1
            rented_pct = round(dash.asset_rented / total * 100)
            avail_pct = round(dash.asset_available / total * 100)
            maint_pct = round(dash.asset_maintenance / total * 100)
            other_pct = max(0, 100 - rented_pct - avail_pct - maint_pct)
            dash.chart_portfolio_html = (
                f'<div style="margin:6px 0 4px 0;">'
                f'<div style="display:flex;border-radius:6px;overflow:hidden;'
                f'height:16px;background:#dee2e6;">'
                f'<div style="width:{rented_pct}%;background:#198754;" '
                f'title="Alugados"></div>'
                f'<div style="width:{avail_pct}%;background:#0dcaf0;" '
                f'title="Disponíveis"></div>'
                f'<div style="width:{maint_pct}%;background:#ffc107;" '
                f'title="Manutenção"></div>'
                f'<div style="width:{other_pct}%;background:#dee2e6;"></div>'
                f'</div>'
                f'<div style="display:flex;gap:12px;margin-top:8px;flex-wrap:wrap;">'
                f'<span style="font-size:11px;color:#198754;">&#9679; Alugados '
                f'{dash.asset_rented} ({rented_pct}%)</span>'
                f'<span style="font-size:11px;color:#0da8c4;">&#9679; Disponíveis '
                f'{dash.asset_available} ({avail_pct}%)</span>'
                f'<span style="font-size:11px;color:#d4a00a;">&#9679; Manutenção '
                f'{dash.asset_maintenance} ({maint_pct}%)</span>'
                f'<span style="font-size:11px;color:#6f42c1;">&#9679; À Venda '
                f'{dash.asset_for_sale}</span>'
                f'</div></div>'
            )

            # ---- Growth indicator ----
            g = dash.revenue_growth
            if g >= 0:
                dash.growth_html = (
                    f'<span style="color:#198754;font-weight:700;font-size:1rem;">&#9650; '
                    f'{g:.1f}%</span>'
                    f'<span style="color:#6c757d;font-size:0.8rem;"> vs mês anterior</span>'
                )
            else:
                dash.growth_html = (
                    f'<span style="color:#dc3545;font-weight:700;font-size:1rem;">&#9660; '
                    f'{abs(g):.1f}%</span>'
                    f'<span style="color:#6c757d;font-size:0.8rem;"> vs mês anterior</span>'
                )

            # ---- Vacancy / Ociosidade chart ----
            # Panel A: urgency breakdown horizontal bars
            idle_total = dash.idle_count or 1
            Contract2 = self.env["property.contract"]
            Asset2 = self.env["property.asset"]
            idle_assets2 = Asset2.search([("status", "in", ["available", "maintenance"])])
            brackets = {"<30d": 0, "30-90d": 0, "90-180d": 0, ">180d": 0, "nunca": 0}
            for asset in idle_assets2:
                lc = Contract2.search(
                    [("asset_id", "=", asset.id), ("status", "=", "closed")],
                    order="end_date desc", limit=1,
                )
                if lc and lc.end_date:
                    d = (today - lc.end_date).days
                    if d <= 30:
                        brackets["<30d"] += 1
                    elif d <= 90:
                        brackets["30-90d"] += 1
                    elif d <= 180:
                        brackets["90-180d"] += 1
                    else:
                        brackets[">180d"] += 1
                else:
                    brackets["nunca"] += 1

            def _bar(count, total, color, label, sublabel):
                pct = round(count / total * 100) if total else 0
                return (
                    f'<div style="margin-bottom:10px;">'
                    f'<div style="display:flex;justify-content:space-between;'
                    f'font-size:11px;margin-bottom:3px;">'
                    f'<span style="color:{color};font-weight:600;">{label}</span>'
                    f'<span style="color:#6c757d;">{count} imóveis ({pct}%)</span>'
                    f'</div>'
                    f'<div style="background:#f0f0f0;border-radius:4px;height:10px;">'
                    f'<div style="width:{pct}%;background:{color};border-radius:4px;'
                    f'height:10px;min-width:{2 if count else 0}px;"></div>'
                    f'</div>'
                    f'<div style="font-size:9px;color:#999;margin-top:2px;">{sublabel}</div>'
                    f'</div>'
                )

            bars_a = (
                _bar(brackets["<30d"], idle_total, "#198754",
                     "Recém desocupados (&lt; 30 dias)", "Prioridade normal — revisar captação")
                + _bar(brackets["30-90d"], idle_total, "#ffc107",
                       "Atenção (30 – 90 dias)", "Revisar preço e anúncios")
                + _bar(brackets["90-180d"], idle_total, "#fd7e14",
                       "Urgente (90 – 180 dias)", "Acionar estratégia comercial ativa")
                + _bar(brackets[">180d"], idle_total, "#dc3545",
                       "Crítico (&gt; 180 dias)", "Reavaliação completa: preço, reforma, uso")
                + _bar(brackets["nunca"], idle_total, "#6f42c1",
                       "Nunca alugados", "Avaliar viabilidade, posicionamento e mercado")
            )

            # Panel B: cost vs potential comparison (SVG bar)
            cur = cur_sym
            pot = dash.idle_potential_monthly
            burden = dash.idle_total_burden_monthly
            max_b = max(pot, burden, 1)
            pot_h = int(pot / max_b * 80)
            burden_h = int(burden / max_b * 80)

            def _fmt(v):
                if v >= 1000:
                    return f"{cur} {v / 1000:.1f}k"
                return f"{cur} {v:.0f}"

            svg_b = (
                f'<svg viewBox="0 0 180 110" style="width:100%;max-width:200px;">'
                f'<text x="40" y="10" text-anchor="middle" font-size="9" fill="#6c757d">Potencial</text>'
                f'<rect x="10" y="{90 - pot_h}" width="60" height="{pot_h}" fill="#aac8fd" rx="3"/>'
                f'<text x="40" y="{88 - pot_h}" text-anchor="middle" font-size="8" '
                f'fill="#0d6efd" font-weight="bold">{_fmt(pot)}</text>'
                f'<text x="130" y="10" text-anchor="middle" font-size="9" fill="#6c757d">Custo Total</text>'
                f'<rect x="100" y="{90 - burden_h}" width="60" height="{burden_h}" fill="#f5a0a8" rx="3"/>'
                f'<text x="130" y="{88 - burden_h}" text-anchor="middle" font-size="8" '
                f'fill="#dc3545" font-weight="bold">{_fmt(burden)}</text>'
                f'<line x1="0" y1="90" x2="180" y2="90" stroke="#dee2e6" stroke-width="1"/>'
                f'<text x="40" y="103" text-anchor="middle" font-size="8.5" fill="#555">/mês</text>'
                f'<text x="130" y="103" text-anchor="middle" font-size="8.5" fill="#555">/mês</text>'
                f'</svg>'
            )

            # Aging + compliance risks pills
            aging = dash.idle_aging_risk
            std_risk = dash.idle_standard_risk
            risk_pills = ""
            if aging:
                risk_pills += (
                    f'<span style="display:inline-block;background:#fff3cd;color:#856404;'
                    f'border:1px solid #ffc107;border-radius:20px;padding:2px 10px;'
                    f'font-size:11px;margin:2px;">'
                    f'&#9888; {aging} imóvel(is) com +20 anos de construção</span>'
                )
            if std_risk:
                risk_pills += (
                    f'<span style="display:inline-block;background:#f8d7da;color:#842029;'
                    f'border:1px solid #dc3545;border-radius:20px;padding:2px 10px;'
                    f'font-size:11px;margin:2px;">'
                    f'&#10005; {std_risk} imóvel(is) padrão simples — não conformes p/ empresas</span>'
                )
            if not risk_pills:
                risk_pills = (
                    f'<span style="color:#198754;font-size:11px;">&#10003; '
                    f'Nenhum risco crítico de conformidade identificado</span>'
                )

            dash.chart_vacancy_html = (
                f'<div style="display:flex;flex-wrap:wrap;gap:24px;">'
                # Left: urgency bars
                f'<div style="flex:2;min-width:260px;">'
                f'<div style="font-size:10px;font-weight:700;color:#6c757d;'
                f'text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">'
                f'Distribuição por Urgência de Locação</div>'
                f'{bars_a}'
                f'</div>'
                # Right: cost vs potential + risks
                f'<div style="flex:1;min-width:200px;">'
                f'<div style="font-size:10px;font-weight:700;color:#6c757d;'
                f'text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">'
                f'Potencial vs Custo / Mês</div>'
                f'{svg_b}'
                f'<div style="margin-top:16px;">'
                f'<div style="font-size:10px;font-weight:700;color:#6c757d;'
                f'text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">'
                f'Riscos Identificados</div>'
                f'{risk_pills}'
                f'</div>'
                f'</div>'
                f'</div>'
            )

