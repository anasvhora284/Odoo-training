# Odoo Development Guide

This guide provides an overview of key Odoo development concepts, with practical examples and common use cases from your custom modules.

## 1. Module Structure

In Odoo, a module is a directory containing a set of files that define the functionality of the module. The basic structure of a module includes:

- **`__init__.py`**: Initializes the module by importing models and other Python files.
- **`__manifest__.py`**: Contains metadata about the module, such as its name, version, author, dependencies, and data files to load.
- **`models/`**: Contains Python files that define the data models for the module.
- **`views/`**: Contains XML files that define the user interface for the module, such as forms, lists, and menus.
- **`security/`**: Contains security-related files, such as access control lists (ACLs) and record rules.
- **`wizards/`**: Contains Python files that define wizards, which are transient models used for complex user interactions.
- **`static/`**: Used to store static assets like images, CSS, and JavaScript files.
- **`demo/`**: Contains demo data for the module.

## 2. Model Structure

Models in Odoo represent database tables and are defined in Python files within the `models/` directory. Each model is a class that inherits from `models.Model` and includes fields that correspond to table columns.

### Example:

```python
from odoo import models, fields

class ProductRental(models.Model):
    _name = 'product.rental'
    _description = 'Product Rental'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    rental_price = fields.Float(string="Rental Price", required=True)
    rental_duration = fields.Integer(string="Rental Duration (Days)", default=30, required=True)
```

## 3. Static Folder

The `static/` directory is used to store static assets like images, CSS, and JavaScript files. These assets can be used in the module's views and reports.

### Example Usage:

- **Images**: Store images used in the module's interface.
- **CSS/JS**: Include custom styles and scripts to enhance the user interface.

## 4. Model Fields

Odoo provides various field types to define the structure of a model. Common field types include:

- **Char**: For short text strings.
- **Text**: For longer text strings.
- **Integer**: For integer numbers.
- **Float**: For decimal numbers.
- **Boolean**: For true/false values.
- **Date**: For date values.
- **Many2one**: For creating a many-to-one relationship with another model.
- **One2many**: For creating a one-to-many relationship with another model.
- **Many2many**: For creating a many-to-many relationship with another model.

### Example:

```python
name = fields.Char(string="Name", required=True)
price = fields.Float(string="Price")
is_active = fields.Boolean(string="Active", default=True)
```

## 5. XML Views

XML views define the user interface for models in Odoo. They are stored in the `views/` directory and include forms, lists, kanban views, and more.

### Example:

```xml
<record id="view_product_rental_form" model="ir.ui.view">
    <field name="name">product.rental.form</field>
    <field name="model">product.rental</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <group>
                    <field name="product_id"/>
                    <field name="customer_id"/>
                    <field name="rental_price"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

## 6. Relationships

Odoo models can define relationships between different models using fields like `Many2one`, `One2many`, and `Many2many`. These relationships help in linking records across different tables.

- **Many2one**: Creates a many-to-one relationship with another model. It is used to link a record to a single record in another model.

  Example:

  ```python
  product_id = fields.Many2one('product.product', string="Product", required=True)
  ```

- **One2many**: Creates a one-to-many relationship with another model. It is used to link a record to multiple records in another model.

  Example:

  ```python
  rental_ids = fields.One2many('product.rental', 'customer_id', string="Rentals")
  ```

- **Many2many**: Creates a many-to-many relationship with another model. It is used to link multiple records in one model to multiple records in another model.

  Example:

  ```python
  tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
  ```

## 7. Decorators and Methods

Odoo provides several decorators to define methods with specific behaviors:

- **@api.model**: Used for methods that do not operate on a specific recordset. These methods are called at the model level.

  Example:

  ```python
  @api.model
  def create_log(self, vals):
      return self.create(vals)
  ```

- **@api.depends**: Used to specify that a method's result depends on the fields listed. It is used for computed fields.

  Example:

  ```python
  @api.depends('rental_price', 'quantity', 'rental_duration')
  def _compute_total_price(self):
      for record in self:
          record.total_price = record.rental_price * record.quantity * record.rental_duration
  ```

- **@api.onchange**: Used to trigger a method when a field value changes in the form view.

  Example:

  ```python
  @api.onchange('product_id')
  def _onchange_product_id(self):
      if self.product_id:
          self.price = self.product_id.list_price
  ```

## 8. Notifications

Odoo allows you to display notifications to users using the `ir.actions.client` action. This is useful for providing feedback or alerts.

Example:

```python
return {
    'type': 'ir.actions.client',
    'tag': 'display_notification',
    'params': {
        'title': _('Success'),
        'message': _('The operation was completed successfully.'),
        'type': 'success',
        'sticky': False,
    }
}
```

## 9. Security and Access Rights

Security in Odoo is managed through access control lists (ACLs) and record rules. These define what operations users can perform on models and records.

- **Access Control Lists (ACLs)**: Define permissions for create, read, write, and delete operations on models.

  Example:

  ```xml
  <record id="access_my_model_user" model="ir.model.access">
      <field name="name">my.model.user</field>
      <field name="model_id" ref="model_my_model"/>
      <field name="group_id" ref="group_my_users"/>
      <field name="perm_read" eval="1"/>
      <field name="perm_write" eval="1"/>
      <field name="perm_create" eval="1"/>
      <field name="perm_unlink" eval="1"/>
  </record>
  ```

- **Record Rules**: Define domain-based rules to restrict access to specific records.

  Example:

  ```xml
  <record id="rule_my_model" model="ir.rule">
      <field name="name">My Model Rule</field>
      <field name="model_id" ref="model_my_model"/>
      <field name="domain_force">[('user_id', '=', user.id)]</field>
      <field name="groups" eval="[(4, ref('my_module.group_my_users'))]"/>
  </record>
  ```

## 10. Wizards

Wizards in Odoo are transient models used for complex user interactions. They are typically used for guiding users through a series of steps or for performing batch operations.

### Example:

```python
class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _description = 'My Wizard'
```

### Wizard View:

```xml
<record id="view_my_wizard_form" model="ir.ui.view">
    <field name="name">my.wizard.form</field>
    <field name="model">my.wizard</field>
    <field name="arch" type="xml">
        <form>
            <!-- Form content -->
        </form>
    </field>
</record>
```

## 11. Reports and QWeb

Odoo uses QWeb for creating reports. Reports are defined in XML and can be rendered in various formats like PDF or HTML.

### Example:

```xml
<template id="report_my_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <!-- Report content -->
            </t>
        </t>
    </t>
</template>
```

## 12. Localization and Translations

Odoo supports multiple languages and allows you to translate your module's content.

### Example:

```bash
python odoo-bin -d database -u module --i18n-export=path/to/en_US.po
```

### PO File Structure:

```po
#. module: my_module
#: model:ir.model.fields,field_description:my_module.field_my_model__name
msgid "Name"
msgstr "Translated Name"
```

## 13. Button Actions and Server Actions

Button actions in Odoo are defined in XML and linked to Python methods. They allow users to trigger server-side logic from the UI.

### Example:

```xml
<button name="%{action_name}d"
        string="Button Label"
        type="action"
        class="btn-primary"/>
```

### Python Method:

```python
def action_name(self):
    # Button action logic
    return True
```

## 14. Logging and Error Handling

Logging and error handling are crucial for debugging and maintaining Odoo applications. You can use the `logging` module in Python to log messages.

### Example:

```python
import logging
_logger = logging.getLogger(__name__)

def some_method(self):
    try:
        # Some logic
    except Exception as e:
        _logger.error('An error occurred: %s', e)
        raise
```

This documentation provides a comprehensive overview of key Odoo development concepts. Each section includes practical examples and common use cases. Let me know if you need further customization or additional sections!
