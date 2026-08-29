# -*- coding: utf-8 -*-
import json
import logging
import re
import urllib.error
import urllib.request

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    br_person_type = fields.Selection(
        selection=[
            ("pf", "Pessoa Física"),
            ("pj", "Pessoa Jurídica"),
            ("other", "Outro / Estrangeiro"),
        ],
        string="Tipo BR",
        compute="_compute_br_person_type",
        inverse="_inverse_br_person_type",
        store=True,
        help="Classificação brasileira do contato. É sincronizada com o campo padrão Pessoa/Empresa do Odoo.",
    )

    br_cpf = fields.Char(
        string="CPF",
        size=14,
        help="CPF da pessoa física. Informe com ou sem máscara; o sistema normaliza para 000.000.000-00.",
    )
    br_cnpj = fields.Char(
        string="CNPJ",
        size=18,
        help="CNPJ da pessoa jurídica. Informe com ou sem máscara; o sistema normaliza para 00.000.000/0000-00.",
    )
    br_rg = fields.Char(string="RG", help="Número do RG ou documento estadual equivalente.")
    br_rg_issuer = fields.Char(string="Órgão Expedidor", help="Órgão expedidor do RG. Exemplos: SSP, DETRAN, IFP.")
    br_rg_issuer_state_id = fields.Many2one(
        "res.country.state",
        string="UF Expedidor",
        domain="[('country_id.code', '=', 'BR')]",
        help="UF do órgão expedidor do RG.",
    )
    br_rg_issue_date = fields.Date(string="Data de Expedição RG", help="Data de emissão/expedição do RG.")
    br_birth_date = fields.Date(string="Data de Nascimento", help="Data de nascimento da pessoa física.")
    br_mother_name = fields.Char(
        string="Nome da Mãe",
        help="Campo usado em cadastros, análise cadastral e conferência documental quando necessário.",
    )

    br_legal_name = fields.Char(
        string="Razão Social",
        help="Razão social da pessoa jurídica, quando diferente do nome exibido no contato.",
    )
    br_trade_name = fields.Char(string="Nome Fantasia", help="Nome fantasia da pessoa jurídica.")
    br_state_tax_number = fields.Char(string="Inscrição Estadual", help="Inscrição Estadual da empresa, se aplicável.")
    br_municipal_tax_number = fields.Char(string="Inscrição Municipal", help="Inscrição Municipal da empresa, se aplicável.")

    br_district = fields.Char(string="Bairro", help="Bairro retornado pela consulta de CEP ou preenchido manualmente.")
    br_ibge_code = fields.Char(
        string="Código IBGE Município",
        help="Código IBGE do município retornado pela consulta de CEP.",
        readonly=True,
        copy=False,
    )
    br_zip_source = fields.Selection(
        selection=[
            ("brasilapi", "BrasilAPI"),
            ("viacep", "ViaCEP"),
            ("manual", "Manual"),
        ],
        string="Fonte do CEP",
        readonly=True,
        copy=False,
        help="Fonte usada para preencher o endereço a partir do CEP.",
    )
    br_zip_lookup_date = fields.Datetime(
        string="Última Consulta CEP",
        readonly=True,
        copy=False,
        help="Data/hora da última tentativa de consulta do CEP.",
    )
    br_zip_lookup_status = fields.Selection(
        selection=[
            ("ok", "CEP encontrado"),
            ("not_found", "CEP não encontrado"),
            ("unavailable", "Serviço indisponível"),
            ("invalid", "CEP inválido"),
            ("manual", "Preenchimento manual"),
        ],
        string="Status da Consulta CEP",
        readonly=True,
        copy=False,
        help="Resultado da última tentativa de preenchimento automático por CEP.",
    )
    br_zip_lookup_message = fields.Text(
        string="Mensagem da Consulta CEP",
        readonly=True,
        copy=False,
        help="Mensagem de diagnóstico da última consulta de CEP. Não bloqueia o cadastro.",
    )

    # -------------------------------------------------------------------------
    # Tipo PF/PJ
    # -------------------------------------------------------------------------
    @api.depends("company_type")
    def _compute_br_person_type(self):
        for partner in self:
            if partner.company_type == "company":
                partner.br_person_type = "pj"
            elif partner.company_type == "person":
                partner.br_person_type = "pf"
            else:
                partner.br_person_type = "other"

    def _inverse_br_person_type(self):
        for partner in self:
            if partner.br_person_type == "pj":
                partner.company_type = "company"
            elif partner.br_person_type == "pf":
                partner.company_type = "person"

    # -------------------------------------------------------------------------
    # Normalização e validação documental
    # -------------------------------------------------------------------------
    @staticmethod
    def _only_digits(value):
        return re.sub(r"\D", "", value or "")

    @staticmethod
    def _format_cpf(value):
        digits = re.sub(r"\D", "", value or "")
        if len(digits) != 11:
            return value or False
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

    @staticmethod
    def _format_cnpj(value):
        digits = re.sub(r"\D", "", value or "")
        if len(digits) != 14:
            return value or False
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"

    @staticmethod
    def _format_zip(value):
        digits = re.sub(r"\D", "", value or "")
        if len(digits) != 8:
            return value or False
        return f"{digits[:5]}-{digits[5:]}"

    @classmethod
    def _is_valid_cpf(cls, value):
        digits = cls._only_digits(value)
        if not digits:
            return True
        if len(digits) != 11 or digits == digits[0] * 11:
            return False
        for pos in [9, 10]:
            total = sum(int(digits[i]) * ((pos + 1) - i) for i in range(pos))
            check = (total * 10) % 11
            if check == 10:
                check = 0
            if check != int(digits[pos]):
                return False
        return True

    @classmethod
    def _is_valid_cnpj(cls, value):
        digits = cls._only_digits(value)
        if not digits:
            return True
        if len(digits) != 14 or digits == digits[0] * 14:
            return False
        weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        weights_2 = [6] + weights_1
        for size, weights in [(12, weights_1), (13, weights_2)]:
            total = sum(int(digits[i]) * weights[i] for i in range(size))
            check = 11 - (total % 11)
            if check >= 10:
                check = 0
            if check != int(digits[size]):
                return False
        return True

    @api.constrains("br_cpf", "br_cnpj")
    def _check_br_documents(self):
        for partner in self:
            if partner.br_cpf and not self._is_valid_cpf(partner.br_cpf):
                raise ValidationError(_("CPF inválido para o contato %s.") % partner.display_name)
            if partner.br_cnpj and not self._is_valid_cnpj(partner.br_cnpj):
                raise ValidationError(_("CNPJ inválido para o contato %s.") % partner.display_name)

    @api.onchange("br_cpf")
    def _onchange_br_cpf(self):
        for partner in self:
            if partner.br_cpf:
                partner.br_cpf = self._format_cpf(partner.br_cpf)
                if not partner.vat:
                    partner.vat = self._only_digits(partner.br_cpf)

    @api.onchange("br_cnpj")
    def _onchange_br_cnpj(self):
        for partner in self:
            if partner.br_cnpj:
                partner.br_cnpj = self._format_cnpj(partner.br_cnpj)
                if not partner.vat:
                    partner.vat = self._only_digits(partner.br_cnpj)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._prepare_br_document_vals(vals)
        return super().create(vals_list)

    def write(self, vals):
        vals = dict(vals)
        self._prepare_br_document_vals(vals)
        return super().write(vals)

    def _prepare_br_document_vals(self, vals):
        if vals.get("br_cpf"):
            vals["br_cpf"] = self._format_cpf(vals["br_cpf"])
            vals.setdefault("vat", self._only_digits(vals["br_cpf"]))
        if vals.get("br_cnpj"):
            vals["br_cnpj"] = self._format_cnpj(vals["br_cnpj"])
            vals.setdefault("vat", self._only_digits(vals["br_cnpj"]))
        if vals.get("zip"):
            vals["zip"] = self._format_zip(vals["zip"])

    # -------------------------------------------------------------------------
    # Consulta CEP
    # -------------------------------------------------------------------------
    @api.onchange("zip")
    def _onchange_zip_lookup_br(self):
        """Atualiza o endereço quando o CEP atinge 8 dígitos. Não bloqueia cadastro."""
        for partner in self:
            cep = self._only_digits(partner.zip)
            if not cep:
                continue
            if len(cep) != 8:
                partner.br_zip_lookup_status = "invalid"
                partner.br_zip_lookup_message = _("Informe um CEP com 8 dígitos para consulta automática.")
                continue
            partner.zip = self._format_zip(cep)
            values = partner._lookup_zip_values(cep)
            if values:
                partner._apply_zip_values(values, force=True)
            else:
                partner.br_zip_lookup_status = "not_found"
                partner.br_zip_lookup_date = fields.Datetime.now()
                partner.br_zip_lookup_message = _(
                    "CEP não encontrado ou serviço indisponível. O cadastro não foi bloqueado; preencha o endereço manualmente."
                )

    def action_lookup_zip_br(self):
        """Botão de consulta de CEP. Retorna notificação e nunca bloqueia o contato por falha externa."""
        self.ensure_one()
        cep = self._only_digits(self.zip)
        if len(cep) != 8:
            self.write({
                "br_zip_lookup_status": "invalid",
                "br_zip_lookup_date": fields.Datetime.now(),
                "br_zip_lookup_message": _("Informe um CEP com 8 dígitos antes de consultar."),
            })
            return self._notify_zip_lookup(
                title=_("CEP inválido"),
                message=_("Informe um CEP com 8 dígitos antes de consultar."),
                notification_type="warning",
            )

        values = self._lookup_zip_values(cep)
        if not values:
            self.write({
                "zip": self._format_zip(cep),
                "br_zip_lookup_status": "not_found",
                "br_zip_lookup_date": fields.Datetime.now(),
                "br_zip_lookup_message": _(
                    "CEP não encontrado ou serviço indisponível. Preencha o endereço manualmente ou tente novamente."
                ),
            })
            return self._notify_zip_lookup(
                title=_("CEP não encontrado"),
                message=_("Não foi possível localizar esse CEP agora. O contato não será bloqueado."),
                notification_type="warning",
            )

        self._apply_zip_values(values, force=True)
        return self._notify_zip_lookup(
            title=_("CEP encontrado"),
            message=_("Endereço atualizado pelo CEP."),
            notification_type="success",
        )

    def _notify_zip_lookup(self, title, message, notification_type="info"):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "sticky": False,
                "type": notification_type,
            },
        }

    def _lookup_zip_values(self, cep):
        """Consulta BrasilAPI primeiro e ViaCEP como fallback."""
        self.ensure_one()
        cep = self._only_digits(cep)
        if len(cep) != 8:
            return {}

        result = self._request_brasilapi_cep(cep)
        if result:
            return result
        return self._request_viacep(cep)

    def _http_get_json(self, url, timeout=6):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Odoo Brasil Contact CEP/19.0",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status >= 400:
                    return {}
                payload = response.read().decode("utf-8")
                return json.loads(payload or "{}")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            _logger.info("Falha ao consultar CEP em %s: %s", url, exc)
            return {}

    def _request_brasilapi_cep(self, cep):
        data = self._http_get_json(f"https://brasilapi.com.br/api/cep/v2/{cep}")
        if not data or data.get("type") == "service_error":
            return {}
        city = data.get("city")
        state = data.get("state")
        if not city and not state:
            return {}
        return {
            "source": "brasilapi",
            "zip": self._format_zip(cep),
            "street": data.get("street"),
            "district": data.get("neighborhood"),
            "city": city,
            "state_code": state,
            "ibge_code": data.get("city_ibge_code"),
        }

    def _request_viacep(self, cep):
        data = self._http_get_json(f"https://viacep.com.br/ws/{cep}/json/")
        if not data or data.get("erro"):
            return {}
        return {
            "source": "viacep",
            "zip": data.get("cep") or self._format_zip(cep),
            "street": data.get("logradouro"),
            "street2": data.get("complemento"),
            "district": data.get("bairro"),
            "city": data.get("localidade"),
            "state_code": data.get("uf"),
            "ibge_code": data.get("ibge"),
        }

    def _apply_zip_values(self, values, force=False):
        self.ensure_one()
        country = self.env.ref("base.br", raise_if_not_found=False)
        state = False
        state_code = values.get("state_code")
        if country and state_code:
            state = self.env["res.country.state"].search(
                [("country_id", "=", country.id), ("code", "=", state_code)],
                limit=1,
            )

        update_vals = {}

        def set_if_allowed(field_name, value):
            # Always update if force=True, otherwise only if field is empty
            if force or not self[field_name]:
                if value is not None:  # Allow empty strings, but not None
                    update_vals[field_name] = value

        set_if_allowed("zip", values.get("zip"))
        set_if_allowed("street", values.get("street"))
        # Use street2 for district (bairro) in standard Odoo field
        district = values.get("district")
        if district:
            set_if_allowed("street2", district)
        set_if_allowed("city", values.get("city"))
        if country and (force or not self.country_id):
            update_vals["country_id"] = country.id
        if state and (force or not self.state_id):
            update_vals["state_id"] = state.id
        update_vals.update({
            "br_ibge_code": values.get("ibge_code") or False,
            "br_zip_source": values.get("source") or "manual",
            "br_zip_lookup_date": fields.Datetime.now(),
            "br_zip_lookup_status": "ok",
            "br_zip_lookup_message": _("Endereço atualizado pelo CEP."),
        })
        self.update(update_vals)
