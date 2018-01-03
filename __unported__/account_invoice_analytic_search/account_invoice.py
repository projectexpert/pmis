# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
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

from openerp.osv import fields, osv


class account_invoice(osv.osv):

    _inherit = "account.invoice"

    def _get_analytic_accounts(self, cursor, user, ids, name, arg,
                               context=None):
        res = {}
        for invoice in self.browse(cursor, user, ids, context=context):
            res[invoice.id] = []
            for invoice_line in invoice.invoice_line:
                if invoice_line.account_analytic_id:
                    res[invoice.id].append(
                        invoice_line.account_analytic_id.id)
        return res

    def _get_analytic_account_user_ids(self, cursor, user, ids, name, arg,
                                       context=None):
        res = {}
        for invoice in self.browse(cursor, user, ids, context=context):
            res[invoice.id] = []
            for invoice_line in invoice.invoice_line:
                if invoice_line.account_analytic_id:
                    if invoice_line.account_analytic_id.user_id:
                        res[invoice.id].append(
                            invoice_line.account_analytic_id.user_id.id)
        return res

    def _search_analytic_accounts(self, cr, uid, obj, name, args, context):

        invoice_line_obj = self.pool.get('account.invoice.line')
        res = []
        for field, operator, value in args:
            assert field == name
            invoice_line_ids = invoice_line_obj.search(
                cr, uid, [('account_analytic_id', operator, value)])
            invoice_ids = [invoice_line.invoice_id and
                           invoice_line.invoice_id.id for
                           invoice_line in
                           invoice_line_obj.browse(
                            cr, uid, invoice_line_ids)
                           ]
            res.append(('id', 'in', invoice_ids))
        return res

    def _search_analytic_account_user_ids(self, cr, uid, obj, name, args,
                                          context):

        invoice_line_obj = self.pool.get('account.invoice.line')
        res = []
        for field, operator, value in args:
            assert field == name
            invoice_line_ids = invoice_line_obj.search(
                cr, uid, [('account_analytic_user_id', operator, value)])
            invoice_ids = [invoice_line.invoice_id and
                           invoice_line.invoice_id.id for
                           invoice_line in
                           invoice_line_obj.browse(
                            cr, uid, invoice_line_ids)
                           ]
            res.append(('id', 'in', invoice_ids))
        return res

    _columns = {
        'account_analytic_ids': fields.function(
            _get_analytic_accounts, type='many2many',
            string='Analytic Account', method=True,
            fnct_search=_search_analytic_accounts,
            readonly=True),

        'account_analytic_user_ids': fields.function(
            _get_analytic_account_user_ids, type='many2many',
            string='Project Manager', method=True,
            fnct_search=_search_analytic_account_user_ids,
            readonly=True),
    }

account_invoice()
