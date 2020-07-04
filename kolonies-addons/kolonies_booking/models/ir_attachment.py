# -*- coding: utf-8 -*-


from odoo import models, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def check(self, mode, values=None):
        return super(IrAttachment, self.sudo()).check(mode, values)
