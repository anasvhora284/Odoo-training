from odoo import models, fields, api
from datetime import datetime

class ImportExportLog(models.Model):
    _name = 'purchase.order.import.export.log'
    _description = 'Purchase Order Import/Export Log'
    _order = 'create_date desc'

    name = fields.Char(string='Name', required=True)
    operation_type = fields.Selection([
        ('import', 'Import'),
        ('export', 'Export')
    ], string='Operation Type', required=True)
    
    file_name = fields.Char(string='File Name')
    date_time = fields.Datetime(string='Date Time', default=fields.Datetime.now)
    status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Status', required=True)
    
    error_message = fields.Text(string='Error Message')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    purchase_order_ids = fields.Many2many('purchase.order', string='Purchase Orders')
    
    total_orders = fields.Integer(string='Total Orders', compute='_compute_total_orders')
    
    @api.depends('purchase_order_ids')
    def _compute_total_orders(self):
        for record in self:
            record.total_orders = len(record.purchase_order_ids)

    @api.model
    def create_log(self, vals):
        """Helper method to create logs easily"""
        return self.create({
            'name': vals.get('name', 'Purchase Order Operation'),
            'operation_type': vals.get('operation_type'),
            'file_name': vals.get('file_name'),
            'status': vals.get('status', 'failed'),
            'error_message': vals.get('error_message', ''),
            'purchase_order_ids': vals.get('purchase_order_ids', [])
        }) 