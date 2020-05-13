# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SellerLocalisation(models.Model):
	_name = 'seller.localisation'
	_rec_name = 'name'
	_description = 'Seller Localisation'

	name = fields.Char(compute='_compute_name')
	city = fields.Char('City', required=True)
	neighborhood = fields.Char('Neighborhood')
	country_id = fields.Many2one('res.country', 'Country', required=True)

	@api.depends('city', 'neighborhood', 'country_id')
	def _compute_name(self):
		for record in self:
			name = ''
			if record.city:
				name = record.city
			if record.neighborhood:
				name += ' ' + record.neighborhood
			if record.country_id:
				name += ' ' + record.country_id.name
			record.name = name
