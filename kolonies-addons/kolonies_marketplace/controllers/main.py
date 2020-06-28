# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import WebsiteSale, QueryURL, TableCompute
from odoo.addons.odoo_marketplace.controllers.main import MarketplaceSellerProfile

SPG = 20  # Shops/sellers Per Page
SPR = 4  # Shops/sellers Per Row


class MarketplaceSellerProfile(MarketplaceSellerProfile):

	@http.route([
		'/sellers/list/',
		'/sellers/list/page/<int:page>',
	], type='http', auth="public", website=True)
	def load_mp_all_seller(self, page=0, search='', localisation='', skills='', ppg=False, **post):
		print('loc', localisation, 'ski', skills, 'sear', search)
		if not ppg:
			ppg = request.env['website'].get_current_website().seller_ppg
		PPR = request.env['website'].get_current_website().seller_ppr
		if ppg:
			try:
				ppg = int(ppg)
			except ValueError:
				ppg = SPG
			post["ppg"] = ppg
		else:
			ppg = SPG
		domain = self._get_seller_search_domain(search)
		keep = QueryURL('/sellers/list', search=search)

		url = "/sellers/list"
		if search:
			post["search"] = search

		seller_obj = request.env['res.partner']
		seller_count = seller_obj.sudo().search_count(domain)
		total_active_seller = seller_obj.sudo().search_count(self._get_seller_search_domain(""))
		pager = request.website.pager(url=url, total=seller_count, page=page, step=ppg, scope=7, url_args=post)
		seller_objs = seller_obj.sudo().search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

		values = {
			'search': search,
			'pager': pager,
			'seller_objs': seller_objs,
			'search_count': seller_count,
			'bins': TableCompute().process(seller_objs, ppg, PPR),
            'ppg': ppg,
            'ppr': PPR,
            'rows': SPR,
            'keep': keep,
            'total_active_seller': total_active_seller,
            'localisation': localisation,
            'skills': skills,
        }
        return request.render('odoo_marketplace.sellers_list', values)


class BuyerController(http.Controller):

    @http.route('/my/dashboard', type='http', auth="user", website=True)
    def my_dashboard(self):
        buyer_menu = request.env.ref('kolonies_marketplace.wk_buyer_dashboard', raise_if_not_found=False)
        url = "/web#menu_id=" + str(buyer_menu.id)
        return request.redirect(url)
