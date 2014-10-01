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

import time
from openerp.report import report_sxw
from datetime import datetime
import operator

#
# Use period and Journal for selection or resources
#
class project_progress(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(project_progress, self).__init__(cr, uid, name, context=context)
        self.localcontext.update( {
            'time': time,
            'get_project_structure': self._get_project_structure,
            'get_project_milestones': self._get_project_milestones,
            'get_project_tasks': self._get_project_tasks,
            'get_project_meetings': self._get_project_meetings,
            'get_project_issues': self._get_project_issues,
            
        })
        self.acc_ids = []
        self.read_data = []

    def get_children(self, ids):
        read_data = self.pool.get('project.project').read(self.cr, self.uid, ids,['id','project_child_complete_ids','complete_wbs_code','complete_wbs_name','class', 'date_start','date','state'])
        for data in read_data:
            if (data['id'] not in self.acc_ids):
                self.acc_ids.append(data['id'])
                self.read_data.append(data)
                if data['project_child_complete_ids']:
                    self.get_children(data['project_child_complete_ids'])
        return True


    def _get_project_structure(self):
        self.read_data = []
        self.acc_ids = []
        self.get_children(self.ids)
        
        self.read_data.sort(key=operator.itemgetter('complete_wbs_code'))

        return self.read_data
    


    def _get_project_milestones(self, project_id):
        
        tsk_ids = self.pool.get('project.task').search(self.cr, self.uid, [('project_id', '=', project_id),('milestone','=',True)])
        read_data = self.pool.get('project.task').read(self.cr, self.uid, tsk_ids,['name','date_late_finish','state'])
        
        
        
        results_data = []
        
        if read_data:
            for data_i in read_data:
                results = {}
                results['name'] = data_i['name']
                results['state']= data_i['state']
                results['date_late_finish'] = data_i['date_late_finish']
                
                if data_i['date_late_finish']:         
                    if ( ( data_i['state'] in ('draft','ready') ) and ( datetime.strptime(data_i['date_late_finish'],"%Y-%m-%d %H:%M:%S") < datetime.today() ) or
                        ( data_i['state'] in ('draft','ready','pending','open') ) and ( datetime.strptime(data_i['date_late_finish'],"%Y-%m-%d %H:%M:%S") < datetime.today() ) ):  
                        results['overdue'] = "X"
                        
                
                results_data.append(results)
        else:
            results = {}
            results['name'] = '-'
            results['state']= '-'
            results['date_late_finish'] = '-'
            results['overdue'] = '-' 
            results_data.append(results)
        
        results_data.sort(key=operator.itemgetter('date_late_finish'))
    
        return results_data

    def _get_project_tasks(self, project_id):
        
        tsk_ids = self.pool.get('project.task').search(self.cr, self.uid, [('project_id', '=', project_id),('milestone','=',False)])
        read_data = self.pool.get('project.task').read(self.cr, self.uid, tsk_ids,
                                                       ['name',
                                                        'duration',
                                                        'user_id',
                                                        'date_early_start',
                                                        'date_late_finish',
                                                        'state'])

        
        results_data = []
        if read_data:
            for data_i in read_data:
                results = {}
                results['name'] = data_i['name']
                results['duration'] = data_i['duration']
                if data_i['user_id']:
                    results['user_id.name'] = data_i['user_id'][1]
                else:
                    results['user_id.name'] = ""
                    
                results['state']= data_i['state']
                results['date_early_start'] = data_i['date_early_start']
                
                if data_i['date_early_start']:
                    if ( ( data_i['state'] in ('draft','ready') ) and ( datetime.strptime(data_i['date_early_start'],"%Y-%m-%d %H:%M:%S") < datetime.today() ) or
                        ( data_i['state'] in ('draft','ready','pending','open') ) and ( datetime.strptime(data_i['date_late_finish'],"%Y-%m-%d %H:%M:%S") < datetime.today() ) ):  
                        results['overdue'] = "X"
                    
                
                results_data.append(results)
        else:
            results = {}
            results['name'] = '-'
            results['user_id.name'] = '-'
            results['duration'] = '-'
            results['state']= '-'
            results['date_early_start'] = '-'
            results['overdue'] = '-' 
            results_data.append(results)
                
        results_data.sort(key=operator.itemgetter('date_early_start'))
            
        return results_data

    def _get_project_meetings(self, project_id):
        
        tsk_ids = self.pool.get('calendar.event').search(self.cr, self.uid, [('project_id', '=', project_id)])
        read_data = self.pool.get('calendar.event').read(self.cr, self.uid, tsk_ids,
                                                       ['name',
                                                        'user_id',
                                                        'categ_id',
                                                        'location',
                                                        'allday',
                                                        'date',
                                                        'date_deadline',
                                                        'duration',
                                                        'state'])


        results_data = []
        if read_data:            
            for data_i in read_data:
                results = {}
                results['name'] = data_i['name']
                if data_i['user_id']:
                    results['user_id.name'] = data_i['user_id'][1]
                else:
                    results['user_id.name'] = ""
                    
                if data_i['categ_id']:
                    results['categ_id']= data_i['categ_id'][1]
                else:
                    results['categ_id']= ""
                    
                results['location']= data_i['location']
                results['allday']= data_i['allday']
                results['date']= data_i['date']
                results['duration']= data_i['duration']
                results['state']= data_i['state']
                
                if data_i['date']:
                    if ( ( data_i['state'] in ('draft') ) and ( datetime.strptime(data_i['date'],"%Y-%m-%d %H:%M:%S") < datetime.today() ) or
                        ( data_i['state'] in ('draft','open') ) and ( datetime.strptime(data_i['date_deadline'],"%Y-%m-%d %H:%M:%S") < datetime.today() ) ):  
                        results['overdue'] = "X"
                        
                
                results_data.append(results)
        else:
            results = {}
            results['name'] = '-'
            results['user_id.name'] = '-'
            results['categ_id']= '-'
            results['location']= '-'
            results['allday']= '-'
            results['date']= '-'
            results['duration']= '-'
            results['state']= '-'    
            results['overdue'] = '-' 
            results_data.append(results)
                
        results_data.sort(key=operator.itemgetter('date'))
        
        return results_data
        
    def _get_project_issues(self, project_id):
        
        tsk_ids = self.pool.get('project.issue').search(self.cr, self.uid, [('project_id', '=', project_id)])
        read_data = self.pool.get('project.issue').read(self.cr, self.uid, tsk_ids,
                                                       ['name',
                                                        'user_id',
                                                        'categ_id',
                                                        'assigned_to',
                                                        'priority',
                                                        'state'])
        

        

        results_data = []
        if read_data:
            for data_i in read_data:
                results = {}
                results['name'] = data_i['name']     
                if data_i['user_id']:       
                    results['user_id.name'] = data_i['user_id'][1]
                else:
                    results['user_id.name'] = ""
                    
                if data_i['categ_id']:
                    results['categ_id']= data_i['categ_id'][1]
                else:
                    results['categ_id']= ""
                    
                if data_i['assigned_to']:
                    results['assigned_to.name']= data_i['assigned_to'][1]
                else:
                    results['assigned_to.name']= ""
                    
                results['priority']= data_i['priority']
                results['state']= data_i['state']
                
                results_data.append(results)
        else:
            results = {}
            results['name'] = '-'
            results['user_id.name'] = '-'
            results['categ_id']= '-'
            results['assigned_to.name'] = '-'
            results['priority']= '-'
            results['state']= '-' 
            results_data.append(results)            
        return results_data  

report_sxw.report_sxw('report.project.progress',
        'project.project', 'addons/project_integration_analysis/report/project_progress.rml',
        parser=project_progress, header="internal")
