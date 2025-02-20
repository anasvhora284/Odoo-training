{
    'name': 'Real Estate Management',
    'version': '1.1',
    'summary': 'Manage real estate properties',
    'author': 'Anas vhora',
    'category': 'Real Estate',
    'depends': ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
}