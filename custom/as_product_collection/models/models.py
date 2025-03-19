# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request

class ProductCollection(models.Model):
    _name = 'website.product.collection'
    _description = 'Product Collection'
    _inherit = ['website.multi.mixin']

    name = fields.Char(string='Name', required=True)
    product_ids = fields.Many2many('product.template', string='Products')

    def get_collection_products(self):
        self.ensure_one()
        website = self.env['website'].get_current_website()
        pricelist = website._get_current_pricelist()
        products_data = []
        
        for product in self.product_ids:
            combination_info = product.with_context(
                website_id=website.id,
                pricelist=pricelist.id,
            )._get_combination_info()
            
            image_url = f'/web/image/product.template/{product.id}/image_512'
            
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': combination_info['price'],
                'price_formatted': pricelist.currency_id.format(combination_info['price']),
                'image_url': image_url,
            })
            
        return products_data
