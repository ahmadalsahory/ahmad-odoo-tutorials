# Odoo Developer Training Activity Log

This log documents the concepts learned, modules implemented, and daily progress during the Odoo training period.


### 2026-07-22
- **Key Concepts Learned**:
  - [x] Defining range percentage configuration models (`sales.commission.plan.line`) and computing dynamic flat bracket commission rates.
  - [x] Implementing transient wizard models (`sales.commission.report.wizard`) to aggregate posted and paid customer invoices (`out_invoice`) minus credit notes (`out_refund`).
  - [x] Validating model fields using `@api.constrains` and raising `ValidationError` for invalid range boundaries.
  - [x] Extending `res.users` model and inheriting `base.view_users_form` XML view to assign and display commission plans on salesperson pages.

- **Commits**:
  - `7bee9bf` - feat(sales_commission): display salesperson commission plan in report wizard and QWeb PDF
  - `cfc5395` - fix(sales_commission): target notebook container in res_users_views.xml
  - `49400ed` - feat(sales_commission): add commission plan field to res.users form view
  - `9b03e0c` - fix(sales_commission): correct parent menu XML ID to sale.menu_reporting_sales
  - `669308f` - feat(sales_commission): add range validation constraints and unit tests
  - `ac5340c` - feat(sales_commission): implement module structure and configuration models

### 2026-07-19
- **Key Concepts Learned**:
  - [x] Defining automatic, date-based database sequences using `ir.sequence` records within XML files.
  - [x] Overriding the Odoo ORM `@api.model_create_multi` decorated `create()` method to dynamically fetch and assign sequence numbers.
- **Commits**:
  - `d7489a4` - refactor(todo): simplify task sequence prefix to Task-
  - `64329e4` - feat(todo): implement automatic date-based sequence for tasks
  - `ade89a1` - feat(todo): add task report and integrate date field in timesheets

### 2026-07-13
- **Key Concepts Learned**:
  - [x] Defining a custom search panel (`<searchpanel>`) inside Odoo search views to enable multi-selection filtering on relational fields.
  - [x] Controlling Kanban view column grouping, ordering, and expansion for Selection fields using the ORM `group_expand` attribute mapped to a model-level Python method.
  - [x] Implementing soft UI warnings using `@api.onchange` returning warning payloads to alert users of threshold violations in the form view without blocking database commits.
- **Commits**:
  - `052d1ea` - feat(todo): calculate remaining hours until exact end of due date in local timezone
  - `f6051bf` - style(todo): display hours limit warning as non-blocking toast notification
  - `78e45ec` - refactor(todo): separate TodoTaskTimesheet model into a separate python file
  - `35e7a49` - feat(todo): implement task timesheets with dynamic soft warning limits
  - `f4437a2` - feat(todo): implement todo_app with Kanban and searchpanel

### 2026-07-12
- **Key Concepts Learned**:
  - [x] Defining server actions (`ir.actions.server`) to execute Python code from list/form views using `binding_model_id`.
  - [x] Configuring a custom Dockerfile and multi-file docker-compose setup to build and cache development-only dependencies in VS Code Dev Containers.
  - [x] Using `decoration-*` attributes (e.g., `decoration-danger`) on list views with invisible computed boolean fields to conditionally style entire rows based on record state.
  - [x] Defining `ir.cron` scheduled actions in XML data to periodically invoke model methods at configurable intervals (e.g., daily).
  - [x] Defining QWeb PDF/HTML reports using `ir.actions.report` records paired with a `<template>` block, and referencing the model via the auto-generated `model_<name>` external ID on `binding_model_id`.

- **Commits**:
  - `c4c4c99` - feat(estate): add QWeb property report with styled table layout
  - `e803942` - feat(estate): add ir.cron scheduled action for late property emails
  - `359ebb2` - feat(estate): add is_late computed field and list row decoration
  - `b4eafe9` - chore(docker): setup custom Dockerfile and compose override
  - `33c1135` - feat(estate): implement server action to cancel properties

### 2026-07-11
- **Key Concepts Learned**:
  - [x] Integrating Odoo Chatter thread component and configuring message tracking on fields using `tracking=True`.

- **Commits**:
  - `fa06b01` - chore(docker): setup dev container and configure vscode debugging
  - `e34d3f9` - feat(estate): integrate odoo chatter and field tracking

### 2026-07-09
- **Commits**:
  - `3fbaaea` - docs(agents): refine rules for key concepts and clean up training log
  - `9b17705` - fix(estate): resolve property state actions and button visibility logic

### 2026-07-08
- **Commits**:
  - `ae5efd5` - chore(agents): add .bobignore to exclude docs and .agents

### 2026-07-07
- **Key Concepts Learned**:
  - [x] Overriding `_run_buy` on `stock.rule` to customize vendor selection dynamically in Odoo 19.
  - [x] Overriding `_make_po_get_domain` on `stock.rule` to dynamically control PO merging and consolidation per Sales Order.
  - [x] Modernizing Odoo XML views for configuration settings using `<block>` and `<setting>` tags in Odoo 19.
  - [x] Implementing dynamic field properties using python expressions (`required`, `invisible`) instead of legacy `attrs` in Odoo 17/18/19.
  - [x] Inheriting TransientModel (`res.config.settings`) to store company-dependent config parameters.
  - [x] Patching Odoo frontend JS interactions utilizing `@web/core/utils/patch` to dynamically update DOM elements.
  - [x] Customizing e-commerce product price elements on variant changes by extending `_onChangeCombination`.
  - [x] Utilizing `main_object` model checks in QWeb templates to apply conditional styling based on page context.
- **Commits**:
  - `9b91f7b` - feat(retail_price): enable dynamic retail price updates on website variant switch
  - `f13050a` - feat(dropship): implement custom dropshipping supplier flow and PO consolidation

### 2026-07-06
- **Key Concepts Learned**:
  - [x] Inheriting and restructuring complex Odoo QWeb layouts (website_sale.cta_wrapper_boxed).
  - [x] Implementing table-like pricing layouts inside Odoo website views.
- **Commits**:
  - `9ec4459` - feat(retail_price): implement retail price layout customization on website sale product template

### 2026-07-05
- **Key Concepts Learned**:
  - [x] Creating a custom Odoo module inheriting from the standard `account` module.
  - [x] Extending standard Odoo models via inheritance (`_inherit`).
  - [x] Designing custom Odoo list and search views with default sorting and grouping.
  - [x] Inheriting default form views via XPath to insert a smart button.
  - [x] Defining custom QWeb PDF reports and nesting structures in templates.
  - [x] Querying model records from QWeb templates using custom helper methods.
  - [x] Configuring Odoo window actions to open list views in floating modal dialogs using `'target': 'new'`.
  - [x] Defining stored related fields (`store=True`) to enable database-level sorting on relational models.
  - [x] Configuring dynamic column selectors using `optional="show"` and `optional="hide"` attributes in list views.
  - [x] Implementing state-transition action methods on Odoo models.
  - [x] Enforcing server-side validation and displaying user feedback using `UserError`.
  - [x] Styling form `<header>` statusbar using Bootstrap utility classes like `bg-view`.
- **Commits**:
  - `5a8f01a` - feat(prev_invoices): add stored related due date and sort invoices chronologically by issue date
  - `637ee16` - feat(prev_invoices): open previous invoices lines in a floating modal
  - `52c2b12` - feat(prev_invoices): implement outstanding invoices report and register views
  - `e7ed8ef` - feat(prev_invoices): implement previous invoices lines backend logic and views
  - `23ad588` - feat(prev_invoices): initialize custom account module skeleton
  - `5832515` - feat(estate): implement statusbar action buttons and UserError validations

### 2026-07-04
- **Key Concepts Learned**:
  - [x] Defining Many2one and One2many model relations in Odoo 19.
  - [x] Rendering relational list fields as badges using the `many2many_tags` widget.
  - [x] Implementing Many2many model relationships and configuring custom SQL join tables (`relation` and `column1`/`column2`).
  - [x] Setting character string size limits at the database level and validating minimum lengths in Python.
  - [x] Building bi-directional relational views (nesting child sub-grids in notebook form pages).
  - [x] Designing Odoo `<search>` views, complying with RelaxNG structure validation (ordering, mandatory search fields, clean group tags).
  - [x] Implementing predefined filtering via Odoo Domain tuple syntax (`in` operator) and custom "Group By" context mappings.
  - [x] Structuring form layouts with the sheet container and configuring interactive statusbars using clickable options.
  - [x] Configuring dynamic default values via environment context (self.env.user) and cascade deletes on relational models.
  - [x] Implementing computed fields using the `compute` attribute and `@api.depends` decorator with relational mapping.
  - [x] Creating dynamic UI updates via client-side triggers using the `@api.onchange` decorator.
- **Commits**:
  - `8de52a0` - feat(estate): implement computed best price and garden onchange
  - `fed62b4` - chore(agents): add safe file modification protocol rule
  - `0d2fc32` - feat(estate): implement model relationships and tabbed form views
  - `afac56a` - chore(agents): simplify commit workflow in AGENTS.md
  - `449cce9` - feat(estate): add sheet layout and statusbar to property form view
  - `6e07e4a` - feat(estate): implement custom search view with available properties filter and postcode grouping
  - `8073d9d` - chore(agents): enforce single commit workflow for training logs
  - `31c5cef` - docs(training): document many2many relations and validation learning outcomes
  - `ccdb2b5` - feat(estate): implement estate.owner.tag model and many2many relationship
  - `412c79d` - chore(agents): refine rules to avoid repetitive concept logging in training log
  - `3235f96` - docs(training): document model relations and constraints learning outcomes
  - `a895486` - feat(estate): implement estate.owner model and relational views

### 2026-07-02
- **Key Concepts Learned**:
  - [x] Docker volume mapping optimization (mapping extra-addons to named volumes).
  - [x] Configuring multiple addons paths in Odoo configuration.
  - [x] Setting up and installing custom web themes (`theme_addons`).
  - [x] Developing Python scripts to scrape and clean web documentation.
  - [x] Writing custom compiler scripts to convert Sphinx documentation HTML to formatted Markdown.
  - [x] Configuring project-specific agent instruction rules in `AGENTS.md`.
  - [x] Overriding low-level Odoo ORM `_search` method and adapting arguments to Odoo 19 signature.
  - [x] Overriding Odoo ORM `write` and `unlink` methods for custom save and delete hooks.
  - [x] Troubleshooting missing filestore assets (FileNotFoundError) by querying `ir_attachment` and upgrading Odoo base/custom modules to rebuild assets.
  - [x] Customizing Odoo App Icons and Menu Icons (understanding PNG vs SVG support in `ir.module.module` vs `ir.ui.menu`).
  - [x] Configuring `web_icon` on root menu items in XML views.
  - [x] Managing multi-database environments in Docker by removing the `-d` restriction.
- **Commits**:
  - `12f98da` - feat(estate): add app icon and configure root menu web icon
  - `384fb41` - feat(estate): override ORM write and unlink methods
  - `9a02493` - feat(estate): override _search method and modernize super call
  - `8eda998` - docs(training): check off completed learning outcomes in training log
  - `61cdf5f` - docs(training): initialize training activity log
  - `152e272` - docs(training): add training log and git commit hook automation
  - `dc1b6b4` - docs: compile Odoo 19 developer reference manual
  - `d85eeca` - feat(themes): add web themes and layout modules under theme_addons
  - `6f4d20d` - chore(docker): mount theme_addons volume and update addons_path
  - `021b172` - chore(docker): map extra-addons to named volume to prevent anonymous volumes

### 2026-07-01
- **Key Concepts Learned**:
  - [x] Overriding Odoo ORM methods (e.g. `create()`) to print creation status.
  - [x] Implementing database model constraints (`_sql_constraints` and `@api.constrains`).
  - [x] Expected price validation logic and setting field default values.
- **Commits**:
  - `d10cf61` - feat(estate): override create method to print creation status
  - `133a813` - feat(estate): add expected price validation and set field defaults
  - `cb7213d` - feat(estate): implement model validations and unique name constraint

### 2026-06-30
- **Key Concepts Learned**:
  - [x] Designing form views, statusbars, and action buttons in XML.
  - [x] Custom stylesheets integration and styling input field widths in form views.
  - [x] Setting up default agent skills, config locks, tutoring guidelines, and clean-code rules.
  - [x] Adding hidden fields and active status checkboxes to list views.
- **Commits**:
  - `2ff6ddc` - revert manual changes to match commit 894a585
  - `5804e34` - style(estate): register custom stylesheet and apply form class
  - `5f55823` - style(estate): limit input field widths on property form
  - `ea5617b` - feat(estate): implement status actions and update form statusbar
  - `894a585` - feat(estate): add custom form view layout for properties
  - `df01064` - docs(skills): add custom odoo clean-code guidelines skill
  - `669c318` - docs(agents): define custom tutoring and explaining rules
  - `228f067` - chore(agents): add default agent skills and config lock
  - `bd17dad` - Add hidden fields for active status and state in property list view
  - `205ab49` - Add views references
  - `25990c3` - (UI) Add menus and property view
  - `48cc772` - Update estate_property fields

### 2026-06-29
- **Key Concepts Learned**:
  - [x] Creating basic Odoo models (`estate.property` and test models).
  - [x] Configuring Odoo security groups and access rights (`ir.model.access.csv`).
  - [x] Custom database configuration and paths (`data_dir`) inside `odoo.conf`.
  - [x] Docker Compose settings to trigger module updates automatically on restart.
- **Commits**:
  - `9bd1e8b` - Add data_dir configuration to odoo.conf
  - `b985a6b` - Add security to the estate_model
  - `a47ac30` - Add security to estate module and ir.model.access.csv file to secure estate_property model by base group
  - `d0c545d` - Add estate_property model
  - `f9e9cf6` - Update docker compose to make it update estate module when restart or up down and remove environments because they are in odoo.conf - Add test_model in estate module
  - `7a72d82` - Update the password in the docker-compose - Odoo replace admin password by hashed pass

### 2026-06-28
- **Key Concepts Learned**:
  - [x] Setting up Docker environments for Odoo and PostgreSQL.
  - [x] Connecting database management tools to Odoo's PostgreSQL database.
  - [x] Creating basic manifest files (`__manifest__.py`) and initializing Odoo modules.
  - [x] Repository setup, `.gitignore` configuration, and cloning Odoo tutorials.
- **Commits**:
  - `0322514` - Update pass in the docker compose file
  - `25c521e` - Add __init__.py and __manifest__.py files
  - `be5bdc5` - Move .gitignore to the root of repo
  - `5cb8ef6` - Clone odoo/tutorials
  - `d1f6e78` - Update docker-compose.yml to connect to it by database management tool and save the master password as comment
  - `7e917e6` - Delete Dockerfile - Update docker-compose.yml - Add odoo.conf
  - `a7d85f6` - Adding Dockerfile and docker-dompose.yml files
