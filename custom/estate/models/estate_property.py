from odoo import models, fields, api, exceptions
from odoo.tools import date_utils, float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default= date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Garden Orientation")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], string="Status", default='new', required=True, copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, readonly=True)
    seller_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area"
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price"
    )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Expected price must be strictly positive!'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'Selling price must be positive!')
    ]

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'canceled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_price_difference(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_digits=2) and
                float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price! "
                    f"The expected price is {record.expected_price}, "
                    f"so the selling price should be at least {record.expected_price * 0.9}"
                )

    def action_print_property(self):
        return self.env.ref('estate.report_estate_property').report_action(self)