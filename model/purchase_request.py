# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseRequestLine(models.Model):

    _inherit = 'purchase.request.line'

    analytic_resource_plan_lines = fields.Many2many(
        'analytic.resource.plan.line',
        string='Analytic Planning Lines',
        copy=False,
        readonly=True)
