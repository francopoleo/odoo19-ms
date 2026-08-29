from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # S3 Configuration Fields
    s3_enabled = fields.Boolean(
        string="Habilitar S3/DigitalOcean Spaces",
        help="Marque para ativar armazenamento em S3/DigitalOcean Spaces"
    )
    s3_endpoint = fields.Char(
        string="S3 Endpoint",
        help="Exemplo: https://nyc3.digitaloceanspaces.com",
        config_parameter='document_s3_storage.endpoint'
    )
    s3_access_key = fields.Char(
        string="S3 Access Key",
        help="Sua chave de acesso DigitalOcean Spaces",
        config_parameter='document_s3_storage.access_key'
    )
    s3_secret_key = fields.Char(
        string="S3 Secret Key",
        help="Sua chave secreta DigitalOcean Spaces",
        config_parameter='document_s3_storage.secret_key'
    )
    s3_bucket = fields.Char(
        string="S3 Bucket Name",
        help="Nome do seu Space/Bucket (ex: odoo-documentos)",
        config_parameter='document_s3_storage.bucket'
    )
    s3_region = fields.Char(
        string="S3 Region",
        default='nyc3',
        help="Região do Space (nyc3, sfo3, sgp1, ams3, fra1, etc)",
        config_parameter='document_s3_storage.region'
    )

    @api.onchange('s3_enabled')
    def _onchange_s3_enabled(self):
        """
        Se desabilitar S3, limpar os campos de configuração.
        Se habilitar, prepara para preenchimento de credenciais.
        """
        if not self.s3_enabled:
            self.s3_endpoint = ''
            self.s3_access_key = ''
            self.s3_secret_key = ''
            self.s3_bucket = ''
            self.s3_region = 'nyc3'

    def set_values(self):
        """Salva valores de configuração"""
        from odoo.exceptions import ValidationError

        # Se habilitou S3, validar configuração
        if self.s3_enabled:
            if not all([self.s3_endpoint, self.s3_access_key, self.s3_secret_key, self.s3_bucket]):
                raise ValidationError("Todos os campos de S3 devem ser preenchidos para habilitar!")

            # Testar conexão
            self._test_s3_connection()

        # Salvar configuração
        super().set_values()

    @api.model
    def get_values(self):
        """Carrega valores de configuração"""
        res = super().get_values()

        # Odoo handles config_parameter fields automatically via the parent class
        # Just ensure s3_enabled is set based on bucket configuration
        if not res.get('s3_bucket'):
            res['s3_enabled'] = False

        return res

    def _test_s3_connection(self):
        """Testa conexão com S3"""
        from odoo.exceptions import UserError

        try:
            import boto3

            s3 = boto3.client(
                's3',
                endpoint_url=self.s3_endpoint,
                aws_access_key_id=self.s3_access_key,
                aws_secret_access_key=self.s3_secret_key,
                region_name=self.s3_region,
            )

            # Test: listar buckets
            s3.head_bucket(Bucket=self.s3_bucket)

        except Exception as e:
            raise UserError(f"Erro ao conectar com S3: {str(e)}")

    def action_test_s3_connection(self):
        """Action para testar conexão (chamado do botão)"""
        self._test_s3_connection()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sucesso!',
                'message': 'Conexão com S3 validada com sucesso!',
                'type': 'success',
                'sticky': False,
            }
        }