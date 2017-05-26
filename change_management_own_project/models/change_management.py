# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class ChangeManagementChange(models.Model):
    _inherit = 'change.management.change'

    @api.multi
    def _create_change_project(self):
        for change in self:
            data = {
                'name': '%s - %s' % (change.name, change.description),
                'parent_id': change.project_id.analytic_account_id.id,
                'notes': (
                    '<h1>Reason</h1> %s'
                    '<h1>Cause</h1> %s'
                    '<h1>Effect</h1> %s' % (
                        change.description_event,
                        change.description_cause,
                        change.description_effect
                    )
                )
            }
        return data

    change_project_id = fields.Many2one(
        'project.project',
        'Proposed Project',
        readonly="True"
    )

    @api.multi
    def button_create_change_project(self):
        for change in self:
            if change.change_project_id:
                raise UserError(_('A Change Management Project'
                                  'already exists.'))
            project_data = change._create_change_project()
            project = self.env['project.project'].create(project_data)
            change.write({'change_project_id': project.id})
        return True

    @api.multi
    def write(self, vals):
        res = super(ChangeManagementChange, self).write(vals)
        if 'project_id' in vals:
            for change in self:
                if change.change_project_id:
                    change.change_project_id.\
                        write({'parent_id': change.project_id.
                               analytic_account_id.id})
        return res
