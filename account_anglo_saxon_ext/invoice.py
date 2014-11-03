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
from openerp.osv import osv


class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    def move_line_get(self, cr, uid, invoice_id, context=None):
        res = super(account_invoice_line, self).move_line_get(cr, uid, invoice_id, context=context)
        inv = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=context)

        if inv.type in ('out_invoice', 'out_refund'):
            for i_line in inv.invoice_line:
                if i_line.product_id and i_line.product_id.valuation == 'real_time':
                    if inv.type == 'out_invoice':
                        # debit account dacc will be the output account
                        # first check the product, if empty check the category
                        dacc = i_line.product_id.property_stock_account_output and i_line.product_id.property_stock_account_output.id
                        if not dacc:
                            dacc = i_line.product_id.categ_id.property_stock_account_output_categ and i_line.product_id.categ_id.property_stock_account_output_categ.id
                    else:
                        # = out_refund
                        # debit account dacc will be the input account
                        # first check the product, if empty check the category
                        dacc = i_line.product_id.property_stock_account_input and i_line.product_id.property_stock_account_input.id
                        if not dacc:
                            dacc = i_line.product_id.categ_id.property_stock_account_input_categ and i_line.product_id.categ_id.property_stock_account_input_categ.id
                    # in both cases the credit account cacc will be the expense account
                    # first check the product, if empty check the category
                    cacc = i_line.product_id.property_account_expense and i_line.product_id.property_account_expense.id
                    if not cacc:
                        cacc = i_line.product_id.categ_id.property_account_expense_categ and i_line.product_id.categ_id.property_account_expense_categ.id
                    if dacc and cacc:
                        for r in res:
                            if r['account_id'] == dacc:
                                r['account_analytic_id'] = i_line.account_analytic_id.id
                            if r['account_id'] == cacc:
                                r['account_analytic_id'] = i_line.account_analytic_id.id
        return res
