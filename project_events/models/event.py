# -*- encoding: utf-8 -*-

from openerp.osv import orm, fields


class EventEvent(orm.Model):
    _inherit = 'event.event'

    def _task_count(
        self, cr, uid, ids, field_name, arg, context=None
    ):
        res = {}
        for event in self.browse(
            cr, uid, ids, context=context
        ):
            res[event.id] = len(event.task_ids)
        return res

    _columns = {
        'project_id': fields.many2one(
            'project.project', 'Project'
        ),
        'task_count': fields.function(
            _task_count, type='integer',
            string='Tasks'
        ),
        'task_ids': fields.many2many(
            'project.task', 'rel_task_event',
            'event_id', 'task_id', 'Tasks'
        ),
    }

    def agenda_description(
        self, cr, uid, ids, context=None
    ):
        if context is None:
            context = {}

        for event in self.browse(
            cr, uid, ids, context=context
        ):
            if event.task_count > 0:
                agenda = "<p><strong>Agenda:</strong></p>\n<ul>\n"
                for task in event.task_ids:
                    agenda += "<li>" + task.name + "</li>\n"
                agenda += "</ul>\n"

                self.write(cr, uid, event.id,
                           {'description': (event.description or '') + agenda},
                           context=context)
        return True
