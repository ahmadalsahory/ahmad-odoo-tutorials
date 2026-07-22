# -*- coding: utf-8 -*-
{
    'name': 'Sales Commission Report',
    'version': '19.0.1.0.0',
    'category': 'Sales/Commission',
    'summary': 'Configure salesperson commission plans and generate commission reports',
    'description': """
Sales Commission Module
========================
- Define flexible commission plans with ranged percentage brackets.
- Assign salespersons to commission plans.
- Generate sales commission report based on posted and paid customer invoices minus credit notes.
    """,
    'author': 'Ahmad',
    'depends': ['sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_commission_plan_views.xml',
        'views/sales_commission_report_views.xml',
        'views/menu_views.xml',
        'report/sales_commission_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
