{
    'name': 'Real Estate Management',
    'version': '1.1',
    'summary': 'Manage real estate properties',
    'author': 'Anas vhora',
    'category': 'Real Estate',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'data/estate_demo.xml',
        'data/estate_property_demo.xml',
        'data/estate_property_offer_demo.xml',
    ],
    'installable': True,
    'application': True,
}