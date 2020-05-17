# -*- coding: utf-8 -*-

from odoo import fields, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    message_attachment_count = fields.Integer(groups="base.group_user,odoo_marketplace.marketplace_draft_seller_group,kolonies_base.marketplace_buyer_group")
