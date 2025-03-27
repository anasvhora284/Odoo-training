# -*- coding: utf-8 -*-
{
    'name': "Global Color Filters",

    'summary': "Add global color filters to Odoo views",

    'description': """
This module allows you to add global color filters to Odoo views.
You can define filters that can be applied globally across different views and gives a selected background & text colors.
    """,

    'author': "Atharva Systems Pvt. Ltd.",
    'website': "https://www.atharvasystems.com",
    'license': "LGPL-3",
    'category': 'Atharva Systems',
    'version': '0.1',
    'sequence': 1,
    'application': True,
    'installable': True,
    'auto_install': False,

    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            '/as_filters_extended/static/src/js/list_view_colors.js',
        ],
    },
}