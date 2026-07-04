{
    'name': 'Real Estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/property_type_views.xml',
        'views/property_tag_views.xml',
        'views/property_offer_views.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
    ],
    'application': True,
}