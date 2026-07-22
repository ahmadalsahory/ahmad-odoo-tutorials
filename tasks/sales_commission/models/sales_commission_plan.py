# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesCommissionPlan(models.Model):
    _name = 'sales.commission.plan'
    _description = 'Sales Commission Plan'

    name = fields.Char(string='Plan Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='sales_commission_plan_user_rel',
        column1='plan_id',
        column2='user_id',
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
        for line in self.line_ids:
            if line.amount_from <= net_amount <= line.amount_to:
                return line.rate
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
