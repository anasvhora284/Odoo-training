from odoo import fields, models, api
from odoo.exceptions import UserError

class ProductRentalRequest(models.Model):
    _name = 'product.rental.request'
    _description = 'Product Rental Request'
    _order = 'create_date desc'

    rental_id = fields.Many2one('product.rental', string="Product", required=True)
    product_id = fields.Many2one(related='rental_id.product_id', string="Product")
    customer_id = fields.Many2one(
        'res.partner', 
        string="Customer", 
        required=True, 
        default=lambda self: self.env.user.partner_id,
    )
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    rental_duration = fields.Integer(string="Duration (Days)", required=True, default=30)
    rental_start_date = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    rental_end_date = fields.Date(string="End Date", compute='_compute_end_date', store=True)
    state = fields.Selection([
        ('draft', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned')
    ], string="Status", default='draft')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    rental_price = fields.Float(related='rental_id.rental_price', readonly=True)
    total_price = fields.Float(compute='_compute_total_price', store=True)

    @api.depends('rental_start_date', 'rental_duration')
    def _compute_end_date(self):
        for record in self:
            if record.rental_start_date and record.rental_duration:
                record.rental_end_date = fields.Date.add(
                    record.rental_start_date, 
                    days=record.rental_duration
                )

    @api.depends('rental_price', 'quantity', 'rental_duration')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.rental_price * record.quantity * record.rental_duration

    def action_approve(self):
        self.ensure_one()
        if self.quantity > self.rental_id.available_quantity:
            raise UserError("Not enough quantity available!")
        self.state = 'approved'
        self.env['product.rental.history'].create({
            'rental_id': self.rental_id.id,
            'customer_id': self.customer_id.id,
            'quantity': self.quantity,
            'rental_start_date': self.rental_start_date,
            'rental_end_date': self.rental_end_date,
            'total_price': self.total_price
        })
        self.rental_id.write({
            'state': 'rented',
            'available_quantity': self.rental_id.available_quantity - self.quantity
        })
        return True

    def action_reject(self):
        self.ensure_one()
        self.state = 'rejected'
        return True

    def action_return(self):
        self.ensure_one()
        self.state = 'returned'
        return True

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('product_rental_custom.group_rental_manager'):
            vals['customer_id'] = self.env.user.partner_id.id
        return super().create(vals)

    def write(self, vals):
        if not self.env.user.has_group('product_rental_custom.group_rental_manager'):
            if 'customer_id' in vals:
                vals.pop('customer_id')
        return super().write(vals) 