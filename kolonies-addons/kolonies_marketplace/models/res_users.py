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
