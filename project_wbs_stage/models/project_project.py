# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = "project.project"

    def _default_stage_id(self):
        return self.env["project.project.stage"].search(
            [('case_default', '=', True)], limit=1)

    stage_id = fields.Many2one(
        'project.project.stage', 'Stage',
        default=_default_stage_id,
        domain="[('fold', '=', False)]")

    @api.multi
    def write(self, values):
        res = super(ProjectProject, self).write(values)
        if values.get('stage_id'):
            stage_obj = self.env['project.project.stage']
            for project in self:
                # Search if there's an associated project
                new_stage = stage_obj.browse(values.get('stage_id'))
                # If the new stage is found in the child accounts, then set
                # it as well (only if the new stage sequence is greater than
                #  the current)
                child_ids = self.search([('parent_id', '=', project.id)])
                for child in self.browse(child_ids):
                    if child.stage_id.sequence < new_stage.sequence:
                        child.write({'stage_id': new_stage.id})
        return res
