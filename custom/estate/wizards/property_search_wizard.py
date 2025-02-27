from odoo import api, fields, models

class PropertySearchWizard(models.TransientModel):
    _name = 'estate.property.search.wizard'
    _description = 'Search Properties by Name'

    name = fields.Char(string='Property Name')
    result_ids = fields.Many2many(
        'estate.property', 
        'estate_property_search_rel',
        'wizard_id',
        'property_id',
        string='Search Results'
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        properties = self.env['estate.property'].search([
            ('state', 'not in', ['sold', 'canceled'])
        ])
        if 'result_ids' in fields_list:
            res['result_ids'] = [(6, 0, properties.ids)]
        return res

    def action_search(self):
        domain = [('state', 'not in', ['sold', 'canceled'])]
        if self.name:
            domain += [('name', 'ilike', self.name)]
            
        properties = self.env['estate.property'].search(domain)
        self.result_ids = [(6, 0, properties.ids)]
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.search.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_search_sold(self):
        domain = [('state', '=', 'sold')]
        if self.name:
            domain += [('name', 'ilike', self.name)]
            
        properties = self.env['estate.property'].search(domain)
        self.result_ids = [(6, 0, properties.ids)]
        
        return self._reopen_view()

    def _reopen_view(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.search.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        } 