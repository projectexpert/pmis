# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import logging
from openerp import netsvc
from openerp.tools import float_compare

_logger = logging.getLogger(__name__)


class StockMove(orm.Model):

    _inherit = "stock.move"

    _columns = {
        'analytic_account_user_id': fields.related(
            'analytic_account_id', 'user_id', type='many2one',
            relation='res.users', string='Project Manager', store=True,
            readonly=True
        ),
    }


    def action_scrap(self, cr, uid, ids, quantity, location_id, context=None):
        """ Move the scrap/damaged product into scrap location
        @param cr: the database cursor
        @param uid: the user id
        @param ids: ids of stock move object to be scrapped
        @param quantity : specify scrap qty
        @param location_id : specify scrap location
        @param context: context arguments
        @return: Scraped lines
        Attention!!! This method overrides the standard without calling Super
        The changes introduced by this module are encoded within a
        comments START OF and END OF stock_analytic_account.
        """

        # quantity should in MOVE UOM
        if quantity <= 0:
            raise osv.except_osv(
                _('Warning!'),
                _('Please provide a positive quantity to scrap.'))
        res = []
        for move in self.browse(cr, uid, ids, context=context):
            source_location = move.location_id
            if move.state == 'done':
                source_location = move.location_dest_id
            if source_location.usage != 'internal':
                # restrict to scrap from a virtual location
                # because it's meaningless and it may introduce
                # errors in stock ('creating' new products from nowhere)
                raise osv.except_osv(
                    _('Error!'),
                    _('Forbidden operation: it is not allowed '
                      'to scrap products from a virtual location.'))
            move_qty = move.product_qty
            uos_qty = quantity / move_qty * move.product_uos_qty
            default_val = {
                'location_id': source_location.id,
                'product_qty': quantity,
                'product_uos_qty': uos_qty,
                'state': move.state,
                'scrapped': True,
                'location_dest_id': location_id,
                'tracking_id': move.tracking_id.id,
                'prodlot_id': move.prodlot_id.id,
                # START OF stock_analytic_account
                'analytic_account_id': move.analytic_account_id.id,
                # ENF OF stock_analytic_account
            }
            new_move = self.copy(cr, uid, move.id, default_val)

            res += [new_move]
            product_obj = self.pool.get('product.product')
            for product in product_obj.browse(cr, uid, [move.product_id.id],
                                              context=context):
                if move.picking_id:
                    uom = product.uom_id.name if product.uom_id else ''
                    message = _("%s %s %s has been <b>moved to</b> scrap.") \
                        % (quantity, uom, product.name)
                    move.picking_id.message_post(body=message)

        self.action_done(cr, uid, res, context=context)
        return res
