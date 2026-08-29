# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import io
import unicodedata

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_pix import const


# ---------------------------------------------------------------------------
# Utilitários PIX
# ---------------------------------------------------------------------------

def _crc16_ccitt(data: str) -> int:
    """Calcula CRC16-CCITT (polinômio 0x1021, valor inicial 0xFFFF).

    Utilizado na geração do BR Code PIX conforme especificação BACEN.
    """
    crc = 0xFFFF
    for byte in data.encode('utf-8'):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc


def _ascii_upper(text: str) -> str:
    """Remove acentos e diacríticos, converte para ASCII maiúsculo.

    O padrão BACEN exige que nome e cidade do recebedor estejam em ASCII.
    """
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).upper()


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    # Estende o campo custom_mode do payment_custom com o novo modo 'pix'.
    # Usa 'set null' porque custom_mode não possui default definido no campo base.
    custom_mode = fields.Selection(
        selection_add=[('pix', 'PIX')],
        ondelete={'pix': 'set null'},
    )

    pix_key_type = fields.Selection(
        string="Tipo de Chave PIX",
        selection=[
            ('cpf',    'CPF'),
            ('cnpj',   'CNPJ'),
            ('phone',  'Telefone'),
            ('email',  'E-mail'),
            ('random', 'Chave Aleatória (EVP)'),
        ],
        default='random',
    )
    pix_key = fields.Char(
        string="Chave PIX",
        help=(
            "Chave PIX cadastrada no Banco Central: CPF, CNPJ, e-mail, "
            "telefone (+55DDD...) ou chave aleatória (UUID)."
        ),
    )
    pix_merchant_name = fields.Char(
        string="Nome do Recebedor",
        help="Nome do recebedor conforme padrão BACEN — máx. 25 caracteres, sem acentos.",
        size=25,
    )
    pix_merchant_city = fields.Char(
        string="Cidade do Recebedor",
        help="Cidade do recebedor — máx. 15 caracteres, sem acentos.",
        size=15,
    )

    # === CONSTRAINT METHODS === #

    @api.constrains('state', 'custom_mode', 'pix_key', 'pix_merchant_name', 'pix_merchant_city')
    def _check_pix_fields_before_enabling(self):
        """Impede ativação do provedor PIX sem os campos obrigatórios preenchidos."""
        for provider in self.filtered(
            lambda p: p.custom_mode == 'pix' and p.state != 'disabled'
        ):
            if not provider.pix_key:
                raise ValidationError(
                    _("Configure a Chave PIX antes de ativar o provedor.")
                )
            if not provider.pix_merchant_name:
                raise ValidationError(
                    _("Configure o Nome do Recebedor antes de ativar o provedor PIX.")
                )
            if not provider.pix_merchant_city:
                raise ValidationError(
                    _("Configure a Cidade do Recebedor antes de ativar o provedor PIX.")
                )

    # === CRUD METHODS === #

    def _get_default_payment_method_codes(self):
        """Override de payment para retornar os códigos padrão do PIX."""
        self.ensure_one()
        if self.code != 'custom' or self.custom_mode != 'pix':
            return super()._get_default_payment_method_codes()
        return const.DEFAULT_PAYMENT_METHOD_CODES

    # === ACTION METHODS === #

    def action_recompute_pending_msg(self):
        """Override de payment_custom para tratar provedores PIX."""
        pix_providers = self.filtered(lambda p: p.custom_mode == 'pix')
        pix_providers._pix_update_pending_msg()
        return super(PaymentProvider, self - pix_providers).action_recompute_pending_msg()

    # === PIX METHODS === #

    def _pix_update_pending_msg(self):
        """Atualiza o pending_msg com as instruções de pagamento PIX."""
        for provider in self:
            key = provider.pix_key or _("(chave não configurada)")
            provider.pending_msg = (
                f'<div>'
                f'<h5>{_("Realize o pagamento via PIX")}</h5>'
                f'<p>{_("Escaneie o QR Code ao lado ou utilize a chave PIX abaixo.")}</p>'
                f'<h6>{_("Chave PIX")}</h6>'
                f'<ul><li><pre>{key}</pre></li></ul>'
                f'<p><br/></p>'
                f'</div>'
            )

    def _pix_ensure_pending_msg_is_set(self):
        """Inicializa o pending_msg de provedores PIX que ainda não possuem mensagem.

        Chamado via <function> no XML de dados após a criação do provedor.
        """
        providers = self.filtered(lambda p: p.custom_mode == 'pix' and not p.pending_msg)
        providers._pix_update_pending_msg()

    def _pix_build_br_code(self, amount, txid=''):
        """Gera a string EMV/BR Code para pagamento PIX conforme especificação BACEN.

        Implementa o formato de QR Code Dinâmico (Point of Initiation = 12) com:
        - Merchant Account Information (tag 26) contendo a chave PIX
        - Valor da transação (tag 54)
        - txid do Odoo como referência adicional (tag 62/05)
        - CRC16-CCITT ao final (tag 6304)

        Referência:
            Manual de Padrões para Iniciação do PIX — Banco Central do Brasil
            https://www.bcb.gov.br/content/estabilidadefinanceira/pix/
        """
        self.ensure_one()
        if not self.pix_key:
            return ''

        def emv(tag, value):
            value = str(value)
            return f"{tag}{len(value):02d}{value}"

        # Merchant Account Information (MAI) — tag 26
        mai = emv("00", "BR.GOV.BCB.PIX") + emv("01", self.pix_key)

        # Nome e cidade em ASCII maiúsculo (requisito BACEN)
        name = _ascii_upper(self.pix_merchant_name or 'RECEBEDOR')[:25]
        city = _ascii_upper(self.pix_merchant_city or 'BRASIL')[:15]

        # txid: apenas alfanumérico, máx. 25 caracteres
        safe_txid = ''.join(c for c in (txid or '') if c.isalnum())[:25] or '***'

        payload = (
            emv("00", "01")                    # Payload Format Indicator
            + emv("01", "12")                  # Point of Initiation: 12 = QR dinâmico
            + emv("26", mai)                   # Merchant Account Information (PIX)
            + emv("52", "0000")                # Merchant Category Code
            + emv("53", "986")                 # Currency: BRL (ISO 4217)
            + emv("54", f"{amount:.2f}")       # Transaction Amount
            + emv("58", "BR")                  # Country Code
            + emv("59", name)                  # Merchant Name (máx. 25)
            + emv("60", city)                  # Merchant City (máx. 15)
            + emv("62", emv("05", safe_txid))  # Additional Data Field — txid
            + "6304"                           # CRC16 tag (tamanho sempre 04)
        )
        crc = _crc16_ccitt(payload)
        return payload + f"{crc:04X}"

    def _pix_build_qr_code_base64(self, amount, txid=''):
        """Retorna o QR Code PIX como data URI PNG (base64).

        Utiliza a biblioteca `qrcode` (já presente nas dependências do Odoo).
        Retorna False se a chave PIX não estiver configurada ou em caso de erro.
        """
        self.ensure_one()
        if not self.pix_key:
            return False
        try:
            import qrcode  # noqa: PLC0415 — import condicional intencional

            br_code = self._pix_build_br_code(amount, txid)
            if not br_code:
                return False
            img = qrcode.make(br_code)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            b64 = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{b64}"
        except Exception:
            return False