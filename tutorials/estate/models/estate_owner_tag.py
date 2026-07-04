from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstateOwnerTag(models.Model):
    _name = 'estate.owner.tag'
    _description = 'Owner Tag'

    name = fields.Char(string="Tag Name", required=True, size=20)
    owner_ids = fields.Many2many(
        'estate.owner',
        relation='estate_owner_tag_rel',
        column1='tag_id',
        column2='owner_id',
        string="Owners"
    )

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'The Tag Name must be unique.'
    )

    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if record.name and len(record.name) < 3:
                raise ValidationError("The Tag Name must be at least 3 characters long.")
