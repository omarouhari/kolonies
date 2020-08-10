# -*- coding: utf-8 -*-

from odoo import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)
        res.create_associated_employee()
        return res

    def create_associated_employee(self):
        self.ensure_one()
        return self.env['hr.employee'].create({'name': self.name, 'user_id': self.id})

    def check_user_is_draft_seller(self):
        result = super(ResUsers, self).check_user_is_draft_seller()
        if not self.partner_id.seller and self.has_group('kolonies_base.marketplace_buyer_group'):
            return True
        return result
