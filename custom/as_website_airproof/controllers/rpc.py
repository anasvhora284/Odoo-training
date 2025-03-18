from odoo import http
from odoo.http import request

class SimpleRPCController(http.Controller):
    """Simple controller for RPC demonstrations"""
    
    @http.route('/simple_rpc/test', type='http', auth='public', website=True)
    def rpc_test_page(self, **kw):
        """Display a page with RPC test examples"""
        return request.render('as_website_airproof.simple_rpc_test_template', {})
    
    @http.route('/simple_rpc/products', type='json', auth='public', csrf=False)
    def get_products_json(self, **kw):
        """JSON-RPC endpoint to get products"""
        limit = kw.get('limit', 10)
        
        try:
            # Call the model method
            result = request.env['as_website_airproof.rpc_demo'].sudo().get_product_list(limit=limit)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    @http.route('/simple_rpc/menus', type='json', auth='public', csrf=False)
    def get_menus_json(self, **kw):
        """JSON-RPC endpoint to get menu items"""
        menu_type = kw.get('menu_type', 'both')
        
        try:
            # Call the model method
            result = request.env['as_website_airproof.rpc_demo'].sudo().get_menu_items(menu_type=menu_type)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 