# -*- coding: utf-8 -*-
import base64
import logging
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from odoo import fields, models, _

_logger = logging.getLogger(__name__)

PREFIX = "DEMO-IMOB"
SEED_VERSION = "19.0.1.0.12"
_OPTIONAL_SKIP_MODELS_BY_CURSOR = {}


class PropertyDemoGenerator(models.TransientModel):
    _name = "property.demo.generator"
    _description = "Gerador de Massa de Testes Imobiliária"

    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.company, required=True)
    contract_count = fields.Integer("Quantidade de Contratos", default=60, required=True)
    months_past = fields.Integer("Meses anteriores", default=10, required=True)
    months_future = fields.Integer("Meses futuros", default=8, required=True)
    create_payment_proofs = fields.Boolean("Criar comprovantes conciliados", default=True)
    create_dossiers = fields.Boolean("Criar dossiês e documentos", default=True)
    create_governance_cases = fields.Boolean("Criar casos de governança", default=True)
    create_amendments = fields.Boolean("Criar aditivos", default=True)
    create_operations = fields.Boolean("Criar vistorias e manutenções", default=True)
    create_valuation_data = fields.Boolean("Criar dados de avaliação", default=True)
    create_commercial_network = fields.Boolean("Criar corretores, mandatos e comissões", default=True)
    create_owner_repasses = fields.Boolean("Criar proprietários, repasses e extratos", default=True)
    create_leads_acquisitions = fields.Boolean("Criar leads, compradores, vendedores e aquisições", default=True)
    create_media_gallery = fields.Boolean("Criar mídias, fotos e arquivos técnicos", default=True)
    create_contract_history_ocr = fields.Boolean("Criar históricos OCR e templates", default=True)
    create_help_agenda = fields.Boolean("Criar ajuda, tags, agenda e comunicações", default=True)
    clear_previous = fields.Boolean("Apagar massa DEMO-IMOB antes de gerar", default=False)
    summary_html = fields.Html("Resumo", readonly=True, sanitize=False)

    # ------------------------------------------------------------------
    # Utilidades seguras para variações entre módulos instalados
    # ------------------------------------------------------------------
    def _notify(self, title, message, sticky=False, kind="success"):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"title": title, "message": message, "sticky": sticky, "type": kind},
        }

    def _get_model(self, model_name):
        try:
            return self.env[model_name].sudo()
        except KeyError:
            return False


    def _table_exists(self, table_name):
        """Confere a existência física da tabela/view no PostgreSQL.

        Usa to_regclass(%s) e isola em savepoint para não abortar a transação
        quando a base tem módulos quebrados/parcialmente instalados.
        """
        if not table_name:
            return True
        try:
            with self.env.cr.savepoint():
                self.env.cr.execute("SELECT to_regclass(%s)", (table_name,))
                return bool(self.env.cr.fetchone()[0])
        except Exception as exc:
            _logger.warning("[%s] Falha ao verificar tabela/view %s: %s", PREFIX, table_name, exc)
            return False

    def _optional_skip_key(self):
        """Chave de cache por banco/cursor, sem gravar atributo no recordset.

        Em Odoo 19, recordsets não aceitam atributos arbitrários como
        `self._demo_optional_skip_models`. Isso causava AttributeError no botão
        Gerar. O cache abaixo fica em memória de processo e é isolado por banco
        e cursor da requisição.
        """
        dbname = getattr(self.env.cr, "dbname", None) or getattr(self.env.cr, "_cnx", None) or "default"
        return (str(dbname), id(self.env.cr))

    def _reset_optional_skip_set(self):
        _OPTIONAL_SKIP_MODELS_BY_CURSOR[self._optional_skip_key()] = set()

    def _optional_skip_set(self):
        """Conjunto em memória para evitar repetir criação/busca em models quebrados.

        Alguns ambientes mantêm classes de models no registry mesmo quando a tabela
        física ainda não existe, por exemplo após módulo removido, não instalado ou
        parcialmente carregado. Sem esse bloqueio, o wizard gera centenas de logs
        iguais e pode ficar lento.
        """
        return _OPTIONAL_SKIP_MODELS_BY_CURSOR.setdefault(self._optional_skip_key(), set())

    def _mark_model_skipped(self, model_name, reason):
        skipped = self._optional_skip_set()
        if model_name not in skipped:
            _logger.warning("[%s] Model opcional ignorado em toda a execução: %s (%s)", PREFIX, model_name, reason)
        skipped.add(model_name)

    def _model_table_ready(self, model_name, Model=None):
        """Retorna False quando o model existe no registry, mas a tabela não existe.

        Isso acontece em bases com módulos antigos/quebrados ou no addons_path com
        módulos não instalados. O Odoo permite acessar `self.env[model]`, mas o
        PostgreSQL falha no INSERT/SEARCH com `relation ... does not exist`.
        """
        if model_name in self._optional_skip_set():
            return False
        Model = Model if Model is not None else self._get_model(model_name)
        if Model is False:
            return False
        # Não confiar em `_auto=False` para liberar a criação. Em alguns módulos
        # customizados o model fica no registry, mas a tabela/view física ainda
        # não existe; se retornarmos True aqui, o create/search chega ao PostgreSQL
        # e gera `relation ... does not exist`. Portanto, sempre que o model tiver
        # `_table`, verificamos a relação física com to_regclass.
        table = getattr(Model, "_table", None)
        if not table:
            return True
        if not self._table_exists(table):
            self._mark_model_skipped(model_name, "tabela/view %s inexistente" % table)
            return False
        return True

    def _ref(self, xmlid):
        return self.env.ref(xmlid, raise_if_not_found=False)

    def _filter_vals(self, model_or_recordset, vals):
        """Remove campos inexistentes, sem confundir model vazio com model ausente.

        Em Odoo, `self.env[model]` é um recordset vazio e pode avaliar como
        False em contexto booleano. A versão anterior tratava esse recordset
        como se o model não existisse e acabava criando registros sem nenhum
        campo informado, como `res.partner` sem `name`.
        """
        if model_or_recordset is False or model_or_recordset is None:
            return {}
        return {key: value for key, value in vals.items() if key in model_or_recordset._fields}

    def _safe_create(self, model_name, vals):
        Model = self._get_model(model_name)
        if Model is False:
            return False
        return Model.create(self._filter_vals(Model, vals))

    def _safe_write(self, recordset, vals, label=None):
        if not recordset:
            return False
        try:
            # O wizard é TransientModel; usar sudo evita que uma regra/acesso
            # secundário mascare o erro real da limpeza.
            target = recordset.sudo() if hasattr(recordset, "sudo") else recordset
            with self.env.cr.savepoint():
                target.write(self._filter_vals(target, vals))
            return True
        except Exception as exc:
            _logger.warning("[%s] Escrita ignorada em %s: %s", PREFIX, label or getattr(recordset, '_name', recordset), exc)
            return False

    def _safe_unlink(self, recordset, label):
        """Apaga em lote e, se um registro bloquear o lote, tenta item a item.

        Em massa de teste é comum um único registro ficar preso por FK/regra
        e impedir que todo o recordset seja apagado. A versão anterior retornava
        0 no lote inteiro. Agora os registros apagáveis são removidos e os
        bloqueados aparecem no log, sem abortar a limpeza completa.
        """
        if not recordset:
            return 0
        try:
            count = len(recordset)
            with self.env.cr.savepoint():
                recordset.unlink()
            return count
        except Exception as exc:
            _logger.warning("[%s] Não foi possível apagar %s em lote: %s. Tentando item a item.", PREFIX, label, exc)

        deleted = 0
        for rec in recordset.exists():
            try:
                with self.env.cr.savepoint():
                    rec.unlink()
                deleted += 1
            except Exception as item_exc:
                _logger.warning(
                    "[%s] Não foi possível apagar %s id=%s: %s",
                    PREFIX, label, getattr(rec, "id", "?"), item_exc
                )
        return deleted

    def _selection(self, model_or_recordset, field_name, preferred, fallback=None):
        if model_or_recordset is False or model_or_recordset is None or field_name not in model_or_recordset._fields:
            return fallback
        available = [item[0] for item in (model_or_recordset._fields[field_name].selection or [])]
        if preferred in available:
            return preferred
        if fallback in available:
            return fallback
        return available[0] if available else fallback

    def _merge_stats(self, base, extra):
        for key, value in (extra or {}).items():
            if isinstance(value, (int, float)):
                base[key] = base.get(key, 0) + value
        return base

    def _safe_create_optional(self, model_name, vals, label=None):
        Model = self._get_model(model_name)
        if Model is False or not self._model_table_ready(model_name, Model):
            return False
        try:
            with self.env.cr.savepoint():
                return Model.create(self._filter_vals(Model, vals))
        except RecursionError as exc:
            self._mark_model_skipped(model_name, "recursão no create/write: %s" % exc)
            return False
        except Exception as exc:
            msg = str(exc)
            # Se mesmo após a checagem o PostgreSQL sinalizar tabela/view ausente
            # ou model quebrado, pula o model pelo restante da execução. Isso evita
            # repetir o mesmo erro várias vezes no log. Para tabela ausente, não
            # repetimos um segundo WARNING por registro, pois o _mark_model_skipped
            # já registra uma única linha explicativa.
            if "does not exist" in msg or "UndefinedTable" in msg or "relation" in msg:
                self._mark_model_skipped(model_name, msg)
                return False
            _logger.warning("[%s] Criação opcional ignorada em %s: %s", PREFIX, label or model_name, exc)
            return False

    def _safe_search(self, model_name, domain=None, limit=None, order=None):
        Model = self._get_model(model_name)
        if Model is False:
            return False
        if not self._model_table_ready(model_name, Model):
            return Model.browse()
        try:
            with self.env.cr.savepoint():
                return Model.search(domain or [], limit=limit, order=order)
        except Exception as exc:
            _logger.warning("[%s] Busca opcional ignorada em %s: %s", PREFIX, model_name, exc)
            return Model.browse()

    def _demo_partner(self, code, name, is_company=False, vat_seed=None, email_prefix=None):
        Partner = self.env["res.partner"].sudo()
        partner = Partner.search([("name", "=", name)], limit=1)
        if partner:
            return partner
        return Partner.create(self._filter_vals(Partner, {
            "name": name,
            "is_company": bool(is_company),
            "company_type": "company" if is_company else "person",
            "email": "%s.demo@example.com" % (email_prefix or code.lower().replace(" ", "")),
            "phone": "+55 11 4100-%04d" % ((vat_seed or 1) % 10000),
            "mobile": "+55 11 99100-%04d" % ((vat_seed or 1) % 10000),
            "street": "Av. Dados de Teste %s" % (vat_seed or 1),
            "city": "Barueri",
            "zip": "06460-000",
            "vat": self._cpf(50000 + (vat_seed or 1)),
            "company_id": self.company_id.id,
        }))

    # ------------------------------------------------------------------
    # Ações do wizard
    # ------------------------------------------------------------------
    def action_clear(self):
        self.ensure_one()
        self._reset_optional_skip_set()

        # Em base limpa, o botão Apagar não deve varrer models opcionais nem
        # depender de módulos parcialmente instalados. Deve simplesmente
        # retornar zero apagados.
        if not self._has_demo_marker_for_cleanup():
            deleted_stats = {"apagados": 0, "contratos_encontrados": 0, "contratos_apagados": 0}
            self._safe_write(self, {"summary_html": self._format_summary(deleted_stats)}, label="resumo do wizard")
            return self._notify(
                _("Nenhuma massa DEMO-IMOB encontrada"),
                _("Não havia registros DEMO-IMOB centrais para apagar."),
                kind="info",
            )

        try:
            with self.env.cr.savepoint():
                deleted_stats = self._clear_previous_demo_data()
        except Exception as exc:
            # Última barreira: se algum erro escapar de um savepoint interno,
            # não deixa o botão quebrar com InFailedSqlTransaction.
            _logger.exception("[%s] Falha geral durante limpeza DEMO-IMOB", PREFIX)
            try:
                self.env.cr.rollback()
            except Exception:
                pass
            deleted_stats = {
                "apagados": 0,
                "contratos_encontrados": 0,
                "contratos_apagados": 0,
                "erro_limpeza": str(exc)[:500],
            }
            self._safe_write(self, {"summary_html": self._format_summary(deleted_stats)}, label="resumo do wizard")
            return self._notify(
                _("Limpeza DEMO-IMOB não concluída"),
                _("A limpeza encontrou um erro e foi interrompida sem derrubar a sessão. Veja o resumo e o log do servidor."),
                sticky=True,
                kind="warning",
            )

        self._safe_write(self, {"summary_html": self._format_summary(deleted_stats)}, label="resumo do wizard")
        return self._notify(
            _("Massa de teste removida"),
            _("Registros DEMO-IMOB apagados: %(total)s. Contratos apagados: %(contracts)s/%(found)s") % {
                "total": deleted_stats.get("apagados", 0),
                "contracts": deleted_stats.get("contratos_apagados", 0),
                "found": deleted_stats.get("contratos_encontrados", 0),
            }
        )

    def action_generate(self):
        self.ensure_one()
        self._reset_optional_skip_set()
        self.contract_count = max(self.contract_count or 1, 1)
        self.months_past = max(self.months_past or 1, 1)
        self.months_future = max(self.months_future or 1, 1)

        if self.clear_previous:
            if self._has_demo_marker_for_cleanup():
                try:
                    with self.env.cr.savepoint():
                        self._clear_previous_demo_data()
                except Exception as exc:
                    _logger.exception("[%s] Falha ao limpar antes de gerar", PREFIX)
                    try:
                        self.env.cr.rollback()
                    except Exception:
                        pass
                    self._safe_write(self, {"summary_html": self._format_summary({"erro_limpeza_previa": str(exc)[:500]})}, label="resumo do wizard")
                    return self._notify(
                        _("Limpeza prévia falhou"),
                        _("A geração foi interrompida para não misturar dados novos com massa anterior. Veja o log do servidor."),
                        sticky=True,
                        kind="warning",
                    )
        else:
            existing = self.env["property.contract"].sudo().search_count([("name", "ilike", PREFIX)])
            if existing:
                self._safe_write(self, {"summary_html": self._format_summary({"contratos_existentes": existing})}, label="resumo do wizard")
                return self._notify(
                    _("Massa de teste já existe"),
                    _("Já existem %s contratos DEMO-IMOB. Marque 'Apagar massa DEMO-IMOB antes de gerar' para reconstruir.") % existing,
                    sticky=True,
                    kind="warning",
                )

        stats = self._generate_demo_data()
        self._safe_write(self, {"summary_html": self._format_summary(stats)}, label="resumo do wizard")
        return self._notify(
            _("Massa de teste criada"),
            _("Criados %(contracts)s contratos, %(rents)s parcelas, %(payments)s recebimentos e %(proofs)s comprovantes.") % {
                "contracts": stats.get("contracts", 0),
                "rents": stats.get("rents", 0),
                "payments": stats.get("payments", 0),
                "proofs": stats.get("proofs", 0),
            },
            sticky=True,
        )

    def _format_summary(self, stats):
        rows = "".join(
            "<tr><td><b>%s</b></td><td class='text-end'>%s</td></tr>" % (key, value)
            for key, value in sorted(stats.items())
        )
        return """
        <div class="alert alert-info">
          <h3>Massa de teste DEMO-IMOB</h3>
          <table class="table table-sm table-striped">%s</table>
          <p><b>Prefixo:</b> DEMO-IMOB. Use este prefixo para filtrar contratos, locatários, dossiês, casos, parcelas e comprovantes.</p>
        </div>
        """ % rows

    def _or_domain(self, terms):
        terms = [term for term in (terms or []) if term]
        if not terms:
            return []
        domain = [terms[0]]
        for term in terms[1:]:
            domain = ["|"] + domain + [term]
        return domain

    def _search_ids_if_field_exists(self, model_name, field_name, domain):
        Model = self._get_model(model_name)
        if Model is False or not self._model_table_ready(model_name, Model):
            return set()
        if field_name and field_name not in Model._fields:
            return set()
        try:
            with self.env.cr.savepoint():
                return set(Model.search(domain).ids)
        except Exception as exc:
            _logger.warning("[%s] Busca de IDs ignorada em %s: %s", PREFIX, model_name, exc)
            return set()

    def _safe_search_count(self, model_name, domain):
        Model = self._get_model(model_name)
        if Model is False or not self._model_table_ready(model_name, Model):
            return 0
        try:
            with self.env.cr.savepoint():
                return Model.search_count(domain or [])
        except Exception as exc:
            _logger.warning("[%s] Contagem opcional ignorada em %s: %s", PREFIX, model_name, exc)
            return 0

    def _has_demo_marker_for_cleanup(self):
        """Evita varrer dezenas de models quando não existe massa DEMO.

        O botão Apagar deve ser idempotente: em uma base limpa ele precisa
        apenas responder zero apagados. Em alguns ambientes há models no
        registry sem tabela física, fields antigos ou views SQL quebradas;
        varrer tudo sem necessidade pode gerar erro mesmo sem haver dados
        DEMO-IMOB. Por isso primeiro buscamos marcadores centrais e baratos.
        """
        checks = [
            ("res.partner", [("name", "ilike", PREFIX)]),
            ("property.asset", [("name", "ilike", PREFIX)]),
            ("property.contract", [("name", "ilike", PREFIX)]),
        ]
        Contract = self._get_model("property.contract")
        if Contract is not False and "additional_clauses" in getattr(Contract, "_fields", {}):
            checks.append(("property.contract", [("additional_clauses", "ilike", PREFIX)]))
        for model_name, domain in checks:
            if self._safe_search_count(model_name, domain):
                return True
        return False

    def _demo_contract_ids_for_cleanup(self):
        """Encontra contratos DEMO mesmo quando o nome foi trocado por sequência.

        Alguns fluxos do contrato podem renomear o registro ao confirmar/ativar.
        Por isso a limpeza não pode depender só de `property.contract.name`.
        O contrato também é identificado por cláusulas, locatário/parceiro
        DEMO-IMOB, pagador autorizado, parcelas, recebimentos e comprovantes.
        """
        Contract = self._get_model("property.contract")
        if Contract is False or not self._model_table_ready("property.contract", Contract):
            return []

        ids = set()
        contract_terms = []
        if "name" in Contract._fields:
            contract_terms.append(("name", "ilike", PREFIX))
        if "additional_clauses" in Contract._fields:
            contract_terms.append(("additional_clauses", "ilike", PREFIX))
        if "tenant_id" in Contract._fields:
            contract_terms.append(("tenant_id.partner_id.name", "ilike", PREFIX))
        if "partner_id" in Contract._fields:
            contract_terms.append(("partner_id.name", "ilike", PREFIX))

        if contract_terms:
            try:
                with self.env.cr.savepoint():
                    ids |= set(Contract.search(self._or_domain(contract_terms)).ids)
            except Exception as exc:
                _logger.warning("[%s] Busca principal de contratos DEMO ignorada: %s", PREFIX, exc)

        # Relações que podem preservar o prefixo mesmo quando o contrato foi renomeado.
        Rent = self._get_model("property.rent")
        if Rent is not False and self._model_table_ready("property.rent", Rent):
            for domain in [
                [("contract_id.name", "ilike", PREFIX)],
                [("contract_id.additional_clauses", "ilike", PREFIX)],
                [("payment_notes", "ilike", PREFIX)] if "payment_notes" in Rent._fields else [],
                [("receipt_number", "ilike", PREFIX)] if "receipt_number" in Rent._fields else [],
            ]:
                if not domain:
                    continue
                try:
                    with self.env.cr.savepoint():
                        ids |= set(Rent.search(domain).mapped("contract_id").ids)
                except Exception as exc:
                    _logger.warning("[%s] Busca de contratos via parcelas ignorada: %s", PREFIX, exc)

        Payment = self._get_model("property.rent.payment")
        if Payment is not False and self._model_table_ready("property.rent.payment", Payment):
            for domain in [
                [("notes", "ilike", PREFIX)] if "notes" in Payment._fields else [],
                [("rent_id.contract_id.name", "ilike", PREFIX)] if "rent_id" in Payment._fields else [],
                [("rent_id.contract_id.additional_clauses", "ilike", PREFIX)] if "rent_id" in Payment._fields else [],
            ]:
                if not domain:
                    continue
                try:
                    with self.env.cr.savepoint():
                        ids |= set(Payment.search(domain).mapped("rent_id.contract_id").ids)
                except Exception as exc:
                    _logger.warning("[%s] Busca de contratos via recebimentos ignorada: %s", PREFIX, exc)

        Payer = self._get_model("property.payment.authorized.payer")
        if Payer is not False and self._model_table_ready("property.payment.authorized.payer", Payer):
            for domain in [
                [("name", "ilike", PREFIX)] if "name" in Payer._fields else [],
                [("notes", "ilike", PREFIX)] if "notes" in Payer._fields else [],
            ]:
                if not domain:
                    continue
                try:
                    with self.env.cr.savepoint():
                        ids |= set(Payer.search(domain).mapped("contract_id").ids)
                except Exception as exc:
                    _logger.warning("[%s] Busca de contratos via pagadores autorizados ignorada: %s", PREFIX, exc)

        return sorted(ids)

    def _domain_or_prefix_and_contract(self, model_name, prefix_terms, contract_ids, contract_field="contract_id"):
        Model = self._get_model(model_name)
        if Model is False:
            return []
        fields_map = getattr(Model, "_fields", {})
        terms = []
        for term in (prefix_terms or []):
            # Só valida o primeiro campo da cadeia dotted, ex.: contract_id.name.
            if isinstance(term, (tuple, list)) and term:
                root_field = str(term[0]).split(".")[0]
                if root_field in fields_map:
                    terms.append(tuple(term))
        if contract_ids and contract_field in fields_map:
            terms.append((contract_field, "in", contract_ids))
        return self._or_domain(terms)

    def _clear_previous_demo_data(self):
        total = 0
        stats = {"apagados": 0, "contratos_encontrados": 0, "contratos_apagados": 0}
        contract_ids = self._demo_contract_ids_for_cleanup()
        stats["contratos_encontrados"] = len(contract_ids)

        models_domains = [
            # Dependentes e rastros técnicos primeiro
            ("property.payment.proof.match", ["|", ("proof_id.transaction_id", "ilike", PREFIX), ("proof_id.raw_text", "ilike", PREFIX)], "sugestões de conciliação"),
            ("property.payment.proof", self._domain_or_prefix_and_contract("property.payment.proof", [
                ("transaction_id", "ilike", PREFIX), ("raw_text", "ilike", PREFIX)
            ], contract_ids), "comprovantes"),
            ("property.rent.payment", self._domain_or_prefix_and_contract("property.rent.payment", [
                ("notes", "ilike", PREFIX)
            ], contract_ids, contract_field="contract_id"), "recebimentos"),
            ("property.rent", self._domain_or_prefix_and_contract("property.rent", [
                ("contract_id.name", "ilike", PREFIX), ("contract_id.additional_clauses", "ilike", PREFIX),
                ("payment_notes", "ilike", PREFIX), ("receipt_number", "ilike", PREFIX)
            ], contract_ids), "parcelas"),

            # OCR / documentos / dossiês / governança antes dos contratos
            ("property.contract.history.line", [("history_id.name", "ilike", PREFIX)], "linhas histórico OCR"),
            ("property.contract.history", ["|", ("name", "ilike", PREFIX), ("contract_filename", "ilike", PREFIX)], "históricos OCR"),
            ("property.contract.ocr.template.line", [("template_id.name", "ilike", PREFIX)], "linhas template OCR"),
            ("property.contract.ocr.template", [("name", "ilike", PREFIX)], "templates OCR"),
            ("document.document", ["|", ("notes", "ilike", PREFIX), ("name", "ilike", PREFIX)], "documentos"),
            ("dossier.dossier", [("name", "ilike", PREFIX)], "dossiês"),
            ("governance.case", [("name", "ilike", PREFIX)], "casos"),

            # Fluxos imobiliários vinculados ao contrato/imóvel
            ("property.owner.repasse", [("notes", "ilike", PREFIX)], "repasses proprietário"),
            ("property.rent.adjustment", [("notes", "ilike", PREFIX)], "reajustes"),
            ("property.commission", [("notes", "ilike", PREFIX)], "comissões"),
            ("property.broker.assignment", [("notes", "ilike", PREFIX)], "mandatos"),
            ("property.lead", [("name", "ilike", PREFIX)], "leads"),
            ("property.acquisition", [("name", "ilike", PREFIX)], "aquisições"),
            ("property.media", [("name", "ilike", PREFIX)], "mídias"),
            ("property.media.category", [("code", "ilike", PREFIX)], "categorias de mídia"),
            ("property.contract.amendment", self._domain_or_prefix_and_contract("property.contract.amendment", [
                ("note", "ilike", PREFIX)
            ], contract_ids), "aditivos"),
            ("property.inspection", self._domain_or_prefix_and_contract("property.inspection", [
                ("observations", "ilike", PREFIX)
            ], contract_ids), "vistorias"),
            ("property.maintenance", [("description", "ilike", PREFIX)], "manutenções"),
            ("property.market.comparable", [("name", "ilike", PREFIX)], "comparáveis"),
            ("property.price.m2.reference", [("notes", "ilike", PREFIX)], "referências m²"),
            ("property.valuation.run", [("review_notes", "ilike", PREFIX)], "estimativas"),
            ("property.payment.authorized.payer", self._domain_or_prefix_and_contract("property.payment.authorized.payer", [
                ("name", "ilike", PREFIX), ("notes", "ilike", PREFIX)
            ], contract_ids), "pagadores autorizados"),

            # Help center / common
            ("help.metric", [("path", "ilike", PREFIX)], "métricas de ajuda"),
            ("help.feedback", [("comment", "ilike", PREFIX)], "feedbacks de ajuda"),
            ("help.learning.step", [("name", "ilike", PREFIX)], "etapas de trilha"),
            ("help.learning.path", [("name", "ilike", PREFIX)], "trilhas de aprendizado"),
            ("help.checklist.progress", [("template_id.name", "ilike", PREFIX)], "progresso checklist"),
            ("help.checklist.item", [("name", "ilike", PREFIX)], "itens checklist"),
            ("help.checklist.template", [("name", "ilike", PREFIX)], "checklists de ajuda"),
            ("help.tip", [("name", "ilike", PREFIX)], "dicas de ajuda"),
            ("help.suggestion.rule", [("name", "ilike", PREFIX)], "regras de sugestão"),
            ("help.context", [("name", "ilike", PREFIX)], "contextos de ajuda"),
            ("help.article", [("name", "ilike", PREFIX)], "artigos de ajuda"),
            ("help.category", [("code", "ilike", PREFIX)], "categorias de ajuda"),
            ("help.tag", [("name", "ilike", PREFIX)], "tags de ajuda"),
            ("common.agenda.event", [("name", "ilike", PREFIX)], "eventos de agenda"),
            ("common.communication.base", [("channel_origin", "ilike", PREFIX)], "comunicações comuns"),

            # Contratos e cadastros-base por último
            ("property.contract", [("id", "in", contract_ids)] if contract_ids else [("name", "ilike", PREFIX)], "contratos"),
            ("property.tenant", [("partner_id.name", "ilike", PREFIX)], "locatários"),
            ("property.buyer", [("partner_id.name", "ilike", PREFIX)], "compradores"),
            ("property.seller", [("partner_id.name", "ilike", PREFIX)], "vendedores"),
            ("property.investor", [("partner_id.name", "ilike", PREFIX)], "investidores"),
            ("property.developer", [("partner_id.name", "ilike", PREFIX)], "incorporadoras"),
            ("property.broker", [("name", "ilike", PREFIX)], "corretores"),
            ("property.brokerage", [("partner_id.name", "ilike", PREFIX)], "imobiliárias"),
            ("property.owner", [("name", "ilike", PREFIX)], "proprietários"),
            ("property.stakeholder.profile", [("partner_id.name", "ilike", PREFIX)], "perfis imobiliários"),
            ("res.partner", [("name", "ilike", PREFIX)], "contatos"),
            ("property.asset", [("name", "ilike", PREFIX)], "imóveis fallback"),
            ("property.valuation.source", [("name", "ilike", PREFIX)], "fontes de avaliação"),
        ]

        for model_name, domain, label in models_domains:
            Model = self._get_model(model_name)
            if Model is False or not self._model_table_ready(model_name, Model):
                continue
            if not domain:
                continue
            try:
                with self.env.cr.savepoint():
                    records = Model.search(domain)
            except Exception as exc:
                _logger.warning("[%s] Limpeza ignorada em %s (%s): %s", PREFIX, model_name, label, exc)
                continue
            deleted = self._safe_unlink(records, label)
            total += deleted
            if model_name == "property.contract":
                stats["contratos_apagados"] = deleted

        stats["apagados"] = total
        if stats["contratos_encontrados"] and stats["contratos_apagados"] < stats["contratos_encontrados"]:
            _logger.warning(
                "[%s] Limpeza apagou %s de %s contratos DEMO encontrados. Veja logs de bloqueio por FK/regra.",
                PREFIX, stats["contratos_apagados"], stats["contratos_encontrados"]
            )
        return stats

    # ------------------------------------------------------------------
    # Geração principal
    # ------------------------------------------------------------------
    def _generate_demo_data(self):
        today = date.today()
        stats = {
            "partners": 0,
            "tenants": 0,
            "contracts": 0,
            "rents": 0,
            "payments": 0,
            "proofs": 0,
            "authorized_payers": 0,
            "dossiers": 0,
            "documents": 0,
            "governance_cases": 0,
            "amendments": 0,
            "operations": 0,
            "valuation_records": 0,
            "dossier_templates": 0,
            "owners": 0,
            "brokers": 0,
            "brokerages": 0,
            "buyers": 0,
            "sellers": 0,
            "investors": 0,
            "developers": 0,
            "mandates": 0,
            "commissions": 0,
            "owner_repasses": 0,
            "leads": 0,
            "acquisitions": 0,
            "rent_adjustments": 0,
            "media": 0,
            "common_tags": 0,
            "agenda_events": 0,
            "communications": 0,
            "help_records": 0,
            "ocr_templates": 0,
            "contract_histories": 0,
            "model_families_seeded": 0,
        }

        stats["dossier_templates"] = self._ensure_real_estate_dossier_templates()
        if self.create_help_agenda:
            self._merge_stats(stats, self._create_common_help_agenda_records(today))
        if self.create_contract_history_ocr:
            self._merge_stats(stats, self._create_contract_history_ocr_seed(today))

        assets = self._get_or_create_assets(self.contract_count)
        if not assets:
            return stats

        network = {}
        if self.create_commercial_network or self.create_owner_repasses or self.create_leads_acquisitions:
            network = self._create_property_business_network(assets, today)
            self._merge_stats(stats, network.get("stats", {}))

        for idx in range(1, self.contract_count + 1):
            asset = assets[(idx - 1) % len(assets)]
            partner, tenant = self._create_tenant(idx)
            stats["partners"] += 1 if partner else 0
            stats["tenants"] += 1 if tenant else 0

            bucket = self._contract_bucket(idx)
            start_date, end_date = self._contract_dates(idx, bucket, today)
            monthly_rent = self._rent_value(asset, idx)
            contract = self._create_contract(asset, tenant, partner, idx, bucket, start_date, end_date, monthly_rent)
            if not contract:
                continue
            stats["contracts"] += 1

            self._merge_stats(stats, self._enrich_contract_with_business_flow(contract, idx, today, network))

            if self._create_authorized_payer(contract, partner, idx):
                stats["authorized_payers"] += 1

            self._activate_or_generate_rents(contract)
            self._set_contract_bucket(contract, bucket)

            rents_created, payments_created, proofs_created = self._shape_rents(contract, idx, bucket, today)
            stats["rents"] += rents_created
            stats["payments"] += payments_created
            stats["proofs"] += proofs_created

            if self.create_dossiers and idx <= max(10, self.contract_count // 2):
                dossier, docs = self._create_contract_dossier(contract, idx, today)
                if dossier:
                    stats["dossiers"] += 1
                    stats["documents"] += docs

            if self.create_governance_cases and idx % 5 == 0:
                if self._create_governance_case(contract, idx, today):
                    stats["governance_cases"] += 1

            if self.create_amendments and idx % 7 == 0:
                if self._create_amendment(contract, idx, today):
                    stats["amendments"] += 1

            if self.create_operations and idx % 6 == 0:
                stats["operations"] += self._create_operations(contract, idx, today)

            if self.create_valuation_data and idx % 4 == 0:
                stats["valuation_records"] += self._create_valuation_data(contract.asset_id, idx, today)

            if idx % 25 == 0:
                self.env.cr.commit()

        if self.create_owner_repasses:
            self._merge_stats(stats, self._create_owner_repasses_for_demo(today, network))

        stats["model_families_seeded"] = len([v for v in [
            stats.get("contracts"), stats.get("rents"), stats.get("payments"), stats.get("proofs"),
            stats.get("owners"), stats.get("brokers"), stats.get("mandates"), stats.get("commissions"),
            stats.get("dossiers"), stats.get("documents"), stats.get("governance_cases"), stats.get("valuation_records"),
            stats.get("media"), stats.get("help_records"), stats.get("contract_histories"), stats.get("agenda_events"),
        ] if v])
        return stats

    def _contract_bucket(self, idx):
        if idx % 10 == 0:
            return "closed"
        if idx % 8 == 0:
            return "defaulting"
        if idx % 6 == 0:
            return "expiring"
        return "active"

    def _contract_dates(self, idx, bucket, today):
        if bucket == "closed":
            start = today - relativedelta(months=self.months_past + 18 + (idx % 8))
            end = today - relativedelta(months=1 + (idx % 4))
            return start, end
        if bucket == "expiring":
            start = today - relativedelta(months=self.months_past + (idx % 5))
            end = today + relativedelta(days=20 + idx)
            return start, end
        start = today - relativedelta(months=self.months_past + (idx % 6))
        end = today + relativedelta(months=self.months_future + (idx % 10))
        return start, end

    def _rent_value(self, asset, idx):
        base = getattr(asset, "rental_value", 0.0) or getattr(asset, "current_monthly_rent", 0.0) or 0.0
        if not base:
            base = 2500.0 + (idx % 12) * 850.0
            if getattr(asset, "asset_type", False) in ("commercial", "industrial", "mixed", "land"):
                base += 3500.0
        return round(base, 2)

    def _get_or_create_assets(self, count):
        Asset = self.env["property.asset"].sudo()
        domain = [("company_id", "=", self.company_id.id)] if "company_id" in Asset._fields else []
        assets = Asset.search(domain, order="id asc", limit=count)
        if len(assets) >= count:
            return assets

        country = self._ref("base.br")
        for i in range(1, count - len(assets) + 1):
            vals = {
                "name": "%s Imóvel Fallback %03d" % (PREFIX, i),
                "asset_type": "commercial" if i % 3 else "residential",
                "permitted_use": "commercial" if i % 3 else "residential",
                "construction_standard": "medium",
                "status": "available",
                "address": "Alameda Demo %s" % i,
                "address_number": str(1000 + i),
                "neighborhood": "Tamboré" if i % 2 else "Alphaville",
                "city": "Barueri",
                "state_name": "SP",
                "zip_code": "06460-000",
                "total_area": 80 + i * 4,
                "useful_area": 65 + i * 3,
                "rental_value": 3000 + i * 350,
                "notes": "<p>%s - imóvel fallback criado porque a base não tinha imóveis suficientes.</p>" % PREFIX,
                "company_id": self.company_id.id,
            }
            if country:
                vals["country_id"] = country.id
            assets |= Asset.create(self._filter_vals(Asset, vals))
        return assets

    def _cpf(self, seed):
        base = "%09d" % (100000000 + int(seed))
        nums = [int(d) for d in base]
        d1 = 11 - (sum((10 - i) * nums[i] for i in range(9)) % 11)
        d1 = 0 if d1 >= 10 else d1
        nums.append(d1)
        d2 = 11 - (sum((11 - i) * nums[i] for i in range(10)) % 11)
        d2 = 0 if d2 >= 10 else d2
        nums.append(d2)
        return "".join(str(n) for n in nums)

    def _create_tenant(self, idx):
        Partner = self.env["res.partner"].sudo()
        Tenant = self.env["property.tenant"].sudo()
        is_company = idx % 3 != 0
        partner = Partner.create(self._filter_vals(Partner, {
            "name": "%s Locatário %03d %s" % (PREFIX, idx, "Ltda" if is_company else "Pessoa Física"),
            "is_company": bool(is_company),
            "email": "locatario%03d.demo@example.com" % idx,
            "phone": "+55 11 4000-%04d" % idx,
            "mobile": "+55 11 99000-%04d" % idx,
            "street": "Rua dos Testes %03d" % idx,
            "city": "Barueri",
            "zip": "06460-000",
            "vat": self._cpf(idx),
            "company_id": self.company_id.id,
        }))
        tenant = Tenant.create(self._filter_vals(Tenant, {
            "partner_id": partner.id,
            "notes": "%s - locatário criado para massa de testes enterprise." % PREFIX,
            "company_id": self.company_id.id,
        }))
        return partner, tenant

    def _create_contract(self, asset, tenant, partner, idx, bucket, start_date, end_date, monthly_rent):
        Contract = self.env["property.contract"].sudo()
        asset_type = getattr(asset, "asset_type", False)
        contract_type = "commercial" if asset_type in ("commercial", "industrial", "land", "mixed") else "residential"
        vals = {
            "name": "%s Contrato %03d - %s" % (PREFIX, idx, (asset.display_name or asset.name or "Imóvel")[:55]),
            "asset_id": asset.id,
            "tenant_id": tenant.id if tenant else False,
            "partner_id": partner.id if partner else False,
            "contract_type": contract_type,
            "sign_date": start_date - timedelta(days=7),
            "start_date": start_date,
            "end_date": end_date,
            "monthly_rent": monthly_rent,
            "deposit_value": monthly_rent * 3,
            "adjustment_index": "ipca" if idx % 2 else "igpm",
            "adjustment_period_months": 12,
            "rent_due_day": [5, 10, 15, 22][idx % 4],
            "late_fee_percent": 2.0,
            "late_interest_percent_month": 1.0,
            "late_grace_days": 0,
            "jurisdiction": "Barueri/SP",
            "additional_clauses": "<p>%s - contrato gerado para teste de fluxo imobiliário, parcelas, conciliação, dossiês e governança.</p>" % PREFIX,
            "status": "draft",
            "company_id": self.company_id.id,
        }
        return Contract.create(self._filter_vals(Contract, vals))

    def _activate_or_generate_rents(self, contract):
        try:
            contract.action_activate()
        except Exception as exc:
            _logger.warning("[%s] action_activate falhou no contrato %s: %s. Tentando gerar parcelas diretamente.", PREFIX, contract.display_name, exc)
            try:
                contract.action_generate_rents()
            except Exception as inner:
                _logger.warning("[%s] action_generate_rents também falhou no contrato %s: %s", PREFIX, contract.display_name, inner)
            self._safe_write(contract, {"status": "active"})
            if contract.asset_id:
                self._safe_write(contract.asset_id, {"status": "rented"})

    def _set_contract_bucket(self, contract, bucket):
        if bucket == "closed":
            self._safe_write(contract, {"status": "closed"})
            if contract.asset_id and not contract.asset_id.contract_ids.filtered(lambda c: c.status == "active" and c.id != contract.id):
                self._safe_write(contract.asset_id, {"status": "available"})
        elif bucket == "defaulting":
            self._safe_write(contract, {"status": "defaulting"})
        elif bucket == "expiring":
            self._safe_write(contract, {"status": "expiring"})
        else:
            self._safe_write(contract, {"status": "active"})
            if contract.asset_id:
                self._safe_write(contract.asset_id, {"status": "rented"})

    def _create_authorized_payer(self, contract, partner, idx):
        return self._safe_create("property.payment.authorized.payer", {
            "contract_id": contract.id,
            "partner_id": partner.id if partner else False,
            "name": "%s Pagador Autorizado %03d" % (PREFIX, idx),
            "vat": self._cpf(1000 + idx),
            "pix_key": "pix.demo.%03d@example.com" % idx,
            "bank_name": "Banco Demo",
            "relation_type": "company" if idx % 3 else "tenant",
            "notes": "%s - pagador autorizado para testar matching por pagador alternativo." % PREFIX,
        })

    # ------------------------------------------------------------------
    # Parcelas, recebimentos e comprovantes conciliados
    # ------------------------------------------------------------------
    def _shape_rents(self, contract, idx, bucket, today):
        rents = contract.rent_ids.sorted(lambda r: r.due_date or date.max)
        payments_created = 0
        proofs_created = 0
        for seq, rent in enumerate(rents, start=1):
            if hasattr(rent, "_ensure_base_rent_line"):
                rent._ensure_base_rent_line()
            due = rent.due_date
            if not due:
                continue
            amount_due = rent.amount_due or rent.amount or contract.monthly_rent
            if due > today:
                self._safe_write(rent, {"status": "open"})
                continue

            if bucket == "closed" or seq % 5 in (1, 2, 3):
                offset = [-2, 0, 2, 7, 12][(idx + seq) % 5]
                pay_date = due + timedelta(days=offset)
                payment = self._create_payment(rent, amount_due, pay_date, idx, seq, partial=False)
                payments_created += 1 if payment else 0
                if self.create_payment_proofs:
                    proof = self._create_payment_proof(rent, payment, amount_due, pay_date, idx, seq, offset, partial=False)
                    proofs_created += 1 if proof else 0
                self._safe_write(rent, {
                    "amount_paid": amount_due,
                    "payment_date": pay_date,
                    "payment_method": "pix",
                    "payment_notes": "%s - pagamento integral sintético." % PREFIX,
                    "status": "paid",
                    "receipt_number": "%s-REC-%03d-%03d" % (PREFIX, idx, seq),
                    "receipt_date": pay_date,
                    "receipt_state": "issued",
                })
            elif seq % 5 == 4:
                paid = round(amount_due * 0.55, 2)
                pay_date = due + timedelta(days=3)
                payment = self._create_payment(rent, paid, pay_date, idx, seq, partial=True)
                payments_created += 1 if payment else 0
                if self.create_payment_proofs:
                    proof = self._create_payment_proof(rent, payment, paid, pay_date, idx, seq, 3, partial=True)
                    proofs_created += 1 if proof else 0
                self._safe_write(rent, {
                    "amount_paid": paid,
                    "payment_date": pay_date,
                    "payment_method": "transfer",
                    "payment_notes": "%s - pagamento parcial sintético." % PREFIX,
                    "status": "partial",
                })
            else:
                self._safe_write(rent, {
                    "status": "late",
                    "payment_notes": "%s - parcela em atraso para testes de régua de cobrança." % PREFIX,
                })
        return len(rents), payments_created, proofs_created

    def _create_payment(self, rent, amount, pay_date, idx, seq, partial=False):
        return self._safe_create("property.rent.payment", {
            "rent_id": rent.id,
            "payment_date": pay_date,
            "amount": amount,
            "payment_method": "transfer" if partial else "pix",
            "notes": "%s - recebimento %s gerado para testes (%03d/%03d)." % (PREFIX, "parcial" if partial else "integral", idx, seq),
            "state": "posted",
        })

    def _create_payment_proof(self, rent, payment, amount, pay_date, idx, seq, offset, partial=False):
        payer_name = rent.partner_id.name if not partial else "%s Pagador Autorizado %03d" % (PREFIX, idx)
        transaction_id = "%s-E2E-%03d-%03d" % (PREFIX, idx, seq)
        raw_text = """
{prefix} COMPROVANTE PIX DEMO
Pagador: {payer}
Recebedor: {company}
Valor: R$ {amount:.2f}
Data: {date}
ID: {txid}
Parcela: {rent}
""".format(
            prefix=PREFIX,
            payer=payer_name,
            company=self.company_id.name,
            amount=amount,
            date=pay_date,
            txid=transaction_id,
            rent=rent.display_name,
        )
        return self._safe_create("property.payment.proof", {
            "company_id": self.company_id.id,
            "raw_text": raw_text,
            "extraction_log": "%s - comprovante criado diretamente pela massa de teste." % PREFIX,
            "payment_method": "transfer" if partial else "pix",
            "payment_date": pay_date,
            "debit_date": pay_date,
            "amount": amount,
            "payer_name": payer_name,
            "payer_vat": self._cpf(1000 + idx) if partial else (rent.partner_id.vat or False),
            "pix_key": "pix.demo.%03d@example.com" % idx,
            "receiver_name": self.company_id.name,
            "transaction_id": transaction_id,
            "bank_name": "Banco Demo",
            "contract_id": rent.contract_id.id,
            "rent_id": rent.id,
            "payment_id": payment.id if payment else False,
            "confidence_score": 96.0 if not partial else 88.0,
            "proof_type": "normal",
            "late_handling": "waive" if offset > 0 else "none",
            "state": "reconciled",
        })

    # ------------------------------------------------------------------
    # Dossiês e documentos
    # ------------------------------------------------------------------

    def _ensure_real_estate_dossier_templates(self):
        """Cria templates imobiliários sem declarar dependência dura no XML.

        O módulo de massa de teste precisa ser instalável mesmo quando os módulos
        opcionais de dossiê/governança ainda não estiverem carregados. Por isso
        os templates são criados dinamicamente apenas quando os models existem.
        """
        Template = self._get_model("document.dossier.template")
        Line = self._get_model("document.dossier.template.line")
        if Template is False or Line is False:
            return 0

        specs = [
            {
                "code": "REAL_ESTATE_LEASE_COMMERCIAL_FULL",
                "name": "Locação Comercial - Dossiê Completo",
                "sequence": 10,
                "process_xmlids": ["document_dossier.process_property_lease"],
                "description": "Checklist completo para contrato de locação comercial, garantias, documentos societários, vistorias e governança.",
                "lines": [
                    (10, "Contrato de locação assinado", "document_core.doc_type_legal_lease_contract", True),
                    (20, "Minuta aprovada", "document_core.doc_type_legal_contract_draft", False),
                    (30, "Documentos do locatário / representante", "document_core.doc_type_identity_legal_representative_id", True),
                    (40, "Comprovante de endereço", "document_core.doc_type_identity_address_proof", True),
                    (50, "Garantia locatícia", "document_core.doc_type_commercial_guarantee", True),
                    (60, "Seguro fiança / apólice", "document_core.doc_type_commercial_insurance_bond", False),
                    (70, "Laudo de vistoria inicial", "document_core.doc_type_commercial_initial_inspection_term", True),
                    (80, "Matrícula / registro do imóvel", "document_core.doc_type_legal_title_registry", True),
                    (90, "AVCB / licença aplicável", "document_core.doc_type_regulatory_avcb", False),
                    (100, "Parecer jurídico", "document_core.doc_type_governance_legal_opinion", False),
                ],
            },
            {
                "code": "REAL_ESTATE_LEASE_RESIDENTIAL_PF",
                "name": "Locação Residencial - Pessoa Física",
                "sequence": 20,
                "process_xmlids": ["document_dossier.process_property_lease"],
                "description": "Checklist para locação residencial com documentos pessoais, garantia, vistoria e contrato.",
                "lines": [
                    (10, "Contrato de locação assinado", "document_core.doc_type_legal_lease_contract", True),
                    (20, "RG ou CNH", "document_core.doc_type_identity_rg", True),
                    (30, "CPF", "document_core.doc_type_identity_cpf", True),
                    (40, "Comprovante de endereço", "document_core.doc_type_identity_address_proof", True),
                    (50, "Comprovante de estado civil", "document_core.doc_type_identity_marital_status_proof", False),
                    (60, "Garantia locatícia", "document_core.doc_type_commercial_guarantee", True),
                    (70, "Termo de entrega de chaves", "document_core.doc_type_protocol_keys_delivery_term", True),
                    (80, "Laudo fotográfico", "document_core.doc_type_inspection_photo_report", True),
                ],
            },
            {
                "code": "REAL_ESTATE_ASSET_REGULARIZATION",
                "name": "Regularização Documental do Imóvel",
                "sequence": 30,
                "process_xmlids": ["document_dossier.process_property_purchase", "document_dossier.process_property_sale"],
                "description": "Checklist de regularidade jurídica, fiscal, técnica e operacional do imóvel.",
                "lines": [
                    (10, "Escritura", "document_core.doc_type_legal_deed", True),
                    (20, "Matrícula atualizada", "document_core.doc_type_legal_title_registry", True),
                    (30, "Certidão negativa", "document_core.doc_type_legal_negative_certificate", True),
                    (40, "Certidão de ônus", "document_core.doc_type_legal_encumbrance_certificate", True),
                    (50, "IPTU / imposto predial", "document_core.doc_type_financial_property_tax", True),
                    (60, "Habite-se", "document_core.doc_type_regulatory_habite_se", False),
                    (70, "Planta arquitetônica", "document_core.doc_type_technical_architectural_plan", False),
                    (80, "Laudo técnico", "document_core.doc_type_technical_inspection_report", False),
                    (90, "Seguro patrimonial", "document_core.doc_type_financial_insurance_policy", False),
                ],
            },
            {
                "code": "REAL_ESTATE_CONTRACT_RENEWAL_ADDENDUM",
                "name": "Renovação / Aditivo Contratual",
                "sequence": 40,
                "process_xmlids": ["document_dossier.process_property_lease"],
                "description": "Dossiê para aditivos de prazo, reajuste, garantias e revisão jurídica.",
                "lines": [
                    (10, "Aditivo contratual assinado", "document_core.doc_type_legal_contract_addendum", True),
                    (20, "Aditivo de renovação", "document_core.doc_type_legal_renewal_addendum", False),
                    (30, "Aditivo de reajuste", "document_core.doc_type_legal_adjustment_addendum", False),
                    (40, "Parecer jurídico", "document_core.doc_type_governance_legal_opinion", True),
                    (50, "Memória de cálculo do reajuste", "document_core.doc_type_financial_adjustment_calculation", False),
                    (60, "Comunicação formal às partes", "document_core.doc_type_governance_formal_communication", False),
                ],
            },
            {
                "code": "REAL_ESTATE_COLLECTION_DEFAULT",
                "name": "Cobrança / Inadimplência Locatícia",
                "sequence": 50,
                "process_xmlids": ["document_dossier.process_property_lease"],
                "description": "Dossiê para régua de cobrança, notificações, negociação, confissão de dívida e despejo.",
                "lines": [
                    (10, "Demonstrativo de débitos", "document_core.doc_type_financial_charges_statement", True),
                    (20, "Extrato do proprietário / repasse", "document_core.doc_type_financial_owner_statement", False),
                    (30, "Notificação extrajudicial", "document_core.doc_type_legal_extrajudicial_notice", True),
                    (40, "Protocolo de entrega da notificação", "document_core.doc_type_protocol_document_delivery", False),
                    (50, "Carta de cobrança", "document_core.doc_type_legal_collection_letter", False),
                    (60, "Confissão de dívida", "document_core.doc_type_legal_debt_confession", False),
                    (70, "Acordo de parcelamento", "document_core.doc_type_legal_installment_agreement", False),
                    (80, "Ação de despejo", "document_core.doc_type_legal_eviction_action", False),
                ],
            },
            {
                "code": "REAL_ESTATE_INSPECTION_DEFAULT",
                "name": "Vistoria Imobiliária",
                "sequence": 60,
                "process_xmlids": ["document_dossier.process_property_inspection"],
                "description": "Template para vistoria de entrada, saída ou intermediária, com laudos, fotos, checklist e chaves.",
                "lines": [
                    (10, "Laudo fotográfico", "document_core.doc_type_inspection_photo_report", True),
                    (20, "Checklist de vistoria", "document_core.doc_type_inspection_checklist", True),
                    (30, "Laudo de entrada", "document_core.doc_type_inspection_entry_report", False),
                    (40, "Laudo de saída", "document_core.doc_type_inspection_exit_report", False),
                    (50, "Evidências de danos", "document_core.doc_type_photo_damage_evidence", False),
                    (60, "Termo de entrega/devolução de chaves", "document_core.doc_type_protocol_keys_delivery_term", True),
                    (70, "Lista de reparos pendentes", "document_core.doc_type_inspection_repair_punch_list", False),
                ],
            },
        ]

        created_or_updated = 0
        for spec in specs:
            template = Template.search([("code", "=", spec["code"])], limit=1)
            vals = {
                "name": spec["name"],
                "code": spec["code"],
                "sequence": spec["sequence"],
                "description": spec["description"],
                "active": True,
            }
            if template:
                template.write(self._filter_vals(Template, vals))
            else:
                template = Template.create(self._filter_vals(Template, vals))
            created_or_updated += 1

            for sequence, name, xmlid, required in spec["lines"]:
                line = Line.search([("template_id", "=", template.id), ("name", "=", name)], limit=1)
                doc_type = self._ref(xmlid)
                line_vals = {
                    "template_id": template.id,
                    "sequence": sequence,
                    "name": name,
                    "document_type_id": doc_type.id if doc_type else False,
                    "required": required,
                    "requires_file": True,
                    "notes": "%s - item criado pelo seed imobiliário enterprise." % PREFIX,
                }
                if line:
                    line.write(self._filter_vals(Line, line_vals))
                else:
                    Line.create(self._filter_vals(Line, line_vals))

            for process_xmlid in spec.get("process_xmlids", []):
                process = self._ref(process_xmlid)
                if process and "template_ids" in process._fields:
                    process.write({"template_ids": [(4, template.id)]})

        return created_or_updated

    def _create_contract_dossier(self, contract, idx, today):
        Dossier = self._get_model("dossier.dossier")
        if Dossier is False:
            return False, 0
        process = self._ref("document_dossier.process_property_lease") or self.env["dossier.process"].sudo().search([("domain", "=", "property")], limit=1)
        if not process:
            return False, 0
        dossier = Dossier.create(self._filter_vals(Dossier, {
            "name": "%s Dossiê Contrato %03d - %s" % (PREFIX, idx, contract.partner_id.name[:40]),
            "description": "%s - dossiê criado para testar pendências, documentos obrigatórios e vínculo com contrato." % PREFIX,
            "process_id": process.id,
            "target_model": "property.contract",
            "target_res_id": contract.id,
            "target_name": contract.display_name,
            "responsible_id": self.env.user.id,
            "created_date": today,
            "target_date": today + timedelta(days=15),
            "state": "draft",
        }))
        before = len(dossier.document_ids)
        try:
            dossier.apply_templates(create_only_missing=True)
        except Exception as exc:
            _logger.warning("[%s] Falha ao aplicar template no dossiê %s: %s", PREFIX, dossier.display_name, exc)
        docs = dossier.document_ids
        for doc_seq, doc in enumerate(docs, start=1):
            vals = {"notes": "%s - documento de dossiê gerado em massa de teste." % PREFIX}
            if doc_seq % 3 != 0:
                vals.update({
                    "issue_date": today - timedelta(days=30 + doc_seq),
                    "received_date": today - timedelta(days=25 + doc_seq),
                    "has_physical_original": True,
                    "document_state": "active",
                    "source": "tenant" if doc_seq % 2 else "internal",
                })
                if getattr(doc, "requires_expiry", False):
                    vals["expiry_date"] = today + timedelta(days=180 + doc_seq)
                if getattr(doc, "requires_review", False):
                    vals["review_date"] = today + timedelta(days=90 + doc_seq)
                if getattr(doc, "requires_validation", False):
                    vals["validated_by"] = self.env.user.id
                    vals["validation_date"] = today - timedelta(days=20)
                self._safe_write(doc.with_context(document_core_system_defaults=True), vals)
                self._attach_demo_file(doc, idx, doc_seq)
            else:
                self._safe_write(doc.with_context(document_core_system_defaults=True), vals)
        return dossier, max(len(dossier.document_ids) - before, len(dossier.document_ids))

    def _attach_demo_file(self, doc, idx, doc_seq):
        content = ("%s\nArquivo sintético para %s\n" % (PREFIX, doc.display_name)).encode("utf-8")
        attachment = self.env["ir.attachment"].sudo().create({
            "name": "%s_documento_%03d_%02d.txt" % (PREFIX.lower(), idx, doc_seq),
            "type": "binary",
            "datas": base64.b64encode(content).decode("ascii"),
            "mimetype": "text/plain",
            "res_model": "document.document",
            "res_id": doc.id,
        })
        self._safe_write(doc, {"attachment_ids": [(4, attachment.id)], "preview_attachment_id": attachment.id})
        return attachment

    # ------------------------------------------------------------------
    # Governança, aditivos e operações
    # ------------------------------------------------------------------
    def _create_governance_case(self, contract, idx, today):
        Case = self._get_model("governance.case")
        if Case is False:
            return False
        case_type = self._ref("governance.case_type_financeiro") if idx % 2 else self._ref("governance.case_type_juridico")
        stage = self._ref("governance.stage_waiting") if idx % 2 else self._ref("governance.stage_planned")
        vals = {
            "name": "%s Caso %03d - %s" % (PREFIX, idx, contract.partner_id.name[:50]),
            "description": "<p>%s - caso vinculado ao contrato para testar governança + imóveis + documentos.</p>" % PREFIX,
            "origin_date": today - timedelta(days=idx % 30),
            "case_type_id": case_type.id if case_type else False,
            "stage_id": stage.id if stage else False,
            "priority": str(idx % 4),
            "responsible_id": self.env.user.id,
            "partner_ids": [(6, 0, [contract.partner_id.id])],
            "asset_ids": [(6, 0, [contract.asset_id.id])],
            "contract_ids": [(6, 0, [contract.id])],
            "company_id": self.company_id.id,
        }
        return Case.with_context(skip_participant_partner_sync=True).create(self._filter_vals(Case, vals))

    def _create_amendment(self, contract, idx, today):
        Amendment = self._get_model("property.contract.amendment")
        Change = self._get_model("property.contract.amendment.change")
        if Amendment is False:
            return False
        amendment = Amendment.create(self._filter_vals(Amendment, {
            "name": "%s Aditivo %03d" % (PREFIX, idx),
            "contract_id": contract.id,
            "amendment_type": self._selection(Amendment, "amendment_type", "rent_increase", "other") if idx % 2 else self._selection(Amendment, "amendment_type", "term_extension", "other"),
            "amendment_scope": "financial" if idx % 2 else "term",
            "economic_effect": "increase" if idx % 2 else "neutral",
            "risk_level": "medium",
            "status": "signed" if idx % 2 else "legal_review",
            "approval_state": "approved" if idx % 2 else "pending",
            "instrument_date": today - timedelta(days=10),
            "sign_date": today - timedelta(days=5) if idx % 2 else False,
            "effective_date": today + timedelta(days=30),
            "commercial_impact": True,
            "financial_impact": bool(idx % 2),
            "legal_impact": True,
            "requires_billing_recalculation": bool(idx % 2),
            "summary_html": "<p>%s - aditivo sintético para teste de workflow.</p>" % PREFIX,
            "note": "%s - aditivo criado para massa de testes." % PREFIX,
        }))
        if Change is not False:
            if idx % 2:
                Change.create(self._filter_vals(Change, {
                    "amendment_id": amendment.id,
                    "field_key": "current_base_rent",
                    "new_value_float": round((contract.monthly_rent or 0.0) * 1.08, 2),
                    "effective_date": today + timedelta(days=30),
                }))
            else:
                Change.create(self._filter_vals(Change, {
                    "amendment_id": amendment.id,
                    "field_key": "current_end_date",
                    "new_value_date": contract.end_date + relativedelta(months=12) if contract.end_date else today + relativedelta(months=12),
                    "effective_date": today + timedelta(days=30),
                }))
        return amendment

    def _create_operations(self, contract, idx, today):
        total = 0
        Inspection = self._get_model("property.inspection")
        Maintenance = self._get_model("property.maintenance")
        if Inspection is not False:
            Inspection.create(self._filter_vals(Inspection, {
                "inspection_type": "periodic" if idx % 2 else "entry",
                "asset_id": contract.asset_id.id,
                "contract_id": contract.id,
                "company_id": self.company_id.id,
                "scheduled_date": today + timedelta(days=idx % 20),
                "date": today - timedelta(days=idx % 15) if idx % 2 else False,
                "inspector_id": contract.partner_id.id,
                "present_ids": [(6, 0, [contract.partner_id.id])],
                "overall_condition": ["excellent", "good", "fair", "poor"][idx % 4],
                "report": "<p>%s - vistoria sintética com observações de teste.</p>" % PREFIX,
                "observations": "%s - vistoria criada na massa de testes." % PREFIX,
                "status": "done" if idx % 2 else "scheduled",
            }))
            total += 1
        if Maintenance is not False:
            Maintenance.create(self._filter_vals(Maintenance, {
                "name": "%s Manutenção %03d" % (PREFIX, idx),
                "description": "%s - manutenção sintética para testar fluxo operacional." % PREFIX,
                "maintenance_type": ["preventive", "corrective", "emergency", "improvement"][idx % 4],
                "priority": str(idx % 4),
                "responsible_party": ["owner", "tenant", "condominium"][idx % 3],
                "asset_id": contract.asset_id.id,
                "contract_id": contract.id,
                "company_id": self.company_id.id,
                "request_date": today - timedelta(days=idx % 30),
                "scheduled_date": today + timedelta(days=idx % 12),
                "completion_date": today - timedelta(days=2) if idx % 3 == 0 else False,
                "cost_estimate": 600 + idx * 35,
                "cost_actual": 550 + idx * 25 if idx % 3 == 0 else 0.0,
                "status": "done" if idx % 3 == 0 else ("scheduled" if idx % 2 else "quoted"),
            }))
            total += 1
        return total

    # ------------------------------------------------------------------
    # Valuation
    # ------------------------------------------------------------------
    def _create_valuation_data(self, asset, idx, today):
        Source = self._get_model("property.valuation.source")
        Ref = self._get_model("property.price.m2.reference")
        Comp = self._get_model("property.market.comparable")
        Run = self._get_model("property.valuation.run")
        total = 0
        source = False
        if Source is not False:
            source = Source.search([("name", "=", "%s Fonte Pesquisa Mercado" % PREFIX)], limit=1)
            if not source:
                source = Source.create(self._filter_vals(Source, {
                    "name": "%s Fonte Pesquisa Mercado" % PREFIX,
                    "source_type": "manual_research",
                    "reliability_score": 75,
                    "notes": "%s - fonte criada para avaliação de teste." % PREFIX,
                    "company_id": self.company_id.id,
                }))
                total += 1

        base_price = 55.0 + (idx % 20) * 2.5
        standard = "medium"
        if getattr(asset, "construction_standard", False) in ("simple", "medium", "high"):
            standard = asset.construction_standard
        if getattr(asset, "construction_standard", False) == "luxury":
            standard = "premium"
        asset_use_type = "commercial" if getattr(asset, "asset_type", False) != "residential" else "residential"

        if Ref is not False:
            Ref.create(self._filter_vals(Ref, {
                "valuation_type": "rent",
                "asset_use_type": asset_use_type,
                "standard": standard,
                "city": asset.city or "Barueri",
                "neighborhood": asset.neighborhood or "Alphaville",
                "price_m2": base_price,
                "valid_from": today - timedelta(days=30),
                "source_id": source.id if source else False,
                "confidence_score": 72,
                "notes": "%s - referência m² de teste." % PREFIX,
                "company_id": self.company_id.id,
            }))
            total += 1

        comparables = Comp.browse() if Comp is not False else False
        if Comp is not False:
            for n in range(1, 4):
                area = max(getattr(asset, "useful_area", 0.0) or getattr(asset, "total_area", 0.0) or 80.0, 30.0) + n * 10
                comp = Comp.create(self._filter_vals(Comp, {
                    "name": "%s Comparável %03d-%d" % (PREFIX, idx, n),
                    "asset_id": asset.id,
                    "source_id": source.id if source else False,
                    "date_observed": today - timedelta(days=10 + n),
                    "valuation_type": "rent",
                    "asset_use_type": asset_use_type,
                    "standard": standard,
                    "conservation": "good",
                    "city": asset.city or "Barueri",
                    "neighborhood": asset.neighborhood or "Alphaville",
                    "address": asset.address or "Endereço de teste",
                    "area_m2": area,
                    "total_price": round(area * (base_price + n * 3), 2),
                    "weight": 1.0,
                    "notes": "%s - comparável sintético." % PREFIX,
                    "company_id": self.company_id.id,
                }))
                comparables |= comp
                total += 1

        if Run is not False:
            try:
                run = Run.create(self._filter_vals(Run, {
                    "asset_id": asset.id,
                    "valuation_date": today,
                    "valuation_type": "rent",
                    "state": "draft",
                    "algorithm_code": "hybrid",
                    "area_m2": max(getattr(asset, "useful_area", 0.0) or getattr(asset, "total_area", 0.0) or 80.0, 30.0),
                    "city": asset.city or "Barueri",
                    "neighborhood": asset.neighborhood or "Alphaville",
                    "asset_use_type": asset_use_type,
                    "standard": standard,
                    "conservation": "good",
                    "source_ids": [(6, 0, [source.id])] if source else False,
                    "comparable_ids": [(6, 0, comparables.ids)] if comparables else False,
                    "base_price_m2": base_price,
                    "review_notes": "%s - estimativa criada para massa de testes." % PREFIX,
                    "company_id": self.company_id.id,
                }))
                if hasattr(run, "action_calculate"):
                    try:
                        run.action_calculate()
                    except Exception as exc:
                        _logger.info("[%s] cálculo de valuation ignorado: %s", PREFIX, exc)
                total += 1
            except Exception as exc:
                _logger.info("[%s] criação de valuation.run ignorada: %s", PREFIX, exc)
        return total

    # ------------------------------------------------------------------
    # Cobertura ampliada: stakeholders, corretores, mandatos, leads,
    # comissões, repasses, histórico OCR, ajuda, agenda e comunicação.
    # ------------------------------------------------------------------
    def _create_property_business_network(self, assets, today):
        stats = {
            "owners": 0,
            "brokers": 0,
            "brokerages": 0,
            "buyers": 0,
            "sellers": 0,
            "investors": 0,
            "developers": 0,
            "common_tags": 0,
            "media": 0,
        }
        network = {"stats": stats}

        stats["common_tags"] += self._ensure_common_tags()
        owners = self._create_demo_owners(max(4, min(12, max(1, self.contract_count // 6)))) if self.create_owner_repasses else self.env["property.owner"].browse()
        brokerages, brokers = self._create_demo_brokerages_and_brokers(max(2, min(6, max(1, self.contract_count // 12))), max(4, min(18, max(2, self.contract_count // 4)))) if self.create_commercial_network else (self._safe_browse("property.brokerage"), self._safe_browse("property.broker"))
        buyers, sellers, investors, developers = self._create_demo_market_parties(max(3, min(10, max(1, self.contract_count // 8)))) if self.create_leads_acquisitions else (self._safe_browse("property.buyer"), self._safe_browse("property.seller"), self._safe_browse("property.investor"), self._safe_browse("property.developer"))

        stats["owners"] += len(owners)
        stats["brokerages"] += len(brokerages)
        stats["brokers"] += len(brokers)
        stats["buyers"] += len(buyers)
        stats["sellers"] += len(sellers)
        stats["investors"] += len(investors)
        stats["developers"] += len(developers)

        if assets:
            self._assign_assets_to_network(assets, owners, brokers)
            if self.create_media_gallery:
                stats["media"] += self._create_media_for_assets(assets, today)

        network.update({
            "owners": owners,
            "brokerages": brokerages,
            "brokers": brokers,
            "buyers": buyers,
            "sellers": sellers,
            "investors": investors,
            "developers": developers,
        })
        return network

    def _safe_browse(self, model_name):
        Model = self._get_model(model_name)
        return Model.browse() if Model is not False else False

    def _ensure_common_tags(self):
        Tag = self._get_model("common.tag")
        if Tag is False:
            return 0
        created = 0
        for seq, (name, category, desc) in enumerate([
            ("%s Alta prioridade" % PREFIX, "general", "Usado para testar filtros e indicadores de urgência."),
            ("%s Comercial" % PREFIX, "property", "Fluxos comerciais, corretores, leads e mandatos."),
            ("%s Documentação pendente" % PREFIX, "governance", "Pendências de documentos e dossiês."),
            ("%s Financeiro" % PREFIX, "financial", "Parcelas, repasses, cobrança e conciliação."),
            ("%s Manutenção" % PREFIX, "maintenance", "Vistorias, chamados técnicos e orçamento."),
        ], start=1):
            tag = Tag.search([("name", "=", name)], limit=1)
            if not tag:
                self._safe_create_optional("common.tag", {
                    "name": name,
                    "sequence": seq * 10,
                    "category": self._selection(Tag, "category", category, "general"),
                    "description": desc,
                    "company_id": self.company_id.id,
                }, "common.tag")
                created += 1
        return created

    def _create_demo_owners(self, count):
        Owner = self._get_model("property.owner")
        if Owner is False:
            return False
        owners = Owner.browse()
        for i in range(1, count + 1):
            name = "%s Proprietário %02d %s" % (PREFIX, i, "Holding" if i % 2 else "Pessoa Física")
            owner = Owner.search([("name", "=", name)], limit=1)
            if not owner:
                owner = self._safe_create_optional("property.owner", {
                    "name": name,
                    "cpf_cnpj": self._cpf(20000 + i),
                    "email": "owner%02d.demo@example.com" % i,
                    "phone": "+55 11 4200-%04d" % i,
                    "mobile": "+55 11 99200-%04d" % i,
                    "street": "Rua dos Proprietários %02d" % i,
                    "city": "Barueri",
                    "state_name": "SP",
                    "is_company": bool(i % 2),
                    "bank_name": "Banco Demo",
                    "bank_agency": "%04d" % (1000 + i),
                    "bank_account": "000%s-0" % i,
                    "pix_key": "owner%02d.demo@example.com" % i,
                    "notes": "%s - proprietário sintético para testar repasses, portfolio e contratos." % PREFIX,
                    "company_id": self.company_id.id,
                }, "property.owner")
            if owner:
                owners |= owner
        return owners

    def _create_demo_brokerages_and_brokers(self, brokerage_count, broker_count):
        Brokerage = self._get_model("property.brokerage")
        Broker = self._get_model("property.broker")
        if Broker is False:
            return False, False
        brokerages = Brokerage.browse() if Brokerage is not False else False
        brokers = Broker.browse()
        if Brokerage is not False:
            for i in range(1, brokerage_count + 1):
                partner = self._demo_partner("BROKERAGE%02d" % i, "%s Imobiliária Parceira %02d" % (PREFIX, i), True, 21000 + i, "brokerage%02d" % i)
                brokerage = Brokerage.search([("partner_id", "=", partner.id)], limit=1)
                if not brokerage:
                    brokerage = self._safe_create_optional("property.brokerage", {
                        "partner_id": partner.id,
                        "notes": "%s - imobiliária/parceira para testar corretores e mandatos." % PREFIX,
                        "company_id": self.company_id.id,
                    }, "property.brokerage")
                if brokerage:
                    brokerages |= brokerage
        for i in range(1, broker_count + 1):
            name = "%s Corretor %02d" % (PREFIX, i)
            broker = Broker.search([("name", "=", name)], limit=1)
            if not broker:
                brokerage = brokerages[(i - 1) % len(brokerages)] if brokerages else False
                broker = self._safe_create_optional("property.broker", {
                    "name": name,
                    "email": "corretor%02d.demo@example.com" % i,
                    "phone": "+55 11 4300-%04d" % i,
                    "mobile": "+55 11 99300-%04d" % i,
                    "creci": "CRECI-SP %06d-F" % (9000 + i),
                    "company_name": brokerage.name if brokerage else "DEMO Imobiliária",
                    "brokerage_id": brokerage.id if brokerage else False,
                    "commission_rate": [4.0, 5.0, 6.0][i % 3],
                    "notes": "%s - corretor sintético para testar autorização, leads e comissões." % PREFIX,
                    "company_id": self.company_id.id,
                }, "property.broker")
            if broker:
                brokers |= broker
        return brokerages, brokers

    def _create_demo_market_parties(self, count):
        Buyer = self._get_model("property.buyer")
        Seller = self._get_model("property.seller")
        Investor = self._get_model("property.investor")
        Developer = self._get_model("property.developer")
        buyers = Buyer.browse() if Buyer is not False else False
        sellers = Seller.browse() if Seller is not False else False
        investors = Investor.browse() if Investor is not False else False
        developers = Developer.browse() if Developer is not False else False
        for i in range(1, count + 1):
            if Buyer is not False:
                partner = self._demo_partner("BUYER%02d" % i, "%s Comprador %02d" % (PREFIX, i), i % 2 == 0, 22000 + i, "buyer%02d" % i)
                rec = Buyer.search([("partner_id", "=", partner.id)], limit=1) or self._safe_create_optional("property.buyer", {"partner_id": partner.id, "notes": "%s - comprador para funil de aquisição/venda." % PREFIX, "company_id": self.company_id.id}, "property.buyer")
                if rec: buyers |= rec
            if Seller is not False:
                partner = self._demo_partner("SELLER%02d" % i, "%s Vendedor %02d" % (PREFIX, i), i % 3 == 0, 23000 + i, "seller%02d" % i)
                rec = Seller.search([("partner_id", "=", partner.id)], limit=1) or self._safe_create_optional("property.seller", {"partner_id": partner.id, "notes": "%s - vendedor para oportunidades de aquisição." % PREFIX, "company_id": self.company_id.id}, "property.seller")
                if rec: sellers |= rec
            if Investor is not False:
                partner = self._demo_partner("INVESTOR%02d" % i, "%s Investidor %02d" % (PREFIX, i), True, 24000 + i, "investor%02d" % i)
                rec = Investor.search([("partner_id", "=", partner.id)], limit=1) or self._safe_create_optional("property.investor", {"partner_id": partner.id, "investment_profile": ["income", "growth", "mixed"][i % 3], "notes": "%s - investidor para análise de aquisição." % PREFIX, "company_id": self.company_id.id}, "property.investor")
                if rec: investors |= rec
            if Developer is not False:
                partner = self._demo_partner("DEVELOPER%02d" % i, "%s Incorporadora %02d" % (PREFIX, i), True, 25000 + i, "developer%02d" % i)
                rec = Developer.search([("partner_id", "=", partner.id)], limit=1) or self._safe_create_optional("property.developer", {"partner_id": partner.id, "notes": "%s - incorporadora para fluxo de aquisição/desenvolvimento." % PREFIX, "company_id": self.company_id.id}, "property.developer")
                if rec: developers |= rec
        return buyers, sellers, investors, developers

    def _assign_assets_to_network(self, assets, owners, brokers):
        if not assets:
            return
        for idx, asset in enumerate(assets, start=1):
            vals = {}
            if owners and "owner_id" in asset._fields:
                vals["owner_id"] = owners[(idx - 1) % len(owners)].id
            if brokers and "exclusive_broker_id" in asset._fields:
                vals["exclusive_broker_id"] = brokers[(idx - 1) % len(brokers)].id
                vals["authorized_broker_ids"] = [(6, 0, brokers[max(0, idx - 2) % len(brokers):(idx % len(brokers)) + 1].ids or [brokers[(idx - 1) % len(brokers)].id])]
                vals["is_exclusive"] = bool(idx % 4 == 0)
                vals["website_visibility"] = self._selection(asset, "website_visibility", "restricted_brokers", "public")
            if "website_published" in asset._fields:
                vals["website_published"] = bool(idx % 3 != 0)
                vals["publish_start_date"] = date.today() - timedelta(days=idx % 20)
                vals["publish_end_date"] = date.today() + timedelta(days=90 + idx)
            if vals:
                self._safe_write(asset, vals)

    def _enrich_contract_with_business_flow(self, contract, idx, today, network):
        stats = {"mandates": 0, "commissions": 0, "leads": 0, "acquisitions": 0, "rent_adjustments": 0}
        brokers = (network or {}).get("brokers")
        owners = (network or {}).get("owners")
        buyers = (network or {}).get("buyers")
        sellers = (network or {}).get("sellers")
        investors = (network or {}).get("investors")
        developers = (network or {}).get("developers")
        broker = brokers[(idx - 1) % len(brokers)] if brokers else False
        owner = owners[(idx - 1) % len(owners)] if owners else False

        if owner and contract.asset_id and "owner_id" in contract.asset_id._fields:
            self._safe_write(contract.asset_id, {"owner_id": owner.id})

        if self.create_commercial_network and broker:
            assignment = self._create_broker_assignment(contract, broker, idx, today)
            stats["mandates"] += 1 if assignment else 0
            commission = self._create_contract_commission(contract, broker, idx, today)
            stats["commissions"] += 1 if commission else 0
            if assignment and commission and "commission_id" in assignment._fields:
                self._safe_write(assignment, {"commission_id": commission.id, "contract_id": contract.id})

        if self.create_leads_acquisitions:
            stats["leads"] += self._create_leads_for_asset(contract.asset_id, broker, idx)
            if idx % 5 == 0:
                acq = self._create_acquisition_opportunity(contract.asset_id, broker, idx, today, buyers, sellers, investors, developers)
                stats["acquisitions"] += 1 if acq else 0

        if idx % 9 == 0:
            adj = self._create_rent_adjustment(contract, idx, today)
            stats["rent_adjustments"] += 1 if adj else 0
        return stats

    def _create_broker_assignment(self, contract, broker, idx, today):
        Assignment = self._get_model("property.broker.assignment")
        if Assignment is False or not contract.asset_id:
            return False
        return self._safe_create_optional("property.broker.assignment", {
            "asset_id": contract.asset_id.id,
            "broker_id": broker.id,
            "assignment_type": "both" if idx % 4 == 0 else "rental",
            "exclusive": bool(idx % 6 == 0),
            "start_date": contract.start_date or today,
            "end_date": (contract.end_date or today) + relativedelta(months=1),
            "contract_id": contract.id,
            "notes": "%s - mandato criado para testar controle de corretor, exclusividade e conversão em contrato." % PREFIX,
            "company_id": self.company_id.id,
        }, "property.broker.assignment")

    def _create_contract_commission(self, contract, broker, idx, today):
        Commission = self._get_model("property.commission")
        if Commission is False:
            return False
        status = "paid" if idx % 3 == 0 else ("cancelled" if idx % 17 == 0 else "pending")
        deal_date = contract.sign_date or contract.start_date or today
        vals = {
            "commission_type": "rental",
            "broker_id": broker.id,
            "contract_id": contract.id,
            "base_value": (contract.monthly_rent or 0.0) * 12,
            "commission_rate": broker.commission_rate or 6.0,
            "deal_date": deal_date,
            "due_date": deal_date + timedelta(days=30),
            "payment_date": deal_date + timedelta(days=35) if status == "paid" else False,
            "status": status,
            "notes": "%s - comissão sintética sobre contrato de locação." % PREFIX,
            "company_id": self.company_id.id,
        }
        return self._safe_create_optional("property.commission", vals, "property.commission")

    def _create_leads_for_asset(self, asset, broker, idx):
        if not asset:
            return 0
        Lead = self._get_model("property.lead")
        if Lead is False:
            return 0
        count = 0
        for n in range(1, 3 if idx % 3 == 0 else 2):
            lead = self._safe_create_optional("property.lead", {
                "name": "%s Lead %03d-%d" % (PREFIX, idx, n),
                "email": "lead%03d_%d.demo@example.com" % (idx, n),
                "phone": "+55 11 4400-%04d" % (idx * 10 + n),
                "asset_id": asset.id,
                "interest_type": ["rent", "buy", "both"][(idx + n) % 3],
                "message": "%s - interessado sintético para testar funil, origem e corretor responsável." % PREFIX,
                "source_channel": ["website_public", "website_portal", "website_broker", "internal"][(idx + n) % 4],
                "access_profile": "demo-corretor" if broker and n % 2 == 0 else "demo-publico",
                "broker_id": broker.id if broker and n % 2 == 0 else False,
                "status": ["new", "contacted", "qualified", "lost"][(idx + n) % 4],
                "company_id": self.company_id.id,
            }, "property.lead")
            count += 1 if lead else 0
        return count

    def _create_acquisition_opportunity(self, asset, broker, idx, today, buyers, sellers, investors, developers):
        Acquisition = self._get_model("property.acquisition")
        if Acquisition is False:
            return False
        seller = sellers[(idx - 1) % len(sellers)] if sellers else False
        buyer = buyers[(idx - 1) % len(buyers)] if buyers else False
        investor = investors[(idx - 1) % len(investors)] if investors else False
        developer = developers[(idx - 1) % len(developers)] if developers else False
        asking = 450000 + idx * 25000
        offer = asking * 0.92
        agreed = asking * 0.95 if idx % 2 == 0 else 0.0
        return self._safe_create_optional("property.acquisition", {
            "name": "%s Aquisição %03d - %s" % (PREFIX, idx, asset.name[:40] if asset else "Imóvel"),
            "priority": str(idx % 3),
            "asset_type": getattr(asset, "asset_type", False) or "commercial",
            "address": getattr(asset, "address", False) or "Rua Demo Aquisição",
            "city": getattr(asset, "city", False) or "Barueri",
            "state_name": getattr(asset, "state_name", False) or "SP",
            "neighborhood": getattr(asset, "neighborhood", False) or "Alphaville",
            "zip_code": getattr(asset, "zip_code", False) or "06460-000",
            "total_area": getattr(asset, "total_area", 0.0) or 120.0,
            "useful_area": getattr(asset, "useful_area", 0.0) or 95.0,
            "seller_partner_id": seller.partner_id.id if seller and seller.partner_id else False,
            "seller_id": seller.id if seller else False,
            "buyer_id": buyer.id if buyer else False,
            "investor_id": investor.id if investor else False,
            "developer_id": developer.id if developer else False,
            "broker_id": broker.id if broker else False,
            "asking_price": asking,
            "offer_price": offer,
            "agreed_price": agreed,
            "estimated_renovation": 35000 + idx * 250,
            "estimated_rent": 4500 + idx * 120,
            "prospect_date": today - timedelta(days=idx),
            "expected_close_date": today + timedelta(days=45 + idx),
            "dd_legal_docs": bool(idx % 2),
            "dd_registration": bool(idx % 3),
            "dd_iptu_clear": bool(idx % 4),
            "dd_environmental": bool(idx % 5),
            "dd_structural": bool(idx % 6),
            "dd_notes": "%s - checklist de due diligence sintético." % PREFIX,
            "description": "Oportunidade criada para homologar funil de aquisição e relação com corretores.",
            "notes": "<p>%s - aquisição sintética.</p>" % PREFIX,
            "stage": ["prospecting", "analysis", "negotiation", "due_diligence", "closing"][(idx // 5) % 5],
            "company_id": self.company_id.id,
        }, "property.acquisition")

    def _create_rent_adjustment(self, contract, idx, today):
        Adjustment = self._get_model("property.rent.adjustment")
        if Adjustment is False:
            return False
        previous = contract.monthly_rent or 1.0
        return self._safe_create_optional("property.rent.adjustment", {
            "contract_id": contract.id,
            "index_type": "ipca" if idx % 2 else "igpm",
            "period_months": 12,
            "index_rate": 4.2 + (idx % 5) * 0.3,
            "previous_rent": previous,
            "adjustment_date": today - timedelta(days=15),
            "effective_date": today + timedelta(days=15),
            "status": "applied" if idx % 2 else "draft",
            "notes": "%s - reajuste de aluguel sintético para testar histórico e agenda." % PREFIX,
        }, "property.rent.adjustment")

    def _create_owner_repasses_for_demo(self, today, network):
        stats = {"owner_repasses": 0}
        owners = (network or {}).get("owners")
        if not owners:
            owners = self._safe_search("property.owner", [("name", "ilike", PREFIX)])
        Repasse = self._get_model("property.owner.repasse")
        if Repasse is False or not owners:
            return stats
        for owner in owners:
            for months_back in range(1, 4):
                ref_date = today - relativedelta(months=months_back)
                first = ref_date.replace(day=1)
                last = first + relativedelta(months=1, days=-1)
                domain = [("contract_id.asset_id.owner_id", "=", owner.id), ("status", "=", "paid"), ("due_date", ">=", first), ("due_date", "<=", last)]
                rents = self._safe_search("property.rent", domain)
                commissions = self._safe_search("property.commission", [("contract_id.asset_id.owner_id", "=", owner.id), ("status", "=", "paid")])
                maintenance = self._safe_search("property.maintenance", [("asset_id.owner_id", "=", owner.id), ("status", "=", "done")])
                repasse = self._safe_create_optional("property.owner.repasse", {
                    "owner_id": owner.id,
                    "period_month": first.month,
                    "period_year": first.year,
                    "date_from": first,
                    "date_to": last,
                    "state": "paid" if months_back >= 2 else "confirmed",
                    "rent_ids": [(6, 0, rents.ids)] if rents else False,
                    "commission_ids": [(6, 0, commissions.ids[:3])] if commissions else False,
                    "maintenance_ids": [(6, 0, maintenance.ids[:3])] if maintenance else False,
                    "management_fee_pct": 10.0,
                    "payment_date": last + timedelta(days=5) if months_back >= 2 else False,
                    "notes": "%s - repasse mensal sintético ao proprietário." % PREFIX,
                    "company_id": self.company_id.id,
                }, "property.owner.repasse")
                stats["owner_repasses"] += 1 if repasse else 0
        return stats

    def _create_media_for_assets(self, assets, today):
        Media = self._get_model("property.media")
        Category = self._get_model("property.media.category")
        if Media is False or Category is False:
            return 0
        created = 0
        cat_specs = [
            ("DEMO_GALLERY", "%s Galeria Comercial" % PREFIX, "asset_gallery", "image"),
            ("DEMO_TECH_DOC", "%s Documento Técnico" % PREFIX, "document_support", "document"),
            ("DEMO_INSPECTION", "%s Vistoria" % PREFIX, "inspection", "image"),
            ("DEMO_MAINTENANCE", "%s Manutenção" % PREFIX, "maintenance", "image"),
        ]
        categories = {}
        for code, name, purpose, kind in cat_specs:
            cat = Category.search([("code", "=", "%s_%s" % (PREFIX, code))], limit=1)
            if not cat:
                cat = self._safe_create_optional("property.media.category", {
                    "name": name,
                    "code": "%s_%s" % (PREFIX, code),
                    "applicable_purpose": self._selection(Category, "applicable_purpose", purpose, "all"),
                    "default_content_kind": self._selection(Category, "default_content_kind", kind, "image"),
                    "publishable_default": purpose == "asset_gallery",
                    "description": "%s - categoria criada para massa de testes." % PREFIX,
                }, "property.media.category")
            if cat:
                categories[purpose] = cat
        # PNG 1x1 transparente, suficiente para passar validação do campo Image.
        png_1x1 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
        text_data = base64.b64encode(("%s arquivo técnico sintético" % PREFIX).encode("utf-8")).decode("ascii")
        for idx, asset in enumerate(assets[:min(len(assets), max(10, self.contract_count // 2))], start=1):
            media = self._safe_create_optional("property.media", {
                "name": "%s Foto Fachada %03d" % (PREFIX, idx),
                "asset_id": asset.id,
                "purpose": "asset_gallery",
                "category_id": categories.get("asset_gallery").id if categories.get("asset_gallery") else False,
                "content_kind": "image",
                "media_role": "gallery",
                "visibility_level": "public",
                "website_published": bool(idx % 2),
                "publication_state": "published" if idx % 2 else "approved",
                "is_cover": bool(idx == 1),
                "image_1920": png_1x1,
                "caption": "Fachada demonstrativa",
                "description": "%s - imagem sintética para testar galeria, site e permissões." % PREFIX,
                "location_note": "Fachada",
                "date_taken": fields.Datetime.now(),
                "company_id": self.company_id.id,
            }, "property.media")
            created += 1 if media else 0
            media_doc = self._safe_create_optional("property.media", {
                "name": "%s Memorial Técnico %03d" % (PREFIX, idx),
                "asset_id": asset.id,
                "purpose": "document_support",
                "category_id": categories.get("document_support").id if categories.get("document_support") else False,
                "content_kind": "document",
                "media_role": "document_support",
                "visibility_level": "internal",
                "publication_state": "draft",
                "file_data": text_data,
                "file_name": "%s_memorial_%03d.txt" % (PREFIX.lower(), idx),
                "caption": "Documento técnico demonstrativo",
                "description": "%s - arquivo de apoio para documento/imóvel." % PREFIX,
                "company_id": self.company_id.id,
            }, "property.media")
            created += 1 if media_doc else 0
        return created

    def _create_common_help_agenda_records(self, today):
        stats = {"help_records": 0, "agenda_events": 0, "communications": 0}
        # Central de ajuda: cria registros apenas se o módulo existir.
        Category = self._get_model("help.category")
        Tag = self._get_model("help.tag")
        Article = self._get_model("help.article")
        ChecklistTemplate = self._get_model("help.checklist.template")
        ChecklistItem = self._get_model("help.checklist.item")
        Tip = self._get_model("help.tip")
        Context = self._get_model("help.context")
        Rule = self._get_model("help.suggestion.rule")
        Learning = self._get_model("help.learning.path")
        Step = self._get_model("help.learning.step")
        tag = False
        category = False
        if Tag is not False:
            tag = Tag.search([("name", "=", "%s Imobiliário" % PREFIX)], limit=1) or self._safe_create_optional("help.tag", {"name": "%s Imobiliário" % PREFIX, "description": "Tag demo para artigos de imóveis."}, "help.tag")
            stats["help_records"] += 1 if tag else 0
        if Category is not False:
            category = Category.search([("code", "=", "%s_HELP_IMOB" % PREFIX)], limit=1) or self._safe_create_optional("help.category", {"name": "%s Ajuda Imobiliária" % PREFIX, "code": "%s_HELP_IMOB" % PREFIX, "sequence": 900}, "help.category")
            stats["help_records"] += 1 if category else 0
        if Article is not False:
            vals = {
                "name": "%s Como testar massa imobiliária" % PREFIX,
                "code": "%s.HELP.MASSA.IMOB" % PREFIX,
                "category_id": category.id if category else False,
                "tag_ids": [(6, 0, [tag.id])] if tag else False,
                "module_name": "property_demo_enterprise_seed",
                "model_name": "property.contract",
                "view_type": "form",
                "article_type": self._selection(Article, "article_type", "howto", "guide"),
                "content_scope": self._selection(Article, "content_scope", "functional", "general"),
                "audience": self._selection(Article, "audience", "user", "all"),
                "body_html": "<p>%s - artigo sintético para testar central de ajuda e contexto.</p>" % PREFIX,
                "sequence": 900,
            }
            if not Article.search([("code", "=", vals["code"])], limit=1):
                stats["help_records"] += 1 if self._safe_create_optional("help.article", vals, "help.article") else 0
        if ChecklistTemplate is not False:
            checklist = ChecklistTemplate.search([("name", "=", "%s Checklist Homologação" % PREFIX)], limit=1) or self._safe_create_optional("help.checklist.template", {"name": "%s Checklist Homologação" % PREFIX, "audience": self._selection(ChecklistTemplate, "audience", "user", "all"), "description": "%s - checklist demo." % PREFIX}, "help.checklist.template")
            if checklist:
                stats["help_records"] += 1
                if ChecklistItem is not False:
                    for seq, name in enumerate(["Verificar contratos", "Verificar parcelas", "Verificar conciliação", "Verificar governança"], start=1):
                        if not ChecklistItem.search([("template_id", "=", checklist.id), ("name", "=", "%s %s" % (PREFIX, name))], limit=1):
                            stats["help_records"] += 1 if self._safe_create_optional("help.checklist.item", {"template_id": checklist.id, "name": "%s %s" % (PREFIX, name), "sequence": seq * 10}, "help.checklist.item") else 0
        if Tip is not False:
            tip_vals = {"name": "%s Dica Dados de Teste" % PREFIX, "content": "Use o prefixo DEMO-IMOB para filtrar todos os registros de homologação.", "audience": self._selection(Tip, "audience", "user", "all"), "module_name": "property_core", "model_name": "property.contract"}
            if not Tip.search([("name", "=", tip_vals["name"])], limit=1):
                stats["help_records"] += 1 if self._safe_create_optional("help.tip", tip_vals, "help.tip") else 0
        if Context is not False:
            ctx_vals = {"name": "%s Contexto Contratos" % PREFIX, "context_kind": self._selection(Context, "context_kind", "model", "other"), "model_name": "property.contract", "description": "%s - contexto de ajuda criado pelo seed." % PREFIX}
            if not Context.search([("name", "=", ctx_vals["name"])], limit=1):
                stats["help_records"] += 1 if self._safe_create_optional("help.context", ctx_vals, "help.context") else 0
        if Rule is not False:
            rule_vals = {"name": "%s Regra Sugestão Contratos" % PREFIX, "rule_type": self._selection(Rule, "rule_type", "model", "keyword"), "model_name": "property.contract", "keyword": "DEMO-IMOB", "active": True}
            if not Rule.search([("name", "=", rule_vals["name"])], limit=1):
                stats["help_records"] += 1 if self._safe_create_optional("help.suggestion.rule", rule_vals, "help.suggestion.rule") else 0
        if Learning is not False:
            path = Learning.search([("name", "=", "%s Trilha Imobiliária" % PREFIX)], limit=1) or self._safe_create_optional("help.learning.path", {"name": "%s Trilha Imobiliária" % PREFIX, "audience": self._selection(Learning, "audience", "user", "all"), "description": "%s - trilha demo." % PREFIX}, "help.learning.path")
            if path:
                stats["help_records"] += 1
                if Step is not False and not Step.search([("learning_path_id", "=", path.id), ("name", "=", "%s Abrir contratos" % PREFIX)], limit=1):
                    stats["help_records"] += 1 if self._safe_create_optional("help.learning.step", {"learning_path_id": path.id, "name": "%s Abrir contratos" % PREFIX, "sequence": 10, "description": "Filtre DEMO-IMOB e percorra os contratos."}, "help.learning.step") else 0

        Agenda = self._get_model("common.agenda.event")
        if Agenda is not False and self._model_table_ready("common.agenda.event", Agenda):
            for i in range(1, 5):
                start_dt = fields.Datetime.to_datetime(today + timedelta(days=i)) + relativedelta(hours=9 + i)
                event = self._safe_create_optional("common.agenda.event", {
                    "name": "%s Agenda Homologação %02d" % (PREFIX, i),
                    "agenda_module": ["property", "governance", "document", "financial"][i - 1],
                    "agenda_type": ["contract", "governance_followup", "dossier", "rent"][i - 1],
                    "state": "scheduled",
                    "start": start_dt,
                    "stop": start_dt + relativedelta(hours=1),
                    "location": "Sala Demo %02d" % i,
                    "description": "<p>%s - evento para testar agenda geral.</p>" % PREFIX,
                    "user_id": self.env.user.id,
                    "responsible_user_ids": [(6, 0, [self.env.user.id])],
                    "visibility": "internal",
                    "company_id": self.company_id.id,
                }, "common.agenda.event")
                stats["agenda_events"] += 1 if event else 0
        Communication = self._get_model("common.communication.base")
        if Communication is not False and self._model_table_ready("common.communication.base", Communication):
            for i in range(1, 4):
                comm = self._safe_create_optional("common.communication.base", {
                    "email_from": "cliente%02d.demo@example.com" % i,
                    "email_to": "governance.demo@example.com",
                    "email_cc": "corretor%02d.demo@example.com" % i,
                    "channel_type": "email",
                    "channel_origin": "%s-COMM-%02d" % (PREFIX, i),
                    "sent_by_odoo": bool(i % 2),
                    "communication_date": fields.Datetime.now(),
                }, "common.communication.base")
                stats["communications"] += 1 if comm else 0
        return stats

    def _create_contract_history_ocr_seed(self, today):
        stats = {"ocr_templates": 0, "contract_histories": 0}
        Template = self._get_model("property.contract.ocr.template")
        Line = self._get_model("property.contract.ocr.template.line")
        Field = self._get_model("ir.model.fields")
        if Template is not False:
            template = Template.search([("name", "=", "%s Template Locação Quadro Resumo" % PREFIX)], limit=1)
            if not template:
                template = self._safe_create_optional("property.contract.ocr.template", {
                    "name": "%s Template Locação Quadro Resumo" % PREFIX,
                    "sequence": 900,
                    "company_id": self.company_id.id,
                    "document_kind": self._selection(Template, "document_kind", "lease_contract", "contract"),
                    "min_auto_detect_score": 55,
                    "contract_type": self._selection(Template, "contract_type", "commercial", "residential"),
                    "extraction_mode": self._selection(Template, "extraction_mode", "hybrid", "regex"),
                    "page_limit": 8,
                    "auto_detect_pattern": r"QUADRO\s+RESUMO|CONTRATO\s+DE\s+LOCA[ÇC][ÃA]O|LOCADOR|LOCAT[ÁA]RIO",
                    "auto_detect_keywords": "locador\nlocatário\naluguel\nquadro resumo\nimóvel",
                    "description": "<p>%s - template OCR sintético para contratos imobiliários.</p>" % PREFIX,
                }, "property.contract.ocr.template")
                stats["ocr_templates"] += 1 if template else 0
            if template and Line is not False and Field is not False:
                model = self.env["ir.model"].sudo().search([("model", "=", "property.contract.history")], limit=1)
                field_specs = [
                    ("party1_name", "Locadora", r"LOCADORA[:\s]+([^\n]+)", True),
                    ("party2_name", "Locatária", r"LOCAT[ÁA]RIA[:\s]+([^\n]+)", True),
                    ("monthly_amount", "Valor do aluguel", r"ALUGUEL[:\s]+R?\$?\s*([0-9\.,]+)", True),
                    ("start_date", "Início", r"IN[ÍI]CIO[:\s]+([0-9]{2}/[0-9]{2}/[0-9]{4})", False),
                    ("end_date", "Término", r"T[ÉE]RMINO[:\s]+([0-9]{2}/[0-9]{2}/[0-9]{4})", False),
                ]
                for seq, (field_name, label, pattern, required) in enumerate(field_specs, start=1):
                    fld = Field.search([("model_id", "=", model.id), ("name", "=", field_name)], limit=1) if model else False
                    if fld and not Line.search([("template_id", "=", template.id), ("field_id", "=", fld.id)], limit=1):
                        line = self._safe_create_optional("property.contract.ocr.template.line", {
                            "template_id": template.id,
                            "sequence": seq * 10,
                            "name": "%s %s" % (PREFIX, label),
                            "field_id": fld.id,
                            "value_type": self._selection(Line, "value_type", "regex", "regex"),
                            "value_mode": self._selection(Line, "value_mode", "first", "first"),
                            "pattern": pattern,
                            "dotall": True,
                            "required": required,
                            "confidence": 88.0,
                            "notes": "%s - regra OCR demo." % PREFIX,
                        }, "property.contract.ocr.template.line")
                        stats["ocr_templates"] += 1 if line else 0
        History = self._get_model("property.contract.history")
        HistoryLine = self._get_model("property.contract.history.line")
        assets = self._safe_search("property.asset", [("name", "ilike", PREFIX)], limit=8) or self._safe_search("property.asset", [], limit=8)
        if History is not False and assets:
            for idx, asset in enumerate(assets, start=1):
                raw = """
{prefix} CONTRATO DE LOCAÇÃO - QUADRO RESUMO
LOCADORA: {company}
LOCATÁRIA: DEMO LOCATÁRIO {idx:03d}
IMÓVEL: {asset}
ALUGUEL: R$ {rent:.2f}
INÍCIO: 05/01/2026
TÉRMINO: 04/01/2029
""".format(prefix=PREFIX, company=self.company_id.name, idx=idx, asset=asset.display_name, rent=3500 + idx * 300)
                hist = self._safe_create_optional("property.contract.history", {
                    "company_id": self.company_id.id,
                    "contract_type": self._selection(History, "contract_type", "lease", "rental"),
                    "state": self._selection(History, "state", "reviewed", "draft"),
                    "contract_filename": "%s_contrato_%03d.pdf" % (PREFIX.lower(), idx),
                    "mimetype": "application/pdf",
                    "raw_text": raw,
                    "extraction_log": "%s - histórico criado pela massa de testes sem OCR real." % PREFIX,
                    "parser_used": "demo_seed_regex",
                    "asset_id": asset.id,
                    "party1_name": self.company_id.name,
                    "party1_vat": self.company_id.vat,
                    "party2_name": "%s Locatário OCR %03d" % (PREFIX, idx),
                    "party2_vat": self._cpf(60000 + idx),
                    "sign_date": today - timedelta(days=30),
                    "start_date": today - relativedelta(months=6),
                    "end_date": today + relativedelta(months=30),
                    "monthly_amount": 3500 + idx * 300,
                    "total_value": (3500 + idx * 300) * 36,
                    "deposit_value": (3500 + idx * 300) * 3,
                    "address": asset.address,
                    "neighborhood": asset.neighborhood,
                    "city": asset.city,
                    "zip_code": asset.zip_code,
                    "property_description": "%s - contrato OCR sintético para homologação." % PREFIX,
                    "ocr_template_id": template.id if Template is not False and template else False,
                }, "property.contract.history")
                if hist:
                    stats["contract_histories"] += 1
                    if HistoryLine is not False:
                        for seq, (field_name, label, value) in enumerate([("party1_name", "Locadora", self.company_id.name), ("party2_name", "Locatária", "%s Locatário OCR %03d" % (PREFIX, idx)), ("monthly_amount", "Aluguel", str(3500 + idx * 300))], start=1):
                            self._safe_create_optional("property.contract.history.line", {
                                "history_id": hist.id,
                                "field_name": field_name,
                                "label": label,
                                "raw_value": value,
                                "parsed_value": value,
                                "field_type": self._selection(HistoryLine, "field_type", "char", "char"),
                                "confidence": 90.0,
                                "accepted": True,
                                "sequence": seq * 10,
                            }, "property.contract.history.line")
        return stats
