from odoo import fields, models, api
from odoo.exceptions import UserError

class ProductRental(models.Model):
    _name = 'product.rental'
    _description = 'Product Rental'
    _order = 'create_date desc'
    _sql_constraints = [
        ('check_rental_price', 'CHECK(rental_price >= 0)', 'Rental price cannot be negative!'),
        ('check_quantity', 'CHECK(quantity > 0)', 'Quantity must be greater than 0!'),
        ('unique_product', 'UNIQUE(product_id)', 'This product is already in the rental list!') # This will prevent adding the same product multiple times
    ]
    _rec_name = "product_id" ## This will set the product_id as the default name field when there's no name field in the model

    product_id = fields.Many2one('product.product', string="Product", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    rental_price = fields.Float(string="Rental Price", required=True, groups="product_rental_custom.group_rental_manager")
    list_price = fields.Float(related='product_id.list_price', string="Sales Price", readonly=True)
    product_image = fields.Binary(related='product_id.image_1920', string="Product Image", readonly=True)
    rental_duration = fields.Integer(string="Rental Duration (Days)", default=30, required=True)
    rental_start_date = fields.Date(string="Start Date", default=fields.Date.today, required=True)
    rental_end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    quantity = fields.Integer(string="Quantity", default=1, required=True)
    product_quantity = fields.Integer(string="Available Stock", default=10, groups="product_rental_custom.group_rental_manager")
    available_quantity = fields.Integer(string="Available Quantity", compute='_compute_available_quantity', store=True)
    total_price = fields.Float(string="Total Price", compute='_compute_total_price', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('rented', 'Rented'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    note = fields.Text(string="Notes")
    active = fields.Boolean(default=True)
    request_ids = fields.One2many('product.rental.request', 'rental_id', string="Rental Requests")
    history_ids = fields.One2many('product.rental.history', 'rental_id', string="Rental History")
    request_count = fields.Integer(compute='_compute_counts')
    history_count = fields.Integer(compute='_compute_counts')

    # 
    @api.depends('request_ids', 'history_ids')
    def _compute_counts(self):
        for record in self:
            record.request_count = len(record.request_ids)
            record.history_count = len(record.history_ids)

    @api.depends('product_id')
    def _compute_rental_counts(self):
        for record in self:
            domain = [('product_id', '=', record.product_id.id)]
            record.total_rental_count = self.search_count(domain)
            record.active_rental_count = self.search_count(domain + [('state', '=', 'rented')])
            record.returned_rental_count = self.search_count(domain + [('state', '=', 'returned')])

    @api.depends('rental_start_date', 'rental_duration')
    def _compute_end_date(self):
        for record in self:
            if record.rental_start_date and record.rental_duration:
                record.rental_end_date = fields.Date.add(record.rental_start_date, days=record.rental_duration)

    @api.depends('rental_price', 'rental_duration', 'quantity')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.rental_price * record.rental_duration * record.quantity

    @api.depends('product_quantity', 'request_ids')
    def _compute_available_quantity(self):
        for record in self:
            rented_quantity = sum(record.request_ids.filtered(
                lambda r: r.state == 'approved'
            ).mapped('quantity'))
            record.available_quantity = record.product_quantity - rented_quantity

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.rental_price = self.product_id.list_price * 0.1  # 10% of sale price
            existing_rental = self.search([('product_id', '=', self.product_id.id)], limit=1)
            if existing_rental:
                self.product_quantity = existing_rental.product_quantity

    def action_rent(self):
        self.ensure_one()
        if not self.customer_id:
            raise UserError("Please select a customer!")
        if self.quantity > self.available_quantity:
            raise UserError("Not enough quantity available!")
        self.state = 'rented'
        return True

    def action_return(self):
        self.ensure_one()
        self.state = 'returned'
        return True

    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancelled'
        return True

    def _create_stock_move(self, move_type):
        stock_location = self.env.ref('stock.stock_location_stock')
        customer_location = self.env.ref('stock.stock_location_customers')
        
        source_location = stock_location if move_type == 'out' else customer_location
        destination_location = customer_location if move_type == 'out' else stock_location
        
        move_vals = {
            'name': f"{self.name} - {'Rental' if move_type == 'out' else 'Return'}",
            'product_id': self.product_id.id,
            'product_uom_qty': self.quantity,
            'product_uom': self.product_id.uom_id.id,
            'location_id': source_location.id,
            'location_dest_id': destination_location.id,
            'company_id': self.company_id.id,
            'state': 'done',
        }
        
        self.env['stock.move'].create(move_vals)

    def action_view_requests(self):
        self.ensure_one()
        return {
            'name': 'Rental Requests',
            'type': 'ir.actions.act_window',
            'res_model': 'product.rental.request',
            'view_mode': 'list,form',
            'domain': [('rental_id', '=', self.id)],
            'context': {'default_rental_id': self.id}
        }

    def action_view_history(self):
        self.ensure_one()
        return {
            'name': 'Rental History',
            'type': 'ir.actions.act_window',
            'res_model': 'product.rental.history',
            'view_mode': 'list,form',
            'domain': [('rental_id', '=', self.id)],
            'context': {'default_rental_id': self.id}
        }

    def action_create_request(self):
        self.ensure_one()
        return {
            'name': 'Create Rental Request',
            'type': 'ir.actions.act_window',
            'res_model': 'product.rental.request',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_rental_id': self.id,
                'default_customer_id': self.env.user.partner_id.id,
            }
        }

    @api.model
    def action_save(self):
        for record in self:
            if not record.product_id:
                raise UserError("Please select a product.")
            if record.rental_price < 0:
                raise UserError("Rental price cannot be negative.")

            record.write({
                'product_id': record.product_id.id,
                'rental_price': record.rental_price,
                'product_quantity': record.product_quantity,
            })
        return True

    @api.model
    def create(self, vals):
        if 'product_id' in vals:
            existing_rental = self.search([('product_id', '=', vals['product_id'])])
            if existing_rental:
                raise UserError("This product is already in the rental list!")
        return super(ProductRental, self).create(vals)