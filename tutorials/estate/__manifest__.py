{
    'name': 'Real Estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/css/estate_property.css',
        ],
    },
    'application': True,
}