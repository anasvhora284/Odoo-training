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
        print("hello from is_sbodr_button_visible method")  # Print hello when checking button visibility
        
        self.ensure_one()
        
        # Check if SBODR is enabled on the website
        website_enabled = self.enable_sbodr
        
        # No need to check product if website setting is off
        if not website_enabled:
            print(f"SBODR website setting is off - will hide button")
            return False
            
        # Check if there's a valid product
        if not product:
            print(f"No product provided - will hide button")
            return False
            
        # Handle both product.template and product.product models
        product_model = product._name
        
        if product_model == 'product.template':
            # If it's a template, check if any variant has SBODR enabled
            variant_enabled = any(variant.enable_sbodr for variant in product.product_variant_ids)
            print(f"Checking template {product.id} - found variants with SBODR: {variant_enabled}")
        else:
            # It's a product.product (variant)
            variant_enabled = getattr(product, 'enable_sbodr', False)
            print(f"Checking variant {product.id} ({product.name}) - SBODR enabled: {variant_enabled}")
        
        result = website_enabled and variant_enabled
        print(f"Final SBODR visibility decision: {result}")
        return result
    
    def check_variant(self, product_variant):
        print("Checking variant:", product_variant.enable_sbodr)
        print("Methods and properties of the product variant:")
        for attr in dir(product_variant):
            print(attr)
        """Check if the product variant is SBODR enabled"""
        if not product_variant.enable_sbodr:
            print("SBODR not enabled for this variant")
            return False
        return True
