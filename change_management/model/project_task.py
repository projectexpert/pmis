# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution
#
#    Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
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
from openerp import models, fields, api


class project_task (models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    change_id = fields.Many2one(
        'change.management.change', 'Action on Change', readonly=True,
        help="Task is an action on a change identified by this label."
    )

project_task()


class project_project (models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    change_ids = fields.One2many(
        'change.management.change',
        'project_id',
        'Project changes'
    )

project_project()
