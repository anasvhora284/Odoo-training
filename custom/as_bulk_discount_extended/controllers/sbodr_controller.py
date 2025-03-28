# -*- coding: utf-8 -*-

from math import prod
from odoo import http
from odoo.http import request

class SBODRController(http.Controller):
    @http.route('/sbodr/get_user_info', type='json', auth="public")
    def get_user_info(self):
        """Get current user information for the bulk discount dialog"""
        user = request.env.user
        is_logged_in = not user._is_public()
        
        if is_logged_in:
            partner = user.partner_id
            return {
                'is_logged_in': True,
                'name': partner.name,
                'email': partner.email,
                'user_id': user.id,
                'partner_id': partner.id,
            }
        else:
            return {
                'is_logged_in': False,
                'name': '',
                'email': '',
            }
    
    @http.route('/sbodr/check_variant', type='json', auth="public")
    def check_variant(self, product_id=None):        
        try:
            if not product_id:
                return {'success': False, 'error': 'No product ID provided'}
                
            product = request.env['product.product'].browse(int(product_id))
            
            if not product.exists():
                return {'success': False, 'error': 'Product not found'}
                
            website = request.env['website'].get_current_website()
            print(product.type)
            is_enabled = website.is_sbodr_button_visible(product) and product.type == 'consu'
            
            return {
                'success': True,
                'is_enabled': is_enabled,
                'product_name': product.name,
                'product_id': product.id
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    @http.route('/sbodr/submit_request', type='json', auth="public")
    def submit_sbodr_request(self, product_id, quantity, discount, notes, **kw):
        """Handle the bulk discount request submission from the frontend modal"""
        try:
            if not product_id:
                return {'success': False, 'error': 'No product ID provided'}
                
            # Find the product
            product = request.env['product.product'].browse(int(product_id))
            
            if not product.exists():
                return {'success': False, 'error': 'Product not found'}
            
            # Get user/partner information
            user = request.env.user
            partner = user.partner_id
            
            # Determine price from list_price (not price)
            product_name = product.name
            variant_name = product.product_tmpl_id.name  # Get the variant name
            price = product.list_price or 0.0
            
            # Get partner info
            full_name = partner.name if partner else 'Website Visitor'
            email = partner.email if partner else request.env.user.email
            
            # Calculate expected revenue - ensure it's a valid number
            try:
                qty = int(quantity) if quantity else 0
                disc = float(discount) if discount else 0
                expected_revenue = qty * price * ((100 - disc) / 100)
            except (ValueError, TypeError):
                expected_revenue = 0.0
            
            # Create a CRM lead with the new name format
            lead = request.env['crm.lead'].sudo().create({
                'name': f"Bulk Order Discount Request - {product_name} ({variant_name}) - {full_name}",
                'partner_name': full_name,
                'partner_id': partner.id if partner.exists() else False,
                'email_from': email,
                'description': f"Special Bulk Order Discount Request: \nProduct: {product_name} ({variant_name})\nQuantity: {quantity}\nRequested Discount: {discount}%\n\nCustomer Message:\n{notes}",
                'type': 'opportunity',
                'priority': '2',
                'expected_revenue': expected_revenue if expected_revenue > 0 else 0.0,
            })
            
            # Also create SBODR request record if the model exists
            if 'sbodr.request' in request.env:
                request.env['sbodr.request'].sudo().create({
                    'name': f"SBODR-{full_name}-{product_name} ({variant_name})",
                    'full_name': full_name,
                    'email': email,
                    'quantity': quantity,
                    'discount': float(discount) if discount else 0.0,
                    'description': notes,
                    'state': 'submitted',
                })
            
            return {
                'success': True,
                'lead_id': lead.id
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}