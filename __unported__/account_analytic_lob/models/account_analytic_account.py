# -*- coding: utf-8 -*-

from openerp import models, fields


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    lob = fields.Many2one(
        'account.analytic.lob',
        'Line of Business'
    )
