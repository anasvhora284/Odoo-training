{
    'name': 'Airproof Website',
    'version': '1.0',
    'category': 'Website',
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
    ],

    'data': [
        'data/presets.xml',
        'views/website_templates.xml',
        'data/presets.xml',
        'data/website_menu.xml',
        'data/pages/404.xml',
        'views/snippets/s_airproof_snippet.xml',
        'views/snippets/s_airproof_another_snippet.xml',
        'views/snippets/options.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'web/static/lib/owl/owl.js',
            '/as_website_airproof/static/src/js/counter_component.js',
            '/as_website_airproof/static/src/xml/counter_component.xml',
            '/as_website_airproof/static/src/snippets/s_airproof_snippet/000.js',
        ],
        'website.assets_wysiwyg': [
            '/as_website_airproof/static/src/snippets/s_airproof_snippet/option.js',
        ],
        'web.assets_backend': [
            '/as_website_airproof/static/src/js/*',
        ],
    },
}
