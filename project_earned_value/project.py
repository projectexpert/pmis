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
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
import time


class project(osv.osv):

    _inherit = "project.project"

    @staticmethod
    def _total_plan_cost(cr, ids):

        cr.execute(
            'SELECT abs(sum(LP.amount)) '
            'FROM account_analytic_line_plan AS LP '
            'INNER JOIN account_analytic_account AS AA '
            'ON LP.version_id = AA.active_analytic_planning_version '
            'AND LP.account_id = AA.id '
            'WHERE LP.account_id IN %s '
            'AND LP.amount < 0',
            (tuple(ids),)
        )
        cr_result = cr.fetchone()
        return cr_result and cr_result[0] or 0.0

    @staticmethod
    def _total_actual_cost_to_date(cr, ids, to_date):

        cr.execute(
            'SELECT abs(sum(amount)) '
            'FROM account_analytic_line '
            'WHERE account_id IN %s '
            'AND amount < 0'
            'AND date <= %s ',
            (tuple(ids), to_date)
        )
        cr_result = cr.fetchone()
        return cr_result and cr_result[0] or 0.0

    @staticmethod
    def _total_plan_cost_to_date(cr, ids, to_date):

        # The planned cost to date is a linear interpolation of the planned cost from start date to end date
        plan_cost_to_date = 0

        cr.execute(
            '''
SELECT LP.account_id as account_id,
abs(sum(LP.amount)) as total_plan_cost,
sum(cast(to_char(date_trunc('day',AA.date) - date_trunc('day',AA.date_start),'DD') as int) +1 ) as no_of_days_total,
sum(cast(to_char(date_trunc('day',date(%s)) - date_trunc('day',AA.date_start),'DD') as int) + 1) as no_of_days_to_date
FROM account_analytic_line_plan AS LP
INNER JOIN account_analytic_account AS AA
ON LP.version_id = AA.active_analytic_planning_version
AND LP.account_id = AA.id
WHERE LP.account_id IN %s
AND LP.amount < 0
GROUP BY LP.id
    ''',
            (to_date, tuple(ids))
        )
        for account_id, total_plan_cost, no_of_days_total, no_of_days_to_date in cr.fetchall():
            if no_of_days_total and no_of_days_to_date:
                plan_cost_to_date += total_plan_cost * no_of_days_to_date / no_of_days_total
        return plan_cost_to_date

    @staticmethod
    def _get_evm_ratios(ac, pv, ev, bac):

        res = {
            'ac': ac,
            'pv': pv,
            'ev': ev,
            'bac': bac,
        }

        # PCC: Costs to date / Total costs
        try:
            res['pcc'] = res['ac'] / res['pv']
        except ZeroDivisionError:
            res['pcc'] = 0

        # SV: Schedule variance
        res['sv'] = res['ev'] - res['pv']

        # SVP: Schedule variance in percentage
        try:
            res['svp'] = res['sv'] / res['pv']
        except ZeroDivisionError:
            res['svp'] = 0

        # SPI: Schedule Performance Index
        try:
            res['spi'] = res['ev'] / res['pv']
        except ZeroDivisionError:
            res['spi'] = 0

        # CV: Cost Variance
        res['cv'] = res['ev'] - res['ac']

        # CVP: Cost Variance Percent
        try:
            res['cvp'] = (res['cv'] / res['ev']) * 100
        except ZeroDivisionError:
            res['cvp'] = 0

        # CPI: Cost Performance Index
        try:
            res['cpi'] = res['ev'] / res['ac']
        except ZeroDivisionError:
            res['cpi'] = 1

        # TCPI: To-complete Performance Index
        bac_ac_amount = res['bac'] - res['ac']
        try:
            res['tcpi'] = (res['bac'] - res['ev']) / bac_ac_amount
        except ZeroDivisionError:
            res['tcpi'] = 1

        # EAC: Estimate at completion
        try:
            res['eac'] = res['bac'] / res['cpi']
        except ZeroDivisionError:
            res['eac'] = res['bac']

        # VAC: Variance at Completion
        res['vac'] = res['bac'] - res['eac']

        # VACP: Variance at Completion Percent
        try:
            res['vacp'] = (res['vac'] / res['bac']) * 100
        except ZeroDivisionError:
            res['vacp'] = 0

        # ETC: Estimate To Complete
        try:
            res['etc'] = (res['bac'] - res['ev'])/res['cpi']
        except ZeroDivisionError:
            res['etc'] = 0

        # EAC: Estimate At Completion
        try:
            res['eac'] = res['bac']/res['cpi']
        except ZeroDivisionError:
            res['eac'] = 0

        # POC - Percent of Completion
        try:
            res['poc'] = res['ev'] / res['bac'] * 100
        except ZeroDivisionError:
            res['poc'] = 0

        return res

    def _earned_value(self, cr, uid, ids, names, arg, context=None):

        res = {}
        if context is None:
            context = {}

        measurement_type_obj = self.pool.get('progress.measurement.type')
        project_obj = self.pool.get('project.project')
        def_meas_type_ids = measurement_type_obj.search(cr, uid, [('is_default', '=', True)], context=context)

        if def_meas_type_ids:
            progress_measurement_type = measurement_type_obj.browse(cr, uid,
                                                                    def_meas_type_ids[0],
                                                                    context=context)
            progress_max_value = progress_measurement_type.default_max_value
        else:
            progress_measurement_type = False
            progress_max_value = 0

        # Search for child projects
        for project_id in ids:
            res[project_id] = {
                'pv': 0,
                'ev': 0,
                'ac': 0,
                'cv': 0,
                'cvp': 0,
                'cpi': 0,
                'tcpi': 0,
                'sv': 0,
                'svp': 0,
                'spi': 0,
                'eac': 0,
                'etc': 0,
                'vac': 0,
                'vacp': 0,
                'bac': 0,
                'pcc': 0,
                'poc': 0,
            }
            if def_meas_type_ids:
                date_today = time.strftime('%Y-%m-%d')
                wbs_projects_data = project_obj._get_project_analytic_wbs(cr, uid, [project_id], context=context)
                # Compute the Budget at Completion
                total_bac = self._total_plan_cost(cr, wbs_projects_data.values())
                pv = self._total_plan_cost_to_date(cr, wbs_projects_data.values(), date_today)
                ac = self._total_actual_cost_to_date(cr, wbs_projects_data.values(), date_today)
                ev = 0

                if total_bac > 0:
                    for wbs_project_id in wbs_projects_data.keys():
                        # Compute the Budget at Completion
                        bac = self._total_plan_cost(cr, [wbs_projects_data[wbs_project_id]])

                        # Obtain the latest progress measurement for this project
                        cr.execute('SELECT DISTINCT ON (a.project_id) value '
                                   'FROM project_progress_measurement AS a '
                                   'WHERE a.project_id IN %s '
                                   'AND a.progress_measurement_type = %s '
                                   'AND a.communication_date <= %s '
                                   'ORDER BY a.project_id, a.communication_date DESC ',
                                   (tuple([wbs_project_id]), def_meas_type_ids[0], date_today))
                        cr_result = cr.fetchone()
                        measurement_value = cr_result and cr_result[0] or 0.0

                        ev += bac * measurement_value / progress_max_value

                res[project_id].update(self._get_evm_ratios(ac, pv, ev, total_bac))

        return res

    _columns = {
        'pv': fields.function(_earned_value, method=True, multi=_earned_value,
                              string='PV', type='float',
                              digits_compute=dp.get_precision('Account'),
                              help="""Planned Value (PV) or Budgeted Cost of Work Scheduled
                               is the total cost of the work scheduled/planned
                               as of a reporting date."""),
        'ev': fields.function(_earned_value, method=True, multi=_earned_value,
                              string='EV', type='float',
                              digits_compute=dp.get_precision('Account'),
                              help="""Earned Value (PV) or Budgeted Cost of Work Performed
                               is the amount of work that has been completed to date,
                               expressed as the planned value for that work."""),
        'ac': fields.function(_earned_value, method=True, multi=_earned_value,
                              string='AC', type='float',
                              digits_compute=dp.get_precision('Account'),
                              help="""Actual Cost (AC) or Actual Cost of Work Performed
                               is an indication of the level of resources that have been
                               expended to achieve the actual work performed to date."""),
        'cv': fields.function(_earned_value, method=True, multi=_earned_value,
                              string='CV', type='float',
                              digits_compute=dp.get_precision('Account'),
                              help="""Cost Variance (CV) shows whether a project is under
                              or over budget. It is determined as EV - AC.
                              A negative value indicates that the project is
                              over budget."""),
        'cvp': fields.function(_earned_value, method=True, multi=_earned_value,
                               digits_compute=dp.get_precision('Account'),
                               help="""Cost Variance % (CVP) shows whether a project is under
                               or over budget. It is determined as CV / EV.
                               A negative value indicates that the project is over budget."""),
        'cpi': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='CPI', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="""Cost Performance Index (CPI) indicates how efficiently
                               the team is using its resources. It is determined as EV / AC.
                               A value of 0.8 indicates that the project has a cost efficiency
                               that provides 0.8 worth of work for every unit spent to date."""),
        'tcpi': fields.function(_earned_value, method=True, multi=_earned_value,
                                string='TCPI', type='float',
                                digits_compute=dp.get_precision('Account'),
                                help="""To-Complete Cost Performance Index (TCPI) helps the team
                                determine the efficiency that must be achieved on the remaining work
                                for a project to meet the Budget at Completion (BAC). It is determined
                                as (BAC - EV) / (BAC - AC)"""),
        'sv': fields.function(
            _earned_value, method=True, multi=_earned_value,
            string='SV', type='float',
            digits_compute=dp.get_precision('Account'),
            help="""Schedule Variance (SV) determines whether a project is
            ahead or behind schedule. It is calculated as EV - PV.
            A negative value indicates an unfavorable condition."""
        ),
        'svp': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='SVP', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="""Schedule Variance % (SVP) determines whether a project is
                               ahead or behind schedule. It is calculated as SV / PV.
                               A negative value indicates what percent of the planned work
                               has not been accomplished"""),
        'spi': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='SPI', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="""Schedule Performance Index (SPI) indicates
                               how efficiently the project team is using its time. It is
                               calculated as EV / PV. For example, on a day, indicates
                               how many hours worth of the planned work is being performed."""),
        'eac': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='EAC', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="""Estimate at Completion (EAC) provides an estimate
                               of the final cost of the project if current performance trends
                               continue. It is calculated as BAC / CPI."""),
        'etc': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='ETC', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="""Estimate to Complete (ETC) provides an estimate
                               of what will the remaining work cost. It is calculated as
                               (BAC - EV) / CPI."""),
        'vac': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='VAC', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="""Variance at Completion (VAC) shows the team
                               whether the project will finish under or over budget.
                               It is calculated as BAC - EAC."""),
        'vacp': fields.function(_earned_value, method=True, multi=_earned_value,
                                string='VACP', type='float',
                                digits_compute=dp.get_precision('Account'),
                                help="""Variance at Completion % (VACP) shows the team
                                whether the project will finish under or over budget.
                                It is calculated as VAC / BAC."""),
        'bac': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='BAC', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="Budget at Completion (BAC)"),
        'pcc': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='PCC', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="Costs to date / Total costs"),

        'poc': fields.function(_earned_value, method=True, multi=_earned_value,
                               string='POC', type='float',
                               digits_compute=dp.get_precision('Account'),
                               help="Aggregated Percent of Completion"),

    }

    def update_project_evm(self, cr, uid, project_ids,
                           progress_measurement_type_id, context=None):

        project_obj = self.pool.get('project.project')
        project_evm_obj = self.pool.get('project.evm')
        progress_measurement_type_obj = self.pool.get('progress.measurement.type')

        progress_measurement_type = progress_measurement_type_obj.browse(cr, uid,
                                                                         progress_measurement_type_id,
                                                                         context=context)
        progress_max_value = progress_measurement_type.default_max_value

        for project_id in project_ids:

            project = project_obj.browse(cr, uid, project_id, context=context)

            # Delete current project.evm records
            project_evm_ids = project_evm_obj.search(cr, uid,
                                                     [('project_id', '=', project_id)],
                                                     context=context)
            project_evm_obj.unlink(cr, uid, project_evm_ids, context=context)

            # Obtain all child projects
            projects_data = project_obj._get_project_analytic_wbs(cr, uid, [project_id], context=context)
            wbs_project_ids = projects_data.keys()
            wbs_analytic_account_ids = projects_data.values()

            # Get the earliest and latest dates for based on the project

            if not project.date_start:
                date_start = datetime.today()
            else:
                date_start = datetime.strptime(project.date_start, "%Y-%m-%d")

            if not project.date:
                date_end = datetime.today()
            else:
                date_end = datetime.strptime(project.date, "%Y-%m-%d")

            l_days = list(rrule(DAILY, dtstart=date_start, until=date_end))

            # Earned Value
            ev_projects = {}
            bac = self._total_plan_cost(cr, wbs_analytic_account_ids)
            projects_total_amount = {}

            for projects_data_project_id, projects_data_analytic_account_id in projects_data.items():
                # Total planned_cost
                projects_total_amount[projects_data_project_id] = \
                    self._total_plan_cost(cr, [projects_data_analytic_account_id])

            records = []
            for day_datetime in l_days:

                day_date = day_datetime.date()
                ac = self._total_actual_cost_to_date(cr, wbs_analytic_account_ids, day_date)
                pv = self._total_plan_cost_to_date(cr, wbs_analytic_account_ids, day_date)

                # Record the earned value as a function of the progress measurements
                # Current progress
                cr.execute('SELECT project_id, value '
                           'FROM project_progress_measurement '
                           'WHERE project_id IN %s '
                           'AND communication_date = %s '
                           'AND progress_measurement_type = %s',
                           (tuple(wbs_project_ids), day_date, progress_measurement_type_id))

                res_project_measurements = cr.fetchall()
                progress_measurements_at_date = {}
                for res_project_measurement in res_project_measurements:
                    progress_measurements_at_date[res_project_measurement[0]] = res_project_measurement[1]

                ev = 0

                for projects_data_project_id, projects_data_analytic_account_id in projects_data.items():
                    # If we identify a progress measurement on this date, record new earned value
                    #  Otherwise will maintain the previous value
                    if projects_data_project_id in progress_measurements_at_date:
                        # If the project is completed on this date, then record earned value
                        #  as a function of the progress.
                        progress_value = progress_measurements_at_date[projects_data_project_id]
                        if projects_data_project_id in projects_total_amount:
                            ev_projects[projects_data_project_id] = \
                                projects_total_amount[projects_data_project_id] * \
                                progress_value / \
                                progress_max_value

                for projects_data_project_id, projects_data_analytic_account_id in projects_data.items():
                    if projects_data_project_id in ev_projects.keys():
                        ev += ev_projects[projects_data_project_id]

                ratios = self._get_evm_ratios(ac, pv, ev, bac)
                # Create the EVM records
                records.extend(project_obj.create_evm_record(cr, uid, project_id, day_date, ratios))

            return records

    def create_evm_record(self, cr, uid, project_id,  eval_date, ratios, context=None):
        records = []
        project_evm_obj = self.pool.get('project.evm')
        for kpi_type in ratios.keys():
            vals_lines = {'name': '',
                          'date': eval_date,
                          'eval_date': eval_date,
                          'kpi_type': kpi_type.upper(),
                          'project_id': project_id,
                          'kpi_value': ratios[kpi_type],
                          }
            records.extend([project_evm_obj.create(cr, uid, vals_lines)])

        return records

project()
