# -*- coding: utf-8 -*-

from openerp import models, fields


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    cost_category = fields.Selection(
        [
            ('cogs', 'Cost of Goods Sold'),
            ('expense', 'Expense')
        ],
        'Type of Cost',
        help="Defines what type of cost does the analytic account carry "
             "from an employee perspective.",
        default='expense'
    )
