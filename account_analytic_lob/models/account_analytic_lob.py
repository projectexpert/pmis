# -*- coding: utf-8 -*-
# (C) 2014 Eficent (<http://www.eficent.com/>)
# <jordi.ballester@eficent.com>

from openerp import models, fields


class AccountAnalyticLob(models.Model):

    _name = "account.analytic.lob"
    _description = 'Line of Business'
    _order = 'name'

    code = fields.Char(
        'Code',
        size=4,
        required=True,
        translate=True
    )

    name = fields.Char(
        'Name',
        size=32,
        required=True,
        translate=True
    )
