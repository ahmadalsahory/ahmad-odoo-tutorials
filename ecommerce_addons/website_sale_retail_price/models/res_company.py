from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    retail_pricelist_id = fields.Many2one('product.pricelist', string='Retail Pricelist')
