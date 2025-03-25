from odoo import models, fields, api
import ast

class ColorCondition(models.Model):
    _name = 'color.condition'
    _description = 'Color Conditions for List Views'

    name = fields.Char(string='Name', required=True)
    model_id = fields.Many2one('ir.model', string='Model', required=True, ondelete='cascade', index=True)
    model_name = fields.Char(related='model_id.model', string='Model Name', readonly=True, store=True)
    domain = fields.Char(string='Domain', required=True, default='[]')
    text_color = fields.Char(string='Text Color', default='#FFFFFF')
    background_color = fields.Char(string='Background Color', default='#000000')

    @api.onchange('model_id')
    def _onchange_model_id(self):
        """Reset domain when model changes"""
        self.domain = '[]'

    @api.model
    def get_color_conditions(self, model_name):
        """Get color conditions for a specific model."""
        print(f"Getting color conditions for model: {model_name}")
        model = self.env['ir.model'].search([('model', '=', model_name)], limit=1)
        if not model:
            print(f"No model found for: {model_name}")
            return []
        
        conditions = self.search([('model_id', '=', model.id)])
        print(f"Found {len(conditions)} conditions for model: {model_name}")
        
        result = []
        for condition in conditions:
            try:
                domain = ast.literal_eval(condition.domain or '[]')
                print(f"Condition: {condition.name}, Domain: {domain}")
                result.append({
                    'domain': domain,
                    'text_color': condition.text_color,
                    'background_color': condition.background_color,
                })
            except Exception as e:
                print(f"Error parsing domain for condition {condition.name}: {e}")
                # Skip invalid domains
                continue
        
        return result 