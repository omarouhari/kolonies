# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class KoloniesWebsite(http.Controller):

    @http.route('/web/booking/session/<string:url>', type='http', auth='user', methods=['GET'], website=True)
    def open_session_page(self, url='', **post):
        session = request.env['booking.session'].search([('page_web_url', 'like', url)], limit=1)
        if not session:
            page = request.website.is_publisher() and 'website.page_404' or 'http_routing.404'
            return request.render(page, {})
        values = {
            'product': session.product_id,
            'seller': session.partner_id,
            'partners': session.partner_ids,
            'attachments': session.attachment_ids,
            'surveys': session.survey_ids,
        }
        return request.render('kolonies_etherpad.session_web_page', values)
