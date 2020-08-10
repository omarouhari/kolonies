# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class BuyerController(http.Controller):

    @http.route('/my/dashboard', type='http', auth="user", website=True)
    def my_dashboard(self):
        user = request.env.user
        if user.has_group('odoo_marketplace.marketplace_seller_group'):
            menu = request.env.ref('kolonies_booking.booking_session_menu', raise_if_not_found=False)
        else:
            menu = request.env.ref('kolonies_marketplace.wk_buyer_dashboard', raise_if_not_found=False)
        url = "/web#menu_id=" + str(menu.id)
        return request.redirect(url)
