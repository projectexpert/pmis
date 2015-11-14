# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-Today Synconics Technologies Private Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime
from openerp import tools
from openerp.osv import osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz


class mail_compose_message(osv.osv):

    _name = 'mail.compose.message'
    _inherit = ['mail.compose.message', 'mail.message']

    def default_get(self, cr, uid, fields, context=None):
        result = {}
        result = super(mail_compose_message, self).default_get(
            cr, uid, fields, context=context)
        if context.get('option') == 'forward':
            result['parent_id'] = False
            result['partner_ids'] = False
        return result

    def get_record_data(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        result = {}, False
        body = subject = from_email = mail_date = to_email_id = ''
        to_partner_ids = attachment_ids = []

        result = super(mail_compose_message, self).get_record_data(
            cr, uid, values, context=context)
        if context.get('option') == 'forward':
            parent_id = values.get('parent_id')
            for parent in self.pool.get('mail.message').browse(
                cr, uid, parent_id, context=context
            ):
                active_tz = pytz.timezone(
                    context.get("tz", "UTC")if context else "Europe/Rome"
                )  # For CE time
                attendance_start = datetime.strptime(
                    parent.create_date, DEFAULT_SERVER_DATETIME_FORMAT
                ).replace(tzinfo=pytz.utc).astimezone(active_tz)
                next_attendance_date = datetime.strftime(
                    attendance_start, "%a, %b %d, %Y at %H:%M %p"
                )
                mail_date = datetime.strptime(
                    next_attendance_date, "%a, %b %d, %Y at %H:%M %p"
                ).strftime("%a, %b %d, %Y at %H:%M %p")
                body = tools.ustr(parent.body)
                from_email = parent.email_from
                subject = tools.ustr(parent.subject or parent.record_name or '')
                attachment_ids = [attach.id for attach in parent.attachment_ids]
                if not result['partner_ids']:
                    for partner in self.pool.get('res.partner').browse(
                        cr, uid, [parent.partner_ids.id], context=context
                    ):
                        to_partner_ids.append(partner.id)
                else:
                    to_partner_ids = result['partner_ids']
                    del to_partner_ids[0]

            re_prefix = _('Fwd:')
            if subject and not (
                subject.startswith('Fwd:') or subject.startswith(re_prefix)
            ):
                subject = "%s %s" % (re_prefix, subject)
            result['subject'] = subject

            result['attachment_ids'] = attachment_ids

            for partner in self.pool.get('res.partner').browse(
                cr, uid, list(set(to_partner_ids)), context=context
            ):
                to_email_id += partner.name + ' ' + partner.email + '; '

            from_format = "<br><b>From : </b>"
            date_format = "<br><b>Date : </b>"
            to_format = "<br><b>To : </b>"
            body1_format = "<br><br><br>"
            body2 = """
<br><br>---------- Forwarded message ----------<br><b>Subject: </b>
            """

            if type(from_email) == bool:
                from_email = ''
            if not (from_email) == bool:
                from_email1 = from_email.replace("<", "(")
                from_email2 = from_email1.replace(">", ")")
            body1 = (
                body2 + subject + from_format + from_email2 +
                date_format + mail_date + to_format + to_email_id +
                body1_format + body
            )
            result['body'] = body1
        return result
