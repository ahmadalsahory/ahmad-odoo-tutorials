# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    prev_invoice_line_count = fields.Integer(
        string='Previous Invoice Lines Count',
        compute='_compute_prev_invoice_line_count'
    )

    @api.depends('partner_id', 'invoice_date')
    def _compute_prev_invoice_line_count(self):
        for move in self:
            if not move.invoice_date or not move.partner_id:
                move.prev_invoice_line_count = 0
                continue


            domain = [
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.state', '=', 'posted'),
                ('move_id.commercial_partner_id', '=', move.commercial_partner_id.id),
                ('move_id.invoice_date', '<', move.invoice_date),
                ('display_type', '=', 'product'),
            ]

            move.prev_invoice_line_count = self.env['account.move.line'].search_count(domain)


    def action_view_prev_invoices(self):
        self.ensure_one()
        domain = [
            ('move_id.move_type', '=', 'out_invoice'),
            ('move_id.state', '=', 'posted'),
            ('move_id.commercial_partner_id', '=', self.commercial_partner_id.id),
            ('move_id.invoice_date', '<', self.invoice_date),
            ('display_type', '=', 'product'),
        ]
        # TODO: Return a window action dictionary for 'account.move.line'
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
                'search_default_group_by_product': 1,
                'create': False,
                'edit': False,
            },
        }


    def get_outstanding_invoices(self):
        self.ensure_one()
        if not self.partner_id:
            return self.env['account.move']
            
        domain = [
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'in', ('not_paid', 'partial')),
            ('commercial_partner_id', '=', self.commercial_partner_id.id),
        ]
        return self.env['account.move'].search(domain, order='invoice_date_due asc')
