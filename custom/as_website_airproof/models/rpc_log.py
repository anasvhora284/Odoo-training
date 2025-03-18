from odoo import api, fields, models

class RPCDemo(models.Model):
    """Simple model for RPC demonstrations"""
    _name = 'as_website_airproof.rpc_demo'
    _description = 'RPC Demo'

    name = fields.Char('Name', required=True)
    
    @api.model
    def get_product_list(self, limit=10):
        """Method to retrieve products via RPC"""
        try:
            # Get products from product.template model
            products = self.env['product.template'].search_read(
                domain=[('sale_ok', '=', True)],
                fields=['name', 'list_price', 'default_code'],
                limit=limit
            )
            
            return {
                'success': True,
                'products': products
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    @api.model
    def get_menu_items(self, menu_type='backend'):
        """Method to retrieve menu items via RPC
        
        Args:
            menu_type: Type of menu to retrieve ('backend', 'frontend', or 'both')
        """
        try:
            result = {}
            
            # Get backend menu items
            if menu_type in ['backend', 'both']:
                backend_menus = self.env['ir.ui.menu'].search_read(
                    domain=[('parent_id', '=', False)],
                    fields=['name', 'action', 'child_id', 'sequence'],
                    limit=20
                )
                
                # Add our module's menu items
                airproof_menus = self.env['ir.ui.menu'].search_read(
                    domain=[('parent_path', 'like', '%menu_airproof_root%')],
                    fields=['name', 'action', 'parent_id', 'sequence', 'parent_path']
                )
                
                result['backend_menus'] = {
                    'main_menus': backend_menus,
                    'airproof_menus': airproof_menus
                }
            
            # Get frontend website menu items
            if menu_type in ['frontend', 'both']:
                website_menus = self.env['website.menu'].search_read(
                    domain=[('website_id', '!=', False)],
                    fields=['name', 'url', 'parent_id', 'sequence', 'website_id'],
                    limit=50
                )
                
                # Filter for our module's menus
                airproof_website_menus = [
                    menu for menu in website_menus 
                    if 'services' in menu.get('url', '') or 'simple_rpc' in menu.get('url', '')
                ]
                
                result['frontend_menus'] = {
                    'all_menus': website_menus,
                    'airproof_menus': airproof_website_menus
                }
            
            return {
                'success': True,
                'menu_items': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 