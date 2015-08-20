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

from openerp.osv import fields, osv
from openerp import tools


class task(osv.osv):
    _inherit = 'project.task'

    def get_related_tasks(self, cr, uid, ids, context=None):
        result = {}
        data = []
        read_data = []

        tasks_br = self.browse(cr, uid, ids, context=None)

        for t in tasks_br:
            result[t.id] = True

            for child in t.successor_ids:
                result[child.id] = True

        return result

    def _predecessor_ids_calc(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        if not ids:
            return []
        res = []
        data = []

        tasks_br = self.browse(cr, uid, ids, context=None)

        for t in tasks_br:
            data = []
            str_data = ""
            if t.predecessor_ids:
                for parent in t.predecessor_ids:
                    data.insert(0, str(parent.id))
            else:
                data.insert(0, '')

            data.sort(cmp=None, key=None, reverse=False)
            str_data = ', '.join(data)

            res.append((t.id, str_data))

        return dict(res)

    def _predecessor_names_calc(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        if not ids:
            return []
        res = []
        data = []

        tasks_br = self.browse(cr, uid, ids, context=None)

        for t in tasks_br:
            data = []
            str_data = ""
            if t.predecessor_ids:
                for parent in t.predecessor_ids:
                    data.insert(0, tools.ustr(parent.name))
            else:
                data.insert(0, '')

            data.sort(cmp=None, key=None, reverse=False)
            str_data = ', '.join(data)

            res.append((t.id, str_data))

        return dict(res)

    _columns = {
        'predecessor_ids': fields.many2many(
            'project.task',
            'project_task_predecessor_rel',
            'task_id',
            'parent_id',
            'Predecessor Tasks'
        ),
        'successor_ids': fields.many2many(
            'project.task',
            'project_task_predecessor_rel',
            'parent_id',
            'task_id',
            'Successor Tasks'
        ),

        'predecessor_ids_str': fields.function(
            _predecessor_ids_calc,
            method=True,
            type='char',
            string='Predecessor tasks',
            size=20,
            help='Predecessor tasks ids',
        ),
        'predecessor_names_str': fields.function(
            _predecessor_names_calc,
            method=True,
            type='char',
            string='Predecessor tasks',
            size=512,
            help='Predecessor tasks ids',
        ),
    }

    def do_link_predecessors(
        self,
        cr,
        uid,
        task_id,
        link_predecessors_data,
        context=None
    ):

        task_br = self.browse(
            cr,
            uid,
            task_id,
            context=context
        )

        self.write(
            cr,
            uid,
            [task_br.id],
            {
                'predecessor_ids':
                [
                    (
                        6, 0, link_predecessors_data['predecessor_ids']
                    )
                ],
            }
        )

        return True


task()
