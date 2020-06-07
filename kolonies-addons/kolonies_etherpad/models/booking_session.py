# -*- coding: utf-8 -*-

from odoo import api, fields, models


class BookingSession(models.Model):
    _inherit = 'booking.session'

    iframe_etherpad = fields.Html('Iframe Etherpad', required=False)
