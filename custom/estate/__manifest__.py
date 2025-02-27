{
    'name': 'Real Estate Management',
    'version': '1.0',
    'author': 'Anas Vhora',
    'summary': 'Manage real estate properties and offers',
    'description': """
        Real Estate Management System
        ===========================
        
        This module allows you to:
        * Manage properties
        * Handle property offers
        * Track property types and tags
        * Manage property sales
    """,
    'category': 'Real Estate',
    'depends': ['base'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'wizards/property_search_wizard_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3'
}