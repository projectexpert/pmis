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
{
    "name": "Mail Forward",
    "version": "1.0",
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'https://www.synconics.com',
    "category": "Social Network",
    "summary": "Mail Forward",
    "description": """
    Mail forwarding feature is a normal practice to convey the message to third
    party. While the option is missing, you have to go for lengthy procedure
    which contains download and upload. In Odoo, we have facilitated our user
    with the advancement of some clicks as stated here.

    User can forward the mail to another recipient or group of recipient using
    one click. The Icon (Green Coloured) shows the button having mail forwarding
    option.

    Subject will highlight "FWD:" text preceding with the original content
    of subject. In the body of mail, you can see the data of previous mails and
    on the top you can draft using various formatting option as usual.

    While forwarding mail, If mail contains any attachment then the forward mail
    carry forward the same to the newly composed mail.
    """,
    "depends": ["mail"],
    'data': ["views/mail_forward.xml"],
    'qweb': ['static/src/xml/*.xml'],
    "installable": True,
    "auto_install": False
}
