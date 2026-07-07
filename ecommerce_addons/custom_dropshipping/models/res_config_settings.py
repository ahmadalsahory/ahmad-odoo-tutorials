from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    custom_dropship = fields.Boolean(
        related = 'company_id.custom_dropship',
        readonly = False,
        string = "Custom Drop-ship",
        help = "If enabled, a custom Supplier must be defined on Sales Orders containing dropshipped products."
    )