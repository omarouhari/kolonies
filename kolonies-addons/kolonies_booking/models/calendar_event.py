# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    booking_session_ids = fields.One2many('booking.session', 'event_id', 'Booking Sessions', required=False)
