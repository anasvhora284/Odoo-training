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
    
    # Compute the deadline
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

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != record.id):
                raise UserError("Another offer has already been accepted.")
            
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.offer_ids.filtered(lambda o: o.id != record.id).write({'status': 'refused'})
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'offer_received'
            record.property_id.buyer_id = False
            record.property_id.selling_price = 0.0
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            if property_id:
                property = self.env['estate.property'].browse(property_id)
                
                if property.offer_ids:
                    highest_offer = max(property.offer_ids.mapped('price'))
                    if vals.get('price', 0) <= highest_offer:
                        raise exceptions.UserError(
                            f'Cannot create offer: there is already a higher offer (${highest_offer:,.2f})'
                        )
                    
                property.state = 'offer_received'
        
        return super().create(vals_list)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'Offer price must be strictly positive!')
    ]