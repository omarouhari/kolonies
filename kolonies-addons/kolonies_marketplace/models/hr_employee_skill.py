# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'

    partner_id = fields.Many2one('res.partner', 'Seller')
    employee_id = fields.Many2one(required=False)
