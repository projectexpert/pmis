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


class purchase_order(osv.osv):

    _inherit = "purchase.order"

    def _get_analytic_accounts(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for purchase in self.browse(cursor, user, ids, context=context):
            res[purchase.id] = []
            for po_line in purchase.order_line:
                if po_line.account_analytic_id:
                    res[purchase.id].append(po_line.account_analytic_id.id)
        return res

    def _get_analytic_account_user_ids(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for purchase in self.browse(cursor, user, ids, context=context):
            res[purchase.id] = []
            for po_line in purchase.order_line:
                if po_line.account_analytic_id:
                    if po_line.account_analytic_id.user_id:
                        res[purchase.id].append(po_line.account_analytic_id.user_id.id)
        return res

    def _search_analytic_accounts(self, cr, uid, obj, name, args, context):

        po_line_obj = self.pool.get('purchase.order.line')
        res = []
        for field, operator, value in args:
            assert field == name
            po_line_ids = po_line_obj.search(cr, uid, [('account_analytic_id', operator, value)])
            order_ids = [
                po_line.order_id and po_line.order_id.id for po_line in po_line_obj.browse(
                    cr, uid, po_line_ids
                )
            ]
            res.append(('id', 'in', order_ids))
        return res

    def _search_analytic_account_user_ids(self, cr, uid, obj, name, args, context):

        po_line_obj = self.pool.get('purchase.order.line')
        res = []
        for field, operator, value in args:
            assert field == name
            po_line_ids = po_line_obj.search(
                cr, uid, [('account_analytic_user_id', operator, value)]
            )
            order_ids = [
                po_line.order_id and po_line.order_id.id for po_line in po_line_obj.browse(cr, uid, po_line_ids)
            ]
            res.append(('id', 'in', order_ids))
        return res

    _columns = {
        'account_analytic_ids': fields.function(_get_analytic_accounts,
                                                type='many2many',
                                                string='Analytic Account',
                                                method=True,
                                                fnct_search=_search_analytic_accounts,
                                                readonly=True),

    }

purchase_order()
