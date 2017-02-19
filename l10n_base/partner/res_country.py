# -*- encoding: utf-8 -*-

from openerp import models, fields
from openerp.tools.translate import _


class ResCountry(models.Model):
    _inherit = 'res.country'

    enable_province = fields.Boolean('Show Province?')
    enable_region = fields.Boolean('Show Region?')
    enable_state = fields.Boolean('Show State?')
