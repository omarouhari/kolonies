# -*- coding: utf-8 -*-
{
    'name': 'Kolonies Multi Vendor Marketplace',
    'summary': '',
    'category': 'Website',
    'version': '1.0',
    'sequence': -96,
    'author': 'Omar OUHARI',
    'license': 'Other proprietary',
    'website': '',
    'description': '',
    'depends': [
        'hr',
        'kolonies_base',
    ],
    'data': [
        # data
    # security
    'security/ir.model.access.csv',
    # views
    'views/templates.xml',
    'views/res_partner_view.xml',
    'views/seller_location_view.xml',
  ],
  'application': False,
  'installable': True,
  'auto_install': False,
}
