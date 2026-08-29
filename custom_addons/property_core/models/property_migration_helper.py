from odoo import models


class PropertyMigrationHelper(models.AbstractModel):
    _name = "property.migration.helper"
    _description = "Property Migration Helper"

    def init(self):
        cr = self.env.cr
        # Corrige metadados legados do antigo property.document para o novo document_core.
        cr.execute("""
            UPDATE ir_model_fields
               SET relation = 'document.document'
             WHERE relation = 'property.document'
               AND name = 'document_ids'
               AND model IN ('property.complex', 'property.asset', 'property.contract')
        """)
        cr.execute("""
            UPDATE ir_act_window
               SET res_model = 'document.document'
             WHERE res_model = 'property.document'
        """)
        cr.execute("""
            UPDATE ir_act_window
               SET res_model = 'document.category'
             WHERE res_model = 'property.document.category'
        """)
        cr.execute("""
            UPDATE ir_act_window
               SET res_model = 'document.type'
             WHERE res_model = 'property.document.type'
        """)
        cr.execute("""
            UPDATE ir_act_window
               SET res_model = 'document.location'
             WHERE res_model = 'property.document.location'
        """)
