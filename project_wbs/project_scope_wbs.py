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

from tools.translate import _
from osv import fields, osv


class task(osv.osv):
    _inherit = 'project.task'

    def _project_complete_wbs_name(self, cr, uid, ids, prop, unknow_none, context=None):        
        if not ids:
            return []
        
        res = []        
            
        data_project =[]
        
        project_obj = self.pool.get('project.project')
        
        tasks = self.browse(cr, uid, ids, context=None)   
                
        for task in tasks:            
            if task.project_id:
                task_project_id = task.project_id.id
                data_project = project_obj.read(cr, uid, task_project_id, ['complete_wbs_name'], context=context)            
            if data_project:
                res.append((task.id, data_project['complete_wbs_name']))
            else:
                res.append((task.id, ''))
        return dict(res)  

    def _project_complete_wbs_code(self, cr, uid, ids, prop, unknow_none, context=None):
        
        if not ids:
            return []
        
        res = []        
            
        data_project =[]
        
        project_obj = self.pool.get('project.project')
        
        tasks = self.browse(cr, uid, ids, context=None)   
                
        for task in tasks:            
            if task.project_id:
                task_project_id = task.project_id.id
                data_project = project_obj.read(cr, uid, task_project_id, ['complete_wbs_code'], context=context)            
            if data_project:
                res.append((task.id, data_project['complete_wbs_code']))
            else:
                res.append((task.id, ''))
        return dict(res)  

    

    
    _columns = {
        'project_complete_wbs_name': fields.function(_project_complete_wbs_name, method=True, type='char', string='WBS path name', size=250, help='Project Complete WBS path name',
            store={
                'project.task': (lambda self, cr, uid, ids, c=None: ids, ['project_id'], 10),               
            }),   
        'project_complete_wbs_code': fields.function(_project_complete_wbs_code, method=True, type='char', string='WBS path code', size=250, help='Project Complete WBS path code',
            store={
                'project.task': (lambda self, cr, uid, ids, c=None: ids, ['project_id'], 10),               
            }),    
                            
     }    


task()


class account_analytic_account(osv.osv):
    
    _inherit = 'account.analytic.account'

    def get_child_accounts(self, cr, uid, ids, context=None):    
        result = {}
        read_data = []
        read_data = self.pool.get('account.analytic.account').read(cr, uid, ids,['child_ids'])
        for data in read_data:                
            for curr_id in ids:
                result[curr_id] = True   
            for child_id in data['child_ids']:  
                lchild_id = []
                lchild_id.append(child_id)                                                         
                result.update(self.get_child_accounts(cr, uid, lchild_id, context))         
        return result

    def _complete_wbs_code_calc(self, cr, uid, ids, prop, unknow_none, unknow_dict):        
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
                    data.insert(0,'')                    
                
                acc = acc.parent_id
            data = ' / '.join(data)
            data = '[' + data + '] '   
            
            res.append((account.id, data))
        return dict(res)                                 
    
        
    def _complete_wbs_name_calc(self, cr, uid, ids, prop, unknow_none, unknow_dict):        
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
                    data.insert(0,'')                    

                acc = acc.parent_id
                
            data = ' / '.join(data)
            res.append((account.id, data))
        return dict(res)     

 
    _columns = {   
                                 
        'complete_wbs_code': fields.function(_complete_wbs_code_calc, method=True, type='char', string='Full WBS Code', size=250, help='The full WBS code describes the full path of this component within the project WBS hierarchy',
            store={
                 'account.analytic.account': (get_child_accounts, ['name', 'code', 'parent_id'], 20),                 
                 }),      
        'complete_wbs_name': fields.function(_complete_wbs_name_calc, method=True, type='char', string='Full WBS path', size=250, help='Full path in the WBS hierarchy',
            store={
                 'account.analytic.account': (get_child_accounts, ['name', 'code', 'parent_id'], 20),                 
                 }),                                                                                                          
        'account_class': fields.selection([('project','Project'),('subproject','Subproject'), ('phase','Phase'), ('deliverable','Deliverable'), ('work_package','Work Package')], 'Class', help='The classification allows you to create a proper project Work Breakdown Structure'),
        'lifecycle_stage': fields.many2one('project.lifecycle','Lifecycle Stage'),

     }

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):        
        if not args:
            args = []
        if context is None:
            context = {}
        
        args = args[:]
        accountbycode = self.search(cr, uid, [('complete_wbs_code', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)        
        accountbyname = self.search(cr, uid, [('complete_wbs_name', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
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
            data = ' / '.join(data)
            res.append((account.id, data))
        return res

    def name_get(self, cr, uid, ids, context=None):        

        if not ids:
            return []
        if type(ids) is int:ids = [ids]

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
                
            data = ' / '.join(data)
            res2 = self.code_get(cr, uid, [account.id], context=None)
            if res2:
                data = '[' + res2[0][1] + '] ' + data            

            res.append((account.id, data))
        return res
    
account_analytic_account()


class project(osv.osv):
    _name = "project.project"
    _inherit = "project.project"

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

    def _get_project_wbs(self, cr, uid, ids, name, arg, context=None):

        projects_data = self._get_project_analytic_wbs(cr, uid, ids, context=context)

        return projects_data.keys()

    def name_get(self, cr, uid, ids, context=None):

        if not ids:
            return []
        if type(ids) is int:ids = [ids]
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

    _columns = {        
        'project_child_complete_ids': fields.function(_child_compute, relation='project.project', method=True, string="Project Hierarchy", type='many2many'),
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
project()
