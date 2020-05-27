# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ImLiveChatChannel(models.Model):
    _inherit = 'im_livechat.channel'

    def _get_available_users(self):
        res = super(ImLiveChatChannel, self)._get_available_users()
        # TODO: get the right user according to the channel
        return self.user_ids[1]
