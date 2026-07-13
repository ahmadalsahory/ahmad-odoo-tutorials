from odoo import models, fields, api

class TodoTask(models.Model):
    _name = "todo.task"
    _description = "Todo Task"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True, default='New', tracking=True)
    description = fields.Text()
    date_deadline = fields.Date(string='Due date', copy=False, default=fields.Date.add(fields.Date.today(), days=1), tracking=True)
    
    state = fields.Selection(string='Status', selection=[
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='new', required=True, tracking=True, group_expand='_read_group_state')

    user_ids = fields.Many2many('res.users', string='Assigned users', tracking=True)

    @api.model
    def _read_group_state(self, stages, domain):
        return ['new', 'in_progress', 'completed']
