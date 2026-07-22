# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SalesCommissionPlan(models.Model):
    _name = 'sales.commission.plan'
    _description = 'Sales Commission Plan'

    name = fields.Char(string='Plan Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    user_ids = fields.One2many(
        comodel_name='res.users',
        inverse_name='commission_plan_id',
        string='Salespersons',
    )
    line_ids = fields.One2many(
        comodel_name='sales.commission.plan.line',
        inverse_name='plan_id',
        string='Commission Ranges',
    )

    def get_commission_rate(self, net_amount):
        """Calculate applicable commission rate for a net sales amount."""
        self.ensure_one()
        if not self.line_ids:
            return 0.0

        # 1. Direct match within range
        for line in self.line_ids:
            if line.amount_from <= net_amount <= line.amount_to:
                return line.rate

        # 2. Fallback for range gaps or exceeding upper bound:
        # Return the rate of the preceding tier with the largest amount_to <= net_amount
        preceding_lines = [line for line in self.line_ids if line.amount_to <= net_amount]
        if preceding_lines:
            return max(preceding_lines, key=lambda l: l.amount_to).rate

        return 0.0


class SalesCommissionPlanLine(models.Model):
    _name = 'sales.commission.plan.line'
    _description = 'Sales Commission Plan Line'
    _order = 'amount_from asc'

    plan_id = fields.Many2one(
        comodel_name='sales.commission.plan',
        string='Commission Plan',
        ondelete='cascade',
        required=True,
    )
    amount_from = fields.Float(string='From Amount', required=True)
    amount_to = fields.Float(string='To Amount', required=True)
    rate = fields.Float(string='Commission Rate (%)', required=True)

    @api.constrains('amount_from', 'amount_to', 'rate', 'plan_id')
    def _check_ranges(self):
        for line in self:
            if line.amount_from < 0:
                raise ValidationError("The 'From Amount' cannot be negative.")
            if line.amount_to <= line.amount_from:
                raise ValidationError("The 'To Amount' must be strictly greater than 'From Amount'.")
            if line.rate < 0 or line.rate > 100:
                raise ValidationError("The 'Commission Rate (%)' must be between 0 and 100.")

            other_lines = line.plan_id.line_ids - line
            for other in other_lines:
                if not (line.amount_to < other.amount_from or line.amount_from > other.amount_to):
                    raise ValidationError(
                        f"The commission range ({line.amount_from} - {line.amount_to}) overlaps with "
                        f"existing range ({other.amount_from} - {other.amount_to}) in plan '{line.plan_id.name}'."
                    )

