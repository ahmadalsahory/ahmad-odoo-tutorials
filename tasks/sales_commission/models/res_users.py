# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    commission_plan_id = fields.Many2one(
        comodel_name='sales.commission.plan',
        string='Commission Plan',
        help='Commission plan assigned to this salesperson',
    )
