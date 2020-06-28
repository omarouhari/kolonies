# -*- coding: utf-8 -*-
{
    'name': 'Kolonies Booking',
    'summary': '',
    'category': 'Booking',
    'version': '1.0',
    'sequence': -95,
    'author': 'Omar OUHARI',
    'license': 'Other proprietary',
    'website': '',
    'description': '',
    'depends': [
        'marketplace_booking_system',
        'calendar',
        'kolonies_marketplace',
    ],
    'data': [
        # data
        'data/ir_sequence.xml',
        # security
        'security/res_groups_users.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        # views
        'views/res_partner_view.xml',
        'views/booking_session_view.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
