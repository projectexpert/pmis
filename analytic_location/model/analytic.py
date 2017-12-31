# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2017 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class AccountAnalyticAccount(orm.Model):
    _inherit = 'account.analytic.account'

    _columns = {
        'location_id': fields.many2one(
            'stock.location',
            'Default Stock Location',
            domain=[('usage', '<>', 'view')]
        ),
        'dest_address_id': fields.many2one(
            'res.partner',
            'Delivery Address',
            help="Delivery address for "
            "the current contract "
            "/project."
        ),
    }

    def _default_dest_address(self, cr, uid, context=None):
        if context is None:
            context = {}
        partner_id = context.get('partner_id', False)
        if partner_id:
            return self.pool.get('res.partner').address_get(
                cr, uid, [partner_id], ['delivery']
            )['delivery'],
        else:
            return False

    _defaults = {
        'dest_address_id': _default_dest_address,
        }
