# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Eficent <contact@eficent.com>
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

    _columns = {        
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account'),
    }

    def _create_account_move_line(self, cr, uid, move, src_account_id, dest_account_id, reference_amount, reference_currency_id, context=None):
        """
        Generate the account.move.line values to post to track the stock valuation difference due to the
        processing of the given stock move.
        """
        # prepare default values considering that the destination accounts have the
        # reference_currency_id as their main currency
        partner_id = (move.picking_id.partner_id
                      and self.pool.get('res.partner')._find_accounting_partner(move.picking_id.partner_id).id) or False

        credit_analytic_account_id = False
        debit_analytic_account_id = False
        
        account_obj = self.pool.get('account.account')
        src_acct, dest_acct = account_obj.browse(cr, uid, [src_account_id, dest_account_id], context=context)
        
        if dest_acct.user_type and dest_acct.user_type.report_type in ('income','expense'):
            debit_analytic_account_id = move.analytic_account_id.id
 
        if src_acct.user_type and src_acct.user_type.report_type in ('income','expense'):
            credit_analytic_account_id = move.analytic_account_id.id
                                
        debit_line_vals = {
            'name': move.name,
            'product_id': move.product_id and move.product_id.id or False,
            'quantity': move.product_qty,
            'ref': move.picking_id and move.picking_id.name or False,
            'date': time.strftime('%Y-%m-%d'),
            'partner_id': partner_id,
            'debit': reference_amount,
            'account_id': dest_account_id,
            'analytic_account_id': debit_analytic_account_id,
        }
        credit_line_vals = {
            'name': move.name,
            'product_id': move.product_id and move.product_id.id or False,
            'quantity': move.product_qty,
            'ref': move.picking_id and move.picking_id.name or False,
            'date': time.strftime('%Y-%m-%d'),
            'partner_id': partner_id,
            'credit': reference_amount,
            'account_id': src_account_id,
            'analytic_account_id': credit_analytic_account_id,
        }

        # if we are posting to accounts in a different currency, provide correct values in both currencies correctly
        # when compatible with the optional secondary currency on the account.
        # Financial Accounts only accept amounts in secondary currencies if there's no secondary currency on the account
        # or if it's the same as that of the secondary amount being posted.
        account_obj = self.pool.get('account.account')
        src_acct, dest_acct = account_obj.browse(cr, uid, [src_account_id, dest_account_id], context=context)
        src_main_currency_id = src_acct.company_id.currency_id.id
        dest_main_currency_id = dest_acct.company_id.currency_id.id
        cur_obj = self.pool.get('res.currency')
        if reference_currency_id != src_main_currency_id:
            # fix credit line:
            credit_line_vals['credit'] = cur_obj.compute(cr, uid, reference_currency_id,
                                                         src_main_currency_id, reference_amount,
                                                         context=context)
            if (not src_acct.currency_id) or src_acct.currency_id.id == reference_currency_id:
                credit_line_vals.update(currency_id=reference_currency_id, amount_currency=-reference_amount)
        if reference_currency_id != dest_main_currency_id:
            # fix debit line:
            debit_line_vals['debit'] = cur_obj.compute(cr, uid, reference_currency_id, dest_main_currency_id,
                                                       reference_amount, context=context)
            if (not dest_acct.currency_id) or dest_acct.currency_id.id == reference_currency_id:
                debit_line_vals.update(currency_id=reference_currency_id, amount_currency=reference_amount)

        return [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
    
stock_move()