# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Website(models.Model):
    _inherit = 'website'

    seller_ppr = fields.Integer('Seller PPR', copy=True)
    seller_ppg = fields.Integer('Seller PPG', copy=True)
    is_seller = fields.Boolean('Is Website Seller')

    def write(self, vals):
        if vals.get('seller_ppr') or vals.get('seller_ppg'):
            return super(Website, self.search([])).write(vals)
        return super(Website, self).write(vals)
