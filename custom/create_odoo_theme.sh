#!/bin/bash

# Theme name and path configuration
THEME_NAME="as_website_airproof"
BASE_PATH="$PWD/$THEME_NAME"

# Create directory structure
echo "Creating directory structure for $THEME_NAME..."
mkdir -p "$BASE_PATH"/{data,i18n,lib,views}
mkdir -p "$BASE_PATH/static/"{description,fonts,image_shapes,shapes}
mkdir -p "$BASE_PATH/static/src/"{js,scss,xml}
mkdir -p "$BASE_PATH/static/src/img/"{content,wbuilder}
mkdir -p "$BASE_PATH/static/src/snippets"

# Create __init__.py
echo "Creating __init__.py..."
touch "$BASE_PATH/__init__.py"

# Create __manifest__.py
echo "Creating __manifest__.py..."
cat > "$BASE_PATH/__manifest__.py" << 'EOF'
{
    'name': 'Airproof Theme',
    'description': 'A modern and clean theme for Odoo websites',
    'category': 'Website/Theme',
    'version': '18.0.1.0.0',
    'author': 'Your Name',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'data/presets.xml',
        'views/website_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('prepend', 'as_website_airproof/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_frontend_helpers': [
            ('prepend', 'as_website_airproof/static/src/scss/bootstrap_overridden.scss'),
        ],
        'website.assets_website': [
            'as_website_airproof/static/src/scss/font.scss',
            'as_website_airproof/static/src/scss/theme.scss',
        ],
        'web.assets_frontend': [
            'as_website_airproof/static/src/js/theme.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
EOF

# Create SCSS files
echo "Creating SCSS files..."
cat > "$BASE_PATH/static/src/scss/primary_variables.scss" << 'EOF'
// Colors
$o-color-palettes: map-merge($o-color-palettes,
    (
        'airproof': (
            'o-color-1': #bedb39,
            'o-color-2': #2c3e50,
            'o-color-3': #f2f2f2,
            'o-color-4': #ffffff,
            'o-color-5': #000000,
        ),
    )
);

$o-selected-color-palettes-names: append($o-selected-color-palettes-names, 'airproof');

// Fonts
$o-theme-font-configs: (
    'Poppins': (
        'family': ('Poppins', sans-serif),
        'url': 'Poppins:400,500',
        'properties': (
            'base': (
                'font-size-base': 1rem,
            ),
        ),
    ),
);

// Website values
$o-website-values-palettes: (
    (
        'font': 'Poppins',
        'headings-font': 'Poppins',
        'navbar-font': 'Poppins',
        'buttons-font': 'Poppins',
        'color-palettes-name': 'airproof',
    ),
);

$o-website-values-palettes-parameters: (
    'font-size-base': (
        'type': 'size',
        'string': 'Base font size',
    ),
);
EOF

cat > "$BASE_PATH/static/src/scss/bootstrap_overridden.scss" << 'EOF'
// Typography
$h1-font-size: 4rem;
$h2-font-size: 3rem;

// Navbar
$navbar-nav-link-padding-x: 1rem;

// Buttons + Forms
$input-placeholder-color: o-color('o-color-1');

// Cards
$card-border-width: 0;
EOF

cat > "$BASE_PATH/static/src/scss/theme.scss" << 'EOF'
// Custom styles
body {
    font-family: var(--font);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--headings-font);
}

.navbar {
    font-family: var(--navbar-font);
}

// Custom blockquote style
blockquote {
    border-radius: var(--border-radius-pill);
    color: var(--o-color-3);
    font-family: var(--headings-font);
    padding: 2rem;
    margin: 2rem 0;
    background: var(--o-color-2);
}
EOF

# Create JavaScript file
echo "Creating JavaScript file..."
cat > "$BASE_PATH/static/src/js/theme.js" << 'EOF'
/** @odoo-module **/

import { registry } from "@web/core/registry";

registry.category("website_theme").add("as_website_airproof", {
    setup() {
        // Add your custom JavaScript here
    },
});
EOF

# Create XML files
echo "Creating XML files..."
cat > "$BASE_PATH/data/presets.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="website.template_header_default_align_center" model="ir.ui.view">
        <field name="active" eval="True"/>
    </record>
</odoo>
EOF

cat > "$BASE_PATH/views/website_templates.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="layout" inherit_id="website.layout" name="Airproof Layout">
        <xpath expr="//header" position="attributes">
            <attribute name="class" add="o-header--airproof" separator=" "/>
        </xpath>
    </template>
</odoo>
EOF

# Create empty font.scss
touch "$BASE_PATH/static/src/scss/font.scss"

# Set permissions
chmod -R 755 "$BASE_PATH"

echo "Theme structure created successfully!"
echo "Theme location: $BASE_PATH"
echo ""
echo "Next steps:"
echo "1. Copy the theme folder to your Odoo addons path"
echo "2. Update the addons list in Odoo"
echo "3. Install the theme through the Odoo interface"