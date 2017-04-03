# -*- coding: utf-8 -*-

from openerp import api, fields, models


class AccountAnalyticLinePlan(models.Model):
    _inherit = 'account.analytic.line.plan'

    resource_plan_id = fields.Many2one(
        'analytic.resource.plan.line',
        'Resource Plan Line',
        ondelete='cascade'
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default['resource_plan_id'] = False
        res = super(AccountAnalyticLinePlan, self).copy(default)
        return res
