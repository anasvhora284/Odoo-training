from odoo import http
from odoo.http import request
import json
import time


class AirproofRPCController(http.Controller):
    """Controller to handle RPC-related requests"""
    
    @http.route('/airproof/rpc/test', type='http', auth='public', website=True)
    def rpc_test_page(self, **kw):
        """Display a page with RPC test functionality"""
        return request.render('as_website_airproof.rpc_test_template', {})
    
    @http.route('/airproof/rpc/calculator', type='json', auth='public', website=True, csrf=False)
    def rpc_calculator(self, first_number=0, second_number=0, operation='add', **kw):
        """JSON-RPC endpoint for calculator operations"""
        start_time = time.time()
        
        try:
            # Convert to float
            first_number = float(first_number)
            second_number = float(second_number)
            
            # Call the model method
            RpcLog = request.env['as_website_airproof.rpc_log'].sudo()
            result = RpcLog.perform_calculation(first_number, second_number, operation)
            
            # Log the RPC call
            execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            RpcLog.log_rpc_call(
                'json',
                'calculator',
                params=json.dumps({
                    'first_number': first_number,
                    'second_number': second_number,
                    'operation': operation
                }),
                result=json.dumps(result),
                execution_time=execution_time,
                success=result.get('success', False),
                error_message=result.get('error', None),
                ip_address=request.httprequest.remote_addr
            )
            
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            
            # Log the error
            request.env['as_website_airproof.rpc_log'].sudo().log_rpc_call(
                'json',
                'calculator',
                params=json.dumps({
                    'first_number': first_number,
                    'second_number': second_number,
                    'operation': operation
                }),
                result=None,
                execution_time=execution_time,
                success=False,
                error_message=str(e),
                ip_address=request.httprequest.remote_addr
            )
            
            return {
                'success': False,
                'result': 0,
                'error': str(e)
            }
    
    @http.route('/airproof/rpc/stats', type='json', auth='user')
    def rpc_stats(self, **kw):
        """Get RPC usage statistics"""
        try:
            stats = request.env['as_website_airproof.rpc_log'].sudo().get_statistics()
            return {
                'success': True,
                'stats': stats
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 