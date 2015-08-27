# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2012 Mentis d.o.o.
#    Ported to Odoo 8 (C) 2014 Matmoz d.o.o.
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

from openerp.osv import fields
from openerp.osv import osv
from openerp.tools.translate import _


class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        'date_invoice_creation': fields.date(
            'Invoice Date',
            readonly=True,
            required=True,
            states={'draft': [('readonly', False)]},
            select=True,
            help="Date when invoice was created."
        ),
        'date_invoice': fields.date(
            'Debt Start Date',
            readonly=True,
            states={'draft': [('readonly', False)]},
            select=True,
            help="Date when debt relationship between customer and supplier started."
        ),
        'date_invoice_recieved': fields.date(
            'Date Recieved',
            readonly=True,
            required=True,
            states={'draft': [('readonly', False)]},
            select=True,
            help="Date when supplier invoice was recieved."
        ),
    }
    _defaults = {
        'date_invoice_creation': fields.date.context_today,
        'date_invoice':          fields.date.context_today,
        'date_invoice_recieved': fields.date.context_today,
    }

    def action_date_assign(self, cr, uid, ids, *args):
        for inv in self.browse(cr, uid, ids):
            if not inv.date_due:
                super(account_invoice, self).action_date_assign(cr, uid, ids, *args)
        return True

account_invoice()
