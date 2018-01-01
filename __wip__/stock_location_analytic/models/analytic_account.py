# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    # @api.multi
    # @api.constrains('location_id')
    # def _check_location_id(self):
    #     for project in self:
    #         if (
    #                 project.location_id
    #         ) and (
    #                 project.location_id.analytic_account_id
    #         ) != (
    #                 project.analytic_account_id
    #         ):
    #             raise ValidationError(_("The location does not contain the "
    #                                     "same analytic account"))

    @api.model
    def get_parent_stock_data(self):
        context = self.env.context
        res = {}
        if 'default_parent_id' in context and context['default_parent_id']:
            for project in self.search(
                    [(
                            'analytic_account_id',
                            '=',
                            context['default_parent_id']
                    )], limit=1):
                res['location_id'] = project.location_id
                res['dest_address_id'] = project.dest_address_id
        return res

    @api.model
    def _default_location_id(self):
        res = self.get_parent_stock_data()
        if 'location_id' in res:
            return res['location_id']

    location_id = fields.Many2one(default=_default_location_id)
