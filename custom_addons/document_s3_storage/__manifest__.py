{
    "name": "Document S3 Storage",
    "version": "19.0.1.0.0",
    "category": "Tools/Documents",
    "summary": "S3/DigitalOcean Spaces integration for document storage",
    "description": """
Document S3 Storage
===================

Integração transparente com S3/DigitalOcean Spaces para armazenamento de documentos.

Features:
---------
✓ Configuração via Settings do Odoo (sem odoo.conf)
✓ Suporte a variáveis de ambiente
✓ Upload automático para S3
✓ Download transparente
✓ Funciona em desenvolvimento (local) e produção (S3)
✓ Um único odoo.conf em ambos ambientes

Instalação:
-----------
1. pip install boto3
2. Instale o módulo
3. Vá em Settings > Integrations > S3/DigitalOcean Spaces
4. Configure suas credenciais
5. Pronto!
    """,
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": ["document_core", "base", "base_setup"],
    "external_dependencies": {
        "python": ["boto3"],
    },
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
}