from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RPCLog(models.Model):
    """Model to log and track RPC calls to the Airproof module"""
    _name = 'as_website_airproof.rpc_log'
    _description = 'Airproof RPC Log'
    _order = 'create_date desc'

    name = fields.Char('Name', required=True)
    type = fields.Selection([
        ('xml', 'XML-RPC'),
        ('json', 'JSON-RPC'),
    ], string='RPC Type', required=True)
    function = fields.Char('Function Called', required=True)
    params = fields.Text('Parameters')
    result = fields.Text('Result')
    execution_time = fields.Float('Execution Time (ms)', default=0.0)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    date = fields.Datetime('Date', default=fields.Datetime.now)
    ip_address = fields.Char('IP Address')
    success = fields.Boolean('Success', default=True)
    error_message = fields.Text('Error Message')
    
    def name_get(self):
        """Override name_get to display custom name"""
        result = []
        for record in self:
            name = f"{record.type}: {record.function} ({record.date.strftime('%Y-%m-%d %H:%M:%S')})"
            result.append((record.id, name))
        return result
    
    @api.model
    def log_rpc_call(self, rpc_type, function, params=None, result=None, execution_time=0.0, 
                    success=True, error_message=None, ip_address=None):
        """Method that can be called via RPC to log a call"""
        values = {
            'name': f"{rpc_type.upper()}: {function}",
            'type': rpc_type.lower(),
            'function': function,
            'params': params,
            'result': result,
            'execution_time': execution_time,
            'success': success,
            'error_message': error_message,
            'ip_address': ip_address,
        }
        
        return self.create(values)
    
    @api.model
    def perform_calculation(self, first_number, second_number, operation):
        """Example method that can be called via RPC"""
        result = 0
        success = True
        error_message = None
        
        try:
            if operation == 'add':
                result = first_number + second_number
            elif operation == 'subtract':
                result = first_number - second_number
            elif operation == 'multiply':
                result = first_number * second_number
            elif operation == 'divide':
                if second_number == 0:
                    raise ValidationError(_("Cannot divide by zero"))
                result = first_number / second_number
            else:
                raise ValidationError(_("Invalid operation"))
                
        except Exception as e:
            success = False
            error_message = str(e)
            result = 0
            
        # Log this RPC call
        self.log_rpc_call(
            'external', 
            'perform_calculation',
            params=f"{first_number} {operation} {second_number}",
            result=str(result),
            success=success,
            error_message=error_message
        )
            
        return {
            'success': success,
            'result': result,
            'error': error_message,
        }
        
    def get_statistics(self):
        """Get statistics about RPC usage"""
        return {
            'total_calls': self.search_count([]),
            'successful_calls': self.search_count([('success', '=', True)]),
            'failed_calls': self.search_count([('success', '=', False)]),
            'xml_rpc_calls': self.search_count([('type', '=', 'xml')]),
            'json_rpc_calls': self.search_count([('type', '=', 'json')]),
            'average_execution_time': self.search_read(
                [('execution_time', '>', 0)],
                ['execution_time']
            ),
        } 