# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Odoo Marketplace Booking & Reservation Management",
  "summary"              :  """The Odoo Marketplace admin can create booking products such as movie tickets so the customers can schedule their booking and reservation directly from the marketplace website.""",
  "category"             :  "Marketing",
  "version"              :  "1.0.1",
  "sequence"             :  0,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Booking-Reservation-Management.html",
  "description"          :  """Odoo Marketplace Booking & Reservation Management
Odoo booking & reservation management
Odoo Subscription Management
Odoo Website Subscription Management
Odoo appointment management
Odoo website Appointment Management
Schedule bookings
Tickets
Reservations
Booking Facility in Odoo
Website booking system
Appointment management system in Odoo
Booking & reservation management in Odoo
Reservation management in Odoo
Booking
Reservation
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
multi-vendor Marketplace
Booking and reservation""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_booking_system&lifetime=120&lout=1&custom_url=/",
  "depends"              :  [
                             'odoo_marketplace',
                             'website_booking_system',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/mp_booking_views.xml',
                             'views/mp_booking_timeslots_view.xml',
                             'views/mp_booking_plans_view.xml',
                             'views/marketplace_config_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
  "post_init_hook"       :  "approve_all_timeslots_nd_plans",
}