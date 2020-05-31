# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_ids = fields.One2many('res.users', 'partner_id', 'Users', readonly=True)

    def is_online(self):
        self.ensure_one()
        if self.user_ids and self.user_ids[0].hr_presence_state == 'present':
            return True
        return False
