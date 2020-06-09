# -*- coding: utf-8 -*-

import uuid
from odoo import api, fields, models, _


class BookingSession(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'calendar.event': 'event_id'}
    _name = 'booking.session'
    _description = 'Booking Session'

    booking_slot_id = fields.Many2one('booking.slot', 'Booking Slot', required=True)
    attachment_ids = fields.Many2many('ir.attachment', 'booking_session_attachment_rel', 'book_session_id', 'attachment_id', 'Documents')
    survey_ids = fields.Many2many('survey.survey', 'booking_session_survey_rel', 'book_session_id', 'survey_id', 'Surveys')
    state = fields.Selection([('draft', 'Draft'), ('planed', 'Planed'), ('open', 'Confirmed'), ('in_progress', 'In Progress'),
                              ('finished', 'Finished'), ('cancelled', 'Cancelled')], default='draft', required=True)
    page_uuid = fields.Char('Page UUID', required=False)
    page_web_url = fields.Char('Page Web Url', required=False, compute='_compute_page_web_url', store=True)
    product_id = fields.Many2one('product.product', 'Product')
    day = fields.Selection(related='booking_slot_id.slot_config_id.name', readonly=True, store=True)
    start_time = fields.Float(related='booking_slot_id.time_slot_id.start_time', readonly=True, store=True)
    end_time = fields.Float(related='booking_slot_id.time_slot_id.end_time', realonly=True, store=True)
    event_id = fields.Many2one('calendar.event', 'Calendar Event', required=True, ondelete="restrict")
    participant_count = fields.Integer('Participant Count', compute='_compute_participant_count', store=True, required=False)

    def button_plan(self):
        self.ensure_one()
        self.state = 'planed'
        return True

    def button_confirm(self):
        self.ensure_one()
        self.state = 'open'
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
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if not base_url.endswith('/'):
            base_url += '/web/booking/session/'
        else:
            base_url += 'web/booking/session/'
        for record in self:
            record.page_web_url = base_url + (record.page_uuid or '')

    def button_open_participant_open(self):
        action = self.env.ref('contacts.action_contacts').read()[0]
        action.update({'domain': [('id', 'in', self.partner_ids.ids)]})
        return action

    @api.depends('partner_ids')
    def _compute_participant_count(self):
        for record in self:
            record.participant_count = len(record.partner_ids)

    def add_participant(self, partner=False):
        self.ensure_one()
        if not partner:
            return False
        self.partner_ids = [(4, partner.id)]
        return True
