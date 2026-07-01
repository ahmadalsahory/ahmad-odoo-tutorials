from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True, default="New")
    description = fields.Text()
    postcode = fields.Char(default="000000", size=12)
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[("new", "New"), ("open", "Open"), ("closed", "Closed")],
        default="new"
    )

    _name_unique = models.Constraint(
        'UNIQUE(name)', 
        'The Name must be unique'
    )

    @api.constrains('postcode','date_availability','bedrooms','living_area','facades','garden_area','expected_price')
    def _validate_property_fields(self):
        errors = []
        for record in self:
            errors.extend(record._validate_grater_than_zero())
            errors.extend(record._validate_postcode())
            errors.extend(record._validate_date_availability())
        if errors:
            raise ValidationError("\n".join(errors))


    def _validate_grater_than_zero(self):
        errors = []
        if self.bedrooms <= 0:
            errors.append("Bedrooms must be greater than zero")
        if self.living_area <= 0:
            errors.append("Living Area must be greater than zero")
        if self.facades <= 0:
            errors.append("Facades must be greater than zero")
        if self.garden_area <= 0:
            errors.append("Garden Area must be greater than zero")
        if self.expected_price <= 0:
            errors.append("Expected Price must be greater than zero")
        return errors

    def _validate_postcode(self):
        errors = []
        if self.postcode and (len(self.postcode) < 3 or len(self.postcode) > 12):
            errors.append("Postcode must be between 3 and 12 characters")
        return errors

    def _validate_date_availability(self):
        errors = []
        if self.date_availability and self.date_availability < fields.Date.today():
            errors.append("Date availability must be in the future")
        return errors