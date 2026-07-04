from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EstateOwner(models.Model):
    _name = 'estate.owner'
    _description = 'Perperty Owner'

    name = fields.Char(required = True, default = 'New Owner', size = 30)
    phone = fields.Char(string="Phone Number")
    address = fields.Char(size = 50)
    property_ids = fields.One2many(
        'estate.property',
        'owner_id',
        string="Properties"
    )
    tag_ids = fields.Many2many(
        'estate.owner.tag',
        relation='estate_owner_tag_rel',
        column1='owner_id',
        column2='tag_id',
        string="Tags"
    )

    _name_unique = models.Constraint(
        'UNIQUE(name)', 
        'The Name must be unique'
    )

    @api.constrains('phone','address')
    def _check_length(self):
        errors = []
        for record in self:
            if record.phone and (len(record.phone) < 7 or len(record.phone) > 15):
                errors.append("Phone number length should between 7 and 15")

        if errors:
            raise ValidationError("\n".join(errors))
