# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([('professional', 'Professional'), ('student', 'University Student')], 'Seller Type')
    lang_ids = fields.Many2many('res.lang', 'res_lang_seller_rel', 'partner_id', 'lang_id', 'Spoken Languages')
    resume_line_ids = fields.One2many('hr.resume.line', 'partner_id', 'Diplomas')
    skill_ids = fields.One2many('hr.employee.skill', 'partner_id', 'Skills')
    website_category_ids = fields.Many2many('product.public.category', 'product_category_seller_rel', 'partner_id', 'category_id',
                                            'Website Categories')