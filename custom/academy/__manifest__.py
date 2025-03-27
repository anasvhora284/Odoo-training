# -*- coding: utf-8 -*-
{
    'name': "Academy",
    
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    
    'description': """
        Long description of module's purpose
    """,
    
    'author': "My Company",
    
    'website': "https://www.yourcompany.com",

    'category': 'Atharva Systems',

    'version': '1.0',

    'depends': [
        'website_sale',
        'mail',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/data.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
    'installable': True,
}

