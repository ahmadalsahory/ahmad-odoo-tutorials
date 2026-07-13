from odoo import models, fields

class TodoTaskTimesheet(models.Model):
    _name = 'todo.task.timesheet'
    _description = 'Task Timesheet'

    description = fields.Char(string='Description', required=True)
    hours = fields.Float(string='Time (Hours)', required=True, default=1.0)
    task_id = fields.Many2one(
        'todo.task',
        string='Task',
        ondelete='cascade',
        required=True
    )
