# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.portal.controllers.web import Home as PortalHome
from odoo.addons.web.controllers.main import Home as WebHome
from odoo.http import request


class Home(PortalHome):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        return WebHome.web_client(s_action, **kw)