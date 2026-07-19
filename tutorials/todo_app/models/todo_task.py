import pytz
from datetime import datetime, time
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
    timesheet_ids = fields.One2many(
        'todo.task.timesheet',
        'task_id',
        string='Timesheets'
    )

    @api.onchange('timesheet_ids', 'date_deadline')
    def _onchange_timesheet_hours(self):
        if not self.date_deadline:
            return
        
        user_tz = self.env.user.tz or 'UTC'
        tz = pytz.timezone(user_tz)
        
        now_local = datetime.now(tz)
        deadline_local = tz.localize(datetime.combine(self.date_deadline, time(23, 59, 59)))
        
        diff = deadline_local - now_local
        allowed_hours = max(0.0, diff.total_seconds() / 3600.0)
        
        total_hours = sum(line.hours for line in self.timesheet_ids)
        
        if total_hours > allowed_hours:
            return {
                'warning': {
                    'title': "Hours Limit Exceeded",
                    'message': f"Warning: Total logged hours ({total_hours:.1f}h) exceed the available time until the due date ({allowed_hours:.1f}h).",
                    'type': 'notification',
                    'sticky': False,
                }
            }

    @api.model
    def _read_group_state(self, stages, domain):
        return ['new', 'in_progress', 'completed']

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New' or not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('todo.task') or 'New'
        return super().create(vals_list)

