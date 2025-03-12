# -*- coding: utf-8 -*-
{
    'name': "temp_snippet",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website','web_editor'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/snippets/options.xml',
        'views/snippets/s_airproof_snippet.xml',
    ],
    
    'assets': {
        'web.assets_frontend': [
            'temp_snippet/static/src/snippets/000.js',
        ],
        'website.assets_wysiwyg': [
            'temp_snippet/static/src/snippets/option.js',
        ],
    },
}

