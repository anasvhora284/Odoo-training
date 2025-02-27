# Common ORM Methods

## Create/Update

1. **Model.create(vals_list) → records**  
   Creates new records for the model.

   - **Parameters**:
     - `vals_list (Union[list[dict], dict])`: Values for the model’s fields, as a list of dictionaries. Each dictionary should contain key-value pairs where keys are field names and values are the corresponding values to set.
   - **Returns**: The created records as a recordset.

   - **Raises**:

     - `AccessError`: If the current user is not allowed to create records.
     - `ValidationError`: If an invalid value is provided for a selection field.
     - `ValueError`: If a field name specified does not exist.
     - `UserError`: 🔴 If a loop would be created in a hierarchy of objects. 🔴

   - **Example**:

     ```python
     # Creating a single record
     new_record = Model.create({'name': 'New Record', 'field_id': 1})

     # Creating multiple records
     records = Model.create([
         {'name': 'Record 1', 'field_id': 1},
         {'name': 'Record 2', 'field_id': 2},
     ])
     ```

2. **Model.write(vals)**  
   Updates all records in `self` with the provided values.

   - **Parameters**:
     - `vals (dict)`: Fields to update and the value to set on them.
   - **Raises**:

     - `AccessError`: If the user is not allowed to modify the specified records/fields.
     - `ValidationError`: If invalid values are specified for selection fields.

   - **Example**:
     ```python
     # Updating records
     records.write({'field_name': 'Updated Value'})
     ```

## Search/Read

3. **Model.browse([ids]) → records**  
   Returns a recordset for the ids provided as a parameter.

   - **Parameters**:
     - `ids (int or iterable(int) or None)`: ID(s) of the records to browse.
   - **Returns**: A recordset containing the records corresponding to the provided IDs.

   - **Example**:
     ```python
     # Browsing records by IDs
     records = Model.browse([1, 2, 3])
     ```

4. **Model.search(domain[, offset=0][, limit=None][, order=None])**  
   Search for the records that satisfy the given domain.

   - **Parameters**:
     - `domain`: A search domain, which is a list of conditions to filter records.
     - `offset (int)`: Number of results to ignore (default is 0).
     - `limit (int)`: Maximum number of records to return (default is None).
   - **Returns**: A recordset containing at most `limit` records matching the search criteria.

   - **Example**:
     ```python
     # Searching for records with a specific condition
     records = Model.search([('field_name', '=', 'value')], limit=10)
     ```

5. **Model.search_count(domain[, limit=None]) → int**  
   Returns the number of records matching the provided domain.

   - **Parameters**:
     - `domain`: A search domain.
     - `limit`: Maximum number of records to count (default is None).
   - **Returns**: Count of matching records.

   - **Example**:
     ```python
     # Counting records that match a specific condition
     count = Model.search_count([('field_name', '=', 'value')])
     ```

6. **Model.read([fields])**  
   Read the requested fields for the records in `self`.

   - **Parameters**:
     - `fields (list)`: Field names to return.
   - **Returns**: A list of dictionaries mapping field names to their values.

   - **Example**:
     ```python
     # Reading specific fields from records
     data = records.read(['name', 'field_id'])  # returns a list of dictionaries mapping field names to their values
     ```

7. **Model.unlink()**  
   Deletes the records in `self`.

   - **Raises**:

     - `AccessError`: If the user is not allowed to delete the records.
     - `UserError`: If the record is a default property for other records.

   - **Example**:
     ```python
     # Deleting records
     records.unlink()
     ```

8. **Model.copy(default=None)**  
   Duplicate the record `self`, updating it with default values.

   - **Parameters**:
     - `default (dict)`: Dictionary of field values to override in the original values.
   - **Returns**: New records as a recordset.

   - **Example**:
     ```python
     # Copying a record with default values
     copied_record = original_record.copy({'name': 'Copied Record'})
     ```

9. **Model.default_get(fields_list) → default_values**  
   Return default values for the fields in `fields_list`.

   - **Parameters**:
     - `fields_list (list)`: Names of fields whose default values are requested.
   - **Returns**: A dictionary mapping field names to their corresponding default values.

   - **Example**:
     ```python
     # Getting default values for specific fields
     defaults = Model.default_get(['name', 'description'])
     ```

10. **Model.name_create(name) → record**  
    Create a new record by calling `create()` with only one value provided: the display name.

    - **Parameters**:
      - `name`: Display name of the record to create.
    - **Returns**: The (id, display_name) pair value of the created record.

    - **Example**:
      ```python
      # Creating a record with a display name
      record_id, display_name = Model.name_create('New Display Name')
      ```

# Odoo Development Guide

## 1. ORM Methods

### Basic CRUD Operations

1. **Create Records**

   ```python
   # Single record
   record = Model.create({'field': 'value'})

   # Multiple records
   records = Model.create([
       {'field': 'value1'},
       {'field': 'value2'}
   ])
   ```

2. **Search Records**

   ```python
   # Basic search
   records = Model.search([('field', '=', 'value')])

   # Complex domain
   records = Model.search([
       ('field1', '=', 'value1'),
       '|',
       ('field2', '>=', 10),
       ('field3', 'in', [1, 2, 3])
   ])
   ```

3. **Write/Update Records**

   ```python
   # Direct update
   record.write({'field': 'new_value'})

   # Many2many field commands
   # (0, 0, {values})    - create & link new record
   # (1, ID, {values})   - update existing record
   # (2, ID)            - remove and delete record
   # (3, ID)            - unlink record (remove relation)
   # (4, ID)            - link existing record
   # (5)               - unlink all records
   # (6, 0, [IDs])     - replace with list of IDs
   ```

4. **Delete Records**

   ```python
   records.unlink()
   ```

5. **Browse Records**

   ```python
   record = Model.browse(id)
   records = Model.browse([1, 2, 3])
   ```

6. **Search and Read**

   ```python
   # Search and read in one operation
   results = Model.search_read(
       [('field', '=', 'value')],
       ['field1', 'field2']
   )

   # Count records
   count = Model.search_count([('field', '=', 'value')])
   ```

## 2. Button Actions

### Adding Button Actions

```xml
<button name="%{action_name}d"
        string="Button Label"
        type="action"
        class="btn-primary"/>
```

### Python Methods for Buttons

```python
def action_name(self):
    # Button action logic
    return True
```

## 3. Wizards

### Creating a Wizard

1. **Define Transient Model**

   ```python
   class MyWizard(models.TransientModel):
       _name = 'my.wizard'
       _description = 'My Wizard'
   ```

2. **Create Wizard View**

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

3. **Define Action**
   ```xml
   <record id="action_my_wizard" model="ir.actions.act_window">
       <field name="name">My Wizard</field>
       <field name="res_model">my.wizard</field>
       <field name="view_mode">form</field>
       <field name="target">new</field>
   </record>
   ```

## 4. QWeb Reports

### Document Templates

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

### Report Definition

```xml
<record id="action_report_my_document" model="ir.actions.report">
    <field name="name">My Report</field>
    <field name="model">my.model</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">my_module.report_my_document</field>
</record>
```

## 5. Security

### Creating Groups

```xml
<record id="group_my_users" model="res.groups">
    <field name="name">My Custom Group</field>
    <field name="category_id" ref="base.module_category_my_module"/>
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>
```

### Record Rules

```xml
<record id="rule_my_model" model="ir.rule">
    <field name="name">My Model Rule</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('my_module.group_my_users'))]"/>
</record>
```

### Access Rights

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

## 6. Localization

### Creating Translation Files

1. **Export Translations**

   ```bash
   python odoo-bin -d database -u module --i18n-export=path/to/en_US.po
   ```

2. **PO File Structure**

   ```po
   #. module: my_module
   #: model:ir.model.fields,field_description:my_module.field_my_model__name
   msgid "Name"
   msgstr "Translated Name"
   ```

3. **Load Translations**
   ```bash
   python odoo-bin -d database -u module --i18n-import=path/to/fr_FR.po
   ```

### Translation Context

```xml
<field name="name" string="Name" translate="1"/>
```

This documentation provides a comprehensive overview of key Odoo development concepts. Each section includes practical examples and common use cases.
