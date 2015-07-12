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


class Project_scope(models.Model):
    """Project Scope"""

    _name = 'project.scope'
    _description = __doc__

    project_id = fields.Many2one('project.project', string='Projects')
    justification = fields.Text('Justification')
    objective = fields.Text(string='Objective')
    indicator = fields.Char(string='Indicator')
    target_value = fields.Char(string='Target Value')
    result_obtained = fields.Char(string='Result Obtained')


class Project_boundary(models.Model):
    """Project Boundaries, Assumptions and Constraints"""

    _name = 'project.boundaries'
    _description = __doc__

    project_id = fields.Many2one('project.project', string='Projects')
    boundaries = fields.Text(string='Boundaries')
    assumptions = fields.Text(string='Assumptions')
    constraints = fields.Text(string='Constraints')


# class analytic_plan(models.Model):
#     _inherit = 'account.analytic.line.plan'
#     _columns = {
#         'plan_ids': fields.Many2one('analytic_line_plan_id', 'project_id'),
#     }


# class analytic_plan(models.Model):
#     _inherit = {'account.analytic.line.plan': "analytic_line_plan_id"}
# 
#     _columns = {
#         'supplier_id': fields.many2one(
#             'res.partner',
#             'Supplier',
#             required=False,
#             domain=[('supplier', '=', True)]
#         ),
# 
#         'pricelist_id': fields.many2one(
#             'product.pricelist',
#             'Purchasing Pricelist',
#             required=False
#         ),
# 
#         'price_unit': fields.float(
#             'Unit Price',
#             required=False,
#             digits_compute=dp.get_precision('Purchase Price')
#         ),
# 
#         'analytic_line_plan_id': fields.many2one(
#             'account.analytic.line.plan',
#             'Planning analytic lines',
#             ondelete="cascade",
#             required=True
#         )
#     }
