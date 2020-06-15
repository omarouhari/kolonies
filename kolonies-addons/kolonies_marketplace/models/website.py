# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Website(models.Model):
    _inherit = 'website'

    seller_ppr = fields.Integer('Seller PPR', copy=True)
    seller_ppg = fields.Integer('Seller PPG', copy=True)
