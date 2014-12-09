# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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

from lxml import etree
import time
from datetime import datetime, date

from openerp.tools.translate import _
from openerp.osv import fields, osv

class project(osv.osv):
    _name = "project.project"
    _inherit = "project.project"
    _description = "WBS element"

    def _get_children(self, cr, uid, ids, context=None):

        read_data = self.pool.get('project.project').read(cr, uid, ids,
                                                          ['id', 'analytic_account_id',
                                                           'project_child_complete_ids',
                                                           'state'])
        for data in read_data:
            if data['id'] not in self.project_ids:
                self.projects_data[data['id']] = data['analytic_account_id'][0]
                self.project_ids.append(data['id'])
                if data['state'] not in ('template', 'cancelled'):
                    self.read_data.append(data)
                    if data['project_child_complete_ids']:
                        self._get_children(cr, uid, data['project_child_complete_ids'], context=context)
        return True

    def _get_project_analytic_wbs(self, cr, uid, ids, context=None):

        self.read_data = []
        self.project_ids = []
        self.projects_data = {}
        self._get_children(cr, uid, ids, context=context)

        return self.projects_data

    def _get_project_wbs(self, cr, uid, ids, context=None):

        projects_data = self._get_project_analytic_wbs(cr, uid, ids, context=context)

        return projects_data.keys()

    def name_get(self, cr, uid, ids, context=None):

        if not ids:
            return []
        if type(ids) is int: ids = [ids]
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
            data = ' / '.join(data)
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
                
            data = ' / '.join(data)
            res.append((project_item.id, data))
        return res

    def _child_compute(self, cr, uid, ids, name, arg, context=None):

        result = {}
        if context is None:
            context = {}

        for project_item in self.browse(cr, uid, ids, context=context):
            child_ids = self.search(cr, uid, [('parent_id', '=', project_item.analytic_account_id.id)],
                                    context=context)

            result[project_item.id] = child_ids

        return result

    def _has_child(self, cr, uid, ids, fields, args, context=None):

        if context is None:
            context = {}

        for project_item in self.browse(cr, uid, ids, context=context):
            if project_item.child_ids:
                return True

        return False

    def _resolve_analytic_account_id_from_context(self, cr, uid, context=None):
        """ Returns ID of parent analytic account based on the value of 'default_parent_id'
            context key, or None if it cannot be resolved to a single
            account.analytic.account
        """
        if context is None:
            context = {}
        if type(context.get('default_parent_id')) in (int, long):
            return context['default_parent_id']
        if isinstance(context.get('default_parent_id'), basestring):
            analytic_account_name = context['default_parent_id']
            analytic_account_ids = self.pool.get('account.analytic.account').name_search(cr, uid,
                                                                                         name=analytic_account_name,
                                                                                         context=context)
            if len(analytic_account_ids) == 1:
                return analytic_account_ids[0][0]
        return None

    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        stage_obj = self.pool.get('analytic.account.stage')
        order = stage_obj._order
        access_rights_uid = access_rights_uid or uid
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        analytic_account_id = self._resolve_analytic_account_id_from_context(cr, uid, context=context)
        if analytic_account_id:
            search_domain += ['|', ('analytic_account_ids', '=', analytic_account_id)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(cr, uid, search_domain, order=order,
                                      access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x, y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        fold = {}
        for stage in stage_obj.browse(cr, access_rights_uid, stage_ids, context=context):
            fold[stage.id] = stage.fold or False
        return result, fold

    _columns = {        
        'project_child_complete_ids': fields.function(_child_compute, relation='project.project', method=True, string="Project Hierarchy", type='many2many'),
    }

    _group_by_full = {
        'stage_id': _read_group_stage_ids,
    }

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):       

        if not args:
            args = []
        if context is None:
            context = {}
        
        args = args[:]

        projectbycode = self.search(cr, uid, [('complete_wbs_code', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
        projectbyname = self.search(cr, uid, [('complete_wbs_name', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
        project = projectbycode + projectbyname

        return self.name_get(cr, uid, project, context=context)

    # Override the standard behaviour of duplicate_template not introducing the (copy) string
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
                start_date = date(*time.strptime(proj.date_start, '%Y-%m-%d')[:3])
                end_date = date(*time.strptime(proj.date, '%Y-%m-%d')[:3])
                new_date_end = (datetime(*time.strptime(new_date_start, '%Y-%m-%d')[:3])+(end_date-start_date)).strftime('%Y-%m-%d')
            context.update({'copy': True})
            new_id = self.copy(cr, uid, proj.id, default={
                'name': _("%s") % (proj.name),
                'state': 'open',
                'date_start': new_date_start,
                'date': new_date_end,
                'parent_id': parent_id}, context=context)
            result.append(new_id)

            child_ids = self.search(cr, uid, [('parent_id', '=', proj.analytic_account_id.id)], context=context)
            parent_id = self.read(cr, uid, new_id, ['analytic_account_id'])['analytic_account_id'][0]
            if child_ids:
                self.duplicate_template(cr, uid, child_ids, context={'parent_id': parent_id})

        if result and len(result):
            res_id = result[0]
            form_view_id = data_obj._get_id(cr, uid, 'project', 'edit_project')
            form_view = data_obj.read(cr, uid, form_view_id, ['res_id'])
            tree_view_id = data_obj._get_id(cr, uid, 'project', 'view_project')
            tree_view = data_obj.read(cr, uid, tree_view_id, ['res_id'])
            search_view_id = data_obj._get_id(cr, uid, 'project', 'view_project_project_filter')
            search_view = data_obj.read(cr, uid, search_view_id, ['res_id'])
            return {
                'name': _('Projects'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'project.project',
                'view_id': False,
                'res_id': res_id,
                'views': [(form_view['res_id'], 'form'), (tree_view['res_id'], 'tree')],
                'type': 'ir.actions.act_window',
                'search_view_id': search_view['res_id'],
                'nodestroy': True
            }

    def action_openView(self, cr, uid, ids, module, act_window, context=None):
        """
        :return dict: dictionary value for created view
        """
        project = self.browse(cr, uid, ids[0], context)
        res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, module, act_window, context)
        res['context'] = {
            'search_default_parent_id': project.analytic_account_id and project.analytic_account_id.id or False,
            'default_parent_id': project.analytic_account_id and project.analytic_account_id.id or False,
            'default_partner_id': project.partner_id and project.partner_id.id or False,
        }
        res['nodestroy'] = True
        return res

    def action_openProjectsView(self, cr, uid, ids, context=None):

        return self.action_openView(cr, uid, ids, 'project_wbs', 'open_view_project_projects', context=context)

    def action_openPhasesView(self, cr, uid, ids, context=None):

        return self.action_openView(cr, uid, ids, 'project_wbs', 'open_view_project_phases', context=context)

    def action_openDeliverablesView(self, cr, uid, ids, context=None):

        return self.action_openView(cr, uid, ids, 'project_wbs', 'open_view_project_deliverables', context=context)

    def action_openWorkPackagesView(self, cr, uid, ids, context=None):

        return self.action_openView(cr, uid, ids, 'project_wbs', 'open_view_project_work_packages', context=context)

    def action_openUnclassifiedView(self, cr, uid, ids, context=None):

        return self.action_openView(cr, uid, ids, 'project', 'open_view_project_all', context=context)

    def action_openChildTreeView(self, cr, uid, ids, context=None):

        return self.action_openView(cr, uid, ids, 'project_wbs', 'open_view_project_child_tree', context=context)



    def on_change_parent(self, cr, uid, ids, parent_id, context=None):
        return self.pool.get('account.analytic.account').on_change_parent(cr, uid, ids, parent_id)

project()
