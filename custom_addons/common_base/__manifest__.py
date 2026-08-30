{
    "name": "Common Base",
    "version": "19.0.1.0.0",
    "category": "Real Estate/Base",
    "summary": "Base compartilhada para todo o ERP Imóveis",
    "description": """
        Módulo base que fornece componentes reutilizáveis para todo o ERP:

        • Tags genéricas para classificação
        • Mixins com campos comuns (auditoria, multi-company, etc)
        • Sequências automáticas
        • Configurações globais1
        • Tradução para português
        • Ícones e identidade visual

        Este módulo é a fundação de todos os outros módulos do sistema.
    """,
    "author": "Franco Poleo / Manuela Silva",
    "website": "https://www.suaempresa.com",
    "license": "LGPL-3",
    "depends": ["mail", "calendar", "base"],
    "data": [
        # Security (primeiro)
        "security/common_security.xml",
        "security/ir.model.access.csv",

        # Data
        "data/common_sequence_data.xml",
        "data/common_config_data.xml",
        "data/common_agenda_data.xml",
        "data/common_agenda_security_data.xml",

        # Views
        "views/common_tag_views.xml",
        "views/common_config_views.xml",
        "views/access_overview_views.xml",
        "views/common_menu_views.xml",
        "views/common_agenda_calendar_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "common_base/static/src/js/es2024_polyfills.js",
        ],
        "web.assets_frontend": [
            "common_base/static/src/js/es2024_polyfills.js",
        ],
    },
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": ["static/description/icon.png"],
}
