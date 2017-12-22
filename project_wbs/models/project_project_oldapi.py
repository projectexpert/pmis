# -*- coding: utf-8 -*-
#    Copyright (C) 2015 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright (C) 2015 Eficent (Jordi Ballester Alomar)
#    Copyright (C) 2017 Deneroteam (Vijaykumar Baladaniya)
#    Copyright (C) 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv, orm

class AccountAnalyticAccount(orm.Model):
    _inherit = 'account.analytic.account'

    def get_child_accounts(self, cr, uid, ids, context=None):
        result = {}
        for curr_id in ids:
            result[curr_id] = True
        # Now add the children
        cr.execute('''
        WITH RECURSIVE children AS (
        SELECT parent_id, id
        FROM account_analytic_account
        WHERE parent_id IN %s
        UNION ALL
        SELECT a.parent_id, a.id
        FROM account_analytic_account a
        JOIN children b ON(a.parent_id = b.id)
        )
        SELECT * FROM children order by parent_id
        ''', (tuple(ids),))
        res = cr.fetchall()
        for x, y in res:
            result[y] = True
        return result

    def _complete_wbs_code_calc(
            self, cr, uid, ids, prop, unknow_none,
            unknow_dict
    ):
        if not ids:
            return []
        res = []
        for account in self.browse(cr, uid, ids, context=None):
            data = []
            acc = account
            while acc:
                if acc.code:
                    data.insert(0, acc.code)
                else:
                    data.insert(0, '')

                acc = acc.parent_id
            data = '/'.join(data)
            data = '[' + data + '] '

            res.append((account.id, data))
        return dict(res)

    _columns = {
        'complete_wbs_code_calc': fields.function(
            _complete_wbs_code_calc, method=True, type='char',
            string='Full WBS Code', size=250,
            help='Computed WBS code'),

        'complete_wbs_code': fields.function(
            _complete_wbs_code_calc, method=True, type='char',
            string='Full WBS Code', size=250,
            help='The full WBS code describes the full path of this component '
                 'within the project WBS hierarchy',
            store={
                'account.analytic.account': (
                    get_child_accounts,
                    ['name', 'code', 'parent_id'], 20
                )
            }
        ),
    }
