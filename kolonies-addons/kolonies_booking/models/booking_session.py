# -*- coding: utf-8 -*-

import uuid
from odoo import api, fields, models


class BookingSession(models.Model):
    _name = 'booking.session'
    _description = 'Booking Session'

    name = fields.Char(required=True)
    booking_slot_id = fields.Many2one('booking.slot', 'Booking Slot', required=True)
    seller_id = fields.Many2one('res.partner', 'Seller', required=True)
    partner_ids = fields.Many2many('res.partner', 'booking_session_partner_rel', 'book_session_id', 'partner_id', 'Buyers')
    attachment_ids = fields.Many2many('ir.attachment', 'booking_session_attachment_rel', 'book_session_id', 'attachment_id', 'Documents')
    survey_ids = fields.Many2many('survey.survey', 'booking_session_survey_rel', 'book_session_id', 'survey_id', 'Surveys')
    state = fields.Selection([('draft', 'Draft'), ('planed', 'Planed'), ('confirmed', 'Confirmed'), ('in_progress', 'In Progress'),
                              ('finished', 'Finished'), ('cancelled', 'Cancelled')], default='draft', required=False)
    page_uuid = fields.Char('Page UUID', required=False)
    page_web_url = fields.Char('Page Web Url', required=False, compute='_compute_page_web_url', store=True)
    product_id = fields.Many2one(related='booking_slot_id.slot_config_id.product_id', readonly=True, store=True)
    day = fields.Selection(related='booking_slot_id.slot_config_id.name', readonly=True, store=True)
    start_time = fields.Float(related='booking_slot_id.time_slot_id.start_time', readonly=True, store=True)
    end_time = fields.Float(related='booking_slot_id.time_slot_id.end_time', realonly=True, store=True)

    def button_plan(self):
        self.ensure_one()
        self.state = 'planed'
        return True

    def button_confirm(self):
        self.ensure_one()
        self.state = 'confirmed'
        return True

    def button_start(self):
        self.ensure_one()
        self.state = 'in_progress'
        return True

    def button_finished(self):
        self.ensure_one()
        self.state = 'finished'
        return True

    def button_cancel(self):
        self.ensure_one()
        self.state = 'cancelled'
        return True

    def button_reset(self):
        self.ensure_one()
        self.state = 'draft'
        return True

    @api.model
    def create(self, vals):
        page_uuid = self._get_page_uuid()
        vals.update({'page_uuid': page_uuid, 'name': self.env['ir.sequence'].next_by_code('booking.session.seq')})
        return super(BookingSession, self).create(vals)

    @api.model
    def _get_page_uuid(self):
        return str(uuid.uuid4())

    @api.depends('page_uuid')
    def _compute_page_web_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get('base.web.url')
        for record in self:
            record.page_web_url = base_url + record.page_uuid
