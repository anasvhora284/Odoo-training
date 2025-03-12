# Odoo Web Framework Guide

## Table of Contents

1. [Framework Overview](#framework-overview)
2. [Web Framework Components](#web-framework-components)
   - [Assets](#assets)
   - [Javascript Modules](#javascript-modules)
   - [Owl Components](#owl-components)
   - [Registries](#registries)
   - [Services](#services)
   - [Hooks](#hooks)
   - [Error Handling](#error-handling)
   - [QWeb Templates](#qweb-templates)
   - [Odoo Editor](#odoo-editor)

## Framework Overview

The Odoo Web Framework is a modern JavaScript framework built on top of Owl (Odoo Web Library) that provides a robust architecture for building enterprise web applications.

### Project Structure

```
odoo/
├── addons/
│   └── web/
│       ├── static/
│       │   └── src/
│       │       ├── core/
│       │       ├── views/
│       │       ├── components/
│       │       └── services/
│       └── controllers/
└── web/
    └── frontend/
```

## Web Framework Components

### Assets

Assets in Odoo are managed through asset bundles. These bundles contain JavaScript, CSS, and other static files.

```javascript
// Example asset bundle definition
{
    'web.assets_backend': [
        'web/static/src/scss/main.scss',
        'web/static/src/js/main.js',
    ]
}
```

### Javascript Modules

Odoo uses ES6 modules for organizing JavaScript code.

```javascript
// core/utils.js
export function formatDate(date) {
  return new Intl.DateTimeFormat().format(date);
}

// Using the module
import { formatDate } from "@web/core/utils";
```

### Owl Components

Owl is Odoo's component framework, similar to React or Vue.

```javascript
// components/Dialog.js
import { Component } from "@odoo/owl";

export class Dialog extends Component {
  static template = "web.Dialog";

  setup() {
    this.state = useState({
      isOpen: false,
    });
  }

  toggle() {
    this.state.isOpen = !this.state.isOpen;
  }
}
```

### Registries

Registries are used to store and retrieve components, services, and other objects.

```javascript
// registries/main.js
import { registry } from "@web/core/registry";

// Register a component
registry.category("components").add("Dialog", Dialog);

// Get a component
const Dialog = registry.category("components").get("Dialog");
```

### Services

Services provide global functionality across the application.

```javascript
// services/notification.js
export const notificationService = {
  dependencies: ["rpc"],

  start(env, { rpc }) {
    return {
      notify(message, type = "info") {
        // Implementation
      },
    };
  },
};

registry.category("services").add("notification", notificationService);
```

### Hooks

Custom hooks for common functionality.

```javascript
// hooks/useDebounce.js
import { useState, onMounted, onWillUnmount } from "@odoo/owl";

export function useDebounce(fn, delay) {
  let timeoutId;

  onWillUnmount(() => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  });

  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
```

### Error Handling

Odoo provides a centralized error handling system.

```javascript
// error_handling/error_handler.js
export class ErrorHandler {
  handle(error) {
    if (error instanceof NetworkError) {
      // Handle network errors
    } else if (error instanceof ValidationError) {
      // Handle validation errors
    }
  }
}
```

### QWeb Templates

QWeb is Odoo's template engine.

```xml
<!-- templates/dialog.xml -->
<templates>
    <t t-name="web.Dialog">
        <div class="dialog" t-att-class="{ 'open': state.isOpen }">
            <div class="dialog-content">
                <t t-slot="default"/>
            </div>
            <button t-on-click="toggle">Close</button>
        </div>
    </t>
</templates>
```

### Odoo Editor

The Odoo Editor is a rich text editor component.

```javascript
// editor/editor.js
import { Component } from "@odoo/owl";

export class Editor extends Component {
  static template = "web.Editor";

  setup() {
    this.state = useState({
      content: "",
      toolbar: {
        bold: false,
        italic: false,
      },
    });
  }

  toggleFormat(format) {
    this.state.toolbar[format] = !this.state.toolbar[format];
    // Apply formatting
  }
}
```

## Environment Setup

The environment object provides access to various services and utilities:

```javascript
// Example environment setup
const env = {
  services: {
    notification: notificationService,
    rpc: rpcService,
  },
  bus: new EventBus(),
  debug: process.env.NODE_ENV !== "production",
};
```

## Best Practices

1. **Component Organization**

   - Keep components small and focused
   - Use composition over inheritance
   - Follow the Single Responsibility Principle

2. **State Management**

   - Use `useState` for local state
   - Use services for global state
   - Avoid prop drilling

3. **Error Handling**

   - Use try/catch blocks appropriately
   - Handle errors at the right level
   - Provide meaningful error messages

4. **Performance**
   - Use `useMemo` for expensive computations
   - Implement proper cleanup in `onWillUnmount`
   - Optimize renders with proper key usage

## Debugging

Enable debug mode by adding `?debug=assets` to the URL. This will:

- Load unminified assets
- Enable source maps
- Show additional debugging tools

## Common Issues and Solutions

1. **Component not rendering**

   - Check if the component is properly registered
   - Verify template name matches
   - Check for console errors

2. **Service not available**

   - Verify service registration
   - Check service dependencies
   - Ensure proper startup order

3. **Template errors**
   - Validate XML syntax
   - Check t-name uniqueness
   - Verify expression syntax

## Additional Resources

- [Official Odoo Documentation](https://www.odoo.com/documentation)
- [Owl Documentation](https://github.com/odoo/owl)
- [Community Forums](https://www.odoo.com/forum)
