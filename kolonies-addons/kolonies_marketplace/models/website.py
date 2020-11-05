# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Website(models.Model):
    _inherit = 'website'

    seller_ppr = fields.Integer('Seller PPR', copy=True)
    seller_ppg = fields.Integer('Seller PPG', copy=True)
    is_seller = fields.Boolean('Is Website Seller')
    active = fields.Boolean(default=True)
    is_default_website_marketplace = fields.Boolean('Is Default Website Marketplace', required=False)

    def write(self, vals):
        if vals.get('seller_ppr') or vals.get('seller_ppg'):
            return super(Website, self.search([])).write(vals)
        return super(Website, self).write(vals)

    @api.constrains('is_default_website_marketplace')
    def _check_unique_default_marketplace_website(self):
        for record in self.filtered(lambda web: web.is_default_website_marketplace):
            if self.search_count([('id', '!=', record.id), ('is_default_website_marketplace', '=', True)]):
                raise ValidationError(_('There is already a default marketplace website!'))
