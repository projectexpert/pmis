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


class task(osv.osv):
    _inherit = 'project.task'

    _columns = {
        'milestone': fields.boolean(
            'Milestone',
            help="""
If the active field is set, the task is considered to be a milestone
            """
        ),
        'public_milestone': fields.boolean(
            'Public Milestone',
            help="""
If the active field is set, the task is considered to be a client-relevant
milestone
            """
        ),
        'project_poc': fields.float(
            'Project percentage of completion',
            help="Percentage of completion for the linked project"
        ),
        'invoice_percentage': fields.float(
            'Invoice percentage',
            help="Percentage to invoice"
        ),
    }


task()


class project(osv.osv):

    _inherit = "project.project"

    def _milestones_ids(self, cr, uid, ids, field_name, arg, context=None):
        projects = self.browse(cr, uid, ids)
        res = {}
        for project in projects:
            # get the related tasks
            res[project.id] = self.pool.get("project.task").search(
                cr,
                uid,
                [
                    ('project_id', '=', project.id),
                    ('milestone', '=', True)
                ]
            )
        return res

    _columns = {
        'milestones': fields.function(
            _milestones_ids,
            method=True,
            type='one2many',
            obj='project.task',
            string='Milestones'
        ),
    }


project()
