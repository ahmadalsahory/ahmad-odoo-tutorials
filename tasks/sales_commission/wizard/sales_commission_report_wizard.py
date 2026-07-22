# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesCommissionReportWizard(models.TransientModel):
    _name = 'sales.commission.report.wizard'
    _description = 'Sales Commission Report Wizard'

    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    user_ids = fields.Many2many(
        comodel_name='res.users',
        string='Salespersons',
    )
    line_ids = fields.One2many(
        comodel_name='sales.commission.report.line',
        inverse_name='wizard_id',
        string='Report Lines',
        readonly=True,
    )

    def action_generate_report(self):
        """Compute sales invoice amounts and calculate commissions."""
        self.ensure_one()
        self.line_ids.unlink()

        salespersons = self.user_ids or self.env['res.users'].search([('share', '=', False)])
        report_lines = []

        for user in salespersons:
            # Search posted and paid customer invoices
            invoices = self.env['account.move'].search([
                ('user_id', '=', user.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ('paid', 'in_payment')),
                ('invoice_date', '>=', self.date_from),
                ('invoice_date', '<=', self.date_to),
            ])
            
            # Search posted and paid customer credit notes
            credit_notes = self.env['account.move'].search([
                ('user_id', '=', user.id),
                ('move_type', '=', 'out_refund'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ('paid', 'in_payment')),
                ('invoice_date', '>=', self.date_from),
                ('invoice_date', '<=', self.date_to),
            ])

            invoiced_amount = sum(invoices.mapped('amount_untaxed_signed'))
            refund_amount = abs(sum(credit_notes.mapped('amount_untaxed_signed')))
            net_amount = invoiced_amount - refund_amount

            # Find matching commission plan for user
            plan = self.env['sales.commission.plan'].search([('user_ids', 'in', user.id)], limit=1)
            rate = plan.get_commission_rate(net_amount) if plan else 0.0
            commission_amount = (net_amount * rate) / 100.0 if net_amount > 0 else 0.0

            report_lines.append((0, 0, {
                'user_id': user.id,
                'invoiced_amount': invoiced_amount,
                'refund_amount': refund_amount,
                'net_amount': net_amount,
                'rate': rate,
                'commission_amount': commission_amount,
            }))

        self.line_ids = report_lines

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Commission Report Results',
            'res_model': 'sales.commission.report.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_print_pdf(self):
        """Print QWeb PDF report for the calculated commission results."""
        self.ensure_one()
        if not self.line_ids:
            self.action_generate_report()
        return self.env.ref('sales_commission.action_report_sales_commission').report_action(self)


class SalesCommissionReportLine(models.TransientModel):
    _name = 'sales.commission.report.line'
    _description = 'Sales Commission Report Line'

    wizard_id = fields.Many2one(
        comodel_name='sales.commission.report.wizard',
        string='Wizard Reference',
        ondelete='cascade',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        required=True,
    )
    invoiced_amount = fields.Float(string='Paid Invoices Amount')
    refund_amount = fields.Float(string='Paid Credit Notes Amount')
    net_amount = fields.Float(string='Net Amount')
    rate = fields.Float(string='Commission Rate (%)')
    commission_amount = fields.Float(string='Commission Amount')
