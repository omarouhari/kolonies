# -*- coding: utf-8 -*-
{
    'name': 'Kolonies EtherPad',
    'summary': '',
    'category': 'Tools',
    'version': '1.0',
    'sequence': -98,
    'author': 'Omar OUHARI',
    'license': 'Other proprietary',
    'website': '',
    'description': '',
    'depends': [
        'kolonies_booking',
    ],
    'data': [
        # data
        'data/ir_config_parameter.xml',
        'data/ir_sequence.xml',
        # security
        # views
        'views/templates.xml',
        'views/booking_session_view.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
