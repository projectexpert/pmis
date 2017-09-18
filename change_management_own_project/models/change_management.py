# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError


class ChangeManagementChange(models.Model):
    _inherit = 'change.management.change'

    @api.multi
    def _create_change_project(self):
        for change in self:
            data = {
                'name': '%s - %s' % (change.name, change.description),
                'parent_id': change.project_id.analytic_account_id.id,
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
                        write({'parent_id':
                               change.project_id.analytic_account_id.id})
        return res
