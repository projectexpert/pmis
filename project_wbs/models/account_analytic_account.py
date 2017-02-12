# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
#  - Jordi Ballester Alomar
# © 2015 MATMOZ d.o.o.
#  - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

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

    def _complete_wbs_name_calc(
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
                if acc.name:
                    data.insert(0, acc.name)
                else:
                    data.insert(0, '')

                acc = acc.parent_id

            data = '/'.join(data)
            res.append((account.id, data))
        return dict(res)

    def _wbs_indent_calc(
            self, cr, uid, ids, prop, unknow_none, unknow_dict
    ):
        if not ids:
            return []
        res = []
        for account in self.browse(cr, uid, ids, context=None):
            data = []
            acc = account
            while acc:
                if acc.name and acc.parent_id.parent_id:
                    data.insert(0, '>')
                else:
                    data.insert(0, '')

                acc = acc.parent_id
            data = ''.join(data)
            res.append((account.id, data))
        return dict(res)

    def _resolve_analytic_account_id_from_context(self, cr, uid, context=None):
        """
        Returns ID of parent analytic account based on the value of
        'default_parent_id' context key, or None if it cannot be resolved to
        a single account.analytic.account
        """
        if context is None:
            context = {}
        if type(context.get('default_parent_id')) in (int, long):
            return context['default_parent_id']
        if isinstance(context.get('default_parent_id'), basestring):
            analytic_account_name = context['default_parent_id']
            analytic_account_ids = self.pool.get(
                'account.analytic.account').name_search(
                cr, uid, name=analytic_account_name, context=context
            )
            if len(analytic_account_ids) == 1:
                return analytic_account_ids[0][0]
        return None

    def _get_portfolio_account_id(
            self, cr, uid, ids, prop, unknow_none,
            unknow_dict
    ):
        if not ids:
            return []
        res = dict.fromkeys(ids, False)
        for account in self.browse(cr, uid, ids, context=None):
            acc = account
            while acc:
                if acc.account_class == 'portfolio':
                    res[account.id] = acc.id
                    break
                acc = acc.parent_id
        return res

    def _get_program_account_id(
            self, cr, uid, ids, prop, unknow_none,
            unknow_dict
    ):
        if not ids:
            return []
        res = dict.fromkeys(ids, False)
        for account in self.browse(cr, uid, ids, context=None):
            acc = account
            while acc:
                if acc.account_class == 'program':
                    res[account.id] = acc.id
                    break
                acc = acc.parent_id
        return res

    def _get_project_account_id(
            self, cr, uid, ids, prop, unknow_none,
            unknow_dict
    ):
        if not ids:
            return []
        res = dict.fromkeys(ids, False)
        for account in self.browse(cr, uid, ids, context=None):
            acc = account
            while acc:
                if acc.account_class == 'project':
                    res[account.id] = acc.id
                    break
                acc = acc.parent_id
        return res

    _columns = {
        'wbs_indent': fields.function(
            _wbs_indent_calc, method=True,
            type='char', string='Level',
            size=32, readonly=True
        ),
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
        'complete_wbs_name': fields.function(
            _complete_wbs_name_calc, method=True, type='char',
            string='Full WBS path', size=250,
            help='Full path in the WBS hierarchy',
            store={
                'account.analytic.account': (
                    get_child_accounts,
                    ['name', 'code', 'parent_id'], 20
                )
            }
        ),
        'project_analytic_account_id': fields.function(
            _get_project_account_id, method=True, type='many2one',
            relation='account.analytic.account',
            string='Root Project',
            help='Root Project in the WBS hierarchy',
            store={
                'account.analytic.account': (
                    get_child_accounts,
                    ['account_class', 'parent_id'], 20
                )
            }
        ),
        'program_analytic_account_id': fields.function(
            _get_program_account_id, method=True, type='many2one',
            relation='account.analytic.account',
            string='Program',
            help='Root Program in the WBS hierarchy',
            store={
                'account.analytic.account': (
                    get_child_accounts,
                    ['account_class', 'parent_id'], 20
                )
            }
        ),
        'portfolio_analytic_account_id': fields.function(
            _get_portfolio_account_id, method=True, type='many2one',
            relation='account.analytic.account',
            string='Portfolio',
            help='Root Portfolio in the WBS hierarchy',
            store={
                'account.analytic.account': (
                    get_child_accounts,
                    ['account_class', 'parent_id'], 20
                )
            }
        ),
        'account_class': fields.selection(
            [
                ('portfolio', 'Portfolio'),
                ('program', 'Program'),
                ('project', 'Project'),
                ('phase', 'Phase'),
                ('deliverable', 'Deliverable'),
                ('work_package', 'Work Package')
            ],
            'Class',
            help='The classification allows you to create a proper project '
                 'Work Breakdown Structure'
        ),
    }

    _order = 'complete_wbs_code'

    def name_search(
            self, cr, uid, name, args=None, operator='ilike',
            context=None, limit=100
    ):
        if not args:
            args = []
        if context is None:
            context = {}

        args = args[:]
        accountbycode = self.search(
            cr, uid,
            [(
                'complete_wbs_code',
                'ilike',
                '%%%s%%' % name
            )] + args, limit=limit, context=context
        )
        accountbyname = self.search(
            cr, uid,
            [('complete_wbs_name', 'ilike', '%%%s%%' % name)] + args,
            limit=limit, context=context
        )
        account = accountbycode + accountbyname

        return self.name_get(cr, uid, account, context=context)

    def code_get(self, cr, uid, ids, context=None):

        if not ids:
            return []
        res = []
        for account in self.browse(cr, uid, ids, context=context):
            data = []
            acc = account
            while acc:
                if acc.code:
                    data.insert(0, acc.code)
                else:
                    data.insert(0, '')

                acc = acc.parent_id
            data = '/'.join(data)
            res.append((account.id, data))
        return res

    def name_get(self, cr, uid, ids, context=None):

        if not ids:
            return []
        if type(ids) is int:
            ids = [ids]

        new_list = []
        for i in ids:
            if i not in new_list:
                new_list.append(i)
        ids = new_list

        res = []
        for account in self.browse(cr, uid, ids, context=context):
            data = []
            acc = account
            while acc:
                if acc.name:
                    data.insert(0, acc.name)
                else:
                    data.insert(0, '')
                acc = acc.parent_id

            data = '/'.join(data)
            # res2 = self.code_get(cr, uid, [account.id], context=None)
            # if res2:
            #     data = '[' + res2[0][1] + '] ' + data

            res.append((account.id, data))
        return res
