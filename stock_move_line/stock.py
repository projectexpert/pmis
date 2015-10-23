# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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
import time
from openerp.osv import fields, osv, orm


class stock_move(osv.osv):

    _inherit = "stock.move"

    def _create_account_move_line(
        self, cr, uid, move, src_account_id, dest_account_id, reference_amount,
        reference_currency_id, context=None
    ):
        """
        Generate the account.move.line values to post to track the stock valuation difference due to the
        processing of the given stock move.
        """
        if context is None:
            context = {}

        res = super(stock_move, self)._create_account_move_line(
            cr, uid, move, src_account_id, dest_account_id,
            reference_amount, reference_currency_id, context=None
        )
        debit_line_vals = res[0][2]
        credit_line_vals = res[1][2]

        account_obj = self.pool.get('account.account')
        src_acct, dest_acct = account_obj.browse(
            cr, uid, [credit_line_vals['account_id'], debit_line_vals['account_id']], context=context
        )

        debit_analytic_account_id = False
        credit_analytic_account_id = False

        if dest_acct.user_type and dest_acct.user_type.report_type in ('income', 'expense'):
            debit_analytic_account_id = move.analytic_account_id.id

        if src_acct.user_type and src_acct.user_type.report_type in ('income', 'expense'):
            credit_analytic_account_id = move.analytic_account_id.id

        debit_line_vals['analytic_account_id'] = debit_analytic_account_id
        credit_line_vals['analytic_account_id'] = credit_analytic_account_id

        return [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]

stock_move()
