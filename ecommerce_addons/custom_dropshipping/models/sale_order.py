from odoo import api, fields, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    company_partner_id = fields.Many2one('res.partner', related='company_id.partner_id')
    
    supplier_id = fields.Many2one(
        'res.partner', 
        string='Supplier', 
        domain="[('parent_id', '=', False), ('user_ids', '=', False), ('id', '!=', company_partner_id)]",
        help="Supplier to use for dropshipping all products in this sales order."
    )

    custom_dropship = fields.Boolean(related='company_id.custom_dropship')
    has_dropship_product = fields.Boolean(
        compute='_compute_has_dropship_product',
        store=True,
        string='Has Dropship Product'
    )

    @api.depends('order_line.product_id')
    def _compute_has_dropship_product(self):
        dropship_route = self.env.ref('stock_dropshipping.route_drop_shipping', raise_if_not_found=False)
        for order in self:
            has_dropship = False
            if dropship_route:
                for line in order.order_line:
                    product = line.product_id
                    if product:
                        product_routes = product.route_ids | product.categ_id.route_ids | product.product_tmpl_id.route_ids
                        if dropship_route in product_routes:
                            has_dropship = True
                            break
            order.has_dropship_product = has_dropship

    @api.constrains('supplier_id', 'state', 'order_line')
    def _check_dropship_supplier(self):
        for order in self:
            if (order.custom_dropship 
                    and order.has_dropship_product 
                    and order.state not in ['sale', 'done', 'cancel'] 
                    and not order.supplier_id):
                raise ValidationError(
                    "A Supplier must be set on the Sales Order before confirming "
                    "because it contains dropshipped products."
                )
