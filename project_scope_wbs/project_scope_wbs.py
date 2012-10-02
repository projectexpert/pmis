# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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

    def _project_complete_wbs_name(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        
        if not ids:
            return []
        
        res = []        
            
        data_project =[]
        
        project_obj = self.pool.get('project.project')
        
        tasks = self.browse(cr, uid, ids, context=None)   
                
        for task in tasks:            
            if task.project_id:
                task_project_id = task.project_id.id
                data_project = project_obj.read(cr, uid, task_project_id, ['complete_wbs_name'], context=[])            
            if data_project:
                res.append((task.id, data_project['complete_wbs_name']))
            else:
                res.append((task.id, ''))
        return dict(res)  

    def _project_complete_wbs_code(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        
        if not ids:
            return []
        
        res = []        
            
        data_project =[]
        
        project_obj = self.pool.get('project.project')
        
        tasks = self.browse(cr, uid, ids, context=None)   
                
        for task in tasks:            
            if task.project_id:
                task_project_id = task.project_id.id
                data_project = project_obj.read(cr, uid, task_project_id, ['complete_wbs_code'], context=[])            
            if data_project:
                res.append((task.id, data_project['complete_wbs_code']))
            else:
                res.append((task.id, ''))
        return dict(res)  

    

    
    _columns = {
        'project_complete_wbs_name': fields.function(_project_complete_wbs_name, method=True, type='char', string='WBS path name', size=250, help='Project Complete WBS path name',
            store={
                'project.task': (lambda self, cr, uid, ids, c={}: ids, ['project_id'], 10),               
            }),   
        'project_complete_wbs_code': fields.function(_project_complete_wbs_code, method=True, type='char', string='WBS path code', size=250, help='Project Complete WBS path code',
            store={
                'project.task': (lambda self, cr, uid, ids, c={}: ids, ['project_id'], 10),               
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
                 'account.analytic.account': (get_child_accounts, ['code'], 20),                 
                 }),      
        'complete_wbs_name': fields.function(_complete_wbs_name_calc, method=True, type='char', string='Full WBS path', size=250, help='Full path in the WBS hierarchy',
            store={
                 'account.analytic.account': (get_child_accounts, ['name'], 20),                 
                 }),                                                                                                          
        'class': fields.selection([('project','Project'),('subproject','Subproject'), ('phase','Phase'), ('deliverable','Deliverable'), ('work_package','Work Package')], 'Class', help='The classification allows you to create a proper project Work Breakdown Structure'),
        'lifecycle_stage': fields.many2one('project.lifecycle','Lifecycle Stage'),                
        'child_projects': fields.one2many('project.project', 'parent_id', 'WBS Components'),

     }
     
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        
        args = args[:]
#        if context.get('current_model') == 'project.project':
#            cr.execute("select analytic_account_id from project_project ")
#            project_ids = [x[0] for x in cr.fetchall()]
#            # We cannot return here with normal project_ids, the following process also has to be followed.
#            # The search should consider the name inhere, earlier it was just bypassing it.
#            # Hence, we added the args and let the below mentioned procedure do the trick
#            # Let the search method manage this.
#            args += [('id', 'in', project_ids)]
#            return self.name_get(cr, uid, project_ids, context=context)
        account = self.search(cr, uid, [('complete_wbs_code', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
        if not account:
            account = self.search(cr, uid, [('complete_wbs_name', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)


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
                    data.insert(0,'')   
                    
                acc = acc.parent_id
            data = ' / '.join(data)
            res.append((account.id, data))
        return res
    
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        for account in self.browse(cr, uid, ids, context=context):
            data = []
            acc = account
            while acc:
                data.insert(0, acc.name)
                acc = acc.parent_id
            data = ' / '.join(data)
            res2 = self.code_get(cr, uid, [account.id], context=None)
            if res2:
                data = '[' + res2[0][1] + '] ' + data            
            #if project.partner_id.name:
            #    data = data + ' ('+ project.partner_id.name + ')'

            
            res.append((account.id, data))
        return res
    
account_analytic_account()


class project(osv.osv):
    _name = "project.project"
    _inherit = "project.project"

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        for project in self.browse(cr, uid, ids, context=context):
            data = []
            proj = project
            while proj:
                data.insert(0, proj.name)
                proj = proj.parent_id
            data = ' / '.join(data)
            res2 = self.code_get(cr, uid, [project.id], context=None)
            if res2:
                data = '[' + res2[0][1] + '] ' + data            
            #if project.partner_id.name:
            #    data = data + ' ('+ project.partner_id.name + ')'

            
            res.append((project.id, data))
        return res

    def code_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        for project in self.browse(cr, uid, ids, context=context):
            data = []
            proj = project
            while proj:
                if proj.code:
                    data.insert(0, proj.code)
                else:
                    data.insert(0,'')   
                    
                proj = proj.parent_id
            data = ' / '.join(data)
            res.append((project.id, data))
        return res

 
    def _child_compute(self, cr, uid, ids, name, arg, context=None):
        result = {}
        project_child_ids = []
        if context is None:
            context = {}
        
        for project in self.browse(cr, uid, ids, context=context):
            for child in project.child_ids:
                project_child_list = self.search(cr, uid, [('analytic_account_id','=', child.id)], context=context)
                for project_child_id in project_child_list:
                    project_child_ids.append(project_child_id)
            
                    
            result[project.id] = project_child_ids

        return result

    _columns = {        
        'project_child_complete_ids': fields.function(_child_compute, relation='project.project', method=True, string="Project Hierarchy", type='many2many'),
                                               
    }
    
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        
        args = args[:]
#        if context.get('current_model') == 'project.project':
#            cr.execute("select analytic_account_id from project_project ")
#            project_ids = [x[0] for x in cr.fetchall()]
#            # We cannot return here with normal project_ids, the following process also has to be followed.
#            # The search should consider the name inhere, earlier it was just bypassing it.
#            # Hence, we added the args and let the below mentioned procedure do the trick
#            # Let the search method manage this.
#            args += [('id', 'in', project_ids)]
#            return self.name_get(cr, uid, project_ids, context=context)
        project = self.search(cr, uid, [('complete_wbs_code', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
        if not project:
            project = self.search(cr, uid, [('complete_wbs_name', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
#            newproj = project
#            while newproj:
#                newproj = self.search(cr, uid, [('parent_id', 'in', newproj)]+args, limit=limit, context=context)
#                project += newproj

        return self.name_get(cr, uid, project, context=context)

project()

             