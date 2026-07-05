from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    invoice_date_due = fields.Date(
        related='move_id.invoice_date_due',
        store=True,
        string='Invoice Due Date'
    )

    invoice_group_name = fields.Char(
        string='Invoice Group',
        compute='_compute_invoice_group_name',
        store=True
    )

    @api.depends('date', 'move_id.name')
    def _compute_invoice_group_name(self):
        for line in self:
            inv_name = line.move_id.name or 'Draft'
            if line.date:
                line.invoice_group_name = f"[{line.date}] {inv_name}"
            else:
                line.invoice_group_name = f"[No Date] {inv_name}"
