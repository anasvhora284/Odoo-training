# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    enable_sbodr = fields.Boolean(
        related='website_id.enable_sbodr', 
        readonly=False,
        string="Activate Special Bulk Order Discount Request (Activate SBODR)"
    )

    def action_enable_sbodr_all(self):
        """Enable SBODR for all product variants"""
        self.ensure_one()
        products = self.env['product.product'].search([])
        products.write({'enable_sbodr': True})
        
        # Return notification
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'SBODR activated for {len(products)} product variants',
                'type': 'success',
                'sticky': False,
            }
        }

class Website(models.Model):
    _inherit = "website"

    enable_sbodr = fields.Boolean(
        string="Activate Special Bulk Order Discount Request", 
        help="When enabled, customers can request special discounts for bulk orders on products that have SBODR enabled"
    )

    def is_sbodr_button_visible(self, product=None):
        """
        Check if the SBODR button should be visible based on website settings and product
        """
        
        self.ensure_one()
        
        website_enabled = self.enable_sbodr
        
        if not website_enabled:
            return False
            
        if not product:
            return False
            
        product_model = product._name
        
        if product_model == 'product.template':
            variant_enabled = any(variant.enable_sbodr for variant in product.product_variant_ids)
        else:
            variant_enabled = getattr(product, 'enable_sbodr', False)
        
        result = website_enabled and variant_enabled
        return result
    
    def check_variant(self, product_variant):
        for attr in dir(product_variant):
            print(attr)
        """Check if the product variant is SBODR enabled"""
        if not product_variant.enable_sbodr:
            return False
        return True
