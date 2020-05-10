# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2016-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# License URL :<https://store.webkul.com/license.html/>
##########################################################################

from odoo import api, fields, models, _
from lxml import etree
import logging
_logger = logging.getLogger(__name__)

class BookingTimeSlot(models.Model):
    _inherit = "booking.time.slot"

    @api.model
    def _set_seller_id(self):
        user_obj = self.env['res.users'].sudo().browse(self._uid)
        if user_obj.partner_id and user_obj.partner_id.seller:
            return user_obj.partner_id.id
        return self.env['res.partner']

    marketplace_seller_id = fields.Many2one("res.partner", string="Seller", default=_set_seller_id, copy=False)
    state = fields.Selection([
        ("new", "New"),
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),], "State", required=True, default="new")
    auto_timeslot_approve = fields.Boolean(string="Auto Timeslot Approve",
        default=lambda self: self.env['ir.default'].get('res.config.settings', 'mp_auto_timeslot_approve'))

    def button_approve_timeslot(self):
        self.state = "approved"

    def button_reject_timeslot(self):
        self.state = "rejected"

    def button_set_pending_timeslot(self):
        for rec in self:
            rec.marketplace_seller_id = self.env.user.partner_id.id or rec.marketplace_seller_id
            rec.timeslot_auto_approve()

    def timeslot_auto_approve(self):
        auto_timeslot_approve = self.env['ir.default'].get('res.config.settings', 'mp_auto_timeslot_approve')
        for obj in self:
            obj.write({"state": "pending"})
            if auto_timeslot_approve:
                obj.sudo().button_approve_timeslot()
        return True

    def action_approve_mp_booking_timeslots(self):
        for rec in self:
            if rec.state in ['new','pending']:
                rec.button_approve_timeslot()
        return

    @api.model
    def create(self, vals):
        res = super(BookingTimeSlot, self).create(vals)
        if not (self._context.get('mp_new_booking') or self._context.get("mp_approved_booking")):
            res.state = 'approved'
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='tree', toolbar=False, submenu=False):
        res = super(BookingTimeSlot, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        view_type='tree'
        doc = etree.XML(res['arch'])

        # code to make create false from tree view in approved timeslot menu
        if self._context.get('mp_approved_booking'):
            for node in doc.xpath("//tree"):
                node.set('create', '0')
                node.set('edit', '0')
                node.set('editable', '')

        # code to hide server action from seller end
        officer_group = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_officer_group')[1]
        groups_ids = self.env.user.sudo().groups_id.ids
        if officer_group not in groups_ids and res.get("toolbar", False):
            toolbar_dict = res.get("toolbar", {})
            toolbar_dict["action"] = []
            toolbar_dict["relate"] = []
            for key in toolbar_dict:
                # Remove options from Print menu for seller
                if key == "print":
                    print_list = toolbar_dict[key]
                    for print_list_item in print_list:
                        if print_list_item["xml_id"] not in ["marketplace_booking_system.ir_actions_server_mp_approve_booking_timeslots"]:
                            print_list.remove(print_list_item)
            res["toolbar"] = toolbar_dict

        # code for other seller do not change the timeslot of other seller in new state
        if self._context.get('mp_new_booking') and officer_group not in groups_ids:
            for node in doc.xpath("//tree//field[@name='start_time']"):
                node.set("attrs", "{'readonly':['|',('state','not in',['new']),('marketplace_seller_id','!=',%s)]}" % str(self.env.user.partner_id.id))
            for node in doc.xpath("//tree//field[@name='end_time']"):
                node.set("attrs", "{'readonly':['|',('state','not in',['new']),('marketplace_seller_id','!=',%s)]}" % str(self.env.user.partner_id.id))

        res['arch'] = etree.tostring(doc)
        return res

class BookingPlan(models.Model):
    _inherit = "booking.plan"


    @api.model
    def _set_seller_id(self):
        user_obj = self.env['res.users'].sudo().browse(self._uid)
        if user_obj.partner_id and user_obj.partner_id.seller:
            return user_obj.partner_id.id
        return self.env['res.partner']

    marketplace_seller_id = fields.Many2one("res.partner", string="Seller", default=_set_seller_id, copy=False)
    state = fields.Selection([
        ("new", "New"),
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),], "State", required=True, default="new")
    auto_plan_approve = fields.Boolean(string="Auto Plan Approve",
        default=lambda self: self.env['ir.default'].get('res.config.settings', 'mp_auto_plan_approve'))

    def button_approve_plan(self):
        self.state = "approved"

    def button_reject_plan(self):
        self.state = "rejected"

    def button_set_pending_plan(self):
        for rec in self:
            rec.plan_auto_approve()

    def plan_auto_approve(self):
        auto_plan_approve = self.env['ir.default'].get('res.config.settings', 'mp_auto_plan_approve')
        for obj in self:
            obj.write({"state": "pending"})
            if auto_plan_approve:
                obj.sudo().button_approve_plan()
        return True

    def action_approve_mp_booking_plans(self):
        for rec in self:
            if rec.state in ['new','pending']:
                rec.button_approve_plan()
        return

    @api.model
    def create(self, vals):
        res = super(BookingPlan, self).create(vals)
        if not (self._context.get('mp_new_booking') or self._context.get("mp_approved_booking")):
            res.state = 'approved'
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(BookingPlan, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        view_type='tree'

        # code to hide server action from seller end
        officer_group = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_officer_group')[1]
        groups_ids = self.env.user.sudo().groups_id.ids
        if officer_group not in groups_ids and res.get("toolbar", False):
            toolbar_dict = res.get("toolbar", {})
            toolbar_dict["action"] = []
            toolbar_dict["relate"] = []
            for key in toolbar_dict:
                # Remove options from Print menu for seller
                if key == "print":
                    print_list = toolbar_dict[key]
                    for print_list_item in print_list:
                        if print_list_item["xml_id"] not in ["marketplace_booking_system.ir_actions_server_mp_approve_booking_plans"]:
                            print_list.remove(print_list_item)
            res["toolbar"] = toolbar_dict

        doc = etree.XML(res['arch'])
        if self._context.get('mp_approved_booking'):
            for node in doc.xpath("//tree"):
                node.set('create', '0')
                node.set('edit', '0')
                node.set('editable', '')
            for node in doc.xpath("//form"):
                node.set('create', '0')
                node.set('edit', '0')
        res['arch'] = etree.tostring(doc)
        return res
