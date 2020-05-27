# -*- coding: utf-8 -*-

from odoo import api, fields, models


class NewModule(models.Model):
    _inherit = 'im_livechat.channel'

    def _get_available_users(self):
        res = super(NewModule, self)._get_available_users()
        return res
