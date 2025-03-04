{
    'name': 'Purchase Order Extend',
    'version': '1.0',
    'author': 'Anas Vhora',
    'summary': 'Import/Export Purchase Orders with Excel',
    'sequence': 1,
    'description': """
        Purchase Order Extend
        ===========================
        
        This module allows you to:
        * Import Purchase Order from Excel file
        * Export Purchase Order to Excel file
        * Show logs of import and export
    """,
    'category': 'Purchase',
    'depends': [
        'base',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/import_export_log_views.xml',
        'wizards/purchase_operations_views.xml',
        'views/purchase_order_menus.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}