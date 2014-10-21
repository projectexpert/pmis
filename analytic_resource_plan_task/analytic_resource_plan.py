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

from tools.translate import _
from openerp.osv import fields, osv


class analytic_resource_plan_line(osv.osv):

    _inherit = 'analytic.resource.plan.line'

    def _check_task_project(self, cr, uid, ids):
        for line in self.browse(cr, uid, ids):
            if line.task_id and line.task_id.project_id and line.account_id:
                task_account_id = line.task_id.project_id \
                                  and line.task_id.project_id.analytic_account_id \
                                  and line.task_id.project_id.analytic_account_id.id or False

                if task_account_id != line.account_id.id:
                    return False
        return True

    _columns = {
        'task_id': fields.many2one('project.task', 'Task', required=False, ondelete='cascade'),
    }

    _constraints = [
        (_check_task_project, _('Error! Task must belong to the project.'),
         ['task_id', 'account_id']),
    ]

    def on_change_task_id_resource(self,
                                      cr, uid, ids, account_id,
                                      task_id, name, date, supplier_id,
                                      pricelist_id, product_id, unit_amount,
                                      product_uom_id, price_unit, amount_currency,
                                      currency_id, version_id, journal_id,
                                      ref, company_id, amount, general_account_id, context=None):
        res = {}
        res['value'] = {}
        #Change in task_id affects:
        #  - account_id

        task_obj = self.pool.get('project.task')

        if task_id:
            task = task_obj.browse(cr, uid, task_id, context=context)
            account_id = task.project_id and task.project_id.analytic_account_id and task.project_id.analytic_account_id.id or False
            if account_id:
                res['value'].update({'account_id': account_id})
                res_account_id = self._on_change_account_id_resource(cr, uid, ids, account_id,
                                                                     name, date, supplier_id,
                                                                     pricelist_id, product_id, unit_amount,
                                                                     product_uom_id, price_unit, amount_currency,
                                                                     currency_id, version_id, journal_id,
                                                                     ref, company_id, amount, general_account_id, context=None)
                if res_account_id:
                    res['value'].update(res_account_id)

        if res['value']:
            return res
        else:
            return {}

analytic_resource_plan_line()
