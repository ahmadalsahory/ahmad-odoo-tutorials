from odoo import models, fields

class TodoTaskTimesheet(models.Model):
    _name = 'todo.task.timesheet'
    _description = 'Task Timesheet'

    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    description = fields.Char(string='Description', required=True)
    hours = fields.Float(string='Time (Hours)', required=True, default=1.0)
    task_id = fields.Many2one(
        'todo.task',
        string='Task',
        ondelete='cascade',
        required=True
    )
