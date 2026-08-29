from odoo import fields, models


class PropertyComplexExt(models.Model):
    _inherit = "property.complex"

    # ==================== Imagem ====================
    image_1920 = fields.Image("Foto", max_width=1920, max_height=1920)
    image_512 = fields.Image("Thumbnail", related="image_1920", max_width=512, max_height=512, store=True)
