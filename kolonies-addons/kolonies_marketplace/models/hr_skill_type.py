# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrSkillType(models.Model):
    _inherit = 'hr.skill.type'
    _order = 'sequence'

    sequence = fields.Integer('Sequence')
    ranking = fields.Selection([('label-success', 'Cls. 1'), ('label-heavy', 'Cls. 2'), ('label-moderate', 'Cls. 3'),
                                ('label-normal', 'Cls. 4')], 'Ranking')
