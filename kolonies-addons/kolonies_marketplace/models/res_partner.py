# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([('professional', 'Professional'), ('student', 'University Student')], 'Seller Type')
    resume_line_ids = fields.One2many('hr.resume.line', 'partner_id', 'Diplomas')
    skill_ids = fields.One2many('hr.employee.skill', 'partner_id', 'Skills')
    website_category_ids = fields.Many2many('product.public.category', 'product_category_seller_rel', 'partner_id', 'category_id',
                                            'Website Categories')
    neighborhood = fields.Char('Neighborhood')
    seller_level = fields.Selection([('new', 'New Seller'), ('one', 'Level One'), ('two', 'Level Two'), ('top_rated', 'Top Rated Seller')],
                                    'Seller Level')
    sol_ids = fields.One2many('sale.order.line', 'marketplace_seller_id', 'Sale Order Lines', readonly=True)
    localisation_ids = fields.Many2many('seller.localisation', 'seller_localisation_partner_rel', 'partner_id', 'localisation_id',
                                        'Localisations Served')
    product_ids = fields.One2many('product.template', 'marketplace_seller_id', 'Products', readonly=True)
    session_price = fields.Monetary(compute='_compute_session_price', store=True, compute_sudo=True)

    @api.depends('product_ids', 'product_ids.booking_day_slot_ids', 'product_ids.booking_day_slot_ids.booking_slots_ids')
    def _compute_session_price(self):
        for record in self:
            configs = record.product_ids.mapped('booking_day_slot_ids.booking_slots_ids')
            record.session_price = min(configs.mapped('price') or [0])

    def group_by_skill_type(self):
        group_by = {}
        for skill in self.skill_ids:
            group_by.setdefault(skill.skill_type_id, []).append(skill.display_name)
        print (group_by)
        return group_by

