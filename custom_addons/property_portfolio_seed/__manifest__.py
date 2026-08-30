# -*- coding: utf-8 -*-
{
    "name": "Silva Empreendimentos - Portfólio Imobiliário",
    "summary": "Carteira de imóveis da Silva Empreendimentos, atualizável conforme a lista real.",
    "description": """
Carga opcional da carteira imobiliária da Silva Empreendimentos.

Este módulo contém somente os imóveis da carteira populada, atualmente baseada
na listagem KMS disponível no projeto. A lista pode e deve ser atualizada para
refletir o portfólio real vigente, incluindo inclusões, alterações cadastrais e
retiradas de imóveis. O módulo não cria contratos, documentos, usuários,
casos ou outros dados fictícios de demonstração.

Uso recomendado: instalar em ambientes de desenvolvimento, homologação ou em
uma base operacional após revisar a origem e a atualidade da listagem.
""",
    "version": "19.0.1.0.0",
    "category": "Real Estate",
    "author": "Franco Poleo / Manuela Silva",
    "license": "LGPL-3",
    "depends": ["property_core"],
    "data": ["data/property_asset_silva.xml"],
    "installable": True,
    "application": False,
}
