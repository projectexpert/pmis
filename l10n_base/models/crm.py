# -*- encoding: utf-8 -*-

from openerp import models


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead', 'base.address']
