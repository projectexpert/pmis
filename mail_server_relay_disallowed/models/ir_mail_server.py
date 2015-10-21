# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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
import logging
import threading

from openerp.addons.base.ir.ir_mail_server import extract_rfc2822_addresses
from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp import SUPERUSER_ID
from openerp.osv import osv
from openerp.tools.translate import _
import openerp.tools as tools

_logger = logging.getLogger(__name__)
_test_logger = logging.getLogger('openerp.tests')


class IrMail_Server(osv.Model):
    _inherit = 'ir.mail_server'

    NO_VALID_RECIPIENT = ("At least one valid recipient address should be "
                          "specified for outgoing emails (To/Cc/Bcc)")

    def send_email(
        self, cr, uid, message, mail_server_id=None, smtp_server=None,
        smtp_port=None, smtp_user=None, smtp_password=None,
        smtp_encryption=None, smtp_debug=False, context=None
    ):
        """Override the standard method to fix the issue of using a mail
        client where relaying is disallowed."""
        # Use the default bounce address **only if** no Return-Path was
        # provided by caller.  Caller may be using Variable Envelope Return
        # Path (VERP) to detect no-longer valid email addresses.
        smtp_from = message['Return-Path']
        if not smtp_from:
            smtp_from = self._get_default_bounce_address(
                cr, uid, context=context
            )
        if not smtp_from:
            smtp_from = message['From']
        assert smtp_from, (
            "The Return-Path or From header is required for any outbound email"
        )

        # The email's "Envelope From" (Return-Path), and all recipient
        # addresses must only contain ASCII characters.
        from_rfc2822 = extract_rfc2822_addresses(smtp_from)
        assert from_rfc2822, (
            "Malformed 'Return-Path' or 'From' address: %r - "
            "It should contain one valid plain ASCII email") % smtp_from
        # use last extracted email, to support rarities like
        # 'Support@MyComp <support@mycompany.com>'
        smtp_from = from_rfc2822[-1]
        email_to = message['To']
        email_cc = message['Cc']
        email_bcc = message['Bcc']

        smtp_to_list = filter(
            None,
            tools.flatten(
                map(
                    extract_rfc2822_addresses,
                    [email_to, email_cc, email_bcc]
                )
            )
        )
        assert smtp_to_list, self.NO_VALID_RECIPIENT

        x_forge_to = message['X-Forge-To']
        if x_forge_to:
            # `To:` header forged, e.g. for posting on mail.groups,
            # to avoid confusion
            del message['X-Forge-To']
            del message['To']  # avoid multiple To: headers!
            message['To'] = x_forge_to

        # Do not actually send emails in testing mode!
        if getattr(threading.currentThread(), 'testing', False):
            _test_logger.info("skip sending email in test mode")
            return message['Message-Id']

        # Get SMTP Server Details from Mail Server
        mail_server = None
        if mail_server_id:
            mail_server = self.browse(cr, SUPERUSER_ID, mail_server_id)
        elif not smtp_server:
            mail_server_ids = self.search(
                cr, SUPERUSER_ID, [], order='sequence', limit=1
            )
            if mail_server_ids:
                mail_server = self.browse(cr, SUPERUSER_ID, mail_server_ids[0])

        if mail_server:
            smtp_server = mail_server.smtp_host
            smtp_user = mail_server.smtp_user
            smtp_password = mail_server.smtp_pass
            smtp_port = mail_server.smtp_port
            smtp_encryption = mail_server.smtp_encryption
            smtp_debug = smtp_debug or mail_server.smtp_debug
        else:
            # we were passed an explicit smtp_server or nothing at all
            smtp_server = smtp_server or tools.config.get('smtp_server')
            smtp_port = tools.config.get(
                'smtp_port', 25
            ) if smtp_port is None else smtp_port
            smtp_user = smtp_user or tools.config.get('smtp_user')
            smtp_password = smtp_password or tools.config.get('smtp_password')
            if smtp_encryption is None and tools.config.get('smtp_ssl'):
                smtp_encryption = 'starttls'
                # STARTTLS is the new meaning of the smtp_ssl flag as of v7.0

        if not smtp_server:
            raise osv.except_osv(
                _("Missing SMTP Server"),
                _("Please define at least one SMTP server, or "
                  "provide the SMTP parameters explicitly.")
            )

        try:
            message_id = message['Message-Id']

            # Add email in Maildir if smtp_server contains maildir.
            if smtp_server.startswith('maildir:/'):
                from mailbox import Maildir
                maildir_path = smtp_server[8:]
                mdir = Maildir(maildir_path, factory=None, create=True)
                mdir.add(message.as_string(True))
                return message_id

            smtp = None
            try:
                # START OF CODE ADDED
                smtp = self.connect(
                    smtp_server, smtp_port, smtp_user, smtp_password,
                    smtp_encryption or False, smtp_debug
                )
                # smtp.sendmail(smtp_from, smtp_to_list, message.as_string())

                from email.utils import parseaddr, formataddr
                # exact name and address
                (oldname, oldemail) = parseaddr(message['From'])
                # use original name with new address
                newfrom = formataddr((oldname, smtp_user))
                # need to use replace_header instead '=' to prevent
                # double field
                message.replace_header('From', newfrom)
                smtp.sendmail(smtp_user, smtp_to_list, message.as_string())
                # END OF CODE ADDED
            finally:
                if smtp is not None:
                    smtp.quit()
        except Exception, e:
            msg = _(
                "Mail delivery failed via SMTP server '%s'.\n%s: %s"
            ) % (
                tools.ustr(smtp_server),
                e.__class__.__name__,
                tools.ustr(e)
            )
            _logger.error(msg)
            raise MailDeliveryException(_("Mail Delivery Failed"), msg)
        return message_id
