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

from openerp.osv import fields, orm
from openerp import tools


class Task(orm.Model):
    _inherit = 'project.task'

    def get_related_tasks(self, cr, uid, ids, context=None):
        result = {}
        # data = []
        # read_data = []

        tasks_br = self.browse(cr, uid, ids, context=None)

        for t in tasks_br:
            result[t.id] = True

            for child in t.child_ids:
                result[child.id] = True

        return result

    def _predecessor_ids_calc(
        self, cr, uid, ids, prop, unknow_none, unknow_dict
    ):
        if not ids:
            return []
        res = []
        data = []

        tasks_br = self.browse(cr, uid, ids, context=None)

        for t in tasks_br:
            data = []
            str_data = ""
            if t.parent_ids:
                for parent in t.parent_ids:
                    data.insert(0, str(parent.id))
            else:
                data.insert(0, '')

            data.sort(cmp=None, key=None, reverse=False)
            str_data = ', '.join(data)

            res.append((t.id, str_data))

        return dict(res)

    def _predecessor_names_calc(
        self, cr, uid, ids, prop, unknow_none, unknow_dict
    ):
        if not ids:
            return []
        res = []
        data = []

        tasks_br = self.browse(cr, uid, ids, context=None)

        for t in tasks_br:
            data = []
            str_data = ""
            if t.parent_ids:
                for parent in t.parent_ids:
                    data.insert(0, tools.ustr(parent.name))
            else:
                data.insert(0, '')

            data.sort(cmp=None, key=None, reverse=False)
            str_data = ', '.join(data)

            res.append((t.id, str_data))

        return dict(res)

    _columns = {
        'predecessor_ids_str': fields.function(
            _predecessor_ids_calc,
            method=True, type='char',
            string='Predecessor tasks',
            size=20, help='Predecessor tasks ids',
            # store={
            #     'project.task': (
            #         get_related_tasks,
            #         ['parent_ids','child_ids'], 10
            #     ),
            # }
            ),
        'predecessor_names_str': fields.function(
            _predecessor_names_calc,
            method=True, type='char',
            string='Predecessor tasks',
            size=512, help='Predecessor tasks ids',
            # store={
            #     'project.task': (
            #         get_related_tasks,
            #         ['parent_ids','child_ids'], 10
            #     ),
            # }
            ),

        }

    def do_link_predecessors(
        self, cr, uid, task_id, link_predecessors_data=None, context=None
    ):

        if link_predecessors_data is None:
            link_predecessors_data = {}
        task_br = self.browse(cr, uid, task_id, context=context)

        self.write(cr, uid, [task_br.id], {
            'parent_ids': [(6, 0, link_predecessors_data['parent_ids'])],
        })

        return True
