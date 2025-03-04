from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    import_export_log_ids = fields.Many2many(
        'purchase.order.import.export.log',
        string='Import/Export Logs'
    )

    def action_view_import_export_logs(self):
        self.ensure_one()
        return {
            'name': 'Import/Export Logs',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order.import.export.log',
            'view_mode': 'list,form',
            'domain': [('purchase_order_ids', 'in', self.id)],
            'context': {'default_purchase_order_ids': [(6, 0, [self.id])]},
        } 