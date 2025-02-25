from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1.0,
                        'price_unit': record.selling_price,
                    }),
                    Command.create({
                        'name': 'Commission (6%)',
                        'quantity': 1.0,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1.0,
                        'price_unit': 100.00,
                    }),
                ],
            })
            
        return super().action_sold()