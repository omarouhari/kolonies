# -*- coding: utf-8 -*-

from . import models


def pre_init_no_update(cr):
    query = "UPDATE ir_model_data SET noupdate=false WHERE name='%s' AND module='%s';" % ('res_partner_portal_public_rule', 'base')
    cr.execute(query)
