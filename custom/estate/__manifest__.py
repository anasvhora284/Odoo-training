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
    'depends': ['base', 'web'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'reports/estate_property_report.xml',
        'reports/estate_property_templates.xml',
        'wizards/property_search_wizard_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate_users_demo.xml',
        'demo/estate_tags_n_types_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_offer_demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}