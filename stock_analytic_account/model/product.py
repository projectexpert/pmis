# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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
from openerp.osv import orm


class Product(orm.Model):

    _inherit = "product.product"

    def get_product_available(self, cr, uid, ids, context=None):
        """ Finds whether product is available or not in particular warehouse.
        Attention!!! This method overrides the standard without calling Super
        The changes introduced by this module are encoded within a
        comments START OF and END OF stock_analytic_account.
        @return: Dictionary of values
        """
        if context is None:
            context = {}

        location_obj = self.pool.get('stock.location')
        warehouse_obj = self.pool.get('stock.warehouse')
        shop_obj = self.pool.get('sale.shop')

        states = context.get('states', [])
        what = context.get('what', ())
        if not ids:
            ids = self.search(cr, uid, [])
        res = {}.fromkeys(ids, 0.0)
        if not ids:
            return res

        if context.get('shop', False):
            warehouse_id = shop_obj.read(
                cr, uid, int(context['shop']),
                ['warehouse_id'])['warehouse_id'][0]
            if warehouse_id:
                context['warehouse'] = warehouse_id

        if context.get('warehouse', False):
            lot_id = warehouse_obj.read(
                cr, uid, int(context['warehouse']),
                ['lot_stock_id'])['lot_stock_id'][0]
            if lot_id:
                context['location'] = lot_id

        if context.get('location', False):
            if type(context['location']) == type(1):
                location_ids = [context['location']]
            elif type(context['location']) in (type(''), type(u'')):
                location_ids = location_obj.search(
                    cr, uid, [('name', 'ilike', context['location'])],
                    context=context)
            else:
                location_ids = context['location']
        else:
            location_ids = []
            wids = warehouse_obj.search(cr, uid, [], context=context)
            if not wids:
                return res
            for w in warehouse_obj.browse(cr, uid, wids, context=context):
                location_ids.append(w.lot_stock_id.id)

        # build the list of ids of children of the location given by id
        if context.get('compute_child', True):
            child_location_ids = location_obj.search(
                cr, uid, [('location_id', 'child_of', location_ids)])
            location_ids = child_location_ids or location_ids

        # this will be a dictionary of the product UoM by product id
        product2uom = {}
        uom_ids = []
        for product in self.read(cr, uid, ids, ['uom_id'], context=context):
            product2uom[product['id']] = product['uom_id'][0]
            uom_ids.append(product['uom_id'][0])
        # this will be a dictionary of the UoM resources we need for
        # conversion purposes, by UoM id
        uoms_o = {}
        for uom in self.pool.get('product.uom').browse(cr, uid, uom_ids,
                                                       context=context):
            uoms_o[uom.id] = uom

        results = []
        results2 = []

        from_date = context.get('from_date', False)
        to_date = context.get('to_date', False)
        date_str = False
        date_values = False
        where = [tuple(location_ids), tuple(location_ids), tuple(ids),
                 tuple(states)]
        if from_date and to_date:
            date_str = "date>=%s and date<=%s"
            where.append(tuple([from_date]))
            where.append(tuple([to_date]))
        elif from_date:
            date_str = "date>=%s"
            date_values = [from_date]
        elif to_date:
            date_str = "date<=%s"
            date_values = [to_date]
        if date_values:
            where.append(tuple(date_values))

        prodlot_id = context.get('prodlot_id', False)
        prodlot_clause = ''
        if prodlot_id:
            prodlot_clause = ' and prodlot_id = %s '
            where += [prodlot_id]
        elif 'prodlot_id' in context and not prodlot_id:
            prodlot_clause = ' and prodlot_id is null '

        # START OF stock_analytic_account
        analytic_account_id = context.get('analytic_account_id', False)
        analytic_account_clause = ''
        if analytic_account_id:
            analytic_account_clause = (
                ' and analytic_account_id = %s and '
                'analytic_reserved = True '
            )
            where += [analytic_account_id]
        elif 'analytic_account_id' in context and not analytic_account_clause:
            analytic_account_clause = ' and analytic_account_id is null '
        # END OF stock_analytic_account

        # TODO: perhaps merge in one query.
        if 'in' in what:
            # all moves from a location out of the set to a location in the set
            cr.execute(
                'select sum(product_qty), product_id, product_uom '
                'from stock_move '
                'where location_id NOT IN %s '
                'and location_dest_id IN %s '
                'and product_id IN %s '
                'and state IN %s ' + (
                    date_str and 'and '+date_str+' ' or ''
                ) + ' ' + prodlot_clause + ' ' +
                # START OF stock_analytic_account
                analytic_account_clause +
                # END OF stock_analytic_account
                'group by product_id,product_uom', tuple(where)
            )
            results = cr.fetchall()
        if 'out' in what:
            # all moves from a location in the set to a location out of the set
            cr.execute(
                'select sum(product_qty), product_id, product_uom '
                'from stock_move '
                'where location_id IN %s '
                'and location_dest_id NOT IN %s '
                'and product_id  IN %s '
                'and state in %s ' + (
                    date_str and 'and '+date_str+' ' or ''
                ) + ' ' + prodlot_clause + ' ' +
                # START OF stock_analytic_account
                analytic_account_clause +
                # END OF stock_analytic_account
                'group by product_id,product_uom', tuple(where)
            )
            results2 = cr.fetchall()

        # Get the missing UoM resources
        uom_obj = self.pool.get('product.uom')
        uoms = map(lambda x: x[2], results) + map(lambda x: x[2], results2)
        if context.get('uom', False):
            uoms += [context['uom']]
        uoms = filter(lambda x: x not in uoms_o.keys(), uoms)
        if uoms:
            uoms = uom_obj.browse(cr, uid, list(set(uoms)), context=context)
            for o in uoms:
                uoms_o[o.id] = o

        # TOCHECK: before change uom of product, stock move line are in old
        # uom.
        context.update({'raise-exception': False})
        # Count the incoming quantities
        for amount, prod_id, prod_uom in results:
            amount = uom_obj._compute_qty_obj(
                cr, uid, uoms_o[prod_uom], amount,
                uoms_o[context.get('uom', False) or product2uom[prod_id]],
                context=context)
            res[prod_id] += amount
        # Count the outgoing quantities
        for amount, prod_id, prod_uom in results2:
            amount = uom_obj._compute_qty_obj(
                cr, uid, uoms_o[prod_uom], amount,
                uoms_o[context.get('uom', False) or product2uom[prod_id]],
                context=context)
            res[prod_id] -= amount
        return res
