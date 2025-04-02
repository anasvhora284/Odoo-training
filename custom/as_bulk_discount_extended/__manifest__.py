# -*- coding: utf-8 -*-
{
    'name': "Special Bulk Order Discount Request",

    'summary': "Allows customers to request special discounts for bulk orders",

    'description': """
        This module adds functionality for customers to request special discounts on bulk orders:
        - Add option in website settings to enable SBODR
        - Enable SBODR for all products or specific variants
        - Request form for customers with product quantity and discount
        - Automatic lead generation in CRM
    """,

    'author': "Atharva Systems pvt. ltd.",
    'website': "https://www.atharvasystems.com",
    'category': 'Website/Sales, Atharva Systems',
    'version': '1.0',
    'sequence': 1,

    # Dependencies
    'depends': [
        'base', 
        'crm',
        'product',
        'sale_management',
        'website', 
        'website_sale',
        'web'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/website_settings_views.xml',
        'views/product_variant_views.xml',
        'views/website_sale_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'as_bulk_discount_extended/static/src/js/index.js',
            'as_bulk_discount_extended/static/src/js/**/*',
        ],
    },
    
    'application': True,
    'installable': True,
}

