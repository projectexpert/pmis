##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C)
#    2004-2010 Tiny SPRL (<http://tiny.be>).
#    2009-2010 Veritos (http://veritos.nl).
#    All Rights Reserved
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

from openerp.osv import osv, fields
from openerp.tools.float_utils import float_round as round


class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    _columns = {
        'move_id': fields.many2one(
            'stock.move', string="Move line",
            help="If the invoice was generated from a stock.picking, reference to the related move line."
        ),
    }

    def move_line_get(self, cr, uid, invoice_id, context=None):
        res = super(account_invoice_line, self).move_line_get(cr, uid, invoice_id, context=context)
        inv = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=context)
        if inv.type in ('in_invoice', 'in_refund'):
            for i_line in inv.invoice_line:
                res.extend(self._anglo_saxon_purchase_move_lines(cr, uid, i_line, res, context=context))
        return res

    def _anglo_saxon_purchase_move_lines(self, cr, uid, i_line, res, context=None):
        """Return the additional move lines for purchase invoices and refunds.

        i_line: An account.invoice.line object.
        res: The move line entries produced so far by the parent move_line_get.
        """
        inv = i_line.invoice_id
        company_currency = inv.company_id.currency_id.id
        if i_line.product_id and i_line.product_id.valuation == 'real_time':
            if i_line.product_id.type != 'service':
                # Generate only the extra journal entries if there's
                # not a stock move, or if the stock move is going to a company location.
                if not i_line.move_id or (i_line.move_id and i_line.move_id.location_dest_id.company_id):
                    # get the price difference account at the product
                    acc = (
                        i_line.product_id.property_account_creditor_price_difference and
                        i_line.product_id.property_account_creditor_price_difference.id
                    )
                    if not acc:
                        # if not found on the product get the price difference account at the category
                        acc = (
                            i_line.product_id.categ_id.property_account_creditor_price_difference_categ and
                            i_line.product_id.categ_id.property_account_creditor_price_difference_categ.id
                        )
                    a = None

                    # oa will be the stock input account
                    # first check the product, if empty check the category
                    oa = (
                        i_line.product_id.property_stock_account_input and
                        i_line.product_id.property_stock_account_input.id
                    )
                    if not oa:
                        oa = (
                            i_line.product_id.categ_id.property_stock_account_input_categ and
                            i_line.product_id.categ_id.property_stock_account_input_categ.id
                        )
                    if oa:
                        # get the fiscal position
                        fpos = i_line.invoice_id.fiscal_position or False
                        a = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, oa)
                    diff_res = []
                    decimal_precision = self.pool.get('decimal.precision')
                    account_prec = decimal_precision.precision_get(cr, uid, 'Account')
                    # calculate and write down the possible price difference between invoice price and product price
                    for line in res:
                        if line.get('invl_id', 0) == i_line.id and a == line['account_id']:
                            uom = i_line.product_id.uos_id or i_line.product_id.uom_id
                            valuation_price_unit = self.pool.get('product.uom')._compute_price(
                                cr, uid, uom.id, i_line.product_id.standard_price, i_line.uos_id.id
                            )
                            if i_line.product_id.cost_method != 'standard' and i_line.purchase_line_id:
                                # for average/fifo/lifo costing method, fetch real cost price from incomming moves
                                stock_move_obj = self.pool.get('stock.move')
                                valuation_stock_move = stock_move_obj.search(
                                    cr, uid, [
                                        ('purchase_line_id', '=', i_line.purchase_line_id.id)
                                    ], limit=1, context=context
                                )
                                if valuation_stock_move:
                                    valuation_price_unit = stock_move_obj.browse(
                                        cr, uid, valuation_stock_move[0], context=context
                                    ).price_unit
                            if inv.currency_id.id != company_currency:
                                valuation_price_unit = self.pool.get('res.currency').compute(
                                    cr, uid, company_currency, inv.currency_id.id, valuation_price_unit,
                                    context={'date': inv.date_invoice}
                                )
                            if valuation_price_unit != i_line.price_unit and line[
                                'price_unit'
                            ] == i_line.price_unit and acc:
                                # price with discount and without tax included
                                price_unit = self.pool['account.tax'].compute_all(
                                    cr, uid, line['taxes'],
                                    i_line.price_unit * (1-(i_line.discount or 0.0)/100.0),
                                    line['quantity']
                                )['total']
                                price_line = round(valuation_price_unit * line['quantity'], account_prec)
                                price_diff = round(price_unit - price_line, account_prec)
                                line.update({'price': price_line})
                                diff_res.append({
                                    'type': 'src',
                                    'name': i_line.name[:64],
                                    'price_unit': round(price_diff / line['quantity'], account_prec),
                                    'quantity': line['quantity'],
                                    'price': price_diff,
                                    'account_id': acc,
                                    'product_id': line['product_id'],
                                    'uos_id': line['uos_id'],
                                    'account_analytic_id': line['account_analytic_id'],
                                    'taxes': line.get('taxes', []),
                                    })
                    return diff_res
        return []
