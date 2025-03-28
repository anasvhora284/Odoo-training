from odoo import models, fields

class SBODRWizard(models.TransientModel):
    _name = "sbodr.wizard"
    _description = "Special Bulk Order Discount Request"

    full_name = fields.Char("Full Name", readonly=True)
    email = fields.Char("Email", readonly=True)
    product_id = fields.Many2one('product.product', "Product", required=True)
    quantity = fields.Integer("Quantity", required=True, default=10)
    discount = fields.Float("Discount (%)", required=True, default=1.0)
    description = fields.Text("Reason for Bulk Order")

    def send_request(self):
        self.env['crm.lead'].create({
            'name': f"Bulk Order Request - {self.product_id.name}",
            'partner_name': self.full_name,
            'email_from': self.email,
            'description': self.description,
            'sbodr_discount': self.discount,
            'expected_revenue': self.quantity * self.product_id.list_price * ((100 - self.discount) / 100),
        })
        
