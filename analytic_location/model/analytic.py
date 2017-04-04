# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class AccountAnalyticAccount(orm.Model):
    _inherit = 'account.analytic.account'

    _columns = {
        'warehouse_id': fields.many2one(
            'stock.warehouse',
            'Warehouse',
        ),
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

    def _default_warehouse(self, cr, uid, context=None):
        warehouse_obj = self.pool.get('stock.warehouse')
        company_obj = self.pool.get('res.company')
        company_id = company_obj._company_default_get(
            cr, uid,
            'stock.warehouse',
            context=context
        )
        if context is None:
            context = {}

        warehouse_ids = warehouse_obj.search(
            cr, uid, [('company_id', '=', company_id)], limit=1,
            context=context) or []

        if warehouse_ids:
            return warehouse_ids[0]
        else:
            return False

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
        'warehouse_id': _default_warehouse,
        'dest_address_id': _default_dest_address,
    }
