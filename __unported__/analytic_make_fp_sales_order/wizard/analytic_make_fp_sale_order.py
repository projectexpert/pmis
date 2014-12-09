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

from datetime import datetime
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class analytic_make_fp_sale_order(orm.TransientModel):
    _name = "analytic.make.fp.sale.order"
    _description = "Make Fixed-Price Sales order from Analytic Account"

    _columns = {
        'method': fields.selection([('margin_on_costs', 'Gross margin over planned costs'),
                                    ('resource_sale_price', 'Sales price for planned resources')],
                                   'Sales price method')
    }
    def make_fp_sale_order(self, cr, uid, ids, context=None):
        """
             To make sales orders.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: A dictionary which of fields with values.

        """

        if context is None:
            context = {}
        record_ids = context and context.get('active_ids', False)
        res = []
        if record_ids:
            analytic_obj = self.pool.get('account.analytic.account')
            order_obj = self.pool.get('sale.order')
            order_line_obj = self.pool.get('sale.order.line')
            partner_obj = self.pool.get('res.partner')
            acc_pos_obj = self.pool.get('account.fiscal.position')

            list_line = []

            customer_data = False
            company_id = False
            sale_id = False
            result = []
            for analytic_account in analytic_obj.browse(cr, uid, record_ids, context=context):

                #Obtain the total planned cost
                cr.execute('SELECT SUM(amount) '
                           'FROM account_analytic_line_plan '
                           'WHERE account_id=%s', (analytic_account.id,))
                res = cr.fetchone()

                if res:
                    total_cost = res[0]
                else:
                    total_cost = 0


                uom_id = analytic_account.sale_product_uom_id
                if not uom_id:
                    raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to enter a sales unit of measure in the analytic account.'))


                if analytic_account.sale_qty == 0:
                    raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to enter a sales quantity in the analytic account.'))

                if not analytic_account.sale_name:
                    raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to enter a sales description in the analytic account.'))

                product_id = analytic_account.sale_product_id
                if not product_id:
                    raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to enter a sales product in the analytic account.'))


                if not analytic_account.partner_id:
                    raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to enter a customer.'))

                if customer_data is not False and analytic_account.partner_id != customer_data:
                    raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to select lines from the same customer.'))
                else:
                    customer_data = analytic_account.partner_id

                partner_addr = partner_obj.address_get(cr, uid, [customer_data.id],
                                                       ['default', 'invoice', 'delivery', 'contact'])
                newdate = datetime.today()
                partner = customer_data
                pricelist_id = partner.property_product_pricelist and partner.property_product_pricelist.id or False


                line_company_id = analytic_account.company_id and analytic_account.company_id.id or False
                if company_id is not False and line_company_id != company_id:
                    raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to select lines from the same company.'))
                else:
                    company_id = line_company_id

                shop = self.pool.get('sale.shop').search(cr, uid, [('company_id', '=', company_id)])
                shop_id = shop and shop[0] or False


                price_unit = -1 * total_cost * (1 + analytic_account.sale_gross_margin / 100) / analytic_account.sale_qty

                sale_order_line = {
                    'name': analytic_account.sale_name,
                    'product_uom_qty': analytic_account.sale_qty,
                    'product_id': product_id.id,
                    'product_uom': uom_id.id,
                    'price_unit': price_unit,
                    'notes': analytic_account.sale_notes or False,
                    'analytic_account_id': analytic_account.id,
                }

                taxes_ids = product_id.product_tmpl_id and product_id.product_tmpl_id.taxes_id or False
                if taxes_ids:
                    taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)
                else:
                    taxes = False

                if taxes:
                    sale_order_line.update({
                        'tax_id': [(6, 0, taxes)]
                    })
                list_line.append(sale_order_line)

                if sale_id is False:
                    sale_id = order_obj.create(cr, uid, {
                        'origin': '',
                        'shop_id': shop_id,
                        'partner_id': customer_data.id,
                        'pricelist_id': pricelist_id,
                        'partner_invoice_id': partner_addr['invoice'],
                        'partner_order_id': partner_addr['contact'],
                        'partner_shipping_id': partner_addr['delivery'],
                        'date_order': newdate.strftime('%Y-%m-%d %H:%M:%S'),
                        'fiscal_position': partner.property_account_position and
                                           partner.property_account_position.id or False,
                        'company_id': company_id,
                        'payment_term': partner.property_payment_term and
                                        partner.property_payment_term.id or False,
                    }, context=context)

                sale_order_line.update({
                    'order_id': sale_id
                })

                order_line_id = order_line_obj.create(cr, uid, sale_order_line, context=context)
                result.append(order_line_id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, result))+"])]",
            'name': _('Sales order lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

analytic_make_fp_sale_order()