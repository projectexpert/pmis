# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class Task(orm.Model):
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


class Project(orm.Model):

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
