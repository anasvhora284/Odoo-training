from odoo import models, fields, api, exceptions
from odoo.tools import date_utils
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", required=True, default=7)
    create_date = fields.Date(string="Creation Date", readonly=True)
    date_deadline = fields.Date(
        string="Deadline", 
        compute="_compute_date_deadline", 
        inverse='_inverse_date_deadline',
        store=True
    )
    property_type_id = fields.Many2one(
        'estate.property.type', 
        related='property_id.property_type_id', 
        string="Property Type",
        store=True,
        readonly=True
    )
    seller_id = fields.Many2one(
        'res.users', 
        related='property_id.seller_id', 
        string='Seller',
        store=True
    )
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = date_utils.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = date_utils.add(fields.Date.today(), days=record.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' in vals:
                property = self.env['estate.property'].browse(vals['property_id'])
                if property.state not in ['new', 'offer_received']:
                    raise UserError("You cannot make offers on sold or canceled properties!")
                if property.offer_ids:
                    if vals.get('price', 0) <= max(property.offer_ids.mapped('price')):
                        raise UserError("The offer must be higher than %.2f" % max(property.offer_ids.mapped('price')))
                if property.state == 'new':
                    property.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        if self.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != self.id):
            raise UserError("Another offer has already been accepted!")
        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.offer_ids.filtered(lambda o: o.id != self.id).write({'status': 'refused'})
        return True

    def action_refuse(self):
        self.status = 'refused'
        return True

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'Offer price must be strictly positive!')
    ]