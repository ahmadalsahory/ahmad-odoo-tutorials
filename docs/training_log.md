# Odoo Developer Training Activity Log

This log documents the concepts learned, modules implemented, and daily progress during the Odoo training period.

---

### 2026-07-02
- **Key Concepts Learned**:
  - [x] Docker volume mapping optimization (mapping extra-addons to named volumes).
  - [x] Configuring multiple addons paths in Odoo configuration.
  - [x] Setting up and installing custom web themes (`theme_addons`).
  - [x] Developing Python scripts to scrape and clean web documentation.
  - [x] Writing custom compiler scripts to convert Sphinx documentation HTML to formatted Markdown.
  - [x] Configuring project-specific agent instruction rules in `AGENTS.md`.
- **Commits**:
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
