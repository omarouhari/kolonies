# -*- coding: utf-8 -*-

import pytz

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _add_dispatch_parameters(cls, func):
        """
        Override to let public user access to website switcher
        :param func:
        :return:
        """

        # Force website with query string paramater, typically set from website selector in frontend navbar
        force_website_id = request.httprequest.args.get('fw')
        if (force_website_id and request.session.get('force_website_id') != force_website_id and
                request.env.user.has_group('website.group_multi_website')):
            request.env['website']._force_website(request.httprequest.args.get('fw'))

        context = {}
        if not request.context.get('tz'):
            context['tz'] = request.session.get('geoip', {}).get('time_zone')
            try:
                pytz.timezone(context['tz'] or '')
            except pytz.UnknownTimeZoneError:
                context.pop('tz')

        request.website = request.env['website'].get_current_website()  # can use `request.env` since auth methods are called
        context['website_id'] = request.website.id
        # This is mainly to avoid access errors in website controllers where there is no
        # context (eg: /shop), and it's not going to propagate to the global context of the tab
        # If the company of the website is not in the allowed companies of the user, set the main
        # company of the user.
        if request.website.company_id in request.env.user.company_ids:
            context['allowed_company_ids'] = request.website.company_id.ids
        else:
            context['allowed_company_ids'] = request.env.user.company_id.ids

        # modify bound context
        request.context = dict(request.context, **context)

        super(IrHttp, cls)._add_dispatch_parameters(func)

        if request.routing_iteration == 1:
            request.website = request.website.with_context(request.context)
