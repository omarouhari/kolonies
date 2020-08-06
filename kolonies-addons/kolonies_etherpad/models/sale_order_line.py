# -*- coding: utf-8 -*-

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def button_approve_ol(self):
        res = super(SaleOrderLine, self).button_approve_ol()
        self.booking_session_id.button_confirm()
        return res

    def button_ship_ol(self):
        res = super(SaleOrderLine, self).button_ship_ol()
        self.booking_session_id.button_confirm()
        return res
