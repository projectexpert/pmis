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
from openerp.osv import osv


class project(osv.osv):
    _inherit = "project.project"

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}

        task_obj = self.pool.get('project.task')
        resource_plan_line_obj = self.pool.get('analytic.resource.plan.line')

        if isinstance(ids, (long, int)):
            ids = [ids]

        if 'tasks' in vals:
            if vals['tasks'] and vals['tasks'][0] and vals['tasks'][0][2]:
                resource_vals = {}
                for p in self.browse(cr, uid, ids, context=context):
                    for task_id in vals['tasks'][0][2]:
                        task = task_obj.browse(
                            cr, uid, task_id, context=context
                        )
                        for resource_plan_line in task.resource_plan_lines:
                            resource_vals['account_id'] = (
                                p.analytic_account_id and
                                p.analytic_account_id.id or
                                False
                            )
                            resource_plan_line_obj.write(
                                cr, uid,
                                resource_plan_line.id,
                                resource_vals,
                                context=context
                            )

        return super(project, self).write(cr, uid, ids, vals, context=context)

project()
