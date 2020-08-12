# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, SUPERUSER_ID


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_website_id = fields.Many2one('website', 'Partner Website', required=False)
    user_ids = fields.One2many('res.users', 'partner_id', 'Users', required=False)

    def approve(self):
        res = super(ResPartner, self).approve()
        self.create_website()
        return res

    def create_website(self):
        values = self._prepare_website()
        website = self.env.ref('website.default_website', raise_if_not_found=False).copy(default=values)
        self.partner_website_id = website.id
        return True

    def _prepare_website(self):
        return {
            'name': _('Website of %s') % self.name,
            'company_id': self.company_id or self.env.ref('base.main_company', raise_if_not_found=False).id,
            'default_lang_id': self.get_lang().id,
            'channel_id': self.create_channel().id,
            'is_seller': True
        }

    def create_channel(self):
        values = self._prepare_channel()
        return self.env['im_livechat.channel'].create(values)

    def _prepare_channel(self):
        return {
            'name': _('Channel of %s') % self.name,
            'user_ids': [(6, 0, [self.user_ids.id, self.env.ref('base.user_admin').id])],
            'button_text': _('Have a question? Chat with us.'),
            'default_message': _('Hello!\nHow can I help you?'),
            'input_placeholder': _('Type your message here ...'),
        }

    def get_lang(self):
        lang = self.env['res.lang'].search([('code', '=', self.lang)], limit=1)
        return lang or self.env.ref('base.lang_fr', raise_if_not_found=False)
