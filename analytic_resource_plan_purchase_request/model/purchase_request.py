# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseRequestLine(models.Model):

    _inherit = 'purchase.request.line'

    analytic_resource_plan_lines = fields.Many2many(
        comodel_name='analytic.resource.plan.line',
        relation='purchase_request_line_analytic_resource_plan_line_line_rel',
        column2='analytic_resource_plan_line_id',
        column1='purchase_request_line_id',
        string='Analytic Planning Lines',
        copy=False,
        domain=[('resource_type', '=', 'procurement')],
        readonly=True)
