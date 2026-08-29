# -*- coding: utf-8 -*-
from odoo import fields, models


class HelpImportWizard(models.TransientModel):
    _name = "help.import.wizard"
    _description = "Assistente de Importação da Central de Ajuda"

    reset_before_import = fields.Boolean(
        string="Zerar documentação antes de importar",
        default=False,
        help="Use em homologação quando a base ficou poluída por importações antigas. Remove artigos, contextos, fontes e mapa de cobertura da Central antes de redescobrir os docs versionados.",
    )
    discover_modules = fields.Boolean(string="Varrer módulos instalados", default=True)
    import_sources = fields.Boolean(string="Importar fontes ativas", default=True)
    generate_context_map = fields.Boolean(string="Gerar mapa de contextos", default=True)
    only_modules_with_docs = fields.Boolean(string="Somente módulos com docs", default=True)
    normalize_context = fields.Boolean(
        string="Sanear painel contextual",
        default=True,
        help="Remove do drawer manuais completos, documentação técnica e artigos genéricos globais, mantendo-os apenas na biblioteca.",
    )
    result_message = fields.Text(string="Resultado", readonly=True)

    def action_execute(self):
        self.ensure_one()
        messages = []
        Article = self.env["help.article"].sudo()
        if self.reset_before_import:
            Article.action_reset_documentation_repository()
            messages.append("Documentação anterior da Central zerada.")
        if self.discover_modules:
            count = self.env["help.doc.source"].action_discover_installed_module_docs()
            messages.append("Fontes descobertas/atualizadas: %s" % count)
        if self.import_sources:
            count = self.env["help.doc.source"].action_import_active_sources()
            messages.append("Fontes importadas: %s" % count)
        if self.normalize_context:
            Article.action_normalize_contextual_display()
            messages.append("Painel contextual saneado: manuais completos e artigos genéricos ficaram só na biblioteca.")
        if self.generate_context_map:
            count = self.env["help.context.candidate"].action_generate_candidates(only_modules_with_docs=self.only_modules_with_docs)
            messages.append("Contextos técnicos novos mapeados: %s" % count)
        self.result_message = "\n".join(messages) or "Nenhuma ação executada."
        return {
            "type": "ir.actions.act_window",
            "res_model": "help.import.wizard",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
