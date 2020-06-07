# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_booking_session_data(self):
        return {
            'booking_slot_id': self.booking_slot_id.id,
            'seller_id': self.marketplace_seller_id.id,
            'product_id': self.product_id.id,
            'state': 'draft'
        }
