from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    custom_dropship = fields.Boolean(string="Custom Drop-ship",default = False)