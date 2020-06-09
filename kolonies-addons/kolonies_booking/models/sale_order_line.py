# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.addons.kolonies_base.models.tools import convert_float_to_time


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    booking_session_id = fields.Many2one('booking.session', 'Booking Session', required=False)
    duration_booked = fields.Float('Duration', compute='_compute_duration_booked', store=True, compute_sudo=True)

    def _prepare_booking_session_data(self):
        date_start = datetime.combine(self.booking_date, convert_float_to_time(self.booked_slot_id.start_time))
        date_end = datetime.combine(self.booking_date, convert_float_to_time(self.booked_slot_id.end_time))
        return {
            'booking_slot_id': self.booking_slot_id.id,
            'product_id': self.product_id.id,
            'state': 'planed',
            'start': date_start,
            'stop': date_end,
            'partner_ids': [(6, 0, [self.marketplace_seller_id.id, self.order_partner_id.id])],
            'description': _('Appointment') + '-' + self.product_id.name,
            'user_id': self.marketplace_seller_id.get_associated_user().id
        }

    def button_approve_ol(self):
        res = super(SaleOrderLine, self).button_approve_ol()
        if not self.booking_session_id:
            session = self.marketplace_seller_id.check_booking_session_exist(self.booking_slot_id, self.product_id)
            if session:
                session.add_participant(self.order_partner_id)
            else:
                vals = self._prepare_booking_session_data()
                session = self.env['booking.session'].create(vals)
            self.write({'booking_session_id': session.id})
        self.booking_session_id.write({'state': 'open'})
        return res

    def button_ship_ol(self):
        res = super(SaleOrderLine, self).button_ship_ol()
        if not self.booking_session_id:
            session = self.marketplace_seller_id.check_booking_session_exist(self.booking_slot_id, self.product_id)
            if session:
                session.add_participant(self.order_partner_id)
            else:
                vals = self._prepare_booking_session_data()
                session = self.env['booking.session'].create(vals)
            self.write({'booking_session_id': session.id})
        self.booking_session_id.write({'state': 'open'})
        return res

    @api.depends('booked_slot_id', 'booked_slot_id.start_time', 'booked_slot_id.end_time')
    def _compute_duration_booked(self):
        for sol in self:
            sol.duration_booked = sol.booked_slot_id.end_time - sol.booked_slot_id.start_time
