# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    booking_session_ids = fields.One2many('booking.session', 'partner_id', string='Booking Sessions')
    booking_session_count = fields.Integer('Booking Session Count', compute='_compute_booking_session_count')

    def check_booking_session_exist(self, booking_slot=False, product=False, start_date=False, end_date=False):
        return self.booking_session_ids.filtered(lambda bs: bs.booking_slot_id == booking_slot
                                                            and bs.product_id == product
                                                            and bs.start_date == start_date
                                                            and bs.end_date == end_date)

    def _compute_booking_session_count(self):
        for record in self:
            record.booking_session_count = len(record.booking_session_ids)

    def button_booking_session_show(self):
        self.ensure_one()
        action = self.env.ref('kolonies_booking.booking_session_act_window').read()[0]
        action.update({'domain': [('id', 'in', self.booking_session_ids.ids)], 'view_mode': 'tree,calendar,form'})
        return action

    def get_associated_user(self):
        self.ensure_one()
        return self.env['res.users'].search([('partner_id', '=', self.id)], limit=1)
