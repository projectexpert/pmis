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


class purchase_requisition(osv.osv):
    _inherit = "purchase.requisition"

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

        pr_line_obj = self.pool.get('purchase.requisition.line')
        res = []
        for field, operator, value in args:
            assert field == name
            pr_line_ids = pr_line_obj.search(cr, uid, [('account_analytic_id',
                                                        operator, value)])
            order_ids = [pr_line.requisition_id and pr_line.requisition_id.id
                         for pr_line in pr_line_obj.browse(cr, uid, pr_line_ids)]
            res.append(('id', 'in', order_ids))
        return res

    def _search_analytic_account_user_ids(self, cr, uid, obj, name, args, context):

        pr_line_obj = self.pool.get('purchase.requisition.line')
        res = []
        for field, operator, value in args:
            assert field == name
            pr_line_ids = pr_line_obj.search(cr, uid, [('account_analytic_user_id',
                                                        operator, value)])
            order_ids = [pr_line.requisition_id and pr_line.requisition_id.id
                         for pr_line in pr_line_obj.browse(cr, uid, pr_line_ids)]
            res.append(('id', 'in', order_ids))
        return res

    _columns = {
        'account_analytic_ids': fields.function(_get_analytic_accounts,
                                                type='many2many',
                                                string='Analytic Account',
                                                method=True,
                                                fnct_search=_search_analytic_accounts,
                                                readonly=True),
        'account_analytic_user_ids': fields.function(_get_analytic_account_user_ids,
                                                     type='many2many',
                                                     string='Project Manager',
                                                     method=True,
                                                     fnct_search=_search_analytic_account_user_ids,
                                                     readonly=True),
    }    

    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):

        if context is None:
            context = {}
        res = super(purchase_requisition, self).make_purchase_order(cr, uid, ids, partner_id, context=context)

        pol_obj = self.pool.get('purchase.order.line')
        po_obj = self.pool.get('purchase.order')

        for requisition in self.browse(cr, uid, ids, context=context):
            po_req = po_obj.search(cr, uid, [('requisition_id', '=', requisition.id)], context=context)
            for po_id in po_req:
                pol_ids = pol_obj.search(cr, uid, [('order_id', '=', po_id)])
                for pol_id in pol_ids:
                    pol_brw = pol_obj.browse(cr, uid, pol_id)
                    pol_obj.write(cr, uid, [pol_brw.id], {'account_analytic_id':
                                                              requisition.account_analytic_id.id}, context=context)
        return res

purchase_requisition()
