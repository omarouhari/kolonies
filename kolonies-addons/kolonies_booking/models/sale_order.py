# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.filtered(lambda so: so.is_booking_type).create_booking_session()
        return res

    def create_booking_session(self):
        for line in self.mapped('order_line'):
            vals = line._prepare_booking_session_data()
            session = self.env['booking.session'].create(vals)
            line.write({'booking_session_id': session.id})
        return True
