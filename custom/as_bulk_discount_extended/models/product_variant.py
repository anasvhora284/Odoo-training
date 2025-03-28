# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    enable_sbodr = fields.Boolean(
        string="Enable Bulk Discount Request", 
        default=False,
        help="Enable Special Bulk Order Discount Request for this product variant"
    )
    
    @api.model
    def _is_sbodr_enabled_on_website(self):
        """Check if SBODR is enabled in the current website settings"""
        website = self.env['website'].get_current_website()
        return website.enable_sbodr