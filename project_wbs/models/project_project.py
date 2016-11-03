# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
#  - Jordi Ballester Alomar
# © 2015 MATMOZ d.o.o.
#  - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

# from lxml import etree
import time
from openerp.tools import misc
from datetime import datetime, date
from openerp.tools.translate import _
from openerp.osv import fields, osv


class Project(osv.osv):
    _name = "project.project"
    _inherit = "project.project"
    _description = "WBS element"

    def _get_project_analytic_wbs(self, cr, uid, ids, context=None):

        result = {}
        cr.execute('''
            WITH RECURSIVE children AS (
            SELECT p.id as ppid, p.id as pid, a.id, a.parent_id
            FROM account_analytic_account a
            INNER JOIN project_project p
            ON a.id = p.analytic_account_id
            WHERE p.id IN %s
            UNION ALL
            SELECT b.ppid as ppid, p.id as pid, a.id, a.parent_id
            FROM account_analytic_account a
            INNER JOIN project_project p
            ON a.id = p.analytic_account_id
            JOIN children b ON(a.parent_id = b.id)
            WHERE p.state not in ('template', 'cancelled')
            )
            SELECT * FROM children order by ppid
        ''', (tuple(ids),))
        res = cr.fetchall()
        for r in res:
            if r[0] in result:
                result[r[0]][r[1]] = r[2]
            else:
                result[r[0]] = {r[1]: r[2]}

        return result

    def _get_project_wbs(self, cr, uid, ids, context=None):

        result = []
        projects_data = self._get_project_analytic_wbs(
            cr, uid, ids, context=context
        )
        for ppid in projects_data.values():
            result.extend(ppid.keys())
        return result

    def name_get(self, cr, uid, ids, context=None):

        if not ids:
            return []
        if type(ids) is int:
            ids = [ids]
        res = []

        new_list = []
        for i in ids:
            if i not in new_list:
                new_list.append(i)
        ids = new_list

        for project_item in self.browse(cr, uid, ids, context=context):
            data = []
            proj = project_item

            while proj:
                if proj and proj.name:
                    data.insert(0, proj.name)
                else:
                    data.insert(0, '')

                proj = proj.parent_id
            data = '/'.join(data)
            res2 = self.code_get(cr, uid, [project_item.id], context=None)
            if res2:
                data = '[' + res2[0][1] + '] ' + data

            res.append((project_item.id, data))
        return res

    def code_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        for project_item in self.browse(cr, uid, ids, context=context):
            data = []
            proj = project_item
            while proj:
                if proj.code:
                    data.insert(0, proj.code)
                else:
                    data.insert(0, '')

                proj = proj.parent_id

            data = '/'.join(data)
            res.append((project_item.id, data))
        return res

    def _child_compute(self, cr, uid, ids, name, arg, context=None):

        result = {}
        if context is None:
            context = {}

        for project_item in self.browse(
                cr, uid, ids, context=context
        ):
            child_ids = self.search(
                cr, uid,
                [('parent_id', '=', project_item.analytic_account_id.id)],
                context=context
            )

            result[project_item.id] = child_ids

        return result

    def _has_child(self, cr, uid, ids, fields, args, context=None):

        if context is None:
            context = {}

        for project_item in self.browse(cr, uid, ids, context=context):
            if project_item.child_ids:
                return True

        return False

    def _resolve_analytic_account_id_from_context(
            self, cr, uid, context=None
    ):
        """
        Returns ID of parent analytic account based on the value of
        'default_parent_id'
        context key, or None if it cannot be resolved to a single
        account.analytic.account
        """
        if context is None:
            context = {}
        if type(context.get('default_parent_id')) in (int, long):
            return context['default_parent_id']
        if isinstance(
                context.get('default_parent_id'), basestring
        ):
            analytic_account_name = context['default_parent_id']
            analytic_account_ids = self.pool.get(
                'account.analytic.account').name_search(
                cr, uid, name=analytic_account_name, context=context
            )
            if len(analytic_account_ids) == 1:
                return analytic_account_ids[0][0]
        return None

    def _get_parent_members(self, cr, uid, context=None):
        if context is None:
            context = {}
        member_ids = []
        project_obj = self.pool.get('project.project')
        if 'default_parent_id' in context and context['default_parent_id']:
            for project_id in project_obj.search(
                cr, uid,
                [('analytic_account_id', '=', context['default_parent_id'])]
            ):
                project = project_obj.browse(
                    cr, uid, project_id, context=context
                )
                for member in project.members:
                    member_ids.append(member.id)
        return member_ids

    def _get_analytic_complete_wbs_code(
            self, cr, uid, ids, field_name, arg,
            context=None
    ):
        result = {}
        for project in self.browse(
                cr, uid, ids, context=context
        ):
            result[project.id] = \
                project.analytic_account_id.complete_wbs_code_calc

        return result

    def _complete_wbs_code_search_analytic(
            self, cr, uid, ids, context=None
    ):
        """ Finds projects for an analytic account.
        @return: List of ids
        """
        project_ids = self.pool['project.project'].search(
            cr, uid,
            [('analytic_account_id', 'in', ids)],
            context=context
        )
        return project_ids

    _columns = {
        'project_child_complete_ids': fields.function(
            _child_compute, relation='project.project',
            method=True, string="Project Hierarchy", type='many2many'
        ),

        'c_wbs_code': fields.function(
            _get_analytic_complete_wbs_code, type='char', string='WBS Code',
            method=True, readonly=True,
            store={
                'account.analytic.account': (
                    _complete_wbs_code_search_analytic,
                    ['name', 'code', 'parent_id', 'complete_wbs_code'],
                    10
                )
            }
        )
    }

    _defaults = {
        'members': _get_parent_members,
    }

    _order = "c_wbs_code"

    def name_search(
            self, cr, uid, name, args=None, operator='ilike',
            context=None, limit=100
    ):

        if not args:
            args = []
        if context is None:
            context = {}

        args = args[:]

        projectbycode = self.search(
            cr, uid,
            [('complete_wbs_code', 'ilike', '%%%s%%' % name)] + args,
            limit=limit, context=context
        )
        projectbyname = self.search(
            cr, uid,
            [('complete_wbs_name', 'ilike', '%%%s%%' % name)] + args,
            limit=limit, context=context
        )
        project = projectbycode + projectbyname

        return self.name_get(cr, uid, project, context=context)

    # Override the standard behaviour of duplicate_template not introducing
    # the (copy) string
    # to the copied projects.
    def duplicate_template(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_obj = self.pool.get('ir.model.data')
        result = []
        for proj in self.browse(cr, uid, ids, context=context):
            parent_id = context.get('parent_id', False)
            context.update({'analytic_project_copy': True})
            new_date_start = time.strftime('%Y-%m-%d')
            new_date_end = False
            if proj.date_start and proj.date:
                start_date = date(
                    *time.strptime(proj.date_start, '%Y-%m-%d')[:3]
                )
                end_date = date(*time.strptime(proj.date, '%Y-%m-%d')[:3])
                new_date_end = (
                    datetime(
                        *time.strptime(
                            new_date_start,
                            '%Y-%m-%d'
                        )[:3]
                    ) + (end_date - start_date)
                ).strftime('%Y-%m-%d')
            context.update({'copy': True})
            new_id = self.copy(
                cr, uid, proj.id, default={
                    'name': _("%s") % proj.name,
                    'state': 'open',
                    'date_start': new_date_start,
                    'date': new_date_end,
                    'parent_id': parent_id
                }, context=context
            )
            result.append(new_id)

            child_ids = self.search(
                cr, uid,
                [('parent_id', '=', proj.analytic_account_id.id)],
                context=context
            )
            parent_id = self.read(
                cr, uid, new_id,
                ['analytic_account_id']
            )['analytic_account_id'][0]
            if child_ids:
                self.duplicate_template(
                    cr, uid, child_ids,
                    context={'parent_id': parent_id}
                )

        if result and len(result):
            res_id = result[0]
            form_view_id = data_obj._get_id(
                cr, uid, 'project', 'edit_project'
            )
            form_view = data_obj.read(
                cr, uid, form_view_id, ['res_id']
            )
            tree_view_id = data_obj._get_id(
                cr, uid, 'project', 'view_project'
            )
            tree_view = data_obj.read(
                cr, uid, tree_view_id, ['res_id']
            )
            search_view_id = data_obj._get_id(
                cr, uid, 'project', 'view_project_project_filter'
            )
            search_view = data_obj.read(
                cr, uid, search_view_id, ['res_id']
            )
            return {
                'name': _('Projects'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'project.project',
                'view_id': False,
                'res_id': res_id,
                'views': [
                    (form_view['res_id'], 'form'),
                    (tree_view['res_id'], 'tree')
                ],
                'type': 'ir.actions.act_window',
                'search_view_id': search_view['res_id'],
                'nodestroy': True
            }

    def action_openChildView(
            self, cr, uid, ids, module, act_window,
            context=None
    ):
        """
        :return dict: dictionary value for created view
        """
        if context is None:
            context = {}
        project = self.browse(
            cr, uid, ids[0], context
        )
        child_project_ids = self.pool.get(
            'project.project').search(
            cr, uid, [('parent_id', '=', project.analytic_account_id.id)]
        )
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, module, act_window, context
        )
        res['context'] = {
            'default_parent_id': (
                project.analytic_account_id and
                project.analytic_account_id.id or
                False
            ),
            'default_partner_id': (
                project.partner_id and
                project.partner_id.id or
                False
            ),
            'default_user_id': (
                project.user_id and
                project.user_id.id or
                False
            ),
        }
        res['domain'] = "[('id', 'in', [" + ','.join(
            map(str, child_project_ids)) + "])]"
        res['nodestroy'] = False
        return res

    def action_openProjectsView(
            self, cr, uid, ids, context=None
    ):

        return self.action_openChildView(
            cr, uid, ids, 'project_wbs',
            'open_view_project_projects',
            context=context
        )

    def action_openPhasesView(
            self, cr, uid, ids, context=None
    ):

        return self.action_openChildView(
            cr, uid, ids, 'project_wbs',
            'open_view_project_phases',
            context=context
        )

    def action_openDeliverablesView(
            self, cr, uid, ids, context=None
    ):

        return self.action_openChildView(
            cr, uid, ids, 'project_wbs',
            'open_view_project_deliverables',
            context=context
        )

    def action_openWorkPackagesView(
            self, cr, uid, ids, context=None
    ):

        return self.action_openChildView(
            cr, uid, ids, 'project_wbs',
            'open_view_project_work_packages',
            context=context
        )

    def action_openUnclassifiedView(
            self, cr, uid, ids, context=None
    ):

        return self.action_openChildView(
            cr, uid, ids, 'project_wbs',
            'open_view_unclassified',
            context=context
        )

    def action_openChildTreeView(
            self, cr, uid, ids, context=None
    ):

        return self.action_openChildView(
            cr, uid, ids, 'project_wbs',
            'open_view_wbs_tree',
            context=context
        )

    def action_openParentTreeView(
            self, cr, uid, ids, context=None
    ):
        """
        :return dict: dictionary value for created view
        """
        if context is None:
            context = {}
        project = self.browse(cr, uid, ids[0], context)
        res = self.pool.get('ir.actions.act_window').for_xml_id(
            cr, uid, 'project_wbs', 'open_view_wbs_tree', context
        )
        if project.parent_id:
            for parent_project_id in self.pool.get('project.project').search(
                    cr, uid,
                    [('analytic_account_id', '=', project.parent_id.id)]
            ):
                res['domain'] = "[('id','='," + str(parent_project_id) + ")]"

        res['nodestroy'] = False
        return res

    def on_change_parent(
            self, cr, uid, ids, parent_id, context=None
    ):
        return self.pool.get('account.analytic.account').on_change_parent(
            cr, uid, ids, parent_id
        )
