# -*- coding: utf-8 -*-
{
    'name': "Estate",
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Module for managing Estate properties',
    'description': """
        This module allows the management of estate properties such as listings, prices, gardens, etc.
    """,
    'author': 'Your Name',
    'website': 'http://www.example.com',
    'depends': ['base'],
    'data': [
        # './security/estate_property_security.xml',
        './security/ir.model.access.csv',  # Phân quyền truy cập cho các model
        './views/actions.xml',
        './views/estate_menus.xml',
        './views/estate_property_views.xml',  # Các views của mô-đun
        './views/estate_type_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
