# Odoo 18 Website Theming Guide

## Table of Contents

1. [Building Blocks](#building-blocks)
2. [Layout](#layout)
3. [Navigation](#navigation)
4. [Pages](#pages)
5. [Forms](#forms)
6. [Animations](#animations)
7. [Gradients](#gradients)
8. [Shapes](#shapes)
9. [Translations](#translations)

## Building Blocks

### Core Concepts

Building blocks are the fundamental components of Odoo website pages. They are reusable snippets that can be dragged and dropped into your pages.

### Custom Snippet Structure

```xml
<template id="my_custom_snippet" name="My Custom Snippet">
    <section class="my_snippet">
        <div class="container">
            <!-- Your snippet content -->
        </div>
    </section>
</template>
```

### Registering Snippets

```xml
<template id="website_snippets" inherit_id="website.snippets">
    <xpath expr="//div[@id='snippet_structure']/div[hasclass('o_panel_body')]" position="inside">
        <t t-snippet="website_sale.products_item"
           t-thumbnail="/website_sale/static/src/img/snippet_thumb.png"/>
    </xpath>
</template>
```

### Snippet Options

```xml
<template id="snippet_options" inherit_id="website.snippet_options">
    <xpath expr="//div" position="inside">
        <div data-js="myOption" data-selector=".my_snippet">
            <we-colorpicker string="Background Color" data-select-style="true"/>
            <we-select string="Layout">
                <we-button data-select-class="layout_1">Layout 1</we-button>
                <we-button data-select-class="layout_2">Layout 2</we-button>
            </we-select>
        </div>
    </xpath>
</template>
```

## Layout

### Grid System

Odoo uses Bootstrap's 12-column grid system. Here's how to structure your layouts:

```xml
<div class="container">
    <div class="row">
        <div class="col-lg-6">Left Column</div>
        <div class="col-lg-6">Right Column</div>
    </div>
</div>
```

### Responsive Design

```scss
// Breakpoints
$screen-xs: 475px;
$screen-sm: 576px;
$screen-md: 768px;
$screen-lg: 992px;
$screen-xl: 1200px;

// Example usage
@media (max-width: $screen-md) {
  .my-component {
    flex-direction: column;
  }
}
```

### Custom Layouts

```xml
<template id="custom_layout" inherit_id="website.layout">
    <xpath expr="//header" position="replace">
        <header>
            <!-- Custom header content -->
        </header>
    </xpath>
</template>
```

## Navigation

### Main Menu Structure

```xml
<template id="custom_menu" inherit_id="website.main_menu">
    <xpath expr="//ul[hasclass('nav')]" position="inside">
        <li class="nav-item">
            <a href="/custom-page" class="nav-link">Custom Page</a>
        </li>
    </xpath>
</template>
```

### Mega Menu

```xml
<template id="mega_menu_template">
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle">Mega Menu</a>
        <div class="dropdown-menu">
            <div class="container">
                <div class="row">
                    <!-- Mega menu content -->
                </div>
            </div>
        </div>
    </li>
</template>
```

## Pages

### Page Templates

```xml
<template id="custom_page_template">
    <t t-call="website.layout">
        <div id="wrap">
            <div class="container">
                <!-- Page content -->
            </div>
        </div>
    </t>
</template>
```

### Dynamic Content

```xml
<template id="dynamic_content">
    <t t-foreach="records" t-as="record">
        <div class="card">
            <h3 t-field="record.name"/>
            <p t-field="record.description"/>
        </div>
    </t>
</template>
```

## Forms

### Basic Form Structure

```xml
<template id="custom_form">
    <form action="/submit" method="post" class="s_website_form">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" name="name" required=""/>
        </div>
        <div class="form-group">
            <button type="submit" class="btn btn-primary">Submit</button>
        </div>
    </form>
</template>
```

### Form Controllers

```python
from odoo import http
from odoo.http import request

class CustomFormController(http.Controller):
    @http.route(['/submit'], type='http', auth="public", website=True)
    def submit_form(self, **post):
        # Handle form submission
        return request.render('website.homepage')
```

## Animations

### CSS Animations

```scss
.custom-animation {
  animation: slide-in 0.5s ease-out;
}

@keyframes slide-in {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}
```

### JavaScript Animations

```javascript
odoo.define("website.animation", function (require) {
  "use strict";

  var publicWidget = require("web.public.widget");

  publicWidget.registry.CustomAnimation = publicWidget.Widget.extend({
    selector: ".custom-animation",
    start: function () {
      this.$el.animate(
        {
          opacity: 1,
        },
        1000
      );
    },
  });
});
```

## Gradients

### CSS Gradients

```scss
.custom-gradient {
  background: linear-gradient(45deg, #primary-color, #secondary-color);
}

.multi-color-gradient {
  background: linear-gradient(90deg, #color1 0%, #color2 50%, #color3 100%);
}
```

## Shapes

### SVG Shapes

```xml
<template id="custom_shapes">
    <div class="custom-shape-divider">
        <svg viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path d="M1200 120L0 16.48V0h1200v120z"></path>
        </svg>
    </div>
</template>
```

### CSS Shapes

```scss
.custom-shape {
  clip-path: polygon(0 0, 100% 0, 100% 75%, 0 100%);
}
```

## Translations

### Template Translations

```xml
<template id="translatable_template">
    <div>
        <h1 t-translation="off">Non-translatable heading</h1>
        <p>This text will be translatable</p>
    </div>
</template>
```

### JavaScript Translations

```javascript
odoo.define("website.translations", function (require) {
  "use strict";

  var core = require("web.core");
  var _t = core._t;

  // Usage
  var translatedText = _t("Translate this text");
});
```

## Best Practices

1. **Performance**

   - Minimize CSS/JS files
   - Use lazy loading for images
   - Optimize asset loading

2. **Maintainability**

   - Follow Odoo naming conventions
   - Comment complex code
   - Use meaningful variable names

3. **Responsiveness**

   - Test on multiple devices
   - Use Bootstrap's responsive classes
   - Implement mobile-first design

4. **SEO**
   - Use semantic HTML
   - Implement proper meta tags
   - Optimize image alt texts

## Common Issues and Solutions

1. **CSS Specificity**

   ```scss
   // Use specific selectors when needed
   #wrapwrap .custom-class {
     // Your styles
   }
   ```

2. **JavaScript Loading**

   ```javascript
   // Ensure proper module loading
   odoo.define("module_name.component", function (require) {
     "use strict";
     // Your code
   });
   ```

3. **Template Inheritance**
   ```xml
   <!-- Use proper xpath expressions -->
   <xpath expr="//div[hasclass('target-class')]" position="after">
       <!-- New content -->
   </xpath>
   ```

Remember to adapt these examples to your specific needs and always test thoroughly before deploying to production.
