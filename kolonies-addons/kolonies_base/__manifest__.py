# -*- coding: utf-8 -*-
{
    'name': 'Kolonies Base',
    'summary': '',
    'category': 'Base',
    'version': '1.0',
    'sequence': -99,
    'author': 'Omar OUHARI',
    'license': 'Other proprietary',
    'website': '',
    'description': '',
    'depends': [
        'odoo_marketplace',
        'hr_skills',
        'contacts',
    ],
    'data': [
        # security
    'security/ir_rule.xml',
    'security/users_groups.xml',
    'security/ir.model.access.csv',
    # views
    'views/menu.xml',
    'views/templates.xml',
  ],
  'application': False,
  'installable': True,
  'auto_install': False,
  'pre_init_hook': 'pre_init_no_update',
}
