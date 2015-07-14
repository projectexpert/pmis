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
import time
from openerp.tools.translate import _
from openerp.osv import fields, osv


class account_move_line_make_voucher(osv.osv_memory):

    _name = "account.move.line.make.voucher"
    _description = "Create Payment Vouchers from Account Move Lines"

    _columns = {
        'date': fields.date('Date', required=True),
        'journal_id': fields.many2one('account.journal', 'Journal', required=True),
        'reference': fields.char('Ref #', size=64,
                                 help="Transaction reference number."),
        'number': fields.char('Number', size=32),
        'narration': fields.text('Notes'),

    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def make_vouchers_suppliers(self, cr, uid, ids, context=None):
        """
             To make supplier payments

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: A dictionary which of fields with values.

        """

        if context is None:
            context = {}
        context_multi_currency = context.copy()

        res = []

        make_account_vouchers = self.browse(cr, uid, ids[0], context=context)
        journal = make_account_vouchers['journal_id']
        narration = make_account_vouchers['narration']
        reference = make_account_vouchers['reference']
        number = make_account_vouchers['number']
        date = make_account_vouchers['date']

        record_ids = context and context.get('active_ids', False)

        if record_ids:
            move_line_obj = self.pool.get('account.move.line')
            currency_pool = self.pool.get('res.currency')
            voucher_obj = self.pool.get('account.voucher')
            voucher_line_obj = self.pool.get('account.voucher.line')
            company_id = False
            account_id = False
            partner_id = False
            voucher_id = False
            total_amount = 0.0
            account_voucher_cr_ids = []
            account_voucher_dr_ids = []

            currency_id = journal.company_id.currency_id.id
            company_currency = journal.company_id.currency_id.id

            for line in move_line_obj.browse(cr, uid, record_ids, context=context):

                line_company_id = line.company_id and line.company_id.id or False
                if company_id is not False and line_company_id != company_id:
                    raise osv.except_osv(
                        _('Could not create Supplier Payment!'),
                        _('You have to select Journal Items from the same company.'))
                else:
                    company_id = line_company_id

                line_partner_id = line.partner_id and line.partner_id.id or False

                if line_partner_id is False:
                    raise osv.except_osv(
                        _('Could not create Supplier Payment!'),
                        _('The Journal Item has to reference '
                          'to a Partner.'))

                if partner_id is not False and line_partner_id != partner_id:
                    raise osv.except_osv(
                        _('Could not create Supplier Payment!'),
                        _('You have to select Journal Items '
                          'referencing the same Supplier.'))
                else:
                    partner_id = line_partner_id

                partner_account_id = line.partner_id.property_account_payable.id

                line_account_id = line.account_id and line.account_id.id or False

                if account_id is not False and line_account_id != account_id:
                    raise osv.except_osv(
                        _('Could not create Supplier Payment!'),
                        _('You have to select Journal Items '
                          'referencing the same account.'))
                else:
                    account_id = line_account_id

                account_type = line.account_id.type
                if account_type != 'payable':
                    raise osv.except_osv(
                        _('Could not create Supplier Payment!'),
                        _('You have to select Journal Items '
                          'referencing an Accounts Payable Account.'))

                if line.reconcile_id:
                    raise osv.except_osv(
                        _('Could not create Supplier Payment!'),
                        _('You have to select unreconciled or '
                          'partially reconciled Journal Items.'))

                if line.currency_id and currency_id == line.currency_id.id:
                    amount_original = abs(line.amount_currency)
                    amount_unreconciled = abs(line.amount_residual_currency)
                else:
                    # always use the amount booked in the company currency
                    # as the basis of the conversion into the voucher currency
                    amount_original = currency_pool.compute(cr, uid,
                                                            company_currency,
                                                            currency_id,
                                                            line.credit or
                                                            line.debit or 0.0,
                                                            context=context_multi_currency)
                    amount_unreconciled = currency_pool.compute(cr, uid,
                                                                company_currency,
                                                                currency_id,
                                                                abs(line.amount_residual),
                                                                context=context_multi_currency)

                line_currency_id = line.currency_id and line.currency_id.id or company_currency

                account_voucher_line = {
                    'name': line.move_id.name,
                    'type': line.credit and 'dr' or 'cr',
                    'move_line_id': line.id,
                    'account_id': line.account_id.id,
                    'amount_original': amount_original,
                    'amount': amount_unreconciled,
                    'date_original': line.date,
                    'date_due': line.date_maturity,
                    'amount_unreconciled': amount_unreconciled,
                    'currency_id': line_currency_id,
                    'reconcile': True,
                }
                total_amount += amount_unreconciled

                if voucher_id is False:
                    voucher_id = voucher_obj.create(cr, uid, {
                        'type': 'payment',
                        'partner_id': line_partner_id,
                        'account_id': partner_account_id,
                        'journal_id': journal.id,
                        'narration': narration,
                        'state': 'draft',
                        'amount': total_amount,
                        'reference': reference,
                        'number': number,
                        'payment_option': 'without_writeoff',
                        'date': date,
                        'company_id': self.pool.get('res.company')._company_default_get(cr,
                                                                                        uid,
                                                                                        'account.voucher',
                                                                                        context=context)

                    }, context=context)

                account_voucher_line.update({'voucher_id': voucher_id})

                voucher_line_id = voucher_line_obj.create(cr, uid, account_voucher_line,
                                                          context=context)

                if account_voucher_line['type'] == 'cr':
                    account_voucher_cr_ids.append(voucher_line_id)
                else:
                    account_voucher_dr_ids.append(voucher_line_id)

            values = {
                'line_cr_ids': [(4, line_id) for line_id in account_voucher_cr_ids],
                'line_dr_ids': [(4, line_id) for line_id in account_voucher_dr_ids],
                'amount': total_amount,
            }

            voucher_obj.write(cr, uid, [voucher_id], values)
            res.append(voucher_id)

            return self.open_vouchers(cr, uid, ids, res, context=context)

    def open_vouchers(self, cr, uid, ids, res, context=None):
        """ open a view on one of the given invoice_ids """
        ir_model_data = self.pool.get('ir.model.data')
        form_res = ir_model_data.get_object_reference(cr, uid, 'account_voucher', 'view_vendor_payment_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference(cr, uid, 'account_voucher', 'view_voucher_tree')
        tree_id = tree_res and tree_res[1] or False

        return {
            'name': _('Supplier Payments'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_id': res[0],
            'res_model': 'account.voucher',
            'view_id': False,
            'context': context,
            'type': 'ir.actions.act_window',
            'views': [(form_id, 'form'), (tree_id, 'tree')],
        }

account_move_line_make_voucher()
