# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 OpenERP s.a. (<http://www.openerp.com>).
#    Copyright (C) 2012-2013 Mentis d.o.o. (<http://www.mentis.si>)
#    Copyright (C) 2014 Matmoz d.o.o. (<http://www.matmoz.si>)
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
    'name': 'Invoice Start Debt Relation Date',
    'version': '1.2.1',
    'category': 'Accounting',
    'description': """
    This module adds two new date fields on invoice.

    According to Slovenian accounting standards old 'invoice_date' field on invoice
    acts as start debt relation date, while new 'invoice_date_creation' field serves
    as date of invoice.

    New field 'invoice_date_recieved' also exist on supplier invoices.
    """,
    'author':   "Mentis d.o.o.,"
                "Matmoz d.o.o.",
    'license': "AGPL-3",
    'contributors': [
        'Dušan Laznik <laznik@mentis.si>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'summary': '''Debt start date on invoice different than invoice date''',
    'website':  'http://www.mentis.si,'
                'http://www.matmoz.si',
    'depends': ['account'],
    'data': ['views/account_invoice_view.xml'],
    'demo': [],
    'installable': True,
    'active': False,
}
