from odoo import api, fields, models

class PropertySoldWizard(models.TransientModel):
    _name = 'estate.property.sold.wizard'
    _description = 'Search Sold Properties by Name'

    name = fields.Char(string='Property Name')
    result_ids = fields.Many2many(
        'estate.property', 
        'estate_property_sold_rel',
        'wizard_id',
        'property_id',
        string='Search Results'
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        properties = self.env['estate.property'].search([
            ('state', '=', 'sold'),
            ('selling_price', '>', 0)
        ])
        if 'result_ids' in fields_list:
            res['result_ids'] = [(6, 0, properties.ids)]
        return res

    def action_search_sold(self):
        domain = [
            ('state', '=', 'sold'),
            ('selling_price', '>', 0)
        ]
        if self.name:
            domain += [('name', 'ilike', self.name)]
            
        properties = self.env['estate.property'].search(domain)
        self.result_ids = [(6, 0, properties.ids)]
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.sold.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        } 