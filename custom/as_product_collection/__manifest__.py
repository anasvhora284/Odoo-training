# -*- coding: utf-8 -*-
{
    'name': "as_product_collection",

    'summary': "Product Collection and Display for Websites",

    'description': """
    This module allows you to create product collections and display them with a custom snippet.
    Features include:
    - Collection management
    - Product filtering by website
    - Grid and card view options
    - Price display based on current pricelist
    """,

    'author': "Atharva System",
    'website': "http://www.atharvasystem.com",

    'category': 'Product',
    'version': '0.1',
    'sequence': '1',

    'depends': [
        'base',
        'website',
        'website_sale',
        'website_sale_comparison',
        'website_sale_wishlist'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/product_collection_views.xml',
        'views/website_menu.xml',
        'views/snippets/s_product_collection_snippet/options.xml',
        'views/snippets/s_product_collection_snippet/s_product_collection_snippet.xml',
    ],

    'demo': [
        'demo/product_collection_demo.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            # Module assets
            'as_product_collection/static/src/snippets/s_product_collection_snippet/000.js',
            'as_product_collection/static/src/snippets/s_product_collection_snippet/000.scss',
            # Website sale dependencies
            ('include', 'website_sale.assets_frontend'),
            ('include', 'website_sale_comparison.assets_frontend'),
            ('include', 'website_sale_wishlist.assets_frontend'),
        ],
        'website.assets_wysiwyg': [
            'as_product_collection/static/src/js/components/collection_dialog/collection_dialog.js',
            'as_product_collection/static/src/js/components/collection_dialog/dialog_template.xml',
            'as_product_collection/static/src/snippets/s_product_collection_snippet/options.js',
        ],
    },
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

