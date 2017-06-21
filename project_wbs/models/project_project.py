# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
#  - Jordi Ballester Alomar
# © 2015 MATMOZ d.o.o.
#  - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
from datetime import datetime, date
from openerp.tools.translate import _
from openerp import api, fields, models, _


class Project(models.Model):
    _name = "project.project"
    _inherit = "project.project"
    _description = "WBS element"
    _order = "c_wbs_code"

    @api.multi
    def _get_project_analytic_wbs(self):
        result = {}
        self.env.cr.execute('''
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
            --WHERE p.state not in ('template', 'cancelled')
            )
            SELECT * FROM children order by ppid
        ''', (tuple(self.ids),))
        res = self.env.cr.fetchall()
        for r in res:
            if r[0] in result:
                result[r[0]][r[1]] = r[2]
            else:
                result[r[0]] = {r[1]: r[2]}

        return result

    @api.multi
    def _get_project_wbs(self):
        result = []
        projects_data = self._get_project_analytic_wbs()
        for ppid in projects_data.values():
            result.extend(ppid.keys())
        return result

    @api.multi
    @api.depends('name')
    def name_get(self):
        res = []
        for project_item in self:
            data = []
            proj = project_item

            while proj:
                if proj and proj.name:
                    data.insert(0, proj.name)
                else:
                    data.insert(0, '')

                proj = proj.parent_id
            data = '/'.join(data)
            res2 = project_item.code_get()
            if res2:
                data = '[' + res2[0][1] + '] ' + data

            res.append((project_item.id, data))
        return res

    @api.multi
    @api.depends('code')
    def code_get(self):
        res = []
        for project_item in self:
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

    @api.multi
    @api.depends('parent_id')
    def _child_compute(self):
        for project_item in self:
            child_ids = self.search(
                [('parent_id', '=', project_item.analytic_account_id.id)]
            )
            project_item.project_child_complete_ids = child_ids

    # def _has_child(self, cr, uid, ids, fields, args, context=None):

    #     if context is None:
    #         context = {}

    #     for project_item in self.browse(cr, uid, ids, context=context):
    #         if project_item.child_ids:
    #             return True

    #     return False

    @api.multi
    def _resolve_analytic_account_id_from_context(self):
        """
        Returns ID of parent analytic account based on the value of
        'default_parent_id'
        context key, or None if it cannot be resolved to a single
        account.analytic.account
        """
        context = self.env.context or {}
        if type(context.get('default_parent_id')) in (int, long):
            return context['default_parent_id']
        if isinstance(
                context.get('default_parent_id'), basestring
        ):
            analytic_account_name = context['default_parent_id']
            analytic_account_ids = self.env['account.analytic.account'].name_search(
                name=analytic_account_name)
            if len(analytic_account_ids) == 1:
                return analytic_account_ids[0][0]
        return None

    @api.multi
    def _get_parent_members(self):
        context = self.env.context or {}
        member_ids = []
        project_obj = self.env['project.project']
        if 'default_parent_id' in context and context['default_parent_id']:
            for project in project_obj.search(
                [('analytic_account_id', '=', context['default_parent_id'])]
            ):
                for member in project.members:
                    member_ids.append(member.id)
        return member_ids

    @api.multi
    def _get_analytic_complete_wbs_code(self):
        result = {}
        for project in self:
            result[project.id] = (
                project.analytic_account_id.complete_wbs_code_calc
            )

        return result

    @api.multi
    def _complete_wbs_code_search_analytic(self):
        """ Finds projects for an analytic account.
        @return: List of ids
        """
        project_ids = self.search([('analytic_account_id', 'in', self.ids)])
        return project_ids

    project_child_complete_ids = fields.Many2many(
        'project.project',
        string="Project Hierarchy",
        compute=_child_compute
    )
    c_wbs_code = fields.Char(
        compute=_get_analytic_complete_wbs_code,
        string='WBS Code',
        readonly=True,
        store=True
    )

    members = fields.Many2many('res.users', 'project_user_rel', 'project_id',
                               'uid', 'Project Members', help="""Project's
                               members are users who can have an access to
                               the tasks related to this project.""",
                               default=_get_parent_members,
                               states={'close':[('readonly',True)],
                                       'cancelled':[('readonly',True)]})

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        args = args[:]

        projectbycode = self.search(
            [('complete_wbs_code', 'ilike', '%%%s%%' % name)] + args, limit=limit
        )
        projectbyname = self.search(
            [('complete_wbs_name', 'ilike', '%%%s%%' % name)] + args, limit=limit
        )
        project = projectbycode + projectbyname

        return project.name_get()

    # Override the standard behaviour of duplicate_template not introducing
    # the (copy) string to the copied projects.
    @api.multi
    def duplicate_template(self):
        data_obj = self.env['ir.model.data']
        result = []
        for proj in self:
            parent_id = self.env.context.get('parent_id', False)
            self = self.with_context(analytic_project_copy=True)
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
            self = self.with_context(copy=True)
            new_id = proj.copy(default={
                    'name': _("%s") % proj.name,
                    'state': 'open',
                    'date_start': new_date_start,
                    'date': new_date_end,
                    'parent_id': parent_id
                })
            result.append(new_id)
            child_ids = self.search(
                [('parent_id', '=', proj.analytic_account_id.id)])
            parent_id = new_id.analytic_account_id.id
            if child_ids:
                self = self.with_context(parent_id=parent_id)
                self.duplicate_template(child_ids, context={'parent_id':
                                                                parent_id})
        if result and len(result):
            res_id = result[0]
            form_view_id = data_obj._get_id('project', 'edit_project')
            form_view = data_obj.read(form_view_id, ['res_id'])
            tree_view_id = data_obj._get_id('project', 'view_project')
            tree_view = data_obj.read(tree_view_id, ['res_id'])
            search_view_id = data_obj._get_id(
                'project', 'view_project_project_filter')
            search_view = data_obj.read(search_view_id, ['res_id'])
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

    @api.multi
    def action_openChildView(self, module, act_window):
        """
        :return dict: dictionary value for created view
        """
        res = self.env['ir.actions.act_window'].for_xml_id(module, act_window)
        context = self.env.context.copy() or {}
        domain = []
        project_ids = []
        for project in self:
            child_project_ids = self.search(
                [('parent_id', '=', project.analytic_account_id.id)]
            )
            for child_project_id in child_project_ids:
                project_ids.append(child_project_id.id)
            context.update({
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
            })
        domain.append(('id', 'in', project_ids))
        res.update({
            "domain": domain,
            "nodestroy": False
        })
        return res

    @api.multi
    def action_openProjectsView(self):
        return self.action_openChildView('project_wbs', 'open_view_project_projects')

    @api.multi
    def action_openPhasesView(self):
        return self.action_openChildView('project_wbs', 'open_view_project_phases')

    @api.multi
    def action_openDeliverablesView(self):
        return self.action_openChildView('project_wbs', 'open_view_project_deliverables')

    @api.multi
    def action_openWorkPackagesView(self):
        return self.action_openChildView('project_wbs', 'open_view_project_work_packages')

    @api.multi
    def action_openUnclassifiedView(self):
        return self.action_openChildView('project_wbs', 'open_view_unclassified')

    @api.multi
    def action_openChildTreeView(self):
        return self.action_openChildView('project_wbs', 'open_view_project_wbs')

    @api.multi
    def action_openChildKanbanView(self):
        return self.action_openChildView('project_wbs', 'open_view_wbs_kanban')

    @api.multi
    def action_openParentTreeView(self):
        """
        :return dict: dictionary value for created view
        """
        domain = []
        analytic_account_ids = []
        res = self.env['ir.actions.act_window'].for_xml_id(
            'project_wbs', 'open_view_project_wbs'
        )
        for project in self:
            if project.parent_id:
                for parent_project_id in self.env['project.project'].search(
                        [('analytic_account_id', '=', project.parent_id.id)]
                ):
                    analytic_account_ids.append(parent_project_id.id)
        if analytic_account_ids:
            domain.append(('id', 'in', analytic_account_ids))
            res.update({
                "domain": domain,
                "nodestroy": False
            })
        return res

    @api.multi
    def action_openParentKanbanView(self):
        """
        :return dict: dictionary value for created view
        """
        domain = []
        analytic_account_ids = []
        res = self.env['ir.actions.act_window'].for_xml_id(
            'project_wbs', 'open_view_wbs_kanban'
        )
        for project in self:
            if project.parent_id:
                for parent_project_id in self.pool.get('project.project').search(
                        [('analytic_account_id', '=', project.parent_id.id)]
                ):
                    analytic_account_ids.append(parent_project_id.id)
        if analytic_account_ids:
            domain.append(('id', 'in', analytic_account_ids))
            res.update({
                "domain": domain,
                "nodestroy": False
            })
        return res

    @api.multi
    @api.onchange('parent_id')
    def on_change_parent(self):
        return self.env['account.analytic.account'].on_change_parent()
