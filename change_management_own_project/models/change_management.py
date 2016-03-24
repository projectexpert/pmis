# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ChangeManagementChange(models.Model):
    _inherit = 'change.management.change'

    def _create_change_project(self, cr, uid, change, context=None):
        data = {
            'name': '%s - %s' % (change.name, change.description),
            'parent_id': change.project_id.analytic_account_id.id
            }
        return data

    change_project_id = fields.Many2one(
        'project.project',
        'Project created by this '
        'change'
    )


    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        change_id = super(ChangeManagementChange, self).create(cr, uid, vals,
                                                               context=context)
        project_obj = self.pool['project.project']
        change = self.browse(cr, uid, change_id, context=context)
        project_data = self._create_change_project(cr, uid, change,
                                                   context=context)
        project_id = project_obj.create(cr, uid, project_data, context=context)
        self.write(cr, uid, [change_id], {'change_project_id': project_id},
                   context=context)
        return change_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ChangeManagementChange, self).write(cr, uid, ids, vals,
                                                        context=context)
        if 'project_id' in vals:
            project_obj = self.pool['project.project']
            for change in self.browse(cr, uid, ids, context=context):
                if change.change_project_id:
                    project_obj.write(
                        cr, uid, [change.change_project_id.id],
                        {'parent_id':
                            change.project_id.analytic_account_id.id})
        return res
