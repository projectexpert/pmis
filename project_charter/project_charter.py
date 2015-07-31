# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by MATMOZ d.o.o.
#    Copyright (C) 2015-TODAY MATMOZ d.o.o. (<http://www.matmoz.si>).
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

from openerp import models, fields


class Project(models.Model):

    _inherit = 'project.project'

    notes = fields.Text('Notes')
    project_scope_ids = fields.One2many(
        'project.scope',
        'project_id',
        # string='Scope'
    )
    project_boundaries_ids = fields.One2many(
        'project.boundaries',
        'project_id',
    )
    project_success_ids = fields.One2many(
        'project.success',
        'project_id'
    )


class Project_scope(models.Model):
    """Project Scope"""

    _name = 'project.scope'
    _description = __doc__

    project_id = fields.Many2one('project.project', string='Projects')
    scope = fields.Text('Scope')
    out_scope = fields.Text(string='Out of Scope')


class Success(models.Model):
    """Success and Requirements"""

    _name = 'project.success'
    _description = __doc__

    project_id = fields.Many2one('project.project', string='Projects')
    success = fields.Text('Project Success')
    requirements = fields.Text('Stakeholder Requirements')


class Project_boundary(models.Model):
    """Project Boundaries, Assumptions and Constraints"""

    _name = 'project.boundaries'
    _description = __doc__

    project_id = fields.Many2one('project.project', string='Projects')
    assumptions = fields.Text(string='Assumptions')
    constraints = fields.Text(string='Constraints')
    hlrisks = fields.Text(string='High-level Risk Assessment')
