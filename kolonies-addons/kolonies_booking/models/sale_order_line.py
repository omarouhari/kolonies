# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    booking_session_id = fields.Many2one('booking.session', 'Booking Session', required=False)
    duration_booked = fields.Float('Duration', compute='_compute_duration_booked', store=True, compute_sudo=True)

    def _prepare_booking_session_data(self):
        return {
            'booking_slot_id': self.booking_slot_id.id,
            'seller_id': self.marketplace_seller_id.id,
            'product_id': self.product_id.id,
            'state': 'plan'
        }

    def button_approve_ol(self):
        res = super(SaleOrderLine, self).button_approve_ol()
        if not self.booking_session_id:
            vals = self._prepare_booking_session_data()
            session = self.env['booking.session'].create(vals)
            self.write({'booking_session_id': session.id})
        self.booking_session_id.write({'state': 'confirmed'})
        self.create_calendar_event()
        return res

    def button_ship_ol(self):
        res = super(SaleOrderLine, self).button_ship_ol()
        if not self.booking_session_id:
            vals = self._prepare_booking_session_data()
            session = self.env['booking.session'].create(vals)
            self.write({'booking_session_id': session.id})
        self.booking_session_id.write({'state': 'confirmed'})
        self.create_calendar_event()
        return res

    def create_calendar_event(self):
        self.ensure_one()
        vals = self._prepare_calendar_event_data()
        print(vals)
        self.env['calendar.event'].create(vals)
        return True

    def _prepare_calendar_event_data(self):
        now = fields.Datetime.now()
        return {
            'name': _('Appointment') + '-' + self.product_id.name,
            'start': now,
            'stop': now + timedelta(minutes=round((self.duration_booked or 1.0) * 60)),
            'partner_ids': [(6, 0, self.marketplace_seller_id.ids)],
        }

    @api.depends('booked_slot_id', 'booked_slot_id.start_time', 'booked_slot_id.end_time')
    def _compute_duration_booked(self):
        for sol in self:
            sol.duration_booked = sol.booked_slot_id.end_time - sol.booked_slot_id.start_time
