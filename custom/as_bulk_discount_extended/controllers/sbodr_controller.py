# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class SBODRController(http.Controller):
    @http.route('/sbodr/request', type='json', auth="user", methods=["POST"])
    def sbodr_request(self, full_name, email, quantity, discount, description, **kw):
        # Get product info from session (current product)
        product_id = request.session.get('sale_order_last_product_id')
        product = request.env['product.product'].browse(product_id) if product_id else False
        
        # Get user/partner information
        user = request.env.user
        partner = user.partner_id
        
        # Determine price and product information
        product_name = product.name if product else "Unknown Product"
        price = product.list_price if product else 100.0
        
        # Calculate expected revenue
        expected_revenue = quantity * price * ((100 - float(discount)) / 100)
        
        # Create a CRM lead
        lead = request.env['crm.lead'].create({
            'name': f"Bulk Order Discount Request - {product_name}",
            'partner_name': full_name,
            'partner_id': partner.id if partner else False,
            'email_from': email,
            'description': f"""
Special Bulk Order Discount Request:
Product: {product_name}
Quantity: {quantity}
Requested Discount: {discount}%

Customer Message:
{description}
            """,
            'sbodr_description': description,
            'sbodr_discount': float(discount),
            'sbodr_quantity': quantity,
            'expected_revenue': expected_revenue,
            'type': 'opportunity',
            'priority': '2',
        })
        
        # Also create SBODR request record for tracking
        request.env['sbodr.request'].create({
            'name': f"SBODR-{full_name}-{product_name}",
            'full_name': full_name,
            'email': email,
            'quantity': quantity,
            'discount': float(discount),
            'description': description,
            'state': 'submitted',
        })
        
        # Return success with rainbow man effect
        return {
            'status': 'success',
            'effect': {
                'effect': 'rainbow_man',
                'message': 'Thank you! We will get back to you shortly.',
                'img_url': '/web/static/img/smile.svg',
            }
        }
        
    @http.route('/sbodr/check_variant', type='json', auth="public")
    def check_variant(self, product_id=None):
        """Endpoint to handle variant change events"""
        print("hello")  # Print hello when a variant changes
        
        try:
            if not product_id:
                return {'success': False, 'error': 'No product ID provided'}
                
            # Find the product
            product = request.env['product.product'].sudo().browse(int(product_id))
            
            if not product.exists():
                return {'success': False, 'error': 'Product not found'}
                
            # Get website
            website = request.website
            
            # Check if SBODR is enabled for this product
            is_enabled = website.is_sbodr_button_visible(product)
            print(f"Product ID: {product_id}, Name: {product.name}, SBODR enabled: {is_enabled}")
            
            return {
                'success': True,
                'is_enabled': is_enabled,
                'product_name': product.name,
                'product_id': product.id
            }
        except Exception as e:
            print(f"Error in check_variant: {e}")
            return {'success': False, 'error': str(e)}
            
    @http.route('/sbodr/submit_request', type='json', auth="public")
    def submit_sbodr_request(self, product_id, quantity, discount, notes, **kw):
        """Handle the bulk discount request submission from the frontend modal"""
        try:
            if not product_id:
                return {'success': False, 'error': 'No product ID provided'}
                
            # Find the product
            product = request.env['product.product'].sudo().browse(int(product_id))
            
            if not product.exists():
                return {'success': False, 'error': 'Product not found'}
            
            # Get user/partner information
            user = request.env.user
            partner = user.partner_id
            
            # Determine price from list_price (not price)
            product_name = product.name
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
                'name': f"Bulk Order Discount Request - {product_name} - {full_name}",
                'partner_name': full_name,
                'partner_id': partner.id if partner.exists() else False,
                'email_from': email,
                'description': f"""
Special Bulk Order Discount Request:
Product: {product_name}
Quantity: {quantity}
Requested Discount: {discount}%

Customer Message:
{notes}
                """,
                'type': 'opportunity',
                'priority': '2',
                'expected_revenue': expected_revenue if expected_revenue > 0 else 0.0,
            })
            
            # Also create SBODR request record if the model exists
            if 'sbodr.request' in request.env:
                request.env['sbodr.request'].sudo().create({
                    'name': f"SBODR-{full_name}-{product_name}",
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
