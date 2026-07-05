from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    prev_invoice_line_count = fields.Integer(
        string='Previous Invoices Count',
        compute='_compute_prev_invoice_line_count'
    )

    @api.depends('partner_id', 'invoice_date', 'invoice_line_ids.product_id')
    def _compute_prev_invoice_line_count(self):
        for move in self:
            if not move.invoice_date or not move.partner_id:
                move.prev_invoice_line_count = 0
                continue

            # 1. جلب المنتجات المضافة للفاتورة الحالية
            current_product_ids = move.invoice_line_ids.filtered(lambda l: l.display_type == 'product').mapped('product_id').ids
            if not current_product_ids:
                move.prev_invoice_line_count = 0
                continue

            # 2. حساب عدد السطور السابقة للمنتجات الحالية فقط
            domain = [
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.state', '=', 'posted'),
                ('move_id.commercial_partner_id', '=', move.commercial_partner_id.id),
                ('move_id.invoice_date', '<', move.invoice_date),
                ('display_type', '=', 'product'),
                ('product_id', 'in', current_product_ids),
            ]
            move.prev_invoice_line_count = self.env['account.move.line'].search_count(domain)

    def action_view_prev_invoices(self):
        self.ensure_one()
        current_product_ids = self.invoice_line_ids.filtered(lambda l: l.display_type == 'product').mapped('product_id').ids
        
        domain = [
            ('move_id.move_type', '=', 'out_invoice'),
            ('move_id.state', '=', 'posted'),
            ('move_id.commercial_partner_id', '=', self.commercial_partner_id.id),
            ('move_id.invoice_date', '<', self.invoice_date),
            ('display_type', '=', 'product'),
        ]
        
        if current_product_ids:
            domain.append(('product_id', 'in', current_product_ids))
        else:
            domain.append(('id', '=', False))

        return {
            'name': 'Previous Invoiced Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.line',
            'view_mode': 'list',
            'views': [(self.env.ref('account_prev_invoices.view_move_line_prev_invoices_tree').id, 'list')],
            'search_view_id': self.env.ref('account_prev_invoices.view_move_line_prev_invoices_search').id,
            'domain': domain,
            'target': 'new',
            'context': {
                'search_default_group_by_invoice': 1,
                'create': False,
                'edit': False,
            },
        }
