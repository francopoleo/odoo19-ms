# -*- coding: utf-8 -*-
"""Carrega a configuração operacional fora dos módulos funcionais.

Os arquivos continuam próximos aos módulos que definem seus modelos nesta
primeira etapa para preservar XML IDs públicos e reduzir risco de migração.
O carregamento, porém, pertence exclusivamente a este módulo de configuração.
"""

import logging

from odoo.tools.convert import convert_file


_logger = logging.getLogger(__name__)

CONFIG_FILES = (
    ("common_base", "data/common_config_data.xml"),
    ("property_core", "data/property_contact_categories.xml"),
    ("property_core", "data/property_taxonomy_data.xml"),
    ("property_core", "data/property_media_category_data.xml"),
    ("document_core", "data/document_seed_data.xml"),
    ("document_dossier", "data/dossier_process_data.xml"),
    ("governance", "data/governance_stage_data.xml"),
    ("governance", "data/governance_case_type_data.xml"),
    ("governance", "data/governance_case_type_property_catalog.xml"),
    ("governance", "data/governance_sla_rule_data.xml"),
    ("governance", "data/governance_email_channel_data.xml"),
    ("governance", "data/governance_activity_data.xml"),
    ("property_contract_amendment_enterprise", "data/amendment_reason_data.xml"),
    ("enterprise_configuration_seed", "data/governance_pending_template_data.xml"),
)


def post_init_hook(env):
    """Instala os catálogos padrão uma única vez durante a instalação."""
    for module, filename in CONFIG_FILES:
        _logger.info("[enterprise_configuration_seed] carregando %s/%s", module, filename)
        convert_file(env, module, filename, {}, mode="init", noupdate=False)
    _ensure_dossier_templates(env)


def _ensure_dossier_templates(env):
    """Cria os checklists mínimos que tornam os processos utilizáveis."""
    Template = env["document.dossier.template"].sudo()
    Process = env["dossier.process"].sudo()
    DocumentType = env["document.type"].sudo()
    templates = {
        "CFG-OWNER-VALIDATION": {
            "name": "Cadastro e validação do proprietário",
            "process": "document_dossier.process_property_purchase",
            "description": "Conferência cadastral, identidade, titularidade e poderes de representação.",
            "documents": ["identity_rg", "legal_power_of_attorney"],
        },
        "CFG-ASSET-REGULARIZATION": {
            "name": "Cadastro e regularização do imóvel",
            "process": "document_dossier.process_property_purchase",
            "description": "Formação do dossiê jurídico, técnico e regulatório do imóvel.",
            "documents": ["legal_title_registry", "legal_deed", "legal_negative_certificate", "regulatory_zoning_certificate"],
        },
        "CFG-TENANT-VALIDATION": {
            "name": "Cadastro e validação do locatário",
            "process": "document_dossier.process_property_lease",
            "description": "Identificação, análise cadastral, garantia e documentação da locação.",
            "documents": ["identity_rg", "commercial_registration_form", "commercial_guarantee"],
        },
        "CFG-LEASE-OPERATION": {
            "name": "Formalização e operação da locação",
            "process": "document_dossier.process_property_lease",
            "description": "Contrato, vistoria inicial, seguro e entrega de chaves.",
            "documents": ["legal_lease_contract", "commercial_initial_inspection_term", "financial_insurance_policy", "legal_keys_handover_term"],
        },
        "CFG-AUDIT-COMPLIANCE": {
            "name": "Auditoria e conformidade documental",
            "process": "document_dossier.process_governance_audit",
            "description": "Verificação de validade, evidências, riscos, pendências e aprovação formal.",
            "documents": ["governance_due_diligence", "governance_evidence"],
        },
    }
    for code, values in templates.items():
        template = Template.search([("code", "=", code)], limit=1)
        if not template:
            template = Template.create({
                "name": values["name"],
                "code": code,
                "description": values["description"],
            })
        process = env.ref(values["process"], raise_if_not_found=False)
        if process and template not in process.template_ids:
            process.write({"template_ids": [(4, template.id)]})
        existing = template.line_ids.mapped("document_type_id.code")
        for sequence, document_code in enumerate(values["documents"], 10):
            if document_code in existing:
                continue
            document_type = DocumentType.search([("code", "=", document_code)], limit=1)
            if document_type:
                env["document.dossier.template.line"].sudo().create({
                    "template_id": template.id,
                    "sequence": sequence,
                    "name": document_type.name,
                    "document_type_id": document_type.id,
                    "required": True,
                    "requires_file": True,
                })
