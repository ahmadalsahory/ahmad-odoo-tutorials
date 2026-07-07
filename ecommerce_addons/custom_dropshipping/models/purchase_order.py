from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_id = fields.Many2one('sale.order', string="Sales Order", readonly=True)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _create_or_update_picking(self):
        if self.env.context.get('skip_create_picking'):
            # Bypassing because procurement will manually link the stock moves
            return
        return super()._create_or_update_picking()
