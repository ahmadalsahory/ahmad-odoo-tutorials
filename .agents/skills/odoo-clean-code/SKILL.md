---
name: odoo-clean-code
description: Guidelines and best practices for writing clean, secure, and professional Odoo code (Backend ORM, XML views, OWL frontend, and security) during tutor sessions.
---

# Odoo Clean Code and Best Practices

This skill provides a set of strict guidelines for writing clean, optimized, and professional Odoo code. It is used as a reference when reviewing the user's code, answering queries, or suggesting improvements.

## 1. Database and ORM Best Practices

### A. Naming Conventions
* **Models**: Use singular noun form with dots (e.g., `estate.property`, not `estate.properties` or `estate_property`).
* **Fields**:
  * Many2one fields must end with `_id` (e.g., `partner_id`, `user_id`).
  * Many2many/One2many fields must end with `_ids` (e.g., `tag_ids`, `line_ids`).
  * Boolean fields should start with `is_` or `has_` (e.g., `is_active`, `has_garden`).

### B. ORM Methods & Performance
* **Avoid Database Operations in Loops**: 
  * *Bad:* Running `self.env['res.partner'].search(...)` or `record.write(...)` inside a `for` loop.
  * *Good:* Perform search/computations in bulk, collect data, and write once.
* **ORM Over Raw SQL**: Never use raw SQL (`self.env.cr.execute`) unless absolutely necessary for performance reasons. Raw SQL bypasses ORM caching, security rules, and multi-company checks.
* **Filtered**: Use `filtered()` to filter recordsets in memory instead of searching the database again.

### C. Compute Fields
* **Dependencies (`@api.depends`)**: Always specify *all* fields that the computed field relies on. A missing dependency causes the cache not to update.
* **Readonly by Default**: Computed fields are readonly. If the user needs to edit them, use `inverse`.
* **Store**: Use `store=True` only when searching or sorting on the computed field is required, keeping in mind that stored computed fields recalculate on dependency changes.

---

## 2. XML Views & Actions Best Practices

### A. View Structuring
* Use semantic tags appropriately: `<sheet>` for layout, `<group>` for columns (max 2 columns in standard forms), `<notebook>` and `<page>` for tabbed sections.
* Field attributes should be descriptive (e.g., `widget="monetary"`, `options="{'no_create': True}"`).

### B. Inheriting and Extending Views (XPath)
* Always inherit using `<field name="inherit_id" ref="module.parent_view_id"/>`.
* Use the most specific XPath targets possible (e.g., `<xpath expr="//field[@name='partner_id']" position="after">`). Avoid generic indexes like `//form/sheet/group[1]`.

---

## 3. Security (Access Rights and Rules)

* **Access Rights**: Every new model must have a line in `security/ir.model.access.csv`.
* **Record Rules (`ir.rule`)**: Ensure multi-company or user-specific records are partitioned correctly using domain filters (e.g., `['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]`).

---

## 4. OWL (Odoo Web Library) Frontend Best Practices

* **State Management**: Use `useState` for reactive component state.
* **Lifecycle Hooks**: Align code execution with appropriate hooks (`onWillStart` for asynchronous data loading, `onMounted` for DOM interactions).
* **Component Modularity**: Keep templates (`t-name`) clean, separating layout from logic. Avoid inline JS code in XML templates.
