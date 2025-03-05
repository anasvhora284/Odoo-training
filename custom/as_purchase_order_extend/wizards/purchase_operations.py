import base64
from io import BytesIO
from datetime import datetime
from odoo import models, fields, api, _
import pandas as pd

class PurchaseOrderOperations(models.TransientModel):
    _name = 'purchase.order.operations'
    _description = 'Import Purchase Order'

    file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='File Name')
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('purchase', 'Purchase Order')
    ], string='Purchase Order State', default='draft', required=True)
    
    template_file = fields.Binary(string='Template File', readonly=True)
    template_file_name = fields.Char(string='Template File Name', readonly=True)
    
    # Define the columns for the Excel file
    def _get_excel_columns(self):
        return [
            'Vendor Name', 'Product Name', 'Description', 'Quantity', 
            'Unit Price', 'Taxes', 'Scheduled Date', 'Payment Terms', 
            'Currency', 'Reference'
        ]

    def action_download_template(self):
        columns = self._get_excel_columns()
        
        data = {
            'Vendor Name': ['Vendor ABC'],
            'Product Name': ['Product XYZ'],
            'Description': ['Sample Product Description'],
            'Quantity': [10.0],
            'Unit Price': [100.00],
            'Taxes': ['VAT 15%'],
            'Scheduled Date': ['2024-12-31'],
            'Payment Terms': ['30 Days'],
            'Currency': ['USD'],
            'Reference': ['PO/2024/001'],
        }
        
        df = pd.DataFrame(data, columns=columns)
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False, engine='openpyxl')
        
        excel_file.seek(0)
        attachment = self.env['ir.attachment'].create({
            'name': 'purchase_order_template.xlsx',
            'datas': base64.b64encode(excel_file.read()),
            'type': 'binary',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def action_proceed(self):
        self.ensure_one()
        try:
            return self._import_purchase_orders()
        except Exception as e:
            return self._create_log_and_return_error(str(e))

    def _create_log_and_return_error(self, error_message, operation_type=None, created_pos=None):
        if created_pos is None:
            created_pos = []
        if operation_type is None:
            operation_type = 'import'

        self.env['purchase.order.import.export.log'].create_log({
            'name': 'Import Purchase Orders',
            'operation_type': operation_type,
            'file_name': self.file_name,
            'status': 'failed',
            'error_message': error_message,
            'purchase_order_ids': [(6, 0, created_pos)]
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Error'),
                'message': error_message,
                'type': 'danger',
                'sticky': True,
            }
        }

    def _import_purchase_orders(self):
        if not self.file:
            return self._create_log_and_return_error(_('Please upload a file first.'))

        try:
            excel_file = BytesIO(base64.b64decode(self.file))
            try:
                df = pd.read_excel(excel_file)
            except Exception:
                return self._create_log_and_return_error(_('The uploaded file is not a valid Excel file.'))

            required_columns = self._get_excel_columns()[:4]
            if not all(col in df.columns for col in required_columns):
                return self._create_log_and_return_error(_('Invalid file format. Please use the template provided.'))

            created_pos = []
            current_po = False
            current_vendor = False

            for index, row in df.iterrows():
                try:
                    vendor_name = row['Vendor Name']
                    product_name = row['Product Name']
                    description = row.get('Description', '')
                    quantity = float(row['Quantity'])
                    price_unit = float(row['Unit Price'])
                    taxes = row.get('Taxes', '')
                    scheduled_date = row.get('Scheduled Date')
                    payment_terms = row.get('Payment Terms')
                    currency = row.get('Currency')
                    reference = row.get('Reference')

                    vendor = self.env['res.partner'].search([
                        ('name', '=', vendor_name),
                        ('supplier_rank', '>', 0)
                    ], limit=1)
                    
                    if not vendor:
                        return self._create_log_and_return_error(_(f'Vendor not found in row {index + 2}: {vendor_name}'))

                    if current_vendor != vendor:
                        if current_po:
                            created_pos.append(current_po.id)
                        
                        payment_term = False
                        if payment_terms:
                            payment_term = self.env['account.payment.term'].search([('name', '=', payment_terms)], limit=1)
                        
                        currency_id = False
                        if currency:
                            currency_id = self.env['res.currency'].search([('name', '=', currency)], limit=1)
                        
                        current_vendor = vendor
                        current_po = self.env['purchase.order'].create({
                            'partner_id': vendor.id,
                            'date_order': datetime.now(),
                            'state': 'draft',
                            'payment_term_id': payment_term and payment_term.id or False,
                            'currency_id': currency_id and currency_id.id or False,
                            'partner_ref': reference or False,
                            'date_planned': scheduled_date or datetime.now()
                        })

                    product = self.env['product.product'].search([
                        ('name', '=', product_name)
                    ], limit=1)
                    
                    if not product:
                        return self._create_log_and_return_error(_(f'Product not found in row {index + 2}: {product_name}'))

                    taxes_ids = []
                    if taxes:
                        tax_names = [tax.strip() for tax in taxes.split(',')]
                        for tax_name in tax_names:
                            tax = self.env['account.tax'].search([
                                ('name', '=', tax_name),
                                ('type_tax_use', '=', 'purchase')
                            ], limit=1)
                            if tax:
                                taxes_ids.append(tax.id)

                    self.env['purchase.order.line'].create({
                        'order_id': current_po.id,
                        'product_id': product.id,
                        'name': description or product.name,
                        'product_qty': quantity,
                        'price_unit': price_unit,
                        'product_uom': product.uom_po_id.id,
                        'date_planned': scheduled_date or datetime.now(),
                        'taxes_id': [(6, 0, taxes_ids)]
                    })

                    if self.state == 'sent':
                        current_po.write({'state': 'sent'})

                except Exception as e:
                    return self._create_log_and_return_error(f'Error in row {index + 2}: {str(e)}')

            if current_po:
                created_pos.append(current_po.id)

            purchase_orders = self.env['purchase.order'].browse(created_pos)
            if self.state == 'sent':
                purchase_orders.with_context(mail_notrack=True).write({'state': 'sent'})
                template = self.env.ref('purchase.email_template_edi_purchase')
                if template:
                    for po in purchase_orders:
                        template.send_mail(po.id, force_send=False)
            elif self.state == 'purchase':
                purchase_orders.with_context(mail_notrack=True).button_confirm()
            elif self.state == 'cancel':
                purchase_orders.with_context(mail_notrack=True).button_cancel()

            self.env['purchase.order.import.export.log'].create_log({
                'name': 'Import Purchase Orders',
                'operation_type': 'import',
                'file_name': self.file_name,
                'status': 'success',
                'error_message': '',
                'purchase_order_ids': [(6, 0, created_pos)]
            })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _(f'{len(created_pos)} purchase orders imported successfully.'),
                    'type': 'success',
                    'sticky': False,
                }
            }

        except Exception as e:
            return self._create_log_and_return_error(f'Error importing file: {str(e)}')
        
    def action_view_logs(self):
        return {
            'name': 'Import/Export Logs',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order.import.export.log',
            'view_mode': 'list,form',
            'domain': [('purchase_order_ids', 'in', self.id)],
            'context': {'default_purchase_order_ids': [(6, 0, [self.id])]},
        } 