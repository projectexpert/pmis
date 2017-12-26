# -*- coding: utf-8 -*-
# Copyright (C) 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# Copyright (C) 2018 Luxim d.o.o. (<https://www.luxim.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields

class DeliverableLine(models.Model):
    _name = 'analytic.billing.plan.line'
    _inherit = 'analytic.billing.plan.line'

    change_id = fields.Many2one(
        comodel_name='change.management.change',
        ondelete='cascade',
        string='Source'
    )
