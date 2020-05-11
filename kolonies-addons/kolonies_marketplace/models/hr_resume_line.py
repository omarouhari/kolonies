# -*- coding: utf-8 -*-

from odoo import models, fields


class HrResumeLine(models.Model):
    _inherit = 'hr.resume.line'

    partner_id = fields.Many2one('res.partner', 'Seller')
    employee_id = fields.Many2one(required=False)
