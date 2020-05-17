# -*- coding: utf-8 -*-

from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def check_user_is_seller(self):
        res = super(ResUsers, self).check_user_is_seller()
        if self.has_group('kolonies_base.marketplace_buyer_group'):
            return True
        return res
