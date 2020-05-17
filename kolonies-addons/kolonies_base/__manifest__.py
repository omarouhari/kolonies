# -*- coding: utf-8 -*-
{
  'name': 'Kolonies Base',
  'summary': '',
  'category': 'Base',
  'version': '1.0',
  'sequence': -9,
  'author': 'Omar OUHARI',
  'license': 'Other proprietary',
  'website': '',
  'description': '',
  'depends': [
    'odoo_marketplace',
    'hr_skills',
  ],
  'data': [
    # security
    'security/users_groups.xml',
    'security/ir.model.access.csv',
    # views
    'views/menu.xml',
    'views/templates.xml',
  ],
  'application': False,
  'installable': True,
  'auto_install': False,
}
