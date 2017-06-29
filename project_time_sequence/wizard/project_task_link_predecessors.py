# -*- coding: utf-8 -*-

from openerp.tools.translate import _
from openerp.osv import fields, orm, osv


class ProjectTaskLinkPredecessorsStr(orm.TransientModel):
    _name = 'project.task.link.predecessors.str'
    _description = 'Link predecessor tasks'

    _columns = {
        'predecessor_ids_str': fields.char(
            'Predecessors',
            size=64, required=False, select=True,
            help='List of predecessor task id''s separated by comma'),
    }

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        """
        res = super(ProjectTaskLinkPredecessorsStr, self).default_get(
            cr, uid, fields, context=context
        )
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False
        task_pool = self.pool.get('project.task')
        task_data = []
        task_data = task_pool.read(cr, uid, record_id, ['parent_ids'])
        parent_ids = task_data['parent_ids']
        data = []
        if parent_ids:
            for parent in parent_ids:
                data.insert(0, str(parent))
        else:
            data.insert(0, '')

        data.sort(cmp=None, key=None, reverse=False)
        str_data = ', '.join(data)

        res.update({'predecessor_ids_str': str_data})
        return res

    def link_predecessors_str(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        task_id = context.get('active_id', False)
        task_pool = self.pool.get('project.task')
        link_predecessors_data_str = self.read(
            cr, uid, ids, context=context)[0]
        pred_data_str = link_predecessors_data_str['predecessor_ids_str']
        try:
            link_predecessors_data = pred_data_str.split(',')
        except:
            raise orm.except_orm(
                _('Error!'),
                _('You should separate the ids by comma and space ", " ')
            )

        task_pool = self.pool.get('project.task')
        task_ids_list = []

        for pred_id in link_predecessors_data:
            try:
                task_ids = task_pool.search(cr, uid, [('id', '=', pred_id)])
            except:
                raise orm.except_orm(
                    _('Error!'),
                    _('Task "%s" does not exist.') % (pred_id,)
                )

            task_ids_list.append(task_ids[0])

        predecessor_ids = {}
        predecessor_ids.update({'parent_ids': task_ids_list})

        task_pool.do_link_predecessors(
            cr, uid, task_id, predecessor_ids, context=context
        )

        return {'type': 'ir.actions.act_window_close'}


class ProjectTaskLinkPredecessors(orm.TransientModel):
    _name = 'project.task.link.predecessors'
    _description = 'Link predecessor tasks'

    _columns = {
        'parent_ids': fields.many2many(
            'project.task',
            'project_task_parent_rel',
            'task_id',
            'parent_id',
            'Parent Tasks'
        ),
    }

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        """
        res = super(ProjectTaskLinkPredecessors, self).default_get(
            cr, uid, fields, context=context
        )
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False
        task_pool = self.pool.get('project.task')
        task_data = []
        task_data = task_pool.read(cr, uid, record_id, ['parent_ids'])
        parent_ids = task_data['parent_ids']

        res.update({'parent_ids': parent_ids})
        return res

    def link_predecessors(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        task_id = context.get('active_id', False)
        task_pool = self.pool.get('project.task')
        link_predecessors_data = self.read(cr, uid, ids, context=context)[0]
        task_pool.do_link_predecessors(
            cr, uid, task_id, link_predecessors_data, context=context
        )

        return {'type': 'ir.actions.act_window_close'}
