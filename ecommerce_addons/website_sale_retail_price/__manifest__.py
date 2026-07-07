{
    'name': 'Website Sale Retail Price',
    'version': '1.0',
    'category': 'Website/Website',
    'summary': 'Short description of your module',
    'depends': [
        'product', 
        'website_sale'
    ],
    'data': [
        'views/res_company_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_sale_retail_price/static/src/js/website_sale_retail_price.js',
        ],
    },
    'installable': True,
    'application': False,
}
