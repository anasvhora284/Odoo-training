{
    'name': 'Product Rental Management',
    'version': '1.0',
    'author': 'Anas Vhora',
    'summary': 'Manage Products and it\'s rental',
    'sequence': 1,
    'description': """
        Product Rental Management System
        ===========================
        
        This module allows you to:
        * Manage products and it's rental duration
        * Track rental requests and history
        * Handle rental pricing and approvals
    """,
    'category': 'Atharva Systems',
    'depends': [
        'base',
        'product',
    ],
    'data': [
        'security/product_rental_security.xml',
        'security/ir.model.access.csv',
        'views/product_rental_views.xml',
        'views/product_rental_request_views.xml',
        'views/product_rental_history_views.xml',
        'views/product_rental_menus.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}