from odoo import models, fields, api
from odoo.tools import date_utils

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

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
    
    # Compute the deadline
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = date_utils.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = date_utils.add(fields.Date.today(), days=record.validity)

    @api.depends('create_date', 'validity')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days