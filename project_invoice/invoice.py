# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp import tools


class account_invoice(osv.osv):
    _inherit = "account.invoice"

    def _line_analytic_accounts_get(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for inv in self.browse(cr, uid, ids, context):
            str_data = ''
            analytic_accounts = []
            for line in inv.invoice_line:
                if line.account_analytic_id and line.account_analytic_id not in analytic_accounts:
                    analytic_accounts.append(line.account_analytic_id)
            account_names = []
            account_name = ''
            for analytic_account in analytic_accounts:
                account_name = self.pool.get('account.analytic.account').name_get(
                    cr, uid, [analytic_account.id], context=context
                )
                account_names.append(account_name[0][1])

            str_data = ', '.join(map(tools.ustr, account_names))
            result[inv.id] = str_data

        return result

    def _line_analytic_accounts_search(self, cr, uid, obj, name, args, domain=None, context=None):
        if not args:
            return []

        analytic_account_obj = self.pool.get('account.analytic.account')
        account_invoice_line_obj = self.pool.get('account.invoice.line')
        analytic_account_ids = []
        i = 0
        while i < len(args):
            fargs = args[i][0].split('.', 1)
            if len(fargs) > 1:
                args[i] = (fargs[0], 'in', analytic_account_obj.search(
                    cr, uid, [(fargs[1], args[i][1], args[i][2])])
                )
                i += 1
                continue
            if isinstance(args[i][2], basestring):
                analytic_account_ids = analytic_account_obj.name_search(
                    cr, uid, args[i][2], [], args[i][1]
                )
                args[i] = (args[i][0], 'in', [x[0] for x in analytic_account_ids])
            i += 1

        ids = []
        if analytic_account_ids:
            account_ids = []
            for acc_id in analytic_account_ids:
                account_ids.append(acc_id[0])

            line_ids = account_invoice_line_obj.search(cr, uid, [('account_analytic_id', 'in', account_ids)])
            lines = account_invoice_line_obj.browse(cr, uid, line_ids, context)
            for line in lines:
                if line.invoice_id and line.invoice_id.id not in ids:
                    ids.append(line.invoice_id.id)

        return [('id', 'in', ids)]

    _columns = {
        'line_analytic_accounts': fields.function(
            _line_analytic_accounts_get,
            fnct_search=_line_analytic_accounts_search,
            method=True,
            type="char",
            size=512,
            string="Analytic Accounts"),
    }

account_invoice()
