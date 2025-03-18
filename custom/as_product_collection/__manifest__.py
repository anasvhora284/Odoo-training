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

    'depends': ['base', 'website', 'website_sale', 'web_editor', 'web'],

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
            'as_product_collection/static/src/snippets/s_product_collection_snippet/000.js',
            'as_product_collection/static/src/snippets/s_product_collection_snippet/000.scss',
        ],
        'website.assets_wysiwyg': [
            'as_product_collection/static/src/snippets/s_product_collection_snippet/options.js',
            'as_product_collection/static/src/snippets/s_product_collection_snippet/dialog_template.xml',
        ],
        'web.assets_wysiwyg': [
            'as_product_collection/static/src/snippets/s_product_collection_snippet/options.js',
            'as_product_collection/static/src/snippets/s_product_collection_snippet/dialog_template.xml',
        ],
    },
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

