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


class analytic_resource_plan_line(osv.osv):

    _inherit = 'analytic.resource.plan.line'

    _columns = {
        'task_id': fields.many2one(
            'project.task',
            'Task',
            required=False,
            ondelete='cascade'
        ),
    }

    def on_change_task_id_resource(
        self,
        cr,
        uid,
        ids,
        account_id,
        task_id,
        name,
        date,
        supplier_id,
        pricelist_id,
        product_id,
        unit_amount,
        product_uom_id,
        price_unit,
        # amount_currency,
        currency_id,
        version_id,
        journal_id,
        ref,
        company_id,
        amount,
        general_account_id,
        context=None
    ):

            res = {}
            res['value'] = {}
            # Change in task_id affects:
            #  - account_id

            task_obj = self.pool.get('project.task')

            if task_id:
                task = task_obj.browse(cr, uid, task_id, context=context)
                account_id = (
                    task.project_id and
                    task.project_id.analytic_account_id and
                    task.project_id.analytic_account_id.id or
                    False
                )
                if account_id:
                    res['value'].update({'account_id': account_id})
                    res_account_id = self._on_change_account_id_resource(
                        cr,
                        uid,
                        ids,
                        account_id,
                        name,
                        date,
                        supplier_id,
                        pricelist_id,
                        product_id,
                        unit_amount,
                        product_uom_id,
                        price_unit,
                        # amount_currency,
                        currency_id,
                        version_id,
                        journal_id,
                        ref,
                        company_id,
                        amount,
                        general_account_id,
                        context=None
                    )
                    if res_account_id:
                        res['value'].update(res_account_id)

            if res['value']:
                return res
            else:
                return {}

    def create(
        self, cr, uid, vals, *args, **kwargs
    ):
        context = kwargs.get('context', {})
        task_obj = self.pool.get('project.task')

        if 'task_id' in vals and vals['task_id']:
            task = task_obj.browse(cr, uid, vals['task_id'], context=context)
            vals['account_id'] = (
                task.project_id and
                task.project_id.analytic_account_id and
                task.project_id.analytic_account_id.id or
                False
            )
        return super(analytic_resource_plan_line, self).create(
            cr, uid, vals, *args, **kwargs
        )

    def write(
        self, cr, uid, ids, vals, context=None
    ):
        if context is None:
            context = {}

        if isinstance(ids, (long, int)):
            ids = [ids]
        for p in self.browse(cr, uid, ids, context=context):

            if 'task_id' in vals:
                task_id = vals['task_id']
            else:
                task_id = p.task_id and p.task_id.id or False

            if task_id:
                task_obj = self.pool.get('project.task')
                task = task_obj.browse(cr, uid, task_id, context=context)

                if 'unit_amount' in vals:
                    if (
                        task.default_resource_plan_line and
                        task.default_resource_plan_line.id
                    ) == p.id:
                        if task.planned_hours != vals['unit_amount']:
                            raise osv.except_osv(
                                _('Error !'),
                                _('The quantity is different to the number of '
                                  'planned hours in the associated task.')
                            )

        return super(analytic_resource_plan_line, self).write(
            cr, uid, ids, vals, context=context
        )

analytic_resource_plan_line()
