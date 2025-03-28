# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    enable_sbodr = fields.Boolean(
        string="Enable Bulk Discount Request", 
        default=False,
        help="Enable Special Bulk Order Discount Request for this product variant"
    )
    
    is_sbodr_global_enabled = fields.Boolean(
        string="SBODR Feature Enabled", 
        compute="_compute_is_sbodr_global_enabled", 
        store=False,
        help="Technical field to check if SBODR feature is enabled in website settings"
    )
    
    def _compute_is_sbodr_global_enabled(self):
        """Check if SBODR is enabled in the website settings"""
        # Use the first active website with SBODR enabled
        website_with_sbodr = self.env['website'].search([('enable_sbodr', '=', True)], limit=1)
        enabled = bool(website_with_sbodr)
        
        for product in self:
            product.is_sbodr_global_enabled = enabled
    
    @api.model
    def _is_sbodr_enabled_on_website(self):
        """Check if SBODR is enabled in the current website settings"""
        website = self.env['website'].get_current_website()
        return website.enable_sbodr