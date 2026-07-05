{
    'name': 'Previous Invoice Lines & Outstanding Report',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'View past invoices product lines and print outstanding invoices report',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
