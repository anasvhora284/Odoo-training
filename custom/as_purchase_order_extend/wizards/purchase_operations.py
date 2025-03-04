import base64
from io import BytesIO
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import pandas as pd

class PurchaseOrderOperations(models.TransientModel):
    _name = 'purchase.order.operations'
    _description = 'Purchase Order Operations'

    operation = fields.Selection([
        ('import', 'Import Purchase Orders'),
        ('export', 'Export Purchase Orders')
    ], string='Operation', required=True, default='import')
    
    file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='File Name')
    
    template_file = fields.Binary(string='Template File', readonly=True)
    template_file_name = fields.Char(string='Template File Name', readonly=True)
    
    # Define the columns for the Excel file
    def _get_excel_columns(self):
        return [
            'Vendor Name', 'Product Name', 'Description', 'Quantity', 
            'Unit Price', 'Taxes', 'Scheduled Date', 'Payment Terms', 
            'Currency', 'Reference', 'Status'
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
            'Status': ['RFQ']
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
            if self.operation == 'import':
                return self._import_purchase_orders()
            else:
                return self._export_purchase_orders()
        except Exception as e:
            return self._create_log_and_return_error(str(e))

    def _create_log_and_return_error(self, error_message, operation_type=None, created_pos=None):
        if created_pos is None:
            created_pos = []
        if operation_type is None:
            operation_type = self.operation

        self.env['purchase.order.import.export.log'].create_log({
            'name': 'Import/Export Purchase Orders',
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
        self.ensure_one()
        if not self.file:
            return self._create_log_and_return_error(_('Please select a file to import.'))

        created_pos = []
        
        try:
            excel_file = BytesIO(base64.b64decode(self.file))
            try:
                df = pd.read_excel(excel_file)
            except Exception:
                return self._create_log_and_return_error(_('The uploaded file is not a valid Excel file.'))

            required_columns = self._get_excel_columns()[:4]
            if not all(col in df.columns for col in required_columns):
                return self._create_log_and_return_error(_('Invalid file format. Please use the template provided.'))

            current_vendor = None
            current_po = None

            for index, row in df.iterrows():
                try:
                    vendor_name = row['Vendor Name']
                    product_name = row['Product Name']
                    quantity = float(row['Quantity'])
                    price_unit = float(row['Unit Price'])
                    status = row.get('Status', 'RFQ')

                    if status not in ['RFQ', 'RFQ Sent', 'Purchase Order']:
                        return self._create_log_and_return_error(
                            _('Invalid status in row %d: %s. Allowed values are: RFQ, RFQ Sent, Purchase Order.') 
                            % (index + 2, status)
                        )

                    vendor = self.env['res.partner'].search([
                        ('name', '=', vendor_name),
                        ('supplier_rank', '>', 0)
                    ], limit=1)
                    
                    if not vendor:
                        return self._create_log_and_return_error(_(f'Vendor not found in row {index + 2}: {vendor_name}'))

                    if current_vendor != vendor:
                        if current_po:
                            created_pos.append(current_po.id)
                        
                        current_vendor = vendor
                        current_po = self.env['purchase.order'].create({
                            'partner_id': vendor.id,
                            'date_order': datetime.now(),
                            'state': 'draft' if status == 'RFQ' else 'sent' if status == 'RFQ Sent' else 'purchase'
                        })

                    product = self.env['product.product'].search([
                        ('name', '=', product_name)
                    ], limit=1)
                    
                    if not product:
                        return self._create_log_and_return_error(_(f'Product not found in row {index + 2}: {product_name}'))

                    self.env['purchase.order.line'].create({
                        'order_id': current_po.id,
                        'product_id': product.id,
                        'name': product.name,
                        'product_qty': quantity,
                        'price_unit': price_unit,
                        'product_uom': product.uom_po_id.id,
                        'date_planned': datetime.now(),
                    })

                    if status == 'Purchase Order' and current_po:
                        template = self.env.ref('purchase.email_template_edi_purchase')
                        if template:
                            template.send_mail(current_po.id, force_send=True)

                except Exception as e:
                    return self._create_log_and_return_error(f'Error in row {index + 2}: {str(e)}')

            if current_po:
                created_pos.append(current_po.id)
                if current_po.state == 'purchase':
                    template = self.env.ref('purchase.email_template_edi_purchase')
                    if template:
                        template.send_mail(current_po.id, force_send=True)

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
                    'message': _('%s purchase orders imported successfully.') % len(created_pos),
                    'type': 'success',
                    'sticky': False,
                }
            }

        except Exception as e:
            return self._create_log_and_return_error(f'Error importing file: {str(e)}')

    def _export_purchase_orders(self):
        try:
            purchase_orders = self.env['purchase.order'].search([])
            data = []
            
            for po in purchase_orders:
                for line in po.order_line:
                    data.append({
                        'Order Reference': po.name,
                        'Vendor': po.partner_id.name,
                        'Order Date': po.date_order.strftime('%Y-%m-%d'),
                        'Product': line.product_id.name,
                        'Quantity': line.product_qty,
                        'Unit Price': line.price_unit,
                        'Subtotal': line.price_subtotal
                    })

            df = pd.DataFrame(data)
            excel_file = BytesIO()
            df.to_excel(excel_file, index=False, engine='openpyxl')
            
            self.env['purchase.order.import.export.log'].create_log({
                'name': 'Export Purchase Orders',
                'operation_type': 'export',
                'file_name': 'purchase_orders.xlsx',
                'status': 'success',
                'purchase_order_ids': [(6, 0, purchase_orders.ids)]
            })

            excel_file.seek(0)
            export_data = base64.b64encode(excel_file.read())
            
            attachment = self.env['ir.attachment'].create({
                'name': f'purchase_orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                'datas': export_data,
                'type': 'binary'
            })

            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }

        except Exception as e:
            return self._create_log_and_return_error(f'Error exporting file: {str(e)}')