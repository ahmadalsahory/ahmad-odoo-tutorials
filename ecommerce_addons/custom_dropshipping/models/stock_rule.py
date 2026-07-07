from odoo import models, fields, api

class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _run_buy(self, procurements):
        for procurement, rule in procurements:
            # 1. Check if this is a dropship rule
            is_dropship = rule.picking_type_id.code == 'dropship' or rule.route_id == self.env.ref('stock_dropshipping.route_drop_shipping', raise_if_not_found=False)
            if not is_dropship:
                continue

            # 2. Get the sale order line and order
            sale_line_id = procurement.values.get('sale_line_id')
            if not sale_line_id:
                continue
            sale_line = self.env['sale.order.line'].browse(sale_line_id)
            sale_order = sale_line.order_id

            # 3. Check settings and custom supplier
            if sale_order.company_id.custom_dropship and sale_order.supplier_id:
                supplier = sale_order.supplier_id
                product = procurement.product_id
                
                # Find existing supplierinfo or create a new one dynamically
                supplierinfo = product.seller_ids.filtered(lambda s: s.partner_id == supplier)[:1]
                if not supplierinfo:
                    supplierinfo = self.env['product.supplierinfo'].create({
                        'partner_id': supplier.id,
                        'product_tmpl_id': product.product_tmpl_id.id,
                        'price': 0.0,
                        'min_qty': 0.0,
                    })
                # Force the procurement to use this supplierinfo
                procurement.values['supplierinfo_id'] = supplierinfo

        # Call super, passing skip_create_picking=True in context
        return super(StockRule, self.with_context(skip_create_picking=True))._run_buy(procurements)


    def _make_po_get_domain(self, company_id, values, partner):
        domain = super()._make_po_get_domain(company_id, values, partner)
        sale_line_id = values.get('sale_line_id')
        if sale_line_id:
            sale_line = self.env['sale.order.line'].browse(sale_line_id)
            sale_order = sale_line.order_id
            if sale_order.company_id.custom_dropship and sale_order.supplier_id:
                # Find if any PO is already linked to this Sales Order
                po_lines = self.env['purchase.order.line'].sudo().search([
                    ('sale_line_id', 'in', sale_order.order_line.ids)
                ])
                existing_po = po_lines.mapped('order_id')
                if existing_po:
                    # Force Odoo to add the line to this specific PO
                    return (('id', '=', existing_po[0].id),)
                else:
                    # Enforce that we only group with a draft PO created for this SO
                    domain = (
                        ('sale_id', '=', sale_order.id),
                        ('partner_id', '=', partner.id),
                        ('company_id', '=', company_id.id),
                        ('state', '=', 'draft'),
                    )
        return domain


    def _prepare_purchase_order(self, company_id, origins, values):
        res = super()._prepare_purchase_order(company_id, origins, values)
        if values and values[0].get('sale_line_id'):
            sale_line = self.env['sale.order.line'].browse(values[0]['sale_line_id'])
            res['sale_id'] = sale_line.order_id.id
        return res

