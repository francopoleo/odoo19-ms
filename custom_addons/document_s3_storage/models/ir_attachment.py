import os
import base64
import logging
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    storage_location = fields.Selection(
        [("db", "Database"), ("s3", "S3/DigitalOcean Spaces")],
        string="Storage Location",
        default="db",
        readonly=True,
        help="Where this attachment is physically stored"
    )
    s3_key = fields.Char(
        "S3 Key",
        readonly=True,
        help="Chave do arquivo no bucket S3"
    )

    # ========================================================================
    # Configuração Dinâmica (sem precisar de odoo.conf diferente)
    # ========================================================================

    @staticmethod
    def _get_s3_config():
        """
        Obtém configuração S3 de múltiplas fontes (em ordem de prioridade):
        1. Variáveis de ambiente (ODOO_S3_*)
        2. Settings do Odoo (ir.config.parameter)
        3. odoo.conf (fallback)

        Retorna dict com configuração ou None se não configurado
        """
        import os
        from odoo.tools import config

        # 1. Tentar variáveis de ambiente (maior prioridade)
        env_config = {
            'endpoint': os.environ.get('ODOO_S3_ENDPOINT'),
            'access_key': os.environ.get('ODOO_S3_ACCESS_KEY'),
            'secret_key': os.environ.get('ODOO_S3_SECRET_KEY'),
            'bucket': os.environ.get('ODOO_S3_BUCKET'),
            'region': os.environ.get('ODOO_S3_REGION', 'nyc3'),
        }

        if all(env_config.get(k) for k in ['endpoint', 'access_key', 'secret_key', 'bucket']):
            _logger.info("✓ S3 configurado via variáveis de ambiente")
            return env_config

        # 2. Tentar odoo.conf
        conf_config = {
            'endpoint': config.get('s3_endpoint'),
            'access_key': config.get('s3_access_key'),
            'secret_key': config.get('s3_secret_key'),
            'bucket': config.get('s3_bucket'),
            'region': config.get('s3_region', 'nyc3'),
        }

        if all(conf_config.get(k) for k in ['endpoint', 'access_key', 'secret_key', 'bucket']):
            _logger.info("✓ S3 configurado via odoo.conf")
            return conf_config

        # S3 não configurado
        return None

    @api.model
    def _get_s3_config_from_settings(self):
        """
        Obtém configuração S3 do banco de dados (ir.config.parameter)
        Útil para configurar via Settings do Odoo (web)
        """
        get_param = self.env['ir.config.parameter'].sudo().get_param

        config = {
            'endpoint': get_param('document_s3_storage.endpoint'),
            'access_key': get_param('document_s3_storage.access_key'),
            'secret_key': get_param('document_s3_storage.secret_key'),
            'bucket': get_param('document_s3_storage.bucket'),
            'region': get_param('document_s3_storage.region', 'nyc3'),
        }

        if all(config.get(k) for k in ['endpoint', 'access_key', 'secret_key', 'bucket']):
            _logger.info("✓ S3 configurado via Settings do Odoo")
            return config

        return None

    @staticmethod
    def _is_s3_enabled():
        """Verifica se S3 está configurado em qualquer fonte"""
        return IrAttachment._get_s3_config() is not None

    @staticmethod
    def _get_s3_client():
        """Retorna cliente boto3 configurado"""
        import boto3

        config = IrAttachment._get_s3_config()
        if not config:
            raise UserError(_("S3 não está configurado. Defina as variáveis de ambiente ou configure em odoo.conf"))

        return boto3.client(
            's3',
            endpoint_url=config['endpoint'],
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_key'],
            region_name=config.get('region', 'nyc3'),
        )

    @staticmethod
    def _get_s3_bucket():
        """Retorna nome do bucket S3"""
        config = IrAttachment._get_s3_config()
        if not config:
            return None
        return config['bucket']

    def _generate_s3_key(self):
        """Gera chave única para arquivo no S3"""
        # Formato: documents/YYYY/MM/DD/id_user/filename
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')
        user_id = self.env.user.id

        # Remover extensão original para evitar duplicatas
        filename = self.name or 'attachment'

        s3_key = f"documents/{year}/{month}/{day}/{user_id}/{self.id}_{filename}"
        return s3_key

    def _upload_to_s3(self):
        """Faz upload do arquivo para S3"""
        if not self._is_s3_enabled() or not self.datas:
            return

        try:
            s3_client = self._get_s3_client()
            bucket = self._get_s3_bucket()

            s3_key = self._generate_s3_key()

            # Upload para S3
            s3_client.put_object(
                Bucket=bucket,
                Key=s3_key,
                Body=base64.b64decode(self.datas) if isinstance(self.datas, str) else self.datas,
                ContentType=self.mimetype or 'application/octet-stream',
                Metadata={
                    'odoo-id': str(self.id),
                    'odoo-user': str(self.create_uid.id),
                    'odoo-date': str(self.create_date),
                }
            )

            # Salvar referência e limpar dados locais
            self.write({
                's3_key': s3_key,
                'storage_location': 's3',
                'datas': None,  # Limpar dados do BD após upload
            })

            _logger.info(f"✓ Arquivo '{self.name}' salvo em S3: {s3_key}")

        except Exception as e:
            _logger.error(f"✗ Erro ao fazer upload para S3: {str(e)}")
            raise UserError(_("Erro ao salvar arquivo em S3: %s") % str(e))

    def _download_from_s3(self):
        """Baixa arquivo do S3 quando necessário"""
        if self.storage_location != 's3' or not self.s3_key:
            return self.datas

        try:
            s3_client = self._get_s3_client()
            bucket = self._get_s3_bucket()

            response = s3_client.get_object(Bucket=bucket, Key=self.s3_key)
            file_data = response['Body'].read()

            return base64.b64encode(file_data) if isinstance(file_data, bytes) else file_data

        except Exception as e:
            _logger.error(f"✗ Erro ao baixar arquivo do S3: {str(e)}")
            raise UserError(_("Erro ao recuperar arquivo do S3: %s") % str(e))

    @api.model_create_multi
    def create(self, vals_list):
        """Override create para salvar em S3 se configurado"""
        attachments = super().create(vals_list)

        # Se S3 está habilitado, fazer upload
        if self._is_s3_enabled():
            for attachment in attachments:
                if attachment.datas:
                    attachment._upload_to_s3()

        return attachments

    def write(self, vals):
        """Override write para lidar com arquivo em S3"""
        # Se atualizando arquivo, fazer upload para S3
        if 'datas' in vals and vals['datas'] and self._is_s3_enabled():
            self._upload_to_s3()

        return super().write(vals)

    def unlink(self):
        """Override unlink para limpar arquivo do S3"""
        if self._is_s3_enabled():
            s3_client = self._get_s3_client()
            bucket = self._get_s3_bucket()

            for attachment in self:
                if attachment.s3_key:
                    try:
                        s3_client.delete_object(Bucket=bucket, Key=attachment.s3_key)
                        _logger.info(f"✓ Arquivo removido do S3: {attachment.s3_key}")
                    except Exception as e:
                        _logger.error(f"✗ Erro ao remover arquivo do S3: {str(e)}")

        return super().unlink()

    # Override para buscar dados do S3 transparentemente
    def read(self, fields=None, load='_classic_read'):
        """
        Override read para buscar arquivo do S3 quando necessário
        Mantém transparência para o usuário
        """
        result = super().read(fields, load)

        # Se S3 habilitado e 'datas' está nos campos solicitados
        if self._is_s3_enabled() and (fields is None or 'datas' in fields):
            for record in result:
                attachment = self.browse(record['id'])
                if attachment.storage_location == 's3' and attachment.s3_key:
                    try:
                        record['datas'] = attachment._download_from_s3()
                    except Exception as e:
                        _logger.error(f"✗ Erro ao buscar arquivo do S3: {str(e)}")

        return result