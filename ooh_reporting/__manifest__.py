# -*- coding: utf-8 -*-
{
    'name': "ooh reporting",

    'summary': """These are custom reports and layout""",

    'description': """
    """,

    'author': "Hussein Kadweka",
    'website': "husseinkadweka.com",
    'category': 'Extra Tools',
    'version': '12.0.0.1.0',
    # any module necessary for this one to work correctly
    'depends': ['purchase', 'account', 'sale_management','stock'],
    # always loaded
    'data': [
        'reports/proformerInvoice.xml',
        'reports/purchaseOrder.xml',
        'reports/saleOrder.xml',
        'reports/view_inherit.xml',
        'reports/deliveryNote.xml',
        'reports/etrInvoice.xml',
        'views/printAction.xml'
    ],
}
