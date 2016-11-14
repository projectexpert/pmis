# -*- coding: utf-8 -*-
# (C) 2014 Eficent (<http://www.eficent.com/>)
# <jordi.ballester@eficent.com>

from openerp import models, fields


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    lob = fields.Many2one(
        'account.analytic.lob',
        'Line of Business'
    )
