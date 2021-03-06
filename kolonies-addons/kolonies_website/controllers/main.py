# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.osv import expression
from werkzeug.exceptions import NotFound
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute


class WebsiteSale(WebsiteSale):

	@http.route([
		'''/shop''',
		'''/shop/page/<int:page>''',
		'''/shop/category/<model("product.public.category"):category>''',
		'''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
	], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
	def shop(self, page=0, category=None, search='', ppg=False, **post):
		add_qty = int(post.get('add_qty', 1))
		Category = request.env['product.public.category']
		if category:
			category = Category.search([('id', '=', int(category))], limit=1)
			if not category or not category.can_access_from_current_website():
				raise NotFound()
		else:
			category = Category

		if ppg:
			try:
				ppg = int(ppg)
				post['ppg'] = ppg
			except ValueError:
				ppg = False
		if not ppg:
			ppg = request.env['website'].get_current_website().shop_ppg or 20

		ppr = request.env['website'].get_current_website().shop_ppr or 4

		attrib_list = request.httprequest.args.getlist('attrib')
		attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
		attributes_ids = {v[0] for v in attrib_values}
		attrib_set = {v[1] for v in attrib_values}

		domain = self._get_search_domain(search, category, attrib_values, localisation=post.get('localisation'), skills=post.get('skills'))
		keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))

		pricelist_context, pricelist = self._get_pricelist_context()

		request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

		url = "/shop"
		if search:
			post["search"] = search
		if attrib_list:
			post['attrib'] = attrib_list

		Product = request.env['product.template'].with_context(bin_size=True)

		search_product = Product.search(domain)
		website_domain = request.website.website_domain()
		categs_domain = [('parent_id', '=', False)] + website_domain
		if search:
			search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
			categs_domain.append(('id', 'in', search_categories.ids))
		else:
			search_categories = Category
		categs = Category.search(categs_domain)

		if category:
			url = "/shop/category/%s" % slug(category)

		product_count = len(search_product)
		pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
		products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

		ProductAttribute = request.env['product.attribute']
		if products:
			# get all products without limit
			attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
		else:
			attributes = ProductAttribute.browse(attributes_ids)

		layout_mode = request.session.get('website_sale_shop_layout_mode')
		if not layout_mode:
			if request.website.viewref('website_sale.products_list_view').active:
				layout_mode = 'list'
			else:
				layout_mode = 'grid'

		values = {
			'search': search,
			'category': category,
			'attrib_values': attrib_values,
			'attrib_set': attrib_set,
			'pager': pager,
			'pricelist': pricelist,
			'add_qty': add_qty,
			'products': products,
			'search_count': product_count,  # common for all searchbox
			'bins': TableCompute().process(products, ppg, ppr),
			'ppg': ppg,
			'ppr': ppr,
			'categories': categs,
			'attributes': attributes,
			'keep': keep,
			'search_categories_ids': search_categories.ids,
			'layout_mode': layout_mode,
			'localisation': post.get('localisation', ''),
			'skills': post.get('skills', ''),
			'order': post.get('order')
		}
		if category:
			values['main_object'] = category
		return request.render("website_sale.products", values)

	def _get_search_domain(self, search, category, attrib_values, search_in_description=True, localisation=False, skills=False):
		domains = [request.website.sale_product_domain()]
		if search:
			for srch in search.split(" "):
				subdomains = [
					[('name', 'ilike', srch)],
					[('product_variant_ids.default_code', 'ilike', srch)],
				]

				if search_in_description:
					subdomains.append([('description', 'ilike', srch)])
					subdomains.append([('description_sale', 'ilike', srch)])
				domains.append(expression.OR(subdomains))

		if localisation:
			for srch in localisation.split(" "):
				subdomains = [
					[('marketplace_seller_id.localisation_ids.city', 'ilike', srch)],
					[('marketplace_seller_id.localisation_ids.neighborhood', 'ilike', srch)],
					[('marketplace_seller_id.localisation_ids.country_id.name', 'ilike', srch)],
				]
				domains.append(expression.OR(subdomains))

		if skills:
			for srch in skills.split(" "):
				subdomains = [
					[('marketplace_seller_id.skill_ids.skill_id.name', 'ilike', srch)],
				]
				domains.append(expression.OR(subdomains))

		if category:
			domains.append([('public_categ_ids', 'child_of', int(category))])

		if attrib_values:
			attrib = None
			ids = []
			for value in attrib_values:
				if not attrib:
					attrib = value[0]
					ids.append(value[1])
				elif value[0] == attrib:
					ids.append(value[1])
				else:
					domains.append([('attribute_line_ids.value_ids', 'in', ids)])
					attrib = value[0]
					ids = [value[1]]
			if attrib:
				domains.append([('attribute_line_ids.value_ids', 'in', ids)])

		return expression.AND(domains)
