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
        'html_text',
        'kolonies_base',
    ],
    'data': [
        # data
        'data/website_data.xml',
        'data/hr_resume_type_data.xml',
        'data/hr_skill_type_data.xml',
        # security
        'security/ir.model.access.csv',
        # views
        'views/menu.xml',
        'views/templates.xml',
        'views/res_partner_view.xml',
        'views/hr_skill_type_view.xml',
        'views/seller_location_view.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
