# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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


class AnalyticBillingPlanLineMakeSale(orm.TransientModel):
    _name = "analytic.billing.plan.line.make.sale"
    _description = "Analytic billing plan line make sale"

    def _get_order_lines(self, cr, uid, context=None):
        """
        Returns the order lines associated to the analytic accounts selected.
        """
        if context is None:
            context = {}

        record_ids = context and context.get('active_ids', False)

        if record_ids:
            order_line_ids = []
            line_plan_obj = self.pool.get('analytic.billing.plan.line')

            for line in line_plan_obj.browse(cr, uid, record_ids,
                                             context=context):
                    for order_line in line.order_line_ids:
                        order_line_id = order_line and order_line.id
                        order_line_ids.extend([order_line_id])
            if order_line_ids:
                return order_line_ids
        return False

    # def _get_default_shop(self, cr, uid, context=None):
    #     company_id = self.pool.get('res.users').browse(
    #         cr, uid, uid, context=context).company_id.id
    #     shop_ids = self.pool.get('sale.shop').search(
    #         cr, uid, [('company_id', '=', company_id)], context=context)
    #     if not shop_ids:
    #         raise osv.except_osv(_('Error!'),
    #                              _('There is no default shop '
    #                                'for the current user\'s company!'))
    #     return shop_ids[0]

    _columns = {
        'order_line_ids': fields.many2many('sale.order.line',
                                           'make_sale_order_line_rel',
                                           'order_line_id',
                                           'make_sale_order_id'),
        # 'shop_id': fields.many2one('sale.shop', 'Shop', required=True),
        'invoice_quantity': fields.selection([('order',
                                               'Ordered Quantities')],
                                             'Invoice on',
                                             help="The sales order will "
                                                  "automatically create the "
                                                  "invoice proposition "
                                                  "(draft invoice).",
                                             required=True),
        'order_policy': fields.selection([('manual', 'On Demand')],
                                         'Create Invoice',
                                         help="""This field controls how
                                         invoice and delivery
                                         operations are synchronized.""",
                                         required=True),
    }

    _defaults = {
        'order_line_ids': _get_order_lines,
        # 'shop_id': _get_default_shop,
        'order_policy': 'manual',
        'invoice_quantity': 'order',
    }

    def make_sales_orders(self, cr, uid, ids, context=None):
        """
             To make sales.

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
        make_order = self.browse(cr, uid, ids[0], context=context)
        res = []
        if record_ids:
            billing_plan_obj = self.pool.get('analytic.billing.plan.line')
            order_obj = self.pool.get('sale.order')
            order_line_obj = self.pool.get('sale.order.line')
            partner_obj = self.pool.get('res.partner')
            acc_pos_obj = self.pool.get('account.fiscal.position')

            list_line = []

            customer_data = False
            company_id = False
            sale_id = False
            account_id = False

            for line in billing_plan_obj.browse(cr, uid, record_ids,
                                                context=context):

                    uom_id = line.product_uom_id

                    if not line.customer_id:
                        raise osv.except_osv(
                            _('Could not create sale order !'),
                            _('You have to enter a customer.'))

                    if customer_data is not False \
                            and line.customer_id != customer_data:
                        raise osv.except_osv(
                            _('Could not create sale order !'),
                            _('You have to select lines '
                              'from the same customer.'))
                    else:
                        customer_data = line.customer_id

                    partner_addr = partner_obj.address_get(
                        cr, uid, [customer_data.id], ['default',
                                                      'invoice',
                                                      'delivery',
                                                      'contact'])
                    newdate = datetime.today()
                    partner = customer_data
                    pricelist_id = partner.property_product_pricelist \
                        and partner.property_product_pricelist.id \
                        or False
                    price_unit = line.price_unit

                    line_company_id = line.company_id \
                        and line.company_id.id \
                        or False
                    if company_id is not False \
                            and line_company_id != company_id:
                        raise osv.except_osv(
                            _('Could not create sale order !'),
                            _('You have to select lines '
                              'from the same company.'))
                    else:
                        company_id = line_company_id

                    # shop_id = make_order.shop_id \
                    #     and make_order.shop_id.id \
                    #     or False

                    line_account_id = line.account_id \
                        and line.account_id.id \
                        or False
                    if account_id is not False \
                            and line_account_id != account_id:
                        raise osv.except_osv(
                            _('Could not create billing request!'),
                            _('You have to select lines from the '
                              'same analytic account.'))
                    else:
                        account_id = line_account_id

                    sale_order_line = {
                        'name': line.name,
                        'product_uom_qty': line.unit_amount,
                        'product_id': line.product_id.id,
                        'product_uom': uom_id.id,
                        'price_unit': price_unit,
                        'notes': line.notes,
                    }

                    taxes = False
                    if line.product_id:
                        taxes_ids = line.product_id.product_tmpl_id.taxes_id
                        taxes = acc_pos_obj.map_tax(
                            cr, uid, partner.property_account_position,
                            taxes_ids)
                    if taxes:
                        sale_order_line.update({
                            'tax_id': [(6, 0, taxes)]
                        })
                    list_line.append(sale_order_line)

                    if sale_id is False:
                        sale_id = order_obj.create(cr, uid, {
                            'origin': '',
                            # 'shop_id': shop_id,
                            'partner_id': customer_data.id,
                            'pricelist_id': pricelist_id,
                            'partner_invoice_id': partner_addr['invoice'],
                            'partner_order_id': partner_addr['contact'],
                            'partner_shipping_id': partner_addr['delivery'],
                            'date_order':
                                newdate.strftime('%Y-%m-%d %H:%M:%S'),
                            'fiscal_position':
                                partner.property_account_position and
                                partner.property_account_position.id or False,
                            'company_id': company_id,
                            'payment_term':
                                partner.property_payment_term and
                                partner.property_payment_term.id or False,
                            'project_id': account_id,
                            'invoice_quantity': make_order.invoice_quantity,
                            'order_policy': make_order.order_policy,

                        }, context=context)
                        if line.account_id.user_id:
                            order_obj.message_subscribe_users(
                                cr, uid, [sale_id],
                                user_ids=[line.account_id.user_id.id])

                    sale_order_line.update({
                        'order_id': sale_id
                    })

                    order_line_id = order_line_obj.create(cr, uid,
                                                          sale_order_line,
                                                          context=context)

                    values = {
                        'order_line_ids': [(4, order_line_id)]
                    }

                    billing_plan_obj.write(cr, uid, [line.id], values,
                                           context=context)

                    res.append(order_line_id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Billing request lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

AnalyticBillingPlanLineMakeSale()
