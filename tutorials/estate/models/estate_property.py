from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Title", required=True, default="New", tracking = True)
    description = fields.Text()
    postcode = fields.Char(default="000000", size=12)
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3), tracking = True)
    is_late = fields.Boolean(compute="_compute_is_late")
    
    @api.depends('date_availability')
    def _compute_is_late(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.date_availability and rec.date_availability < today:
                rec.is_late = True
            else:
                rec.is_late = False

    expected_price = fields.Float(required=True, tracking=True)
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
        selection=[("new", "New"), ("offer-received", "Offer Received"), ("offer-accepted", "Offer Accepted"),("sold","Sold"),("cancelled","Cancelled")],
        default="new"
    )

    def property_cancelled(self):
        for rec in self:
            rec.state = 'cancelled'

    def _send_email_for_late_properties(self):
        today = fields.Date.context_today(self)
        late_properties = self.search([
            ('date_availability', '<', today),
            ('state', 'not in', ['sold', 'cancelled'])
        ])
        print('======== SEND EMAILS ========', flush=True)

    owner_id = fields.Many2one("estate.owner",string = 'Owner', tracking = True)
    owner_phone = fields.Char(string = 'Owner Phone', related = 'owner_id.phone')

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    best_price = fields.Float(compute="_compute_best_price", readonly=True)
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            prices = rec.offer_ids.mapped("price")
            rec.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        for rec in self:
            if self.garden:
                self.garden_area=10
                self.garden_orientation="north"
            else:
                rec.garden_orientation = None
                rec.garden_area = 0
            

    _name_unique = models.Constraint(
        'UNIQUE(name)', 
        'The Name must be unique'
    )

    def action_sold_offer(self):
        for rec in self:
            if(rec.state == 'offer-accepted'):
                rec.state = 'sold'
            else:
                raise UserError("You cannot sell the property until an offer has been accepted!")
        return True
    
    def action_cancel_offer(self):
        for rec in self:
            if(rec.state != 'sold'):
                rec.state = 'cancelled'
            else:
                raise UserError("You cannot cancel the property while an offer accepted!")
        return True

    @api.constrains('postcode','date_availability','bedrooms','living_area','facades','garden_area','expected_price')
    def _validate_property_fields(self):
        errors = []
        for record in self:
            errors.extend(record._validate_grater_than_zero())
            errors.extend(record._validate_postcode())
            #errors.extend(record._validate_date_availability())
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
        if self.garden and self.garden_area <= 0:
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


    @api.model_create_multi
    def create(self, vals_list):
        print("======== BEFORE CREATING ========", flush=True)
        result = super(EstateProperty, self).create(vals_list)
        print("======== AFTER CREATING ========", flush=True)
        return result

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, **kwargs):
        print('======== BEFORE SEARCH ========', flush=True)
        result = super(EstateProperty, self)._search(domain, offset, limit, order, **kwargs)
        print('======== AFTER SEARCH ========', flush=True)
        return result

    def write(self, vals):
        print('======== BEFORE WRITING ========', flush=True)
        result = super(EstateProperty, self).write(vals)
        print('======== AFTER WRITING ========', flush=True)
        return result

    def unlink(self):
        print('======== BEFORE DELETING ========', flush=True)
        result = super(EstateProperty, self).unlink()
        print('======== AFTER DELETING ========', flush=True)
        return result