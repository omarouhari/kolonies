# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.addons.kolonies_base.models.tools import hash_string_hex

_logger = logging.getLogger(__name__)


class BookingSession(models.Model):
    _inherit = 'booking.session'

    iframe_etherpad = fields.Text('Iframe Etherpad', required=False)

    def button_confirm(self):
        res = super(BookingSession, self).button_confirm()
        endpoint = self.env['ir.config_parameter'].sudo().get_param('etherpad_endpoint')
        sequence = self.env['ir.sequence'].next_by_code('etherpad.session.seq')
        if not endpoint:
            ValidationError(_('The etherpad endpoint is not defined in system parameters. Please contact your system administrator.'))
        if not sequence:
            ValidationError(_('The etherpad sequence not found.'))
        if not endpoint.endswith('/'):
            endpoint += '/'
        self.iframe_etherpad = endpoint + hash_string_hex(sequence)
        return res
