# -*- coding: utf-8 -*-
{
  'name': 'Kolonies Livechat',
  'summary': '',
  'category': 'website',
  'version': '1.0',
  'sequence': -9,
  'author': 'Omar OUHARI',
  'license': 'Other proprietary',
  'website': '',
  'description': '',
  'depends': [
    'im_livechat',
    'kolonies_marketplace',
  ],
  'data': [
    # security
    'security/ir.model.access.csv',
    # views
    'views/templates.xml',
  ],
  'application': False,
  'installable': True,
  'auto_install': False,
}
