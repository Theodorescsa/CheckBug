# -*- coding: utf-8 -*-
{
    'name': "Book Module",
    'version': '1.0',
    'category': 'Real Book',
    'summary': 'Module for managing Book properties',
    'description': """
        This module allows the management of Book properties such as listings, prices, gardens, etc.
    """,
    'author': 'Your Name',
    'website': 'http://www.example.com',
    'depends': ['base'],
    'data': [
        './security/book_management_security.xml',
        './views/actions.xml',
        './views/book_management_menus.xml',
        './views/book_management_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
