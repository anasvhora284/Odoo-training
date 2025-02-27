from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)',
         'Property tag name must be unique!')
    ]