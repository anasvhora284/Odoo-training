{
    'name': 'Airproof Website',
    'version': '1.0',
    'category': 'Atharva Systems',
    'author': 'Anas Vhora',
    'summary': 'Custom website theme for Airproof',
    'description': """
        Custom website theme for Airproof with enhanced navigation and styling.
    """,
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,

    'depends': [
        'base',
        'website',
        'web_editor',
        'website_sale',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/counter_views.xml',
        'views/counter_template.xml',
        'views/service_templates.xml',
        # 'views/simple_rpc_test_template.xml',
        'views/rpc_demo_template.xml',
        'data/presets.xml',
        'views/website_templates.xml',
        'data/website_menu.xml',
        'data/pages/404.xml',
        'views/snippets/s_airproof_snippet.xml',
        'views/snippets/s_airproof_another_snippet.xml',
        'views/snippets/options.xml',
    ],

    'assets': {
        'web.assets_backend': [
            ('include', 'web._assets_jquery'),
            '/as_website_airproof/static/lib/select2/select2.min.js',
            '/as_website_airproof/static/lib/select2/select2.min.css',
            '/as_website_airproof/static/src/components/counter/counter.js',
            '/as_website_airproof/static/src/components/counter/counter.xml',
            '/as_website_airproof/static/src/components/notification/notification.js',
            '/as_website_airproof/static/src/components/notification/notification.xml',
            '/as_website_airproof/static/src/components/rainbow/rainbow.js',
            '/as_website_airproof/static/src/components/rainbow/rainbow.xml',
            '/as_website_airproof/static/src/components/rainbow/rainbow_menu_button.js',
            '/as_website_airproof/static/src/components/rainbow/rainbow_menu_button.xml',
            '/as_website_airproof/static/src/components/calculator/calculator.js',
            '/as_website_airproof/static/src/components/calculator/calculator.xml',
            # '/as_website_airproof/static/src/components/rpc_demo/rpc_demo.js',
            # '/as_website_airproof/static/src/components/rpc_demo/rpc_demo.xml',
        ],
        'web.assets_frontend': [
            ('include', 'web._assets_jquery'),
            '/as_website_airproof/static/lib/select2/select2.min.js',
            '/as_website_airproof/static/lib/select2/select2.min.css',
            '/as_website_airproof/static/src/components/counter/counter.js',
            '/as_website_airproof/static/src/components/counter/counter.xml',
            '/as_website_airproof/static/src/components/notification/notification.js',
            '/as_website_airproof/static/src/components/notification/notification.xml',
            '/as_website_airproof/static/src/components/rainbow/rainbow.js',
            '/as_website_airproof/static/src/components/rainbow/rainbow.xml',
            '/as_website_airproof/static/src/components/rainbow/rainbow_menu_button.js',
            '/as_website_airproof/static/src/components/rainbow/rainbow_menu_button.xml',
            '/as_website_airproof/static/src/components/calculator/calculator.js',
            '/as_website_airproof/static/src/components/calculator/calculator.xml',
            # '/as_website_airproof/static/src/components/rpc_demo/rpc_demo.js',
            # '/as_website_airproof/static/src/components/rpc_demo/rpc_demo.xml',
            '/as_website_airproof/static/src/snippets/s_airproof_snippet/000.js',
        ],
        'website.assets_wysiwyg': [
            '/as_website_airproof/static/lib/select2/select2.min.js',
            '/as_website_airproof/static/lib/select2/select2.min.css',
            '/as_website_airproof/static/src/snippets/s_airproof_snippet/option.js',
        ],
    },
}
