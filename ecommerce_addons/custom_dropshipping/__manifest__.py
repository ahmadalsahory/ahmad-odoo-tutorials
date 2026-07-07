{
    'name': 'Custom Dropshipping',
    'version': '1.0',
    'summary': 'Configure dropshipping vendors directly on Sales Orders',
    'depends': [
        'sale_management',
        'purchase_stock',
        'stock_dropshipping',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
