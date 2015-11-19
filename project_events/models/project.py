# -*- encoding: utf-8 -*-

from openerp.osv import orm, fields


class ProjectProject(orm.Model):
    _inherit = 'project.project'

    def _event_count(
        self, cr, uid, ids, field_name, arg, context=None
    ):
        res = {}
        for project in self.browse(
            cr, uid, ids, context=context
        ):
            res[project.id] = len(project.event_ids)
        return res

    _columns = {
        'event_count': fields.function(
            _event_count,
            type='integer',
            string='Events'
        ),
        'event_ids': fields.one2many(
            'event.event',
            'project_id',
            'Events'
        ),
    }


class ProjectTask(orm.Model):
    _inherit = 'project.task'

    def _event_count(
        self, cr, uid, ids, field_name, arg, context=None
    ):
        res = {}
        for task in self.browse(
            cr, uid, ids, context=context
        ):
            res[task.id] = len(task.event_ids)
        return res

    def _pending_event_count(
        self, cr, uid, ids, field_name, arg,
        context=None
    ):
        res = {}
        for task in self.browse(
            cr, uid, ids, context=context
        ):
            event_cnt = 0
            for event in task.event_ids:
                if event.state in ('draft', 'confirm'):
                    event_cnt += 1
            res[task.id] = event_cnt
        return res

    _columns = {
        'event_count': fields.function(
            _event_count, type='integer',
            string='Events'
        ),
        'pending_event_count': fields.function(
            _pending_event_count,
            type='integer',
            string='Pending Events'
        ),
        'event_ids': fields.many2many(
            'event.event',
            'rel_task_event',
            'task_id',
            'event_id',
            'Tasks'
        ),
    }

    def action_show_events(
        self, cr, uid, ids, context=None
    ):
        if context is None:
            context = {}

        event_ids = self.pool['event.event'].search(
            cr, uid, [['task_ids', 'in', ids]]
        )

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'kanban,tree,calendar,form',
            'view_type': 'form',
            'target': 'current',
            'domain': [['id', 'in', event_ids]],
            'res_id': event_ids,
        }
