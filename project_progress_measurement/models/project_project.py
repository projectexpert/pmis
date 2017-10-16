# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    progress_measurements = fields.One2many(
        'project.progress.measurement',
        'project_id',
        'Measurements'
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default['progress_measurements'] = False
        return super(Project, self).copy(default=default)
