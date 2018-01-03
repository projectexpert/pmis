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
from openerp.tools.translate import _
from openerp.osv import fields, osv
from datetime import date
from datetime import datetime as dt


class project_task(osv.osv):
    _inherit = "project.task"
    _columns = {
        'resource_plan_lines': fields.one2many(
            'analytic.resource.plan.line',
            'task_id',
            "Planned resources"
        ),
        'default_resource_plan_line': fields.many2one(
            'analytic.resource.plan.line',
            'Default resource plan line',
            required=False,
            help='''
            Resource plan line associated to the
            employee assigned to the task
            ''',
            ondelete="cascade"
        ),
    }

    def _prepare_resource_plan_line(
        self, cr, uid, plan_input, context=None
    ):

        plan_output = {}
        project_obj = self.pool.get('project.project')
        employee_obj = self.pool.get('hr.employee')
        product_obj = self.pool.get('product.product')
        company_obj = self.pool.get('res.company')
        product_price_type_obj = self.pool.get('product.price.type')

        date_start = plan_input.get('date_start', False)
        date_end = plan_input.get('date_end', False)
        company_id = plan_input.get('company_id', False)
        user_id = plan_input.get('user_id', False)
        project_id = plan_input.get('project_id', False)
        planned_hours = plan_input.get('planned_hours', False)
        name = plan_input.get('name', False)

        plan_output['name'] = name

        plan_output['date'] = date.today()
        if date_start:
            dt_start = dt.strptime(date_start, "%Y-%m-%d %H:%M:%S")
            plan_output['date'] = dt_start.date()
        if date_end:
            dt_end = dt.strptime(date_end, "%Y-%m-%d %H:%M:%S")
            plan_output['date'] = dt_end.date()

        plan_output['unit_amount'] = planned_hours

        if project_id:
            project = project_obj.browse(cr, uid, project_id, context=context)
            if project.analytic_account_id:
                pacix = project.analytic_account_id
                plan_output['account_id'] = pacix.id
                plan_output['version_id'] = (
                    pacix.active_analytic_planning_version and
                    pacix.active_analytic_planning_version.id
                )

        plan_output['company_id'] = company_id
        company = company_obj.browse(
            cr, uid, company_id, context=context
        )
        plan_output['currency_id'] = (
            company.currency_id and
            company.currency_id.id or
            False
        )

        # Look for the employee that the user of the task is assigned to
        employee_ids = employee_obj.search(
            cr, uid, [('user_id', '=', user_id)]
        )
        if employee_ids:
            employee_id = employee_ids[0]
        else:
            employee_id = False

        # Obtain the product associated to the employee
        employee = employee_obj.browse(cr, uid, employee_id, context=context)
        if employee.product_id:
            plan_output['product_id'] = employee.product_id.id
            # Obtain the default uom of the product
            plan_output['product_uom_id'] = (
                employee.product_id.uom_id and
                employee.product_id.uom_id.id or
                False
            )

            prod = product_obj.browse(
                cr, uid, employee.product_id.id, context=context
            )
            general_account_id = (
                prod.product_tmpl_id.property_account_expense.id
            )
            pcpaecx = prod.categ_id.property_account_expense_categ
            if not general_account_id:
                general_account_id = pcpaecx.id
            if not general_account_id:
                raise osv.except_osv(
                    _('Error !'),
                    _('There is no expense account defined '
                      'for this product: "%s" (id:%d)')
                    % (prod.name, prod.id,))

            plan_output['general_account_id'] = general_account_id
            plan_output['journal_id'] = (
                prod.expense_analytic_plan_journal_id and
                prod.expense_analytic_plan_journal_id.id or
                False
            )

            product_price_type_ids = product_price_type_obj.search(
                cr,
                uid,
                [('field', '=', 'standard_price')],
                context=context
            )
            pricetype = product_price_type_obj.browse(
                cr, uid, product_price_type_ids, context=context)[0]
            price_unit = prod.price_get(
                pricetype.field, context=context)[prod.id]
            prec = self.pool.get('decimal.precision').precision_get(
                cr, uid, 'Account'
            )
            amount = price_unit * planned_hours or 1.0
            result = round(amount, prec)
            plan_output['price_unit'] = price_unit
            # plan_output['amount_currency'] = -1 * result
            # plan_output['amount'] = plan_output['amount_currency']
            plan_output['amount'] = -1 * result

        return plan_output

    def create(self, cr, uid, vals, *args, **kwargs):
        context = kwargs.get('context', {})
        task = super(project_task, self).create(
            cr, uid, vals, *args, **kwargs
        )
        new_vals = {}
        resource_plan_line_obj = self.pool.get(
            'analytic.resource.plan.line'
        )
        stage_obj = self.pool.get('project.task.type')
        if 'stage_id' in vals:
            if vals['stage_id']:
                stage = stage_obj.browse(cr, uid, vals['stage_id'])
                state = stage.state
            else:
                state = False

        if not state and state != 'cancelled':
            if 'planned_hours' in vals and vals['planned_hours']:
                if 'user_id' in vals and vals['user_id']:
                    if 'project_id' in vals and vals['project_id']:
                        if ('delegated_user_id' not in vals) or (
                                'delegated_user_id' in
                                vals and not
                                vals['delegated_user_id']
                        ):
                            plan_output = self._prepare_resource_plan_line(
                                cr, uid, vals, context=context
                            )
                            plan_output['task_id'] = task
                            new_plan_line_id = (
                                resource_plan_line_obj.create(
                                    cr, uid, vals=plan_output,
                                    context=context
                                )
                            )

                            new_vals['default_resource_plan_line'] = (
                                new_plan_line_id
                            )
                            self.write(
                                cr, uid, [task], new_vals, context=context
                            )
        return task

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        resource_plan_line_obj = self.pool.get('analytic.resource.plan.line')
        stage_obj = self.pool.get('project.task.type')

        if isinstance(ids, (long, int)):
            ids = [ids]

        if (
            'stage_id' in vals or
                'planned_hours' in vals or
                'user_id' in vals or
                'delegated_user_id' in vals or
                'project_id' in vals or
                'default_resource_plan_line' in vals
        ):

            for t in self.browse(cr, uid, ids, context=context):
                plan_input = {}

                if 'stage_id' in vals:
                    plan_input['stage_id'] = vals['stage_id']
                else:
                    plan_input['stage_id'] = t.stage_id

                if 'planned_hours' in vals:
                    plan_input['planned_hours'] = vals['planned_hours']
                else:
                    plan_input['planned_hours'] = t.planned_hours

                if 'user_id' in vals:
                    plan_input['user_id'] = vals['user_id']
                else:
                    plan_input['user_id'] = t.user_id and t.user_id.id or False

                if 'delegated_user_id' in vals:
                    plan_input['delegated_user_id'] = vals['delegated_user_id']
                else:
                    plan_input['delegated_user_id'] = (
                        t.delegated_user_id and
                        t.delegated_user_id.id or
                        False
                    )

                if 'name' in vals:
                    plan_input['name'] = vals['name']
                else:
                    plan_input['name'] = t.name

                if 'date_start' in vals:
                    plan_input['date_start'] = vals['date_start']
                elif t.date_start:
                    plan_input['date_start'] = t.date_start

                if 'date_end' in vals:
                    plan_input['date_end'] = vals['date_end']
                elif t.date_end:
                    plan_input['date_end'] = t.date_end

                if 'project_id' in vals:
                    plan_input['project_id'] = vals['project_id']
                else:
                    plan_input['project_id'] = (
                        t.project_id and
                        t.project_id.id or
                        False
                    )

                if 'company_id' in vals:
                    plan_input['company_id'] = vals['company_id']
                else:
                    plan_input['company_id'] = (
                        t.company_id and
                        t.company_id.id or
                        False
                    )

                if 'default_resource_plan_line' in vals:
                    plan_input['default_resource_plan_line'] = vals[
                        'default_resource_plan_line']
                else:
                    plan_input['default_resource_plan_line'] = (
                        t.default_resource_plan_line and
                        t.default_resource_plan_line.id or
                        False
                    )

                stage = stage_obj.browse(cr, uid, plan_input['stage_id'])
                state = stage.state

                if state != (
                    'cancelled' and
                    plan_input['planned_hours'] > 0.0 and
                    plan_input['user_id'] and not
                    plan_input['delegated_user_id'] and
                    plan_input['project_id']
                ):
                    # Add or update the resource plan line
                    plan_output = self._prepare_resource_plan_line(
                        cr, uid, plan_input, context=context
                    )
                    plan_output['task_id'] = t.id
                    if plan_input['default_resource_plan_line']:

                        res = super(project_task, self).write(
                            cr, uid, ids, vals, context=context
                        )

                        resource_plan_line_obj.write(
                            cr, uid,
                            [plan_input[
                                'default_resource_plan_line']
                             ],
                            plan_output, context
                        )
                        return res

                    else:
                        new_resource_plan_line_id = (
                            resource_plan_line_obj.create(
                                cr, uid, plan_output, context=context
                            )
                        )
                        vals['default_resource_plan_line'] = (
                            new_resource_plan_line_id
                        )
                        return super(project_task, self).write(
                            cr, uid, ids, vals, context=context
                        )

                else:
                    # Remove the resource plan line
                    if t.default_resource_plan_line:
                        resource_plan_line_obj.unlink(
                            cr, uid,
                            [t.default_resource_plan_line.id],
                            context
                        )

        return super(project_task, self).write(
            cr, uid, ids, vals, context=context
        )

    def map_resource_plan_lines(
        self, cr, uid, old_task_id, new_task_id, context=None
    ):
        """ copy and map tasks from old to new project """
        if context is None:
            context = {}
        map_resource_plan_line_id = {}
        default = {}
        resource_plan_line_obj = self.pool.get('analytic.resource.plan.line')

        task = self.browse(cr, uid, old_task_id, context=context)
        new_task = self.browse(cr, uid, new_task_id, context=context)
        default['account_id'] = (
            new_task.project_id and
            new_task.project_id.analytic_account_id and
            new_task.project_id.analytic_account_id.id or
            False
        )

        default['task_id'] = new_task.id
        task_vals = {}
        for resource_plan_line in task.resource_plan_lines:
                new_resource_plan_line = resource_plan_line_obj.copy(
                    cr, uid, resource_plan_line.id, default, context=context
                )
                if new_resource_plan_line:
                    map_resource_plan_line_id[resource_plan_line.id] = (
                        new_resource_plan_line
                    )

                default_resource_plan_line = (
                    task.default_resource_plan_line and
                    task.default_resource_plan_line.id or
                    False
                )
                if resource_plan_line.id == default_resource_plan_line:
                    task_vals['default_resource_plan_line'] = (
                        new_resource_plan_line
                    )
        if map_resource_plan_line_id:
            task_vals['resource_plan_lines'] = [
                (6, 0, map_resource_plan_line_id.values())
            ]

        if task_vals:
            self.write(cr, uid, [new_task_id], task_vals, context=context)

        return True

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}

        default['default_resource_plan_line'] = False
        default['resource_plan_lines'] = []
        res = super(project_task, self).copy(cr, uid, id, default, context)
        self.map_resource_plan_lines(cr, uid, id, res, context)
        return res

project_task()
