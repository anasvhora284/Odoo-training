# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request

class ProductCollection(models.Model):
    _name = 'website.product.collection'
    _description = 'Product Collection'
    _inherit = ['website.multi.mixin']

    name = fields.Char(string='Name', required=True)
    product_ids = fields.Many2many('product.template', string='Products')

    def get_collection_data(self):
        self.ensure_one()
        products = self.get_collection_products()
        return {
            'id': self.id,
            'name': self.name,
            'products': products,
        }
    
    def get_collection_products(self):
        self.ensure_one()
        
        if not self.product_ids:
            return []
            
        website = self.env['website'].get_current_website()
        pricelist = website._get_current_pricelist()
        products_data = []
        
        for product in self.product_ids:
            try:
                product_with_context = product.with_context(
                    website_id=website.id,
                    pricelist=pricelist.id,
                )
                
                combination_info = product_with_context._get_combination_info()
                image_url = f'/web/image/product.template/{product.id}/image_512'
                
                product_variant = self.env['product.product'].search([
                    ('product_tmpl_id', '=', product.id)
                ], limit=1)
                
                products_data.append({
                    'id': product_variant.id,
                    'product_tmpl_id': product.id,
                    'name': product.name,
                    'price': combination_info['price'],
                    'price_formatted': pricelist.currency_id.format(combination_info['price']),
                    'image_url': image_url,
                    'type': product.type,
                    'website_id': website.id,
                    'pricelist_id': pricelist.id,
                    'combination_info': combination_info,
                })
            except Exception:
                continue
                
        return products_data
