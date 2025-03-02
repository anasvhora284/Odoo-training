from odoo import fields, models

class ProductRentalHistory(models.Model):
    _name = 'product.rental.history'
    _description = 'Product Rental History'
    _order = 'create_date desc'

    rental_id = fields.Many2one('product.rental', string="Rental Product", required=True, ondelete='cascade')
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    quantity = fields.Integer(string="Quantity", required=True)
    rental_start_date = fields.Date(string="Start Date", required=True)
    rental_end_date = fields.Date(string="End Date", required=True)
    total_price = fields.Float(string="Total Price", required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id') 