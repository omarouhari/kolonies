# -*- coding: utf-8 -*-

import decimal
from odoo import models, fields, api


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	sol_ids = fields.One2many(related='marketplace_seller_id.sol_ids')
	seller_review_ids = fields.One2many(related='marketplace_seller_id.seller_review_ids')
	sales_count_stored = fields.Float('Sales Count', compute='_compute_stored_sales_count', store=True, readonly=True)
	average_rating = fields.Float('Average Rating', compute='_compute_average_rating', store=True, readonly=True)

	@api.depends('sol_ids')
	def _compute_stored_sales_count(self):
		for record in self:
			record.sales_count_stored = sum(
				record.sol_ids.filtered(lambda l: l.product_id == record.product_variant_id).mapped('product_uom_qty'))

	@api.depends('seller_review_ids')
	def _compute_average_rating(self):
		for record in self:
			add = 0.0
			avg = 0.0
			if record.seller_review_ids:
				for reviews_obj in record.seller_review_ids:
					add += reviews_obj.rating
				avg = add / len(record.seller_review_ids)
			record.average_rating = (round(decimal.Decimal(abs(avg)), 2))
