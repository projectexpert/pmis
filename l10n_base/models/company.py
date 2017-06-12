# -*- encoding: utf-8 -*-

from openerp import models


class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = ['res.company', 'base.address']
