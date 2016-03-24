# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
from openerp.tools import misc
from datetime import datetime, date
from openerp.tools.translate import _
from openerp import api, fields, models


class Project(models.Model):
    _inherit = "project.project"
    _description = "WBS Element"

#    @api.multi
#    def _get_project_analytic_wbs(self):
#        print "_get_project_analytic_wbs ####################################"
#        result = {}
#        cr.execute('''
#            WITH RECURSIVE children AS (
#            SELECT p.id as ppid, p.id as pid, a.id, a.parent_id
#            FROM account_analytic_account a
#            INNER JOIN project_project p
#            ON a.id = p.analytic_account_id
#            WHERE p.id IN %s
#            UNION ALL
#            SELECT b.ppid as ppid, p.id as pid, a.id, a.parent_id
#            FROM account_analytic_account a
#            INNER JOIN project_project p
#            ON a.id = p.analytic_account_id
#            JOIN children b ON(a.parent_id = b.id)
#            WHERE p.state not in ('template', 'cancelled')
#            )
#            SELECT * FROM children order by ppid
#        ''', (tuple(ids),))
#        res = cr.fetchall()
#        for r in res:
#            if r[0] in result:
#                result[r[0]][r[1]] = r[2]
#            else:
#                result[r[0]] = {r[1]: r[2]}
#        return result
#
#    @api.multi
#    def _get_project_wbs(self):
#        result = []
#        projects_data = self._get_project_analytic_wbs()
#        for ppid in projects_data.values():
#            result.extend(ppid.keys())
#        return result

    @api.multi
    @api.depends('name', 'parent_id')
    def name_get(self):
        if not self._ids:
            return []
        if type(self._ids) is not list:
            ids = list(self._ids)
        res = []
        new_list = []
        for i in ids:
            if i not in new_list:
                new_list.append(i)
        ids = new_list
        for project_item in self:
            data = []
            proj = project_item
            while proj:
                if proj and proj.name:
                    data.insert(0, proj.name)
                else:
                    data.insert(0, '')
                proj = proj.parent_id
            data = ' / '.join(data)
            res2 = project_item.code_get()
            if res2:
                data = '[' + res2[0][1] + '] ' + data
            res.append((project_item.id, data))
        return res

    @api.multi
    @api.depends('code', 'parent_id')
    def code_get(self):
        if not self._ids:
            return []
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
            data = ' / '.join(data)
            res.append((project_item.id, data))
        return res

    @api.multi
    @api.depends('analytic_account_id')
    def _child_compute(self):
        result = {}
        for project_item in self:
            child = self.search([('parent_id', '=',
                                  project_item.analytic_account_id.id)])
            result[project_item.id] = child.ids
        return result

    @api.multi
    def _has_child(self, fields, args, context=None):
        for project_item in self:
            if project_item.child_ids:
                return True
        return False

    @api.model
    def _resolve_analytic_account_id_from_context(self):
        """ Returns ID of parent analytic account based on the value of
        'default_parent_id'
            context key, or None if it cannot be resolved to a single
            account.analytic.account
        """
        if type(self._context.get('default_parent_id')) in (int, long):
            return self._context['default_parent_id']
        if isinstance(self._context.get('default_parent_id'), basestring):
            analytic_account_name = self._context['default_parent_id']
            analytic_account_ids = \
                self.env['account.analytic.account'].\
                name_search(name=analytic_account_name)
            if len(analytic_account_ids) == 1:
                return analytic_account_ids[0][0]
        return None

    @api.multi
    def _read_group_stage_ids(self, domain, read_group_order=None,
                              access_rights_uid=None):
        stage_obj = self.env['analytic.account.stage']
        order = stage_obj._order
        access_rights_uid = access_rights_uid or self._uid
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        analytic_account_id = self._resolve_analytic_account_id_from_context()
        if analytic_account_id:
            search_domain += ['|', ('analytic_account_ids', '=',
                                    analytic_account_id)]
        search_domain += [('id', 'in', self._ids)]
        stage_ids = stage_obj._search(search_domain, order=order,
                                      access_rights_uid=access_rights_uid)
        stages = stage_obj.sudo(access_rights_uid).browse(stage_ids)
        result = stages.sudo(access_rights_uid).name_get()
        # restore order of the search
        result.sort(lambda x, y: cmp(stage_ids.index(x[0]),
                                     stage_ids.index(y[0])))
        fold = {}
        for stage in stage_obj.sudo(access_rights_uid).browse(stage_ids):
            fold[stage.id] = stage.fold or False
        return result, fold

    @api.model
    def _get_parent_members(self):
        member_ids = []
        project_obj = self.env['project.project']
        if 'default_parent_id' in self._context and\
                self._context['default_parent_id']:
            for project in project_obj.search([]):
                for member in project.members:
                    member_ids.append(member.id)
        return member_ids

    project_child_complete_ids = fields.Many2many('project.project',
                                                  'proj_proj_child_rel',
                                                  'parent_id', 'child_id',
                                                  compute='_child_compute',
                                                  string="Project Hierarchy",
                                                  store=True)
    c_wbs_code = fields.Char(related='analytic_account_id.complete_wbs_code',
                             string='WBS Code', store=True, readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(Project, self).default_get(fields)
        if 'members' in fields:
            res.update({'members': self._get_parent_members()})
        return res

    _group_by_full = {
        'stage_id': _read_group_stage_ids,
    }

    _order = "c_wbs_code"

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        projectbycode = self.search([('complete_wbs_code', 'ilike',
                                      '%%%s%%' % name)] + args, limit=limit)
        projectbyname = self.search([('complete_wbs_name', 'ilike',
                                      '%%%s%%' % name)] + args, limit=limit)
        project = projectbycode + projectbyname
        return project.name_get()

    # Override the standard behaviour of duplicate_template not introducing
    # the (copy) string
    # to the copied projects.

    @api.multi
    def duplicate_template(self):
        data_obj = self.env['ir.model.data']
        result = []
        cr, uid, context = self.env.args
        context = dict(context)
        for proj in self:
            parent_id = context.get('parent_id', False)
            context.update({'analytic_project_copy': True})
            new_date_start = time.strftime('%Y-%m-%d')
            new_date_end = False
            if proj.date_start and proj.date:
                start_date = date(*time.strptime(proj.date_start,
                                                 '%Y-%m-%d')[:3])
                end_date = date(*time.strptime(proj.date, '%Y-%m-%d')[:3])
                new_date_end = (datetime(*time.strptime(
                    new_date_start,
                    '%Y-%m-%d')[:3]) + (end_date - start_date)).\
                    strftime('%Y-%m-%d')
            context.update({'copy': True})
            new = proj.copy(default={
                'name': _("%s") % (proj.name),
                'state': 'open',
                'date_start': new_date_start,
                'date': new_date_end,
                'parent_id': parent_id})
            result.append(new.id)
            self.env.args = cr, uid, misc.frozendict(context)
            child = self.search(
                [('parent_id', '=', proj.analytic_account_id.id)])
            parent_id = new.analytic_account_id.id
            if child:
                child_context = {'parent_id': parent_id}
                child.with_context(child_context).duplicate_template()

        if result and len(result):
            res_id = result[0]
            form_view = data_obj.xmlid_to_res_id('project.edit_project')
            tree_view = data_obj.xmlid_to_res_id('project.view_project')
            search_view = data_obj.\
                xmlid_to_res_id('project.view_project_project_filter')
            return {
                'name': _('Projects'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'project.project',
                'view_id': False,
                'res_id': res_id,
                'views': [(form_view, 'form'), (tree_view, 'tree')],
                'type': 'ir.actions.act_window',
                'search_view_id': search_view,
                'nodestroy': True
            }

    @api.multi
    def action_openChildView(self, module, act_window):
        """
        :return dict: dictionary value for created view
        """
        project = self[0]
        child_project = self.env['project.project'].\
            search([('parent_id', '=', project.analytic_account_id.id)])
        res = self.env['ir.actions.act_window'].for_xml_id(module, act_window)
        res['context'] = {
            'default_parent_id': project.analytic_account_id and
            project.analytic_account_id.id or False,
            'default_partner_id': project.partner_id and
            project.partner_id.id or False,
            'default_user_id': project.user_id and project.user_id.id or False,
        }
        res['domain'] = "[('id', 'in', [" + ','.\
            join(map(str, child_project.ids)) + "])]"
        res['nodestroy'] = False
        return res

    @api.multi
    def action_openProjectsView(self):
        return self.action_openChildView('project_wbs',
                                         'open_view_project_projects')

    @api.multi
    def action_openPhasesView(self):
        return self.action_openChildView('project_wbs',
                                         'open_view_project_phases')

    @api.multi
    def action_openDeliverablesView(self):
        return self.action_openChildView('project_wbs',
                                         'open_view_project_deliverables')

    @api.multi
    def action_openWorkPackagesView(self):
        return self.action_openChildView('project_wbs',
                                         'open_view_project_work_packages')

    @api.multi
    def action_openUnclassifiedView(self):
        return self.action_openChildView('project', 'open_view_project_all')

    @api.multi
    def action_openChildTreeView(self):
        return self.action_openChildView('project_wbs',
                                         'open_view_wbs_tree')

    @api.multi
    def action_openParentTreeView(self):
        """
        :return dict: dictionary value for created view
        """
        project = self[0]
        res = self.env['ir.actions.act_window'].\
            for_xml_id('project_wbs', 'open_view_wbs_tree')
        if project.parent_id:
            for parent_project in self.env['project.project'].\
                    search([('analytic_account_id', '=',
                             project.parent_id.id)]):
                res['domain'] = "[('id','='," + str(parent_project.id) + ")]"
        res['nodestroy'] = False
        return res

    @api.multi
    def action_open_view_project_form(self):
        self._context['view_buttons'] = True
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form, tree, kanban, gantt',
            'res_model': 'project.project',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self._ids[0],
            'context': self._context
        }
        return view

    @api.onchange('parent_id')
    def on_change_parent(self):
        return self.parent_id.on_change_parent(self.parent_id.id)

    @api.multi
    def write(self, values):
        cr, uid, context = self.env.args
        context = dict(context)
        for p in self:
            if values.get('state') and (not values.get('stage_id') and not
                                        context.get('stage_updated')):
                if not context.get('change_project_stage_from_status'):
                    context.update({
                        'change_project_stage_from_status': True
                    })
                    self.env.args = cr, uid, misc.frozendict(context)
                    # Change the stage corresponding to the new status
                    if p.parent_id and p.parent_id.child_stage_ids:
                        for stage in p.parent_id.child_stage_ids:
                            if stage.project_state == values.get('state'):
                                values.update({'stage_id': stage.id})
        return super(Project, self).write(values)
