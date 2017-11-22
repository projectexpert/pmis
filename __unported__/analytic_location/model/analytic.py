# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
