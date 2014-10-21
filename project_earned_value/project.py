# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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

from datetime import datetime, date
from datetime import datetime as dt
from dateutil.rrule import *
from osv import fields, osv


class project(osv.osv):
    
    _inherit = "project.project"

    def update_project_evm(self, cr, uid, project_ids,
                           progress_measurement_type_id, product_uom_id, context=None):

        project_obj = self.pool.get('project.project')
        project_evm_obj = self.pool.get('project.evm')
        progress_measurement_type_obj = self.pool.get('progress.measurement.type')

        progress_measurement_type = progress_measurement_type_obj.browse(cr, uid,
                                                                         progress_measurement_type_id,
                                                                         context=context)
        progress_max_value = progress_measurement_type.default_max_value

        for project_id in project_ids:

            #Delete current project.evm records
            project_evm_ids = project_evm_obj.search(cr, uid,
                                                     [('project_id', '=', project_id)],
                                                     context=context)
            project_evm_obj.unlink(cr, uid, project_evm_ids, context=context)            

            #Obtain all child projects
            projects_data = project_obj._get_project_analytic_wbs(cr, uid, [project_id], context=context)
            project_ids = projects_data.keys()
            analytic_account_ids = projects_data.values()

            #Get the earliest and latest dates for the progress measurements
            cr.execute('SELECT min(PPM.communication_date), max(PPM.communication_date) '
                       'FROM project_progress_measurement as PPM '
                       'WHERE PPM.project_id IN %s '
                       'AND PPM.progress_measurement_type = %s',
                       (tuple(project_ids), progress_measurement_type_id))

            res_min_max = cr.fetchone()
            min_date_start = max_date_end = False

            if res_min_max:
                min_date_start = res_min_max[0] or False
                max_date_end = res_min_max[1] or False
            if min_date_start is False:
                date_start = date.today() 
            else:
                date_start = dt.strptime(min_date_start, "%Y-%m-%d").date()

            if max_date_end is False:
                date_end = datetime.today()                 
            else:
                date_end = dt.strptime(max_date_end, "%Y-%m-%d").date()

            l_days = list(rrule(DAILY, dtstart=date_start, until=date_end))
            
            #Earned Value
            ev_quantity_projects = {}
            ev_amount_projects = {}

            #Compute the Budget at Completion
            cr.execute('SELECT sum(LP.unit_amount) '
                       'FROM account_analytic_line_plan AS LP '
                       'INNER JOIN account_analytic_account AS AA '
                       'ON LP.version_id = AA.active_analytic_planning_version '
                       'AND LP.account_id = AA.id '
                       'WHERE LP.account_id IN %s '
                       'AND LP.product_uom_id = %s'
                       'AND LP.amount < 0',
                       (tuple(analytic_account_ids), product_uom_id))
            bac_quantity = cr.fetchone()[0] or 0.0
            cr.execute('SELECT abs(sum(LP.amount)) '
                       'FROM account_analytic_line_plan AS LP '
                       'INNER JOIN account_analytic_account AS AA '
                       'ON LP.version_id = AA.active_analytic_planning_version '
                       'AND LP.account_id = AA.id '
                       'WHERE LP.account_id IN %s '
                       'AND LP.amount < 0',
                       (tuple(analytic_account_ids),))
            bac_amount = cr.fetchone()[0] or 0.0

            projects_total_quantity = {}
            projects_total_amount = {}
            for projects_data_project_id, projects_data_analytic_account_id in projects_data.items():
                #Total quantity
                cr.execute('SELECT ABS(SUM(LP.unit_amount)) '
                           'FROM account_analytic_line_plan AS LP '
                           'INNER JOIN account_analytic_account AS AA '
                           'ON LP.version_id = AA.active_analytic_planning_version '
                           'AND LP.account_id = AA.id '
                           'WHERE LP.account_id = %s '                           
                           'AND LP.product_uom_id = %s'
                           'AND LP.amount < 0',
                           (projects_data_analytic_account_id, product_uom_id))
                projects_total_quantity[projects_data_project_id] = cr.fetchone()[0] or 0.0

                #Total amount
                cr.execute('SELECT ABS(SUM(LP.amount)) '
                           'FROM account_analytic_line_plan AS LP '
                           'INNER JOIN account_analytic_account AS AA '
                           'ON LP.version_id = AA.active_analytic_planning_version '
                           'AND LP.account_id = AA.id '
                           'WHERE LP.account_id = %s '
                           'AND LP.amount < 0',
                           (projects_data_analytic_account_id,))
                projects_total_amount[projects_data_project_id] = cr.fetchone()[0] or 0.0

            for day_datetime in l_days:

                day_date = day_datetime.date()

                #Total actual cost
                cr.execute('SELECT sum(unit_amount) '
                           'FROM account_analytic_line '
                           'WHERE account_id IN %s '
                           'AND date <= %s '
                           'AND product_uom_id = %s'
                           'AND amount < 0',
                           (tuple(analytic_account_ids), day_date, product_uom_id))
                value = cr.fetchone()[0] or 0.0
                ac_quantity = value
                cr.execute('SELECT abs(sum(amount)) '
                           'FROM account_analytic_line '
                           'WHERE account_id IN %s '
                           'AND amount < 0'
                           'AND date <= %s ', (tuple(analytic_account_ids), day_date))
                value = cr.fetchone()[0] or 0.0
                ac_amount = value
                
                #Total planned cost
                cr.execute('SELECT sum(LP.unit_amount) '
                           'FROM account_analytic_line_plan AS LP '
                           'INNER JOIN account_analytic_account AS AA '
                           'ON LP.version_id = AA.active_analytic_planning_version '
                           'AND LP.account_id = AA.id '
                           'WHERE LP.account_id IN %s '
                           'AND LP.date <= %s '
                           'AND LP.product_uom_id = %s'
                           'AND LP.amount < 0',
                           (tuple(analytic_account_ids), day_date, product_uom_id))
                value = cr.fetchone()[0] or 0.0
                pv_quantity = value
                cr.execute('SELECT abs(sum(LP.amount)) '
                           'FROM account_analytic_line_plan AS LP '
                           'INNER JOIN account_analytic_account AS AA '
                           'ON LP.version_id = AA.active_analytic_planning_version '
                           'AND LP.account_id = AA.id '
                           'WHERE LP.account_id IN %s '
                           'AND LP.date <= %s '
                           'AND LP.amount < 0',
                           (tuple(analytic_account_ids), day_date))
                value = cr.fetchone()[0] or 0.0                  
                pv_amount = value
            
                #Record the earned value as a function of the progress measurements
                #Current progress
                cr.execute('SELECT project_id, value '
                           'FROM project_progress_measurement '
                           'WHERE project_id IN %s '
                           'AND communication_date = %s '
                           'AND progress_measurement_type = %s',
                           (tuple(project_ids), day_date, progress_measurement_type_id))

                res_project_measurements = cr.fetchall()
                progress_measurements_at_date = {}
                for res_project_measurement in res_project_measurements:
                    progress_measurements_at_date[res_project_measurement[0]] = res_project_measurement[1]

                ev_quantity = 0
                ev_amount = 0

                for projects_data_project_id, projects_data_analytic_account_id in projects_data.items():
                    #If we identify a progress measurement on this date, record new earned value
                    # Otherwise will maintain the previous value
                    if projects_data_project_id in progress_measurements_at_date:
                        #If the project is completed on this date, then record earned value
                        # as a function of the progress.
                        progress_value = progress_measurements_at_date[projects_data_project_id]
                        if projects_data_project_id in projects_total_quantity:
                            ev_quantity_projects[projects_data_project_id] = \
                                projects_total_quantity[projects_data_project_id] * \
                                progress_value / \
                                progress_max_value
                        if projects_data_project_id in projects_total_amount:
                            ev_amount_projects[projects_data_project_id] = \
                                projects_total_amount[projects_data_project_id] * \
                                progress_value / \
                                progress_max_value

                for projects_data_project_id, projects_data_analytic_account_id in projects_data.items():
                    if projects_data_project_id in ev_quantity_projects.keys():
                        ev_quantity += ev_quantity_projects[projects_data_project_id]
                    if projects_data_project_id in ev_amount_projects.keys():
                        ev_amount += ev_amount_projects[projects_data_project_id]

                #CC: %Cost complete
                if pv_amount == 0:
                    pcc_amount = 0
                else:
                    pcc_amount = ac_amount / pv_amount 
                                                                  
                #SV: Calculate schedule variance
                sv_quantity = ev_quantity - pv_quantity
                sv_amount = ev_amount - pv_amount
                
                #SVP: Calculate schedule variance in percentage
                if pv_quantity == 0:
                    svp_quantity = 0                    
                else:    
                    svp_quantity = sv_quantity / pv_quantity
                
                if pv_amount == 0:
                    svp_amount = 0
                else:
                    svp_amount = sv_amount / pv_amount
                
                #SPI: Calculate the Schedule Performance Index
                if pv_quantity == 0:
                    spi_quantity = 0
                else:
                    spi_quantity = ev_quantity / pv_quantity
                
                if ev_quantity == 0:
                    spi_amount = 0
                else:
                    spi_amount = ev_amount / ev_quantity
                
                #CV: Cost Variance
                cv_quantity = ev_quantity - ac_quantity
                cv_amount = ev_amount - ac_amount
                
                #CVP: Cost variance percentage
                if ev_quantity == 0:
                    cvp_quantity = 0
                else:
                    cvp_quantity = cv_quantity / ev_quantity
                
                if ev_amount == 0:
                    cvp_amount = 0
                else:
                    cvp_amount = cv_amount / ev_amount
                                                
                #CPI: Cost Performance Index
                if ac_quantity == 0:
                    cpi_quantity = 1
                else:
                    cpi_quantity = ev_quantity / ac_quantity
                
                if ac_amount == 0:
                    cpi_amount = 1
                else:
                    cpi_amount = ev_amount / ac_amount
            
                #TCPI: To-complete Performance Index
                bac_ac_quantity = bac_quantity - ac_quantity
                if bac_ac_quantity == 0:
                    tcpi_quantity = 1
                else:
                    tcpi_quantity = (bac_quantity - ev_quantity)/bac_ac_quantity

                bac_ac_amount = bac_amount - ac_amount
                if bac_ac_amount == 0:
                    tcpi_amount = 1
                else:
                    tcpi_amount = (bac_amount - ev_amount)/bac_ac_amount
                
                #EAC: Estimate at completion
                if cpi_quantity == 0:
                    eac_quantity = bac_quantity
                else:
                    eac_quantity = bac_quantity / cpi_quantity
                
                if cpi_amount == 0:
                    eac_amount = bac_amount
                else:
                    eac_amount = bac_amount / cpi_amount
                
                #VAC: Variance at Completion
                vac_quantity = bac_quantity - eac_quantity
                vac_amount = bac_amount - eac_amount
                
                #VACP: Variance at Completion Percent
                if bac_quantity == 0:
                    vacp_quantity = 0
                else:
                    vacp_quantity = vac_quantity / bac_quantity

                if bac_amount == 0:
                    vacp_amount = 0
                else:
                    vacp_amount = vac_amount / bac_amount
                
                #ETC: Estimate To Complete
                if cpi_quantity == 0:
                    etc_quantity = bac_quantity
                else:
                    etc_quantity = (bac_quantity - ev_quantity)/cpi_quantity

                if cpi_amount == 0:
                    etc_amount = 0
                else:
                    etc_amount = (bac_amount - ev_amount)/cpi_amount
                
                #EAC: Estimate At Completion
                if cpi_quantity == 0:
                    eac_quantity = 0
                else:
                    eac_quantity = bac_quantity/cpi_quantity

                if cpi_amount == 0:
                    eac_amount = 0
                else:
                    eac_amount = bac_amount/cpi_amount

                #Create the EVM records
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'PV', pv_quantity, pv_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'EV', ev_quantity, ev_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'AC', ac_quantity, ac_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'BAC', bac_quantity, bac_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'CV', cv_quantity, cv_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'CVP', cvp_quantity, cvp_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'SV', sv_quantity, sv_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'SVP', svp_quantity, svp_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'SPI', spi_quantity, spi_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'CPI', cpi_quantity, cpi_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'TCPI', tcpi_quantity, tcpi_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'EAC', eac_quantity, eac_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'VAC', vac_quantity, vac_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'VACP', vacp_quantity, vacp_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'ETC', etc_quantity, etc_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'EAC', eac_quantity, eac_amount)
                project_obj.create_evm_record(cr, uid, project_id, day_date, 'PCC', 0, pcc_amount)
    
    def create_evm_record(self, cr, uid, project_id,  eval_date, kpi_type, kpi_quantity, kpi_amount, context=None):
        
        project_evm_obj = self.pool.get('project.evm')
        
        vals_lines = {'name': '',
                      'date': eval_date,
                      'eval_date': eval_date,
                      'kpi_type': kpi_type,
                      'project_id': project_id,
                      'kpi_amount': kpi_amount,
                      'kpi_quantity': kpi_quantity,
                      }
        
        project_evm_obj.create(cr, uid, vals_lines)                      

project()