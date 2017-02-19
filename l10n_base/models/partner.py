# -*- encoding: utf-8 -*-

from openerp import models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'base.address']
