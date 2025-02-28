from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = "sequence, name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string='Offers Count', compute='_compute_offer_count')
    property_count = fields.Integer(compute='_compute_property_count')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('unique_type_name_company', 'UNIQUE(name, company_id)',
         'Property type name must be unique per company!')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    @api.depends('property_ids')
    def _compute_property_count(self):
        for record in self:
            record.property_count = self.env['estate.property'].search_count([('property_type_id', '=', record.id)])
